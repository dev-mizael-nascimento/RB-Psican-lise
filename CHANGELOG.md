# CHANGELOG — Sistema Clínico RB Psicanálise

Documentação detalhada de todas as funcionalidades implementadas, arquitetura de funcionamento, regras de segurança e histórico de versões do sistema web/desktop da **RB Psicanálise**.

---

## `[v1.0.2]` — Em Revisão (Pronto para Subir ao GitHub)

### Novidades & Melhorias Implementadas

#### 1. Ficha de Acompanhamento Clínico Contínua (Evolução por Sessão)
- **Onde fica:** Aba **05. Acompanhamento Clínico** dentro do Prontuário de cada paciente (`templates/paciente_detalhe.html`).
- **Como funciona:**
  - Permite ao psicanalista registrar as anotações clínicas de cada sessão (`Sessão Nº` sugerido automaticamente, `Data`, `Tema Central / Significantes`, `Anotações Clínicas` e `Intervenções / Continuidade`).
  - Todas as sessões ficam reunidas na **mesma ficha em ordem cronológica contínua**, com possibilidade de editar qualquer sessão diretamente na linha do tempo.
  - Possui impressão dedicada em A4 (**Imprimir Acompanhamento A4** — `templates/impressao_acompanhamento.html`), gerando um dossiê completo com todas as sessões juntas para visualização integral.
- **Sigilo (`RBAC`):** Restrito exclusivamente aos perfis **`psicanalista`** e **`admin_dev`**. Tentativas de acesso pelo perfil `atendente` (inclusive por URL direta) são bloqueadas no servidor com erro **`403`**.

#### 2. Central de Notificações & Lembretes WhatsApp
- **Onde fica:** Menu lateral **Notificações** (`/notificacoes`, `templates/notificacoes.html`), com **ícone de sino** e contador vermelho ao vivo mostrando pendências.
- **Como funciona:**
  - **Compromissos da Agenda (Hoje e Amanhã):** Lista todas as sessões não canceladas de hoje e amanhã com:
    - Botão **Lembrar Paciente (WhatsApp)**: abre a conversa do paciente já com mensagem pronta confirmando dia, horário e modalidade.
    - Botão **Avisar Psicanalista (WhatsApp)**: envia para o número do(a) Psicanalista configurado em *Manutenção (Dev)* apenas nome do paciente, dia, horário e modalidade (sem expor notas clínicas).
    - Controle **Marcar Enviado** (`lembrete_enviado` salvo no SQLite) para a recepção saber quem já foi lembrado.
  - **Pagamentos Pendentes:** Lista sessões realizadas (`Compareceu = Sim`) com status `Pendente` e botão **Enviar Lembrete** via WhatsApp.
  - **Últimos Formulários Respondidos:** Lista com atalho direto para abrir as respostas recém-enviadas pelos pacientes.

#### 3. Dashboard Executivo com Gráficos Reais (`fx-chart` & `fx-bars`)
- **Onde fica:** Tela inicial (`/`, `templates/dashboard.html`).
- **Como funciona:**
  - **Ritmo de Atendimentos (`fx-chart`):** Gráfico de área interativo alimentado pelos agendamentos reais dos últimos 14 dias no SQLite, com cursor dinâmico, tooltip ao passar o mouse e navegação pelas setas do teclado.
  - **Receita Mensal Paga (`fx-bars`):** Gráfico de barras proporcional em `R$` dos últimos 6 meses de sessões com pagamento confirmado (`Pago`), destacando o mês atual.

#### 4. Identidade Visual Minimalista, Ícones SVG & Transições Suaves
- **Ícones SVG Minimalistas:** Substituição de todos os emojis da interface por **27 ícones SVG** da biblioteca `design-taste-frontend` em `RB_Psicanalise_Web/static/icons/`, renderizados inline via helper `icon(nome, tamanho)` em `app.py` (com ajuste automático de `width`/`height` para evitar distorções em logos coloridos como o do WhatsApp).
- **Transições Suaves:** Adicionado `@view-transition { navigation: auto; }`, animação de entrada `pageEnter` (`280ms`), *fade-out* discreto ao trocar de tela/aba e abertura suave de modais com `backdrop-filter: blur(2px)`.

#### 5. Correção do Atalho na Área de Trabalho (OneDrive)
- **Onde fica:** `RB_Psicanalise_Web/desktop_launcher.py`.
- **Como funciona:** Passa a consultar `[Environment]::GetFolderPath('Desktop')` via PowerShell para localizar corretamente a Área de Trabalho mesmo quando sincronizada com o **OneDrive** (`OneDrive\Desktop`).

---

## `[v1.0.1]` — Experiência Desktop (`.exe`) & Ícone Próprio

