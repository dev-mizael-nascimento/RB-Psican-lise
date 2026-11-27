<div align="center">
  <img src="https://github.com/dev-mizael-nascimento/RB-Psican-lise/blob/main/RB%20Psicanalise%20-%20Sistema%20de%20Fichas/04_Identidade_Visual/Logotipo%20minimalista%20de%20Psican%C3%A1lise.png?raw=true" />
</div>

# RB-Psicanálise

Sistema de Atendimento Clínico e Gestão profissional voltado para a Psicanálise, desenvolvido com Flask, SQLite e uma suíte completa de ferramentas de apoio clínico.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge) ![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white&style=for-the-badge) ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white&style=for-the-badge) ![Flask-SQLAlchemy](https://img.shields.io/badge/Flask%20SQLAlchemy-27272A?style=for-the-badge) ![Flask-Login](https://img.shields.io/badge/Flask-Login-27272A?style=for-the-badge) ![Flask-WTF](https://img.shields.io/badge/Flask-WTF-27272A?style=for-the-badge) ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white&style=for-the-badge) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=for-the-badge) ![Gunicorn](https://img.shields.io/badge/Gunicorn-27272A?style=for-the-badge) ![Waitress](https://img.shields.io/badge/Waitress-27272A?style=for-the-badge) ![PyInstaller](https://img.shields.io/badge/PyInstaller-27272A?style=for-the-badge) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=white&style=for-the-badge) ![Pillow](https://img.shields.io/badge/Pillow-27272A?style=for-the-badge) ![pystray](https://img.shields.io/badge/pystray-27272A?style=for-the-badge)

## ✨ Funcionalidades

- **Controle Completo de Pacientes**: Gerenciamento de cadastros, dados de contato e prontuários clínicos organizados.
- **Fichas Interativas e Prontuários**: Ficha de protocolo, cadastro, anamnese clínica e controle de sessões otimizadas para uso em computador ou exportação em PDF.
- **Gestão de Agendamentos (Agenda)**: Organização de consultas, horários e acompanhamento da rotina de atendimentos.
- **Quadro de Evolução Clínica**: Acompanhamento dinâmico do progresso das sessões e anamneses.
- **Formulários Públicos**: Interfaces web para captação e submissão de dados iniciais por pacientes.
- **Empacotamento Desktop**: Suporte nativo para execução local em ambiente Windows via PyInstaller e atalhos em lote (`.bat`).

## 🛠️ Tecnologias

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="40" alt="html5 logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="40" alt="flask logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" height="40" alt="sqlite logo" />
  <img width="12" />
  <img src="https://skillicons.dev/icons?i=githubactions" height="40" alt="githubactions logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" height="40" alt="sqlalchemy logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" height="40" alt="postgresql logo" />
</div>

## 📁 Estrutura do Projeto

```text
RB-Psicanálise/
├── .github/workflows/          # Automações de build e CI/CD
├── RB Psicanalise - Sistema de Fichas/
│   ├── 01_Fichas_Interativas_Computador/  # Fichas em HTML interativo
│   ├── 02_Fichas_Prontas_para_Imprimir_PDF/ # Documentos PDF para impressão
│   ├── 03_Prontuarios_Pacientes/          # Organização de prontuários
│   └── 04_Identidade_Visual/              # Logotipos e recursos visuais
└── RB_Psicanalise_Web/
    ├── static/                 # Arquivos estáticos (ícones, imagens, CSS)
    ├── templates/              # Templates HTML do Flask
    ├── app.py                  # Aplicação principal Flask
    ├── config.py               # Configurações do ambiente
    ├── models.py               # Modelos do banco de dados
    ├── desktop_launcher.py     # Inicializador para ambiente desktop
    ├── Iniciar_Local.bat       # Script em lote para inicialização rápida
    ├── Procfile                # Definição de processos para deploy
    └── requirements.txt        # Dependências do projeto
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior instalado em sua máquina.
- Gerenciador de pacotes `pip`.

### Instalação e Execução Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/dev-mizael-nascimento/RB-Psican-lise.git
   cd RB-Psican-lise
   ```

2. Navegue até a pasta da aplicação web e instale as dependências:
   ```bash
   cd RB_Psicanalise_Web
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente baseando-se no arquivo de exemplo `.env.example`.

4. Inicie a aplicação utilizando o script dedicado ou o comando direto do Flask:
   - **No Windows (via arquivo em lote):**
     Execute o arquivo `Iniciar_Local.bat` dentro da pasta `RB_Psicanalise_Web`.
   - **Via terminal:**
     ```bash
     python app.py
     ```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na pasta `RB_Psicanalise_Web/` utilizando o `.env.example` como referência:

| Variável | Descrição | Obrigatória |
| :--- | :--- | :--- |
| `FLASK_ENV` | Ambiente de execução da aplicação (ex: development, production) | Não |
| `SECRET_KEY` | Chave secreta de criptografia para sessões e segurança do Flask | Sim |
| `DATABASE_URL` | URL de conexão com o banco de dados (SQLite/PostgreSQL) | Sim |
| `APP_BASE_URL` | URL base para rotas e links absolutos | Não |
| `ADMIN_DEV_EMAIL` | E-mail do usuário administrador desenvolvedor | Não |
| `ADMIN_DEV_PASSWORD` | Senha do usuário administrador desenvolvedor | Não |
| `PSICANALISTA_EMAIL` | E-mail padrão do perfil de psicanalista | Não |
| `PSICANALISTA_PASSWORD` | Senha padrão do perfil de psicanalista | Não |
| `ATENDENTE_EMAIL` | E-mail do perfil de atendimento/secretaria | Não |
| `ATENDENTE_PASSWORD` | Senha do perfil de atendimento/secretaria | Não |

## 📜 Scripts Disponíveis

| Comando / Script | Descrição |
| :--- | :--- |
| `python RB_Psicanalise_Web/app.py` | Inicia o servidor de desenvolvimento local da aplicação web. |
| `RB_Psicanalise_Web/Iniciar_Local.bat` | Script em lote (Batch) para inicialização facilitada no Windows. |
| `pytest` | Execula a suíte de testes automatizados do sistema. |

## 📄 Licença

Este projeto encontra-se com licença não especificada. Consulte os mantenedores para mais informações sobre permissões de uso e distribuição.
