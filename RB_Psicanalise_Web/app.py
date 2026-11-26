import os
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import quote
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect

from config import BASE_DIR, DATA_DIR, RESOURCE_DIR, Config
from updater import aplicar_atualizacao_exe, verificar_atualizacao
from version import APP_VERSION
from models import (
    Agendamento,
    Anamnese,
    ConfiguracaoSistema,
    Formulario,
    FormularioEnvio,
    KanbanColuna,
    Paciente,
    Usuario,
    db,
    gerar_proximo_prontuario,
    init_db,
    utcnow,
)

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar o sistema clínico."
login_manager.login_message_category = "warning"


def roles_required(*roles):
    """Restringe acesso da rota aos perfis informados (retorna 403 se não autorizado)."""
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.perfil not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(RESOURCE_DIR, "templates"),
        static_folder=os.path.join(RESOURCE_DIR, "static"),
    )
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    init_db(app)

    @app.context_processor
    def inject_globals():
        return {
            "app_version": APP_VERSION,
            "is_frozen_exe": getattr(sys, "frozen", False),
        }

    @app.errorhandler(403)
    def forbidden(_err):
        return render_template("403.html"), 403

    # =========================================================================
    # AUTENTICAÇÃO
    # =========================================================================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            senha = request.form.get("senha", "")
            user = Usuario.query.filter_by(email=email).first()

            if user and user.ativo and user.check_password(senha):
                login_user(user)
                flash(f"Bem-vindo(a), {user.nome}!", "success")
                next_url = request.args.get("next")
                return redirect(next_url or url_for("dashboard"))

            flash("E-mail ou senha inválidos, ou usuário desativado.", "danger")

        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("Sessão encerrada com segurança.", "info")
        return redirect(url_for("login"))

    # =========================================================================
    # DASHBOARD
    # =========================================================================
    @app.route("/")
    @login_required
    def dashboard():
        total_pacientes = Paciente.query.filter_by(ativo=True).count()
        total_sessoes = Agendamento.query.count()
        pendentes = Agendamento.query.filter_by(pagamento="Pendente").all()
        valor_pendente = sum(s.valor or 0.0 for s in pendentes)
        recebidos = Agendamento.query.filter_by(pagamento="Pago").all()
        valor_recebido = sum(s.valor or 0.0 for s in recebidos)
        ultimos_pacientes = (
            Paciente.query.filter_by(ativo=True)
            .order_by(Paciente.criado_em.desc())
            .limit(6)
            .all()
        )
        form_respondidos = FormularioEnvio.query.filter_by(status="Respondido").count()
        return render_template(
            "dashboard.html",
            total_pacientes=total_pacientes,
            total_sessoes=total_sessoes,
            qtd_pendentes=len(pendentes),
            valor_pendente=valor_pendente,
            valor_recebido=valor_recebido,
            ultimos_pacientes=ultimos_pacientes,
            form_respondidos=form_respondidos,
        )

    # =========================================================================
    # PACIENTES & PRONTUÁRIO
    # =========================================================================
    @app.route("/pacientes")
    @login_required
    def pacientes_lista():
        busca = request.args.get("q", "").strip()
        query = Paciente.query.filter_by(ativo=True)
        if busca:
            like = f"%{busca}%"
            query = query.filter(
                db.or_(
                    Paciente.nome_completo.ilike(like),
                    Paciente.prontuario.ilike(like),
                    Paciente.cpf.ilike(like),
                    Paciente.telefone.ilike(like),
                )
            )
        pacientes = query.order_by(Paciente.nome_completo.asc()).all()
        return render_template("pacientes.html", pacientes=pacientes, busca=busca)

    @app.route("/pacientes/novo", methods=["GET", "POST"])
    @login_required
    def paciente_novo():
        if request.method == "POST":
            nome = request.form.get("nome_completo", "").strip()
            if not nome:
                flash("O nome completo do paciente é obrigatório.", "danger")
                return redirect(url_for("paciente_novo"))

            prontuario = request.form.get("prontuario", "").strip() or gerar_proximo_prontuario()
            if Paciente.query.filter_by(prontuario=prontuario).first():
                prontuario = gerar_proximo_prontuario()

            primeira_coluna = KanbanColuna.query.order_by(KanbanColuna.ordem.asc()).first()
            dados_cad = _extrair_dados_cadastro(request.form)

            p = Paciente(
                prontuario=prontuario,
                nome_completo=nome,
                telefone=request.form.get("telefone", "").strip(),
                email=request.form.get("email", "").strip(),
                cpf=request.form.get("cpf", "").strip(),
                kanban_coluna_id=primeira_coluna.id if primeira_coluna else None,
            )
            p.cadastro = dados_cad
            db.session.add(p)
            db.session.commit()
            flash(f"Paciente {p.nome_completo} cadastrado com prontuário {p.prontuario}.", "success")
            return redirect(url_for("paciente_detalhe", paciente_id=p.id))

        return render_template(
            "paciente_novo.html",
            proximo_prontuario=gerar_proximo_prontuario(),
            hoje_str=datetime.now().strftime("%d/%m/%Y"),
        )

    @app.route("/paciente/<int:paciente_id>")
    @login_required
    def paciente_detalhe(paciente_id):
        paciente = db.session.get(Paciente, paciente_id)
        if not paciente:
            abort(404)

        aba = request.args.get("aba", "cadastro")
        # Atendente não pode abrir a aba anamnese diretamente
        if aba == "anamnese" and not current_user.pode_ver_clinico:
            abort(403)

        sessoes = (
            Agendamento.query.filter_by(paciente_id=paciente.id)
            .order_by(Agendamento.inicio.asc())
            .all()
        )
        envios = (
            FormularioEnvio.query.filter_by(paciente_id=paciente.id)
            .order_by(FormularioEnvio.criado_em.desc())
            .all()
        )
        cfg_url = db.session.get(ConfiguracaoSistema, "app_base_url")
        base_url = (cfg_url.valor if cfg_url and cfg_url.valor else app.config["APP_BASE_URL"]).rstrip("/")
        resumo_sessoes = _calcular_resumo_sessoes(sessoes)
        anamnese = paciente.anamnese
        return render_template(
            "paciente_detalhe.html",
            paciente=paciente,
            cad=paciente.cadastro,
            anamnese=anamnese,
            anam=anamnese.dados if anamnese else {},
            sessoes=sessoes,
            envios=envios,
            base_url=base_url,
            resumo=resumo_sessoes,
            aba=aba,
            hoje_str=datetime.now().strftime("%d/%m/%Y"),
        )

    @app.route("/paciente/<int:paciente_id>/cadastro", methods=["POST"])
    @login_required
    def paciente_salvar_cadastro(paciente_id):
        paciente = db.session.get(Paciente, paciente_id)
        if not paciente:
            abort(404)

        nome = request.form.get("nome_completo", "").strip()
        if nome:
            paciente.nome_completo = nome
        paciente.telefone = request.form.get("telefone", "").strip()
        paciente.email = request.form.get("email", "").strip()
        paciente.cpf = request.form.get("cpf", "").strip()
        paciente.cadastro = _extrair_dados_cadastro(request.form)
        db.session.commit()
        flash("Ficha de Protocolo & Cadastro atualizada com sucesso.", "success")
        return redirect(url_for("paciente_detalhe", paciente_id=paciente.id, aba="cadastro"))

    @app.route("/paciente/<int:paciente_id>/anamnese", methods=["GET", "POST"])
    @roles_required("psicanalista", "admin_dev")
    def paciente_anamnese(paciente_id):
        paciente = db.session.get(Paciente, paciente_id)
        if not paciente:
            abort(404)

        if request.method == "GET":
            return redirect(url_for("paciente_detalhe", paciente_id=paciente.id, aba="anamnese"))

        anamnese = paciente.anamnese
        if not anamnese:
            anamnese = Anamnese(paciente_id=paciente.id)
            db.session.add(anamnese)

        anamnese.data_anamnese = request.form.get("data_anamnese", datetime.now().strftime("%d/%m/%Y")).strip()
        campos = [
            "motivo_procura",
            "historia_queixa",
            "historia_familiar",
            "desenvolvimento_infantil",
            "escolaridade_historico",
            "vida_pessoal",
            "relacionamento_afetivo",
            "saude_fisica",
            "uso_medicamentos",
            "habitos_vida",
            "expectativas",
            "observacoes_iniciais",
        ]
        anamnese.dados = {c: request.form.get(c, "").strip() for c in campos}
        db.session.commit()
        flash("Ficha de Anamnese Clínica salva com sigilo.", "success")
        return redirect(url_for("paciente_detalhe", paciente_id=paciente.id, aba="anamnese"))

    @app.route("/paciente/<int:paciente_id>/sessao/nova", methods=["POST"])
    @login_required
    def paciente_nova_sessao(paciente_id):
        paciente = db.session.get(Paciente, paciente_id)
        if not paciente:
            abort(404)

        data_str = request.form.get("data_sessao", "").strip() or datetime.now().strftime("%Y-%m-%d")
        hora_str = request.form.get("horario", "").strip() or "09:00"
        try:
            inicio_dt = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            inicio_dt = datetime.now()

        fim_dt = inicio_dt.replace(minute=(inicio_dt.minute + 50) % 60)
        valor_raw = request.form.get("valor", "0").replace(",", ".").strip()
        try:
            valor = float(valor_raw) if valor_raw else 0.0
        except ValueError:
            valor = 0.0

        obs = request.form.get("observacao", "").strip()
        if not current_user.pode_ver_clinico and obs:
            # Atendente registra apenas nota administrativa se necessário
            pass

        ag = Agendamento(
            paciente_id=paciente.id,
            usuario_id=current_user.id,
            titulo=f"Sessão - {paciente.nome_completo}",
            inicio=inicio_dt,
            fim=fim_dt,
            modalidade=request.form.get("modalidade", "Presencial"),
            status="Realizado" if request.form.get("compareceu") in ("Sim", "Não") else "Agendado",
            compareceu=request.form.get("compareceu", ""),
            pagamento=request.form.get("pagamento", "Pendente"),
            valor=valor,
            observacao=obs,
        )
        db.session.add(ag)
        db.session.commit()
        flash("Sessão registrada no controle individual.", "success")
        return redirect(url_for("paciente_detalhe", paciente_id=paciente.id, aba="sessoes"))

    @app.route("/paciente/<int:paciente_id>/sessao/<int:sessao_id>/atualizar", methods=["POST"])
    @login_required
    def paciente_atualizar_sessao(paciente_id, sessao_id):
        ag = db.session.get(Agendamento, sessao_id)
        if not ag or ag.paciente_id != paciente_id:
            abort(404)

        ag.compareceu = request.form.get("compareceu", ag.compareceu)
        ag.pagamento = request.form.get("pagamento", ag.pagamento)
        if current_user.pode_ver_clinico or "observacao" in request.form:
            ag.observacao = request.form.get("observacao", ag.observacao)
        if ag.compareceu in ("Sim", "Não"):
            ag.status = "Realizado"
        db.session.commit()
        flash("Sessão atualizada.", "success")
        return redirect(url_for("paciente_detalhe", paciente_id=paciente_id, aba="sessoes"))

    # =========================================================================
    # IMPRESSÃO A4 DAS 3 FICHAS
    # =========================================================================
    @app.route("/paciente/<int:paciente_id>/imprimir/<tipo>")
    @login_required
    def imprimir_ficha(paciente_id, tipo):
        paciente = db.session.get(Paciente, paciente_id)
        if not paciente:
            abort(404)

        if tipo == "cadastro":
            return render_template(
                "impressao_cadastro.html",
                paciente=paciente,
                cad=paciente.cadastro,
                hoje=datetime.now(),
            )
        if tipo == "anamnese":
            if not current_user.pode_ver_clinico:
                abort(403)
            anamnese = paciente.anamnese
            return render_template(
                "impressao_anamnese.html",
                paciente=paciente,
                anamnese=anamnese,
                anam=anamnese.dados if anamnese else {},
                hoje=datetime.now(),
            )
        if tipo == "sessoes":
            sessoes = (
                Agendamento.query.filter_by(paciente_id=paciente.id)
                .order_by(Agendamento.inicio.asc())
                .all()
            )
            return render_template(
                "impressao_sessoes.html",
                paciente=paciente,
                sessoes=sessoes,
                resumo=_calcular_resumo_sessoes(sessoes),
                hoje=datetime.now(),
            )
        abort(404)

    # =========================================================================
    # PAINEL ADMIN / MANUTENÇÃO (EXCLUSIVO admin_dev)
    # =========================================================================
    @app.route("/admin-dev", methods=["GET", "POST"])
    @roles_required("admin_dev")
    def admin_dev():
        if request.method == "POST":
            acao = request.form.get("acao")
            if acao == "criar_usuario":
                nome = request.form.get("nome", "").strip()
                email = request.form.get("email", "").strip().lower()
                senha = request.form.get("senha", "")
                perfil = request.form.get("perfil", "atendente")
                if nome and email and senha and perfil in ("admin_dev", "psicanalista", "atendente"):
                    if Usuario.query.filter_by(email=email).first():
                        flash("Já existe um usuário com este e-mail.", "warning")
                    else:
                        u = Usuario(nome=nome, email=email, perfil=perfil, ativo=True)
                        u.set_password(senha)
                        db.session.add(u)
                        db.session.commit()
                        flash(f"Usuário {nome} ({perfil}) criado com sucesso.", "success")
            elif acao == "toggle_usuario":
                uid = int(request.form.get("usuario_id", 0))
                u = db.session.get(Usuario, uid)
                if u and u.id != current_user.id:
                    u.ativo = not u.ativo
                    db.session.commit()
                    flash(f"Status de {u.nome} atualizado.", "info")
            elif acao == "salvar_configs":
                pares = {
                    "app_base_url": request.form.get("app_base_url", "").strip().rstrip("/"),
                    "whatsapp_psicanalista": request.form.get("whatsapp_psicanalista", "").strip(),
                    "whatsapp_atendimento": request.form.get("whatsapp_atendimento", "").strip(),
                }
                for chave, valor in pares.items():
                    if chave == "app_base_url" and not valor:
                        continue
                    cfg = db.session.get(ConfiguracaoSistema, chave)
                    if not cfg:
                        db.session.add(ConfiguracaoSistema(chave=chave, valor=valor))
                    else:
                        cfg.valor = valor
                db.session.commit()
                flash("Configurações do sistema e WhatsApp atualizadas com sucesso.", "success")
            return redirect(url_for("admin_dev"))

        usuarios = Usuario.query.order_by(Usuario.id.asc()).all()
        cfg_url = db.session.get(ConfiguracaoSistema, "app_base_url")
        cfg_psi = db.session.get(ConfiguracaoSistema, "whatsapp_psicanalista")
        cfg_atend = db.session.get(ConfiguracaoSistema, "whatsapp_atendimento")
        return render_template(
            "admin_dev.html",
            usuarios=usuarios,
            app_base_url=cfg_url.valor if cfg_url else app.config["APP_BASE_URL"],
            whatsapp_psicanalista=cfg_psi.valor if cfg_psi else "",
            whatsapp_atendimento=cfg_atend.valor if cfg_atend else "",
            db_uri=app.config["SQLALCHEMY_DATABASE_URI"],
            data_dir=DATA_DIR,
            app_version=APP_VERSION,
        )

    @app.route("/admin-dev/backup")
    @roles_required("admin_dev")
    def admin_dev_backup():
        uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if not uri.startswith("sqlite:///"):
            flash("Backup direto de arquivo .db está disponível apenas em banco SQLite.", "warning")
            return redirect(url_for("admin_dev"))
        db_path = uri.replace("sqlite:///", "", 1)
        if not os.path.exists(db_path):
            abort(404)
        nome_download = f"backup_rb_psicanalise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        return send_file(db_path, as_attachment=True, download_name=nome_download)

    # =========================================================================
    # ETAPA 4: VERIFICAÇÃO E ATUALIZAÇÃO SEGURA IN-PLACE (.EXE)
    # =========================================================================
    @app.route("/api/sistema/checar-atualizacao")
    @login_required
    def api_checar_atualizacao():
        return jsonify(verificar_atualizacao())

    @app.route("/api/sistema/atualizar", methods=["POST"])
    @login_required
    def api_aplicar_atualizacao():
        info = verificar_atualizacao()
        if not info.get("disponivel"):
            return jsonify({"ok": False, "erro": "O sistema já está na versão mais recente."}), 400
        ok, msg = aplicar_atualizacao_exe(
            info.get("exe_url", ""),
            app.config["SQLALCHEMY_DATABASE_URI"],
            DATA_DIR,
        )
        if not ok:
            return jsonify({"ok": False, "erro": msg}), 400

        def _encerrar():
            time.sleep(0.8)
            os._exit(0)

        threading.Thread(target=_encerrar, daemon=True).start()
        return jsonify({"ok": True, "mensagem": msg})

    # =========================================================================
    # ETAPA 2: QUADRO KANBAN FLEXÍVEL
    # =========================================================================
    @app.route("/kanban")
    @login_required
    def kanban():
        colunas = KanbanColuna.query.order_by(KanbanColuna.ordem.asc(), KanbanColuna.id.asc()).all()
        pacientes_por_coluna = {}
        for col in colunas:
            pacs = (
                Paciente.query.filter_by(ativo=True, kanban_coluna_id=col.id)
                .order_by(Paciente.kanban_ordem.asc(), Paciente.id.desc())
                .all()
            )
            cards = []
            for p in pacs:
                prox = (
                    Agendamento.query.filter(
                        Agendamento.paciente_id == p.id,
                        Agendamento.inicio >= datetime.now(),
                        Agendamento.status != "Cancelado",
                    )
                    .order_by(Agendamento.inicio.asc())
                    .first()
                )
                pendentes = Agendamento.query.filter_by(paciente_id=p.id, pagamento="Pendente").count()
                tel_limpo = "".join(ch for ch in (p.telefone or "") if ch.isdigit())
                cards.append(
                    {
                        "paciente": p,
                        "proximo": prox,
                        "pendentes": pendentes,
                        "tel_limpo": tel_limpo,
                    }
                )
            pacientes_por_coluna[col.id] = cards

        return render_template("kanban.html", colunas=colunas, pacientes_por_coluna=pacientes_por_coluna)

    @app.route("/api/kanban/mover", methods=["POST"])
    @login_required
    def api_kanban_mover():
        data = request.get_json(silent=True) or {}
        paciente_id = data.get("paciente_id")
        coluna_id = data.get("coluna_id")
        ordem_ids = data.get("ordem_ids", [])

        paciente = db.session.get(Paciente, int(paciente_id)) if paciente_id else None
        coluna = db.session.get(KanbanColuna, int(coluna_id)) if coluna_id else None
        if not paciente or not coluna:
            return jsonify({"ok": False, "erro": "Paciente ou coluna não encontrados."}), 404

        paciente.kanban_coluna_id = coluna.id
        for idx, pid in enumerate(ordem_ids):
            p = db.session.get(Paciente, int(pid))
            if p and p.kanban_coluna_id == coluna.id:
                p.kanban_ordem = idx
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/kanban/colunas", methods=["POST"])
    @login_required
    def api_kanban_criar_coluna():
        data = request.get_json(silent=True) or {}
        titulo = (data.get("titulo") or "").strip()
        cor = (data.get("cor") or "#846122").strip()
        if not titulo:
            return jsonify({"ok": False, "erro": "Título obrigatório."}), 400
        max_ordem = db.session.query(db.func.max(KanbanColuna.ordem)).scalar() or 0
        col = KanbanColuna(titulo=titulo, cor=cor, ordem=max_ordem + 1)
        db.session.add(col)
        db.session.commit()
        return jsonify({"ok": True, "coluna": {"id": col.id, "titulo": col.titulo, "cor": col.cor, "ordem": col.ordem}})

    @app.route("/api/kanban/colunas/<int:col_id>/editar", methods=["POST"])
    @login_required
    def api_kanban_editar_coluna(col_id):
        col = db.session.get(KanbanColuna, col_id)
        if not col:
            return jsonify({"ok": False, "erro": "Coluna não encontrada."}), 404
        data = request.get_json(silent=True) or {}
        if "titulo" in data and data["titulo"].strip():
            col.titulo = data["titulo"].strip()
        if "cor" in data and data["cor"].strip():
            col.cor = data["cor"].strip()
        if "ordem" in data:
            col.ordem = int(data["ordem"])
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/kanban/colunas/<int:col_id>/excluir", methods=["POST"])
    @login_required
    def api_kanban_excluir_coluna(col_id):
        col = db.session.get(KanbanColuna, col_id)
        if not col:
            return jsonify({"ok": False, "erro": "Coluna não encontrada."}), 404
        outras = KanbanColuna.query.filter(KanbanColuna.id != col.id).order_by(KanbanColuna.ordem.asc()).all()
        if not outras:
            return jsonify({"ok": False, "erro": "Não é possível excluir a última coluna."}), 400
        # Move pacientes desta coluna para a primeira coluna disponível
        destino = outras[0]
        for p in Paciente.query.filter_by(kanban_coluna_id=col.id).all():
            p.kanban_coluna_id = destino.id
        db.session.delete(col)
        db.session.commit()
        return jsonify({"ok": True, "destino_id": destino.id})

    @app.route("/api/kanban/card-rapido", methods=["POST"])
    @login_required
    def api_kanban_card_rapido():
        data = request.get_json(silent=True) or {}
        nome = (data.get("nome_completo") or "").strip()
        telefone = (data.get("telefone") or "").strip()
        coluna_id = data.get("coluna_id")
        if not nome:
            return jsonify({"ok": False, "erro": "Nome é obrigatório."}), 400

        col = db.session.get(KanbanColuna, int(coluna_id)) if coluna_id else KanbanColuna.query.order_by(KanbanColuna.ordem.asc()).first()
        p = Paciente(
            prontuario=gerar_proximo_prontuario(),
            nome_completo=nome,
            telefone=telefone,
            kanban_coluna_id=col.id if col else None,
        )
        p.cadastro = {"data_inicio": datetime.now().strftime("%d/%m/%Y")}
        db.session.add(p)
        db.session.commit()
        return jsonify({"ok": True, "paciente_id": p.id, "prontuario": p.prontuario})

    # =========================================================================
    # ETAPA 2: CALENDÁRIO VISUAL DE AGENDA
    # =========================================================================
    @app.route("/agenda")
    @login_required
    def agenda():
        pacientes = Paciente.query.filter_by(ativo=True).order_by(Paciente.nome_completo.asc()).all()
        return render_template("agenda.html", pacientes=pacientes)

    @app.route("/api/agendamentos", methods=["GET", "POST"])
    @login_required
    def api_agendamentos():
        if request.method == "GET":
            ags = Agendamento.query.order_by(Agendamento.inicio.asc()).all()
            eventos = []
            for a in ags:
                if a.status == "Cancelado" or a.compareceu == "Não":
                    cor = "#dc2626"
                elif a.pagamento == "Pago" and a.compareceu == "Sim":
                    cor = "#059669"
                elif a.pagamento == "Pendente" and a.compareceu == "Sim":
                    cor = "#d97706"
                else:
                    cor = "#1e293b"

                pac_nome = a.paciente.nome_completo if a.paciente else "Paciente"
                eventos.append(
                    {
                        "id": a.id,
                        "title": f"{pac_nome} ({a.modalidade})",
                        "start": a.inicio.isoformat(),
                        "end": a.fim.isoformat(),
                        "backgroundColor": cor,
                        "borderColor": cor,
                        "extendedProps": {
                            "paciente_id": a.paciente_id,
                            "paciente_nome": pac_nome,
                            "modalidade": a.modalidade,
                            "status": a.status,
                            "compareceu": a.compareceu,
                            "pagamento": a.pagamento,
                            "valor": a.valor or 0.0,
                            "observacao": a.observacao or "",
                        },
                    }
                )
            return jsonify(eventos)

        # POST: Criar novo agendamento
        data = request.get_json(silent=True) or {}
        paciente_id = data.get("paciente_id")
        paciente = db.session.get(Paciente, int(paciente_id)) if paciente_id else None
        if not paciente:
            return jsonify({"ok": False, "erro": "Paciente inválido."}), 400

        try:
            inicio_dt = datetime.fromisoformat(data["inicio"].replace("Z", ""))
            if data.get("fim"):
                fim_dt = datetime.fromisoformat(data["fim"].replace("Z", ""))
            else:
                fim_dt = inicio_dt + timedelta(minutes=50)
        except Exception:
            return jsonify({"ok": False, "erro": "Data/horário inválido."}), 400

        try:
            valor = float(str(data.get("valor", 0) or 0).replace(",", "."))
        except ValueError:
            valor = 0.0

        ag = Agendamento(
            paciente_id=paciente.id,
            usuario_id=current_user.id,
            titulo=f"Sessão - {paciente.nome_completo}",
            inicio=inicio_dt,
            fim=fim_dt,
            modalidade=data.get("modalidade", "Presencial"),
            status="Agendado",
            compareceu=data.get("compareceu", ""),
            pagamento=data.get("pagamento", "Pendente"),
            valor=valor,
            observacao=data.get("observacao", "").strip(),
        )
        db.session.add(ag)
        db.session.commit()
        return jsonify({"ok": True, "id": ag.id})

    @app.route("/api/agendamentos/<int:ag_id>/atualizar", methods=["POST"])
    @login_required
    def api_agendamento_atualizar(ag_id):
        ag = db.session.get(Agendamento, ag_id)
        if not ag:
            return jsonify({"ok": False, "erro": "Agendamento não encontrado."}), 404

        data = request.get_json(silent=True) or {}
        if data.get("inicio"):
            try:
                ag.inicio = datetime.fromisoformat(data["inicio"].replace("Z", ""))
                ag.fim = (
                    datetime.fromisoformat(data["fim"].replace("Z", ""))
                    if data.get("fim")
                    else ag.inicio + timedelta(minutes=50)
                )
            except Exception:
                return jsonify({"ok": False, "erro": "Data inválida."}), 400

        if "modalidade" in data:
            ag.modalidade = data["modalidade"]
        if "compareceu" in data:
            ag.compareceu = data["compareceu"]
            if ag.compareceu in ("Sim", "Não"):
                ag.status = "Realizado"
        if "pagamento" in data:
            ag.pagamento = data["pagamento"]
        if "status" in data:
            ag.status = data["status"]
        if "valor" in data:
            try:
                ag.valor = float(str(data["valor"] or 0).replace(",", "."))
            except ValueError:
                pass
        if "observacao" in data:
            ag.observacao = (data["observacao"] or "").strip()

        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/agendamentos/<int:ag_id>/excluir", methods=["POST"])
    @login_required
    def api_agendamento_excluir(ag_id):
        ag = db.session.get(Agendamento, ag_id)
        if not ag:
            return jsonify({"ok": False, "erro": "Agendamento não encontrado."}), 404
        db.session.delete(ag)
        db.session.commit()
        return jsonify({"ok": True})

    # =========================================================================
    # ETAPA 3: CRIADOR DE FORMULÁRIOS, LINK PÚBLICO & WHATSAPP
    # =========================================================================
    @app.route("/formularios")
    @login_required
    def formularios():
        lista_forms = Formulario.query.order_by(Formulario.id.asc()).all()
        pacientes = Paciente.query.filter_by(ativo=True).order_by(Paciente.nome_completo.asc()).all()
        envios = FormularioEnvio.query.order_by(FormularioEnvio.criado_em.desc()).limit(30).all()
        cfg_url = db.session.get(ConfiguracaoSistema, "app_base_url")
        base_url = (cfg_url.valor if cfg_url and cfg_url.valor else app.config["APP_BASE_URL"]).rstrip("/")
        return render_template(
            "formularios.html",
            formularios=lista_forms,
            pacientes=pacientes,
            envios=envios,
            base_url=base_url,
        )

    @app.route("/api/formularios/salvar", methods=["POST"])
    @login_required
    def api_formularios_salvar():
        data = request.get_json(silent=True) or {}
        form_id = data.get("id")
        titulo = (data.get("titulo") or "").strip()
        descricao = (data.get("descricao") or "").strip()
        campos = data.get("campos") or []

        if not titulo or not campos:
            return jsonify({"ok": False, "erro": "Informe o título e pelo menos uma pergunta."}), 400

        if form_id:
            f = db.session.get(Formulario, int(form_id))
            if not f:
                return jsonify({"ok": False, "erro": "Formulário não encontrado."}), 404
        else:
            f = Formulario(titulo=titulo)
            db.session.add(f)

        f.titulo = titulo
        f.descricao = descricao
        f.sigiloso = bool(data.get("sigiloso", False))
        f.campos = campos
        db.session.commit()
        return jsonify({"ok": True, "id": f.id})

    @app.route("/api/formularios/<int:form_id>/excluir", methods=["POST"])
    @login_required
    def api_formularios_excluir(form_id):
        f = db.session.get(Formulario, form_id)
        if not f:
            return jsonify({"ok": False, "erro": "Formulário não encontrado."}), 404
        if FormularioEnvio.query.filter_by(formulario_id=f.id).count() > 0:
            f.ativo = False
            db.session.commit()
            return jsonify({"ok": True, "arquivado": True})
        db.session.delete(f)
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/formularios/gerar-link", methods=["POST"])
    @login_required
    def api_formularios_gerar_link():
        data = request.get_json(silent=True) or {}
        form_id = data.get("formulario_id")
        paciente_id = data.get("paciente_id")

        form_obj = db.session.get(Formulario, int(form_id)) if form_id else None
        pac_obj = db.session.get(Paciente, int(paciente_id)) if paciente_id else None
        if not form_obj or not pac_obj:
            return jsonify({"ok": False, "erro": "Selecione um formulário e um paciente válidos."}), 400

        token = uuid.uuid4().hex
        envio = FormularioEnvio(
            formulario_id=form_obj.id,
            paciente_id=pac_obj.id,
            token=token,
            status="Aguardando",
        )
        db.session.add(envio)
        db.session.commit()

        cfg_url = db.session.get(ConfiguracaoSistema, "app_base_url")
        base_url = (cfg_url.valor if cfg_url and cfg_url.valor else app.config["APP_BASE_URL"]).rstrip("/")
        link_publico = f"{base_url}/responder/{token}"

        tel_digits = "".join(ch for ch in (pac_obj.telefone or "") if ch.isdigit())
        primeiro_nome = pac_obj.nome_completo.split()[0] if pac_obj.nome_completo else "Paciente"
        msg = (
            f"Olá, {primeiro_nome}! Tudo bem?\n"
            f"Segue o link da *RB Psicanálise* para preenchimento do formulário *{form_obj.titulo}*:\n"
            f"{link_publico}\n\n"
            f"Qualquer dúvida, estamos à disposição!"
        )
        if tel_digits:
            if not tel_digits.startswith("55") and len(tel_digits) <= 11:
                tel_digits = "55" + tel_digits
            whatsapp_url = f"https://wa.me/{tel_digits}?text={quote(msg)}"
        else:
            whatsapp_url = f"https://wa.me/?text={quote(msg)}"

        return jsonify(
            {
                "ok": True,
                "token": token,
                "url": link_publico,
                "whatsapp_url": whatsapp_url,
            }
        )

    @app.route("/responder/<token>", methods=["GET", "POST"])
    def responder_formulario_publico(token):
        envio = FormularioEnvio.query.filter_by(token=token).first()
        if not envio:
            return render_template("formulario_publico.html", erro="Link inválido ou não encontrado."), 404

        if envio.status == "Respondido":
            return render_template(
                "formulario_publico.html",
                envio=envio,
                ja_respondido=True,
            )

        campos = envio.formulario.campos if envio.formulario else []
        if request.method == "POST":
            respostas = {}
            faltando = []
            for idx, c in enumerate(campos):
                cid = c.get("id") or f"campo_{idx}"
                val = request.form.get(cid, "").strip()
                if c.get("obrigatorio") and not val:
                    faltando.append(c.get("label", cid))
                respostas[c.get("label", cid)] = val

            if faltando:
                return render_template(
                    "formulario_publico.html",
                    envio=envio,
                    campos=campos,
                    erro_form=f"Por favor, preencha os campos obrigatórios: {', '.join(faltando)}.",
                ), 400

            envio.respostas = respostas
            envio.status = "Respondido"
            envio.respondido_em = utcnow()
            db.session.commit()

            # Roteamento de notificação WhatsApp respeitando o sigilo
            eh_sigiloso = bool(envio.formulario and envio.formulario.sigiloso)
            chave_wpp = "whatsapp_psicanalista" if eh_sigiloso else "whatsapp_atendimento"
            cfg_wpp = db.session.get(ConfiguracaoSistema, chave_wpp)
            num_wpp = "".join(ch for ch in (cfg_wpp.valor if cfg_wpp and cfg_wpp.valor else "") if ch.isdigit())
            whatsapp_notificar_url = ""
            if num_wpp:
                if not num_wpp.startswith("55") and len(num_wpp) <= 11:
                    num_wpp = "55" + num_wpp
                aviso = (
                    f"Olá! Sou {envio.paciente.nome_completo} e acabei de preencher o formulário "
                    f"*{envio.formulario.titulo if envio.formulario else ''}* na RB Psicanálise."
                )
                whatsapp_notificar_url = f"https://wa.me/{num_wpp}?text={quote(aviso)}"

            return render_template(
                "formulario_publico.html",
                envio=envio,
                enviado_agora=True,
                whatsapp_notificar_url=whatsapp_notificar_url,
            )

        return render_template("formulario_publico.html", envio=envio, campos=campos)

    return app