### Melhorias Implementadas
- **Ícone Próprio do Sistema (`app_icon.png` / `app_icon.ico`):** Gerado a partir do emblema `RB` (primeira parte da logo, sem o texto *Psicanálise*) em quadrado arredondado com borda dourada.
- **Execução Silenciosa sem Tela Preta (`--noconsole`):** Compilação no GitHub Actions sem abertura da janela preta do Prompt de Comando.
- **Ícone na Bandeja do Windows (`pystray`):** O `.exe` roda em segundo plano ao lado do relógio com menu (*Abrir RB Psicanálise*, *Pasta de Dados e Backups*, *Encerrar Sistema*).
- **Instalação Protegida & Instância Única:**
  - Copia o executável para `%LOCALAPPDATA%\RB_Psicanalise\App\RB_Psicanalise.exe` (evitando exclusão acidental pelo usuário).
  - Se o servidor já estiver rodando na porta `5000`, clicar novamente no atalho apenas reabre a aba no navegador sem erro.

---

## `[v1.0.0]` — Fundação do Sistema Web/Desktop & Módulos Principais

### Como Cada Módulo Funciona

#### 1. Segurança, `.env` & 3 Perfis de Acesso (`RBAC`)
- **Configuração (`config.py` & `.env`):** Separa segredos (`SECRET_KEY`, `DATABASE_URL`, `APP_BASE_URL`, credenciais iniciais). Suporta **SQLite** localmente (salvo em `%LOCALAPPDATA%\RB_Psicanalise\` no `.exe`) e **PostgreSQL** em nuvem (`Procfile` + `gunicorn`).
- **3 Perfis:**
  - `admin_dev` (Desenvolvedor / Manutenção): acesso total + painel `/admin-dev` (usuários, `APP_BASE_URL`, WhatsApp de roteamento, checagem de versão e download de backup `.db`).
  - `psicanalista`: acesso clínico completo (incluindo Anamnese, Acompanhamento Clínico e respostas de formulários sigilosos).
  - `atendente` (Recepção): acesso operacional (Kanban, Agenda, Cadastro, Sessões/Pagamentos, Envio de Formulários e Notificações). Bloqueado com `403` em Anamnese, Acompanhamento Clínico e respostas sigilosas.

#### 2. Quadro Kanban Flexível (`/kanban`)
- Colunas customizáveis (criar, renomear, trocar cor, excluir com realocação segura de cards).
- **Drag & Drop** via SortableJS com salvamento automático da posição no SQLite.
- Cards com atalho WhatsApp, próximo horário agendado, alerta de pagamentos pendentes e botão **+ Contato / Paciente Rápido**.

#### 3. Calendário Visual de Agenda (`/agenda`)
- **FullCalendar** em português (visões Mês, Semana, Dia e Lista).
- Agendamento em 2 cliques, remarcação arrastando eventos e baixa rápida de `Compareceu (Sim/Não)` e `Pagamento (Pago/Pendente)` integrada automaticamente ao Controle de Sessões do paciente.

#### 4. Criador de Formulários, Link Público & Sigilo (`/formularios` e `/responder/<token>`)
- Construtor visual de perguntas (*Texto Curto*, *Parágrafo*, *Sim/Não*, *Data*, *Múltipla Escolha* e marcação **Sigiloso**), já com 2 modelos prontos (*Pré-Cadastro & Termo* e *Questionário de Anamnese Inicial*).
- Geração de link exclusivo com token UUID (`/responder/<token>`) + botões **Copiar Link** e **Enviar no WhatsApp**.
- Página pública mobile-friendly com logotipo RB Psicanálise, proteção contra reenvio duplicado e botão final de confirmação no WhatsApp direcionado ao **Psicanalista** (se sigiloso) ou ao **Atendimento da Clínica** (nos demais).

#### 5. Prontuário Unificado & Impressão A4 + Auto-Update
- Impressão A4 fiel às fichas originais da clínica (Cadastro + Termo, Anamnese, Controle Individual de Sessões e Acompanhamento Clínico).
- **Auto-Update Seguro (`updater.py`):** Verifica novas Releases no GitHub, cria backup automático do banco `.db`, baixa apenas o novo `.exe` e reinicia sem precisar reinstalar e sem perda de dados.
- **Compilação Automática:** GitHub Actions (`.github/workflows/build-windows-exe.yml`) gera `RB_Psicanalise.exe` automaticamente a cada `push` / tag `v*`.

---

## Cobertura de Testes Automatizados (`RB_Psicanalise_Web/tests/`)
- `test_etapa1.py`: Login obrigatório, seed dos 3 perfis, CRUD de paciente/sessão/anamnese e bloqueio `403` do atendente.
- `test_etapa2.py`: APIs do Kanban (criar/editar/mover/excluir) e da Agenda Visual integrada ao Controle de Sessões.
- `test_etapa3.py`: Modelos prontos, Form Builder, link público `/responder/<token>`, bloqueio de reenvio, roteamento WhatsApp e sigilo.
- `test_etapa4.py`: Comparação de versões, backup preventivo do SQLite e resiliência offline do verificador de atualizações.
- `test_acompanhamento.py`: Registro contínuo na Ficha de Acompanhamento Clínico, edição, impressão A4 e bloqueio `403` para atendente.
- `test_notificacoes.py`: Central de Notificações, geração de lembretes WhatsApp (paciente e psicanalista) e marcação de enviado.
- **Status atual:** `12 testes` executados via `python -m unittest discover -s RB_Psicanalise_Web/tests -v` — **100% aprovados**.
