# Plano Técnico e Funcional — Sistema Web Clínico RB Psicanálise

## 1. Visão Geral e Objetivo
Construir um **sistema web completo de gestão e atendimento clínico** para a **RB Psicanálise**, projetado para operar:
- **Localmente** no computador da clínica (com banco **SQLite** e opção de executável `.exe` para Windows compilado automaticamente pelo GitHub Actions);
- **Na Nuvem** (hospedado com `gunicorn`, variáveis em **`.env`** e suporte transparente a **PostgreSQL** ou **SQLite**).

Repositório GitHub do projeto: `https://github.com/dev-mizael-nascimento/RB-Psican-lise.git`

---

## 2. Como Cada Módulo Vai Funcionar na Prática

### 2.1. Segurança, Login e os 3 Perfis de Acesso
Ao acessar o sistema, ninguém entra direto sem autenticação (exceto no link exclusivo de resposta de formulário enviado ao paciente).
- **Credenciais e Segredos (`.env`):**
  - `SECRET_KEY`: chave criptográfica para sessões e proteção **CSRF** em todos os formulários.
  - `DATABASE_URL`: define onde os dados são salvos (`sqlite:///rb_psicanalise.db` no local ou URL do PostgreSQL na nuvem).
  - `APP_BASE_URL`: endereço base usado para montar os links dos formulários enviados no WhatsApp (ex.: `http://127.0.0.1:5000`, IP da rede Wi-Fi, URL de túnel ou domínio HTTPS em nuvem).
  - `ADMIN_DEV_EMAIL` / `ADMIN_DEV_PASSWORD`: usuário mestre inicial criado automaticamente na primeira execução.
- **Regras de Permissão (RBAC — aplicadas no servidor, não apenas escondidas na tela):**
  1. **`admin_dev` (Seu Acesso Geral / Manutenção):**
     - Acesso total a todas as telas clínicas e operacionais.
     - Acesso exclusivo ao **Painel de Manutenção (`/admin-dev`)**: criar/editar/desativar usuários da clínica, redefinir senhas, alterar `APP_BASE_URL` dinamicamente, visualizar informações do banco/ambiente e baixar **Backup completo do SQLite (`.db`)** em 1 clique.
  2. **`psicanalista` (Profissional da Clínica):**
     - Acesso total ao fluxo clínico: Dashboard, Quadro Kanban, Calendário Visual de Agenda, Cadastro & Termo de Consentimento, Controle de Sessões/Financeiro, Criador de Formulários/Respostas, **Anamnese Clínica** e **Observações Iniciais/Clínicas**.
  3. **`atendente` (Recepção / Secretaria):**
     - Acesso focado em atendimento e organização: Dashboard operacional, Quadro Kanban, Calendário Visual de Agenda, Cadastro Inicial do Paciente, Controle de Presença (`Sim/Não`) e Pagamento (`Pago/Pendente`), além de gerar e enviar Formulários via WhatsApp.
     - **Sigilo Protegido:** Se um atendente tentar acessar a aba ou rota da **Anamnese** ou **Observações Clínicas** (mesmo digitando a URL direto), o servidor bloqueia com erro `403 Acesso Restrito ao Psicanalista`.

---

### 2.2. Dashboard Inicial (Visão Rápida do Dia)
Assim que entra, o usuário vê um painel limpo no padrão visual da clínica (Slate `#0f172a` + Dourado `#846122` + Logotipo RB Psicanálise):
- **Cartões de Resumo:** Pacientes Ativos, Sessões Agendadas Hoje, Pagamentos Pendentes (com soma em R$ para quem tem permissão) e Formulários Respondidos Recentemente (alertas novos).
- **Lista Rápida:** Próximos atendimentos do dia e busca instantânea por nome, CPF ou nº de prontuário.

---

### 2.3. Quadro Kanban Flexível (`/kanban`)
Feito para os atendentes baterem o olho e saberem em que fase cada paciente está:
- **Colunas Iniciais (100% editáveis):**
  1. *Contato / Triagem*
  2. *Aguardando Documentos / Formulário*
  3. *Agendado*
  4. *Em Análise (Ativo)*
  5. *Pendência / Retorno*
- **Como funciona a flexibilidade:**
  - **Arrastar e Soltar (Drag & Drop):** Ao arrastar o card de um paciente de uma coluna para outra, o sistema salva a nova posição instantaneamente no banco de dados (sem recarregar a página).
  - **Gerenciar Colunas:** Botão para **+ Nova Coluna**, **Renomear**, **Trocar Cor** da tarja superior ou **Reordenar/Excluir** colunas vazias.
  - **Card Inteligente:** Cada card mostra o nome do paciente, nº do prontuário, botão direto de **WhatsApp**, próximo horário agendado e etiquetas visuais (ex: *"2 pag. pendentes"* ou *"Formulário respondido"*). Clicar no card abre o Prontuário do Paciente.

---

### 2.4. Calendário Visual de Agenda (`/agenda`)
Calendário interativo (**FullCalendar**) integrado ao banco de dados:
- **Visões:** Mês, Semana (grade de horários) e Dia.
- **Como funciona para o atendente:**
  - **Agendar em 2 cliques:** Clica em qualquer horário livre no calendário -> abre um modal para escolher o **Paciente** (ou cadastrar rápido), definir **Horário início/fim**, **Modalidade** (`Presencial` ou `Online`), **Valor da Sessão (R$)** e **Observação**.
  - **Remarcar arrastando:** Arrastar o bloco de um horário para outro dia/hora atualiza automaticamente no banco de dados.
  - **Baixa rápida de Presença & Pagamento:** Ao clicar em um agendamento na agenda, o atendente marca na hora: `Compareceu (Sim/Não)` e `Pagamento (Pago/Pendente)` — isso já alimenta automaticamente o **Controle de Sessões** e os relatórios financeiros do paciente.

