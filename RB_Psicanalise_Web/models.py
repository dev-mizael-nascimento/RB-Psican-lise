import json
import os
from datetime import datetime, timezone
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    # Perfis: admin_dev | psicanalista | atendente
    perfil = db.Column(db.String(30), nullable=False, default="atendente")
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=utcnow)

    def set_password(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_active(self):
        return bool(self.ativo)

    @property
    def pode_ver_clinico(self) -> bool:
        """Apenas psicanalista e admin_dev podem ver Anamnese e Observações Clínicas."""
        return self.perfil in ("psicanalista", "admin_dev")

    @property
    def is_admin_dev(self) -> bool:
        return self.perfil == "admin_dev"


class ConfiguracaoSistema(db.Model):
    __tablename__ = "configuracoes"

    chave = db.Column(db.String(80), primary_key=True)
    valor = db.Column(db.Text, nullable=True)


class KanbanColuna(db.Model):
    __tablename__ = "kanban_colunas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    cor = db.Column(db.String(20), nullable=False, default="#846122")
    ordem = db.Column(db.Integer, nullable=False, default=0)

    pacientes = db.relationship("Paciente", backref="kanban_coluna", lazy=True)


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    prontuario = db.Column(db.String(30), unique=True, nullable=False, index=True)
    nome_completo = db.Column(db.String(160), nullable=False, index=True)
    telefone = db.Column(db.String(30), default="")
    email = db.Column(db.String(150), default="")
    cpf = db.Column(db.String(20), default="")
    kanban_coluna_id = db.Column(db.Integer, db.ForeignKey("kanban_colunas.id"), nullable=True)
    kanban_ordem = db.Column(db.Integer, nullable=False, default=0)
    dados_cadastro_json = db.Column(db.Text, nullable=False, default="{}")
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=utcnow)

    anamnese = db.relationship(
        "Anamnese", backref="paciente", uselist=False, cascade="all, delete-orphan"
    )
    agendamentos = db.relationship(
        "Agendamento", backref="paciente", cascade="all, delete-orphan", order_by="Agendamento.inicio.desc()"
    )
    envios_formularios = db.relationship(
        "FormularioEnvio", backref="paciente", cascade="all, delete-orphan"
    )
    evolucoes = db.relationship(
        "EvolucaoClinica",
        backref="paciente",
        cascade="all, delete-orphan",
        order_by="EvolucaoClinica.numero_sessao.asc()",
    )

    @property
    def cadastro(self) -> dict:
        try:
            return json.loads(self.dados_cadastro_json or "{}")
        except json.JSONDecodeError:
            return {}

    @cadastro.setter
    def cadastro(self, data: dict):
        self.dados_cadastro_json = json.dumps(data or {}, ensure_ascii=False)


class Anamnese(db.Model):
    __tablename__ = "anamneses"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), unique=True, nullable=False)
    data_anamnese = db.Column(db.String(20), default="")
    dados_anamnese_json = db.Column(db.Text, nullable=False, default="{}")
    atualizado_em = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

    @property
    def dados(self) -> dict:
        try:
            return json.loads(self.dados_anamnese_json or "{}")
        except json.JSONDecodeError:
            return {}

    @dados.setter
    def dados(self, data: dict):
        self.dados_anamnese_json = json.dumps(data or {}, ensure_ascii=False)


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    titulo = db.Column(db.String(160), default="Sessão de Psicanálise")
    inicio = db.Column(db.DateTime, nullable=False, index=True)
    fim = db.Column(db.DateTime, nullable=False)
    modalidade = db.Column(db.String(30), default="Presencial")
    status = db.Column(db.String(30), default="Agendado")  # Agendado | Realizado | Cancelado
    compareceu = db.Column(db.String(10), default="")  # "" | Sim | Não
    pagamento = db.Column(db.String(20), default="Pendente")  # Pago | Pendente
    valor = db.Column(db.Float, default=0.0)
    observacao = db.Column(db.Text, default="")
    lembrete_enviado = db.Column(db.Boolean, nullable=False, default=False)
    criado_em = db.Column(db.DateTime, default=utcnow)