def _extrair_dados_cadastro(form) -> dict:
    campos = [
        "data_nascimento",
        "idade",
        "estado_civil",
        "profissao",
        "escolaridade",
        "rg",
        "endereco",
        "cidade",
        "cep",
        "contato_emergencial",
        "grau_parentesco",
        "telefone_emergencia",
        "como_conheceu",
        "data_inicio",
        "ja_fez_terapia",
        "detalhe_terapia",
        "faz_uso_medicacao",
        "qual_medicacao",
        "acompanhamento_medico",
        "detalhe_medico",
        "queixa_principal",
        "condicoes_saude",
        "frequencia",
        "duracao",
        "honorarios",
        "formato_atendimento",
    ]
    dados = {c: form.get(c, "").strip() for c in campos}
    dados["termo_aceito"] = form.get("termo_aceito") == "on"
    return dados


def _calcular_resumo_sessoes(sessoes) -> dict:
    total = len(sessoes)
    sim = sum(1 for s in sessoes if s.compareceu == "Sim")
    nao = sum(1 for s in sessoes if s.compareceu == "Não")
    pago = sum(1 for s in sessoes if s.pagamento == "Pago")
    pendente = sum(1 for s in sessoes if s.pagamento == "Pendente")
    total_pago_rs = sum((s.valor or 0.0) for s in sessoes if s.pagamento == "Pago")
    total_pendente_rs = sum((s.valor or 0.0) for s in sessoes if s.pagamento == "Pendente")
    return {
        "total": total,
        "sim": sim,
        "nao": nao,
        "pago": pago,
        "pendente": pendente,
        "total_pago_rs": total_pago_rs,
        "total_pendente_rs": total_pendente_rs,
    }


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["FLASK_ENV"] == "development")