---

### 2.5. Criador de Formulários & Link Público para Pacientes (`/formularios` e `/responder/<token>`)
Pensado para enviar triagens, pré-cadastros ou anamneses para o paciente responder pelo celular antes da sessão:
1. **Construtor Visual (Form Builder):**
   - Já vem com **2 modelos prontos** no banco (*Pré-Cadastro + Termo de Consentimento* e *Questionário de Anamnese Inicial*), mas a clínica pode criar quantos formulários quiser.
   - Tipos de pergunta suportados: *Texto Curto*, *Parágrafo*, *Sim / Não*, *Múltipla Escolha*, *Data* e *Telefone/CPF*.
   - É possível adicionar, remover e reordenar as perguntas.
2. **Geração de Link Único & Atalho WhatsApp:**
   - O atendente escolhe o **Formulário** e o **Paciente** e clica em **"Gerar Link"**.
   - O sistema cria um registro com **token UUID exclusivo** (ex.: `https://.../responder/9f4c2a1b...`).
   - Aparecem dois botões práticos:
     - **Copiar Link**
     - **Enviar no WhatsApp** (abre o WhatsApp Web / App direto na conversa do paciente com mensagem profissional pronta contendo o link).
3. **Como o paciente responde (`/responder/<token>`):**
   - O paciente abre o link no celular, vê apenas uma página elegante com o **Logotipo RB Psicanálise** e as perguntas (sem acesso a nenhuma área interna do sistema).
   - Ao clicar em **"Enviar Respostas"**, os dados vão direto para o banco de dados, o token é marcado como `Respondido` (impedindo reenvio duplicado) e aparece um aviso no Dashboard/Prontuário para o psicanalista/atendente consultar ou imprimir.

---

### 2.6. Prontuário Unificado & Impressão A4 das 3 Fichas (`/paciente/<id>`)
Ao abrir qualquer paciente, tudo fica centralizado em abas organizadas:
- **Aba 1 — Ficha de Protocolo & Cadastro + Termo:** Todos os campos pessoais, contato emergencial, histórico médico, setting e aceite do termo.
- **Aba 2 — Ficha de Anamnese Clínica** *(visível apenas para `psicanalista` e `admin_dev`)*: Todos os 12 blocos da anamnese salvos no banco.
- **Aba 3 — Controle de Sessões Individual:** Histórico cronológico automático vindo da Agenda + possibilidade de lançar sessão avulsa, com totais (`Sessões`, `Sim`, `Não`, `Pago`, `Pendente`, `Total R$`).
- **Aba 4 — Formulários Respondidos:** Lista todos os links enviados ao paciente, status (`Aguardando` / `Respondido`) e respostas detalhadas.
- **Impressão A4 Oficial:** Em cada aba há o botão **"Imprimir / Gerar PDF (A4)"**, que abre a ficha exatamente com a mesma diagramação de alto padrão que criamos antes, já preenchida com os dados do banco de dados.

---

### 2.7. Compilação do `.exe` no GitHub Actions & Deploy em Nuvem
- **GitHub Actions (`.github/workflows/build-windows-exe.yml`):**
  - Configurado para o repositório `https://github.com/dev-mizael-nascimento/RB-Psican-lise.git`.
  - Sempre que houver push na `main` (ou disparo manual `workflow_dispatch`), o GitHub sobe uma máquina Windows (`windows-latest`), instala o Python + dependências e roda o **PyInstaller** empacotando o sistema, templates HTML e logotipo em um executável único `RB_Psicanalise.exe`, disponibilizando o `.zip` para download nos **Artifacts** (e em **Releases** quando criar uma tag `v1.0.0`).
- **Nuvem:**
  - `Procfile` (`web: gunicorn app:app`) + `requirements.txt` com `psycopg2-binary` permitem subir direto em plataformas como Render, Railway ou VPS Linux sem alterar código.

---

## 3. Cronograma de Execução (Etapa por Etapa)

1. **Etapa 1 — Fundação, `.env`, Login 3 Perfis, SQLite, Painel `admin_dev` & Prontuário com Fichas A4**
   - Criação de `RB_Psicanalise_Web/` com `.env`, `.env.example`, `config.py`, `models.py`, `app.py`, templates base, login, dashboard, CRUD de pacientes, prontuário (Cadastro, Anamnese restrita, Sessões) e impressão A4.
   - Testes automatizados (`unittest`) validando login, bloqueio `403` do atendente na Anamnese e CRUD no SQLite.
2. **Etapa 2 — Quadro Kanban Flexível & Calendário Visual de Agenda**
   - Drag & drop, criação/edição/reordenação de colunas, FullCalendar com remarcação por arrasto e integração direta com o Controle de Sessões.
   - Testes de API e validação visual no navegador.
3. **Etapa 3 — Criador de Formulários, Link Público & Atalho WhatsApp**
   - Form builder visual, geração de link `/responder/<token>`, página pública mobile-friendly e recebimento de respostas no prontuário.
   - Testes de token válido/expirado/já respondido e validação em aba anônima.
4. **Etapa 4 — GitHub Actions (`.exe` Windows) & Preparo Nuvem**
   - `build_exe.py` / `pyinstaller`, `.github/workflows/build-windows-exe.yml`, `Procfile`, push/validação para o repositório `dev-mizael-nascimento/RB-Psican-lise`.

---

## 4. Estratégia de Verificação
- **Testes Automatizados:** `python -m unittest discover -s RB_Psicanalise_Web/tests` ao final de cada etapa.
- **Verificação Manual:** Execução local com dados reais de teste no navegador, checando permissões de cada perfil (`admin_dev`, `psicanalista`, `atendente`), impressão A4 e persistência no banco SQLite.