class EvolucaoClinica(db.Model):
    """Ficha de Acompanhamento Clínico (evolução por sessão na mesma ficha do paciente)."""
    __tablename__ = "evolucoes_clinicas"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    numero_sessao = db.Column(db.Integer, nullable=False, default=1)
    data_sessao = db.Column(db.String(20), nullable=False, default="")
    tema_central = db.Column(db.String(220), default="")
    anotacoes_clinicas = db.Column(db.Text, nullable=False, default="")
    intervencoes = db.Column(db.Text, default="")
    criado_em = db.Column(db.DateTime, default=utcnow)
    atualizado_em = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)


class Formulario(db.Model):
    __tablename__ = "formularios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(160), nullable=False)
    descricao = db.Column(db.Text, default="")
    estrutura_campos_json = db.Column(db.Text, nullable=False, default="[]")
    sigiloso = db.Column(db.Boolean, nullable=False, default=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=utcnow)

    @property
    def campos(self) -> list:
        try:
            return json.loads(self.estrutura_campos_json or "[]")
        except json.JSONDecodeError:
            return []

    @campos.setter
    def campos(self, data: list):
        self.estrutura_campos_json = json.dumps(data or [], ensure_ascii=False)


class FormularioEnvio(db.Model):
    __tablename__ = "formulario_envios"

    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey("formularios.id"), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="Aguardando")  # Aguardando | Respondido
    respostas_json = db.Column(db.Text, nullable=False, default="{}")
    criado_em = db.Column(db.DateTime, default=utcnow)
    respondido_em = db.Column(db.DateTime, nullable=True)

    formulario = db.relationship("Formulario")

    @property
    def respostas(self) -> dict:
        try:
            return json.loads(self.respostas_json or "{}")
        except json.JSONDecodeError:
            return {}

    @respostas.setter
    def respostas(self, data: dict):
        self.respostas_json = json.dumps(data or {}, ensure_ascii=False)


def gerar_proximo_prontuario() -> str:
    ano_atual = datetime.now().year
    total = Paciente.query.count() + 1
    while True:
        candidato = f"{total:04d}/{ano_atual}"
        if not Paciente.query.filter_by(prontuario=candidato).first():
            return candidato
        total += 1


def init_db(app):
    """Cria tabelas e popula dados iniciais essenciais se ainda não existirem."""
    with app.app_context():
        db.create_all()

        # Migração segura caso o banco SQLite já exista de etapa anterior
        insp = db.inspect(db.engine)
        cols_form = [c["name"] for c in insp.get_columns("formularios")]
        if "sigiloso" not in cols_form:
            db.session.execute(db.text("ALTER TABLE formularios ADD COLUMN sigiloso BOOLEAN NOT NULL DEFAULT 0"))
            db.session.execute(
                db.text("UPDATE formularios SET sigiloso = 1 WHERE lower(titulo) LIKE '%anamnese%'")
            )
            db.session.commit()

        cols_ag = [c["name"] for c in insp.get_columns("agendamentos")]
        if "lembrete_enviado" not in cols_ag:
            db.session.execute(db.text("ALTER TABLE agendamentos ADD COLUMN lembrete_enviado BOOLEAN NOT NULL DEFAULT 0"))
            db.session.commit()

        # 1. Seed de usuários iniciais
        if Usuario.query.count() == 0:
            usuarios_iniciais = [
                (
                    "Desenvolvedor (Manutenção)",
                    os.environ.get("ADMIN_DEV_EMAIL", "dev@rbpsicanalise.com.br"),
                    os.environ.get("ADMIN_DEV_PASSWORD", "Admin@RB2026"),
                    "admin_dev",
                ),
                (
                    "Psicanalista Responsável",
                    os.environ.get("PSICANALISTA_EMAIL", "clinica@rbpsicanalise.com.br"),
                    os.environ.get("PSICANALISTA_PASSWORD", "Clinica@RB2026"),
                    "psicanalista",
                ),
                (
                    "Recepção / Atendente",
                    os.environ.get("ATENDENTE_EMAIL", "recepcao@rbpsicanalise.com.br"),
                    os.environ.get("ATENDENTE_PASSWORD", "Recepcao@RB2026"),
                    "atendente",
                ),
            ]
            for nome, email, senha, perfil in usuarios_iniciais:
                u = Usuario(nome=nome, email=email.lower().strip(), perfil=perfil, ativo=True)
                u.set_password(senha)
                db.session.add(u)

        # 2. Seed de colunas iniciais do Kanban
        if KanbanColuna.query.count() == 0:
            colunas = [
                ("Contato / Triagem", "#64748b", 1),
                ("Aguardando Formulário", "#d97706", 2),
                ("Agendado", "#2563eb", 3),
                ("Em Análise (Ativo)", "#846122", 4),
                ("Pendência / Retorno", "#dc2626", 5),
            ]
            for titulo, cor, ordem in colunas:
                db.session.add(KanbanColuna(titulo=titulo, cor=cor, ordem=ordem))

        # 3. Seed de Configurações do Sistema
        for chave, padrao in [
            ("app_base_url", app.config.get("APP_BASE_URL", "http://127.0.0.1:5000")),
            ("whatsapp_psicanalista", os.environ.get("WHATSAPP_PSICANALISTA", "")),
            ("whatsapp_atendimento", os.environ.get("WHATSAPP_ATENDIMENTO", "")),
        ]:
            if not db.session.get(ConfiguracaoSistema, chave):
                db.session.add(ConfiguracaoSistema(chave=chave, valor=padrao))

        # 4. Seed de 2 Modelos Prontos de Formulários
        if Formulario.query.count() == 0:
            f1 = Formulario(
                titulo="Pré-Cadastro & Termo de Consentimento",
                descricao="Preenchimento inicial de dados cadastrais e ciência do enquadre analítico.",
                sigiloso=False,
                ativo=True,
            )
            f1.campos = [
                {"id": "nome", "label": "Nome Completo", "tipo": "texto", "obrigatorio": True, "opcoes": []},
                {"id": "nascimento", "label": "Data de Nascimento", "tipo": "data", "obrigatorio": True, "opcoes": []},
                {"id": "cpf", "label": "CPF", "tipo": "texto", "obrigatorio": True, "opcoes": []},
                {"id": "whatsapp", "label": "Telefone / WhatsApp", "tipo": "texto", "obrigatorio": True, "opcoes": []},
                {"id": "emergencia", "label": "Contato Emergencial (Nome e Telefone)", "tipo": "texto", "obrigatorio": True, "opcoes": []},
                {"id": "terapia_previa", "label": "Já realizou psicanálise ou psicoterapia antes?", "tipo": "sim_nao", "obrigatorio": True, "opcoes": []},
                {"id": "medicacao", "label": "Faz uso de medicação contínua? Se sim, qual?", "tipo": "paragrafo", "obrigatorio": False, "opcoes": []},
                {"id": "termo", "label": "Declaro que compreendo a natureza do atendimento, o sigilo profissional e concordo com os termos.", "tipo": "sim_nao", "obrigatorio": True, "opcoes": []},
            ]
            f2 = Formulario(
                titulo="Questionário de Anamnese Inicial",
                descricao="Perguntas iniciais para preparação da primeira entrevista clínica.",
                sigiloso=True,
                ativo=True,
            )
            f2.campos = [
                {"id": "motivo", "label": "Qual o principal motivo que o(a) levou a buscar atendimento?", "tipo": "paragrafo", "obrigatorio": True, "opcoes": []},
                {"id": "inicio_sintomas", "label": "Há quanto tempo percebe essas questões ou sintomas?", "tipo": "texto", "obrigatorio": False, "opcoes": []},
                {"id": "familia", "label": "Como descreve sua dinâmica familiar atual e de origem?", "tipo": "paragrafo", "obrigatorio": False, "opcoes": []},
                {"id": "sono_habitos", "label": "Como está a qualidade do seu sono e rotina diária?", "tipo": "paragrafo", "obrigatorio": False, "opcoes": []},
                {"id": "expectativas", "label": "O que você espera alcançar com o processo analítico?", "tipo": "paragrafo", "obrigatorio": False, "opcoes": []},
            ]
            db.session.add(f1)
            db.session.add(f2)

        db.session.commit()
