# -*- coding: utf-8 -*-
import os

with open('logo_base64.txt', 'r', encoding='utf-8-sig') as f:
    logo_b64 = f.read().strip()

html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ficha de Protocolo & Cadastro Clínico - RB Psicanálise</title>
  
  <!-- Tipografia de Alto Padrão -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <style>
    :root {{
      --primary: #0f172a;
      --primary-light: #1e293b;
      --gold-dark: #846122;
      --gold-main: #9e7834;
      --gold-light: #fef9ee;
      --slate-50: #f8fafc;
      --slate-100: #f1f5f9;
      --slate-200: #e2e8f0;
      --slate-300: #cbd5e1;
      --slate-400: #94a3b8;
      --slate-500: #64748b;
      --slate-600: #475569;
      --slate-700: #334155;
      --slate-800: #1e293b;
      --text-main: #0f172a;
      --border-color: #cbd5e1;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      background-color: #e2e8f0;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: var(--text-main);
      line-height: 1.38;
      padding-bottom: 70px;
    }}

    /* Barra Superior de Ferramentas */
    .action-bar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #090d16;
      color: #fff;
      padding: 12px 28px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      border-bottom: 1px solid rgba(255,255,255,0.12);
    }}

    .action-bar .brand-info {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .action-bar .brand-title {{
      font-family: 'Cinzel', serif;
      font-size: 1.1rem;
      letter-spacing: 0.12em;
      color: #f8fafc;
      font-weight: 700;
    }}

    .action-bar .brand-badge {{
      background: rgba(158, 120, 52, 0.22);
      border: 1px solid rgba(158, 120, 52, 0.6);
      color: #fde047;
      font-size: 0.72rem;
      padding: 3px 9px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 600;
    }}

    .action-buttons {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 8px 16px;
      border-radius: 6px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
      text-decoration: none;
    }}

    .btn-gold {{
      background: linear-gradient(135deg, #b0893f, #846122);
      color: #ffffff;
      box-shadow: 0 2px 10px rgba(132, 97, 34, 0.35);
    }}
    .btn-gold:hover {{
      background: linear-gradient(135deg, #be9547, #966f28);
      transform: translateY(-1px);
    }}

    .btn-dark {{
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #334155;
    }}
    .btn-dark:hover {{
      background: #334155;
      color: #fff;
    }}

    .btn-outline {{
      background: transparent;
      color: #cbd5e1;
      border: 1px solid #475569;
    }}
    .btn-outline:hover {{
      background: rgba(255,255,255,0.08);
      color: #fff;
    }}

    /* Contêiner de Documentos */
    .document-wrapper {{
      max-width: 210mm;
      margin: 28px auto;
      display: flex;
      flex-direction: column;
      gap: 36px;
    }}

    /* Folha A4 Rigorosa */
    .a4-page {{
      background: #ffffff;
      width: 210mm;
      height: 297mm;
      min-height: 297mm;
      max-height: 297mm;
      padding: 13mm 15mm 12mm 15mm;
      margin: 0 auto;
      box-shadow: 0 12px 36px rgba(0,0,0,0.14);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-sizing: border-box;
      overflow: hidden;
    }}

    /* Moldura Perimetral */
    .page-frame {{
      position: absolute;
      top: 6mm;
      left: 7mm;
      right: 7mm;
      bottom: 6mm;
      border: 1px solid #cbd5e1;
      pointer-events: none;
      z-index: 1;
    }}

    .page-frame::after {{
      content: '';
      position: absolute;
      top: 2.5px;
      left: 2.5px;
      right: 2.5px;
      bottom: 2.5px;
      border: 0.5px solid #f1f5f9;
      pointer-events: none;
    }}

    .page-content {{
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      height: 100%;
      justify-content: space-between;
    }}

    /* Cabeçalho Principal (Proeminente & Centralizado) */
    .header-main {{
      border-bottom: 2px solid var(--slate-800);
      padding-bottom: 10px;
      margin-bottom: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 5px;
    }}

    .header-logo-wrap {{
      display: flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      margin-bottom: 2px;
    }}

    .header-logo-wrap img {{
      max-width: 270px;
      max-height: 80px;
      height: auto;
      object-fit: contain;
      filter: contrast(1.15);
    }}

    .header-center {{
      text-align: center;
      width: 100%;
    }}

    .header-center h1 {{
      font-family: 'Cinzel', serif;
      font-size: 1.15rem;
      letter-spacing: 0.09em;
      color: #0f172a;
      font-weight: 700;
      line-height: 1.2;
      text-transform: uppercase;
    }}

    .header-center .sub-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-style: italic;
      font-size: 0.81rem;
      color: #64748b;
      margin-top: 2px;
      letter-spacing: 0.03em;
    }}

    .header-meta-bar {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 24px;
      width: 100%;
      background: #f8fafc;
      padding: 5px 14px;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      margin-top: 4px;
    }}

    .meta-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
    }}

    .meta-item label {{
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.65rem;
      color: #475569;
      letter-spacing: 0.04em;
    }}

    .meta-item input, .meta-item select {{
      font-size: 0.75rem;
      font-weight: 600;
      border: none;
      border-bottom: 1px dotted #94a3b8;
      background: transparent;
      color: #0f172a;
      outline: none;
      font-family: inherit;
      text-align: center;
    }}

    /* Cabeçalho Compacto (Página 2) */
    .header-compact {{
      border-bottom: 1.5px solid var(--slate-800);
      padding-bottom: 8px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .header-compact .logo-mini {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .header-compact img {{
      max-height: 38px;
      max-width: 150px;
      object-fit: contain;
    }}

    .header-compact .compact-title {{
      font-family: 'Cinzel', serif;
      font-size: 0.88rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      color: #0f172a;
      text-transform: uppercase;
    }}

    .header-compact .patient-badge {{
      font-size: 0.74rem;
      color: #475569;
      display: flex;
      gap: 6px;
      align-items: center;
    }}

    .header-compact .patient-badge input {{
      border: none;
      border-bottom: 1px dotted #64748b;
      font-size: 0.78rem;
      font-weight: 600;
      color: #0f172a;
      width: 230px;
      outline: none;
      font-family: inherit;
    }}

    /* Seções Clínicas */
    .section-block {{
      margin-bottom: 10px;
    }}

    .section-title {{
      display: flex;
      align-items: center;
      gap: 7px;
      background: #f1f5f9;
      border-left: 3.5px solid var(--gold-dark);
      padding: 3.5px 8px;
      margin-bottom: 5px;
    }}

    .section-title .section-num {{
      font-family: 'Cinzel', serif;
      font-weight: 700;
      font-size: 0.74rem;
      color: var(--gold-dark);
    }}

    .section-title h2 {{
      font-family: 'Cinzel', serif;
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #1e293b;
    }}

    /* Grids e Campos */
    .form-grid {{
      display: grid;
      gap: 5px 8px;
    }}

    .grid-cols-12 {{ grid-template-columns: repeat(12, 1fr); }}
    .col-12 {{ grid-column: span 12; }}
    .col-10 {{ grid-column: span 10; }}
    .col-9  {{ grid-column: span 9; }}
    .col-8  {{ grid-column: span 8; }}
    .col-7  {{ grid-column: span 7; }}
    .col-6  {{ grid-column: span 6; }}
    .col-5  {{ grid-column: span 5; }}
    .col-4  {{ grid-column: span 4; }}
    .col-3  {{ grid-column: span 3; }}
    .col-2  {{ grid-column: span 2; }}

    .form-group {{
      display: flex;
      flex-direction: column;
    }}

    .form-label {{
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 700;
      color: #475569;
      margin-bottom: 2px;
    }}

    .form-input {{
      height: 27px;
      padding: 3px 8px;
      font-size: 0.8rem;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #0f172a;
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 3px;
      transition: all 0.15s ease;
      outline: none;
      width: 100%;
    }}

    .form-input:focus {{
      border-color: var(--gold-dark);
      background: #fafaf9;
      box-shadow: 0 0 0 2px rgba(132, 97, 34, 0.12);
    }}

    textarea.form-input {{
      height: auto;
      resize: none;
      line-height: 1.4;
      padding: 6px 8px;
    }}

    /* Grupos de Opções Sim/Não */
    .options-group {{
      display: flex;
      align-items: center;
      gap: 14px;
      height: 27px;
      padding: 2px 8px;
      border: 1px solid var(--border-color);
      border-radius: 3px;
      background: #f8fafc;
    }}

    .option-item {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 0.75rem;
      color: #1e293b;
      cursor: pointer;
      user-select: none;
    }}

    .option-item input[type="radio"],
    .option-item input[type="checkbox"] {{
      accent-color: var(--gold-dark);
      cursor: pointer;
      width: 13px;
      height: 13px;
    }}

    /* Caixa Clínica & Pautas de Linhas */
    .clinical-note-box {{
      border: 1px solid var(--border-color);
      border-radius: 3px;
      background: #ffffff;
      padding: 7px 9px;
    }}

    /* Termo de Consentimento Detalhado */
    .consent-box {{
      border: 1px solid #cbd5e1;
      background: #fafaf9;
      border-radius: 4px;
      padding: 9px 13px;
      margin-top: 4px;
      font-size: 0.725rem;
      line-height: 1.48;
      color: #334155;
      text-align: justify;
    }}

    .consent-box h3 {{
      font-family: 'Cinzel', serif;
      font-size: 0.8rem;
      color: #0f172a;
      margin-bottom: 5px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      text-align: center;
    }}

    .consent-clauses {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .clause-item {{
      display: flex;
      gap: 6px;
    }}

    .clause-item span {{
      color: var(--gold-dark);
      font-weight: 700;
    }}

    .clause-item strong {{
      color: #0f172a;
    }}

    .consent-declaration {{
      margin-top: 7px;
      padding: 6px 9px;
      background: #ffffff;
      border: 1px solid var(--gold-dark);
      border-left: 3.5px solid var(--gold-dark);
      border-radius: 3px;
      font-weight: 600;
      color: #0f172a;
    }}

    /* Formalização e Assinaturas */
    .signatures-block {{
      margin-top: 14px;
    }}

    .local-date-wrap {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 6px;
      font-size: 0.77rem;
      margin-bottom: 24px;
      color: #334155;
    }}

    .local-date-wrap input {{
      border: none;
      border-bottom: 1px solid #64748b;
      font-size: 0.77rem;
      font-weight: 600;
      color: #0f172a;
      padding: 1px 4px;
      text-align: center;
      outline: none;
      font-family: inherit;
    }}

    .sign-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 36px;
    }}

    .sign-col {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}

    .sign-line {{
      width: 100%;
      border-top: 1.2px solid #334155;
      margin-bottom: 4px;
    }}

    .sign-title {{
      font-size: 0.74rem;
      font-weight: 700;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .sign-sub {{
      font-size: 0.66rem;
      color: #64748b;
      margin-top: 1px;
    }}

    .sign-meta {{
      font-size: 0.63rem;
      color: #475569;
      margin-top: 3px;
      font-weight: 500;
    }}

    /* Rodapés */
    .page-footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.64rem;
      color: #94a3b8;
      letter-spacing: 0.03em;
    }}

    .page-footer .footer-left {{
      display: flex;
      align-items: center;
      gap: 7px;
    }}

    .page-footer .footer-badge {{
      display: inline-block;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--gold-dark);
    }}

    .page-footer .footer-right {{
      font-weight: 600;
      color: #64748b;
    }}

    /* AJUSTES ESPECÍFICOS PARA IMPRESSÃO DE ALTA RESOLUÇÃO */
    @media print {{
      body {{
        background: #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
      }}

      .action-bar {{
        display: none !important;
      }}

      .document-wrapper {{
        max-width: 100% !important;
        margin: 0 !important;
        gap: 0 !important;
      }}

      .a4-page {{
        box-shadow: none !important;
        margin: 0 !important;
        width: 100% !important;
        height: 297mm !important;
        min-height: 297mm !important;
        max-height: 297mm !important;
        page-break-after: always !important;
        break-after: page !important;
        padding: 12mm 14mm 11mm 14mm !important;
      }}

      .page-frame {{
        border-color: #cbd5e1 !important;
      }}

      /* Remove ícones nativos de calendário e setas de dropdown na impressão */
      input[type="date"]::-webkit-calendar-picker-indicator {{
        display: none !important;
        -webkit-appearance: none !important;
      }}

      select {{
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
        background-image: none !important;
      }}

      .form-input {{
        border-color: #94a3b8 !important;
        background: transparent !important;
        box-shadow: none !important;
      }}

      .options-group {{
        border-color: #94a3b8 !important;
        background: transparent !important;
      }}

      .consent-box {{
        background: #ffffff !important;
        border-color: #94a3b8 !important;
      }}

      @page {{
        size: A4 portrait;
        margin: 0;
      }}
    }}
  </style>
</head>
<body>

  <!-- Barra de Ferramentas Superior (Oculta na Impressão/PDF) -->
  <header class="action-bar">
    <div class="brand-info">
      <span class="brand-title">RB PSICANÁLISE</span>
      <span class="brand-badge">Protocolo Clínico Profissional</span>
    </div>
    <div class="action-buttons">
      <button class="btn btn-gold" onclick="window.print()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Imprimir / Gerar PDF (A4)
      </button>
      <button class="btn btn-dark" onclick="preencherExemplo()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        Exemplo Preenchido
      </button>
      <button class="btn btn-outline" onclick="salvarRascunho()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
        Salvar Rascunho
      </button>
      <button class="btn btn-outline" onclick="limparCampos()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        Limpar
      </button>
    </div>
  </header>

  <!-- Documento Principal -->
  <main class="document-wrapper">

    <!-- ========================================== -->
    <!-- PÁGINA 1: CADASTRO, CONTATOS E HISTÓRICO   -->
    <!-- ========================================== -->
    <article class="a4-page">
      <div class="page-frame"></div>
      <div class="page-content">

        <div>
          <!-- Cabeçalho Principal com Logo em Destaque Central -->
          <header class="header-main">
            <div class="header-logo-wrap">
              <img src="data:image/png;base64,{logo_b64}" alt="Logotipo RB Psicanálise" onerror="this.src='Logotipo minimalista de Psicanálise.png'">
            </div>
            <div class="header-center">
              <h1>Ficha de Protocolo & Cadastro</h1>
              <div class="sub-title">Admissão e Registro de Atendimento Clínico Psicanalítico</div>
            </div>
            <div class="header-meta-bar">
              <div class="meta-item">
                <label>Prontuário Nº:</label>
                <input type="text" id="prontuario" placeholder="0001/2026" style="width: 85px;">
              </div>
              <div class="meta-item">
                <label>Data Início:</label>
                <input type="text" id="data_inicio_topo" placeholder="DD / MM / AAAA" style="width: 95px;">
              </div>
              <div class="meta-item">
                <label>Modalidade:</label>
                <select id="modalidade_top" style="width: 85px;">
                  <option value="Presencial">Presencial</option>
                  <option value="Online">Online</option>
                </select>
              </div>
            </div>
          </header>

          <!-- SEÇÃO 01: DADOS DE IDENTIFICAÇÃO -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">01.</span>
              <h2>Dados de Identificação do(a) Analisando(a)</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-8">
                <label class="form-label" for="nome_completo">Nome Completo</label>
                <input type="text" class="form-input" id="nome_completo" placeholder="Nome completo do paciente/analisando" oninput="sincronizarNome(this.value)">
              </div>
              <div class="form-group col-2">
                <label class="form-label" for="data_nascimento">Data de Nasc.</label>
                <input type="text" class="form-input" id="data_nascimento" placeholder="DD/MM/AAAA" maxlength="10" oninput="mascaraData(this)" onblur="calcularIdadePorTexto(this.value)">
              </div>
              <div class="form-group col-2">
                <label class="form-label" for="idade">Idade</label>
                <input type="text" class="form-input" id="idade" placeholder="Ex: 34 anos">
              </div>

              <div class="form-group col-3">
                <label class="form-label" for="estado_civil">Estado Civil</label>
                <select class="form-input" id="estado_civil">
                  <option value="">Selecione...</option>
                  <option value="Solteiro(a)">Solteiro(a)</option>
                  <option value="Casado(a)">Casado(a)</option>
                  <option value="União Estável">União Estável</option>
                  <option value="Divorciado(a)">Divorciado(a)</option>
                  <option value="Viúvo(a)">Viúvo(a)</option>
                  <option value="Outro">Outro</option>
                </select>
              </div>
              <div class="form-group col-5">
                <label class="form-label" for="profissao">Profissão / Ocupação Atual</label>
                <input type="text" class="form-input" id="profissao" placeholder="Ex: Arquiteto(a) / Autônomo(a)">
              </div>
              <div class="form-group col-4">
                <label class="form-label" for="escolaridade">Grau de Escolaridade</label>
                <select class="form-input" id="escolaridade">
                  <option value="">Selecione...</option>
                  <option value="Ensino Fundamental">Ensino Fundamental</option>
                  <option value="Ensino Médio">Ensino Médio</option>
                  <option value="Superior Incompleto">Superior Incompleto</option>
                  <option value="Superior Completo">Superior Completo</option>
                  <option value="Pós-Graduação / Especialização">Pós-Graduação / Especialização</option>
                  <option value="Mestrado / Doutorado">Mestrado / Doutorado</option>
                </select>
              </div>

              <div class="form-group col-6">
                <label class="form-label" for="cpf">CPF</label>
                <input type="text" class="form-input" id="cpf" placeholder="000.000.000-00" maxlength="14" oninput="mascaraCPF(this)">
              </div>
              <div class="form-group col-6">
                <label class="form-label" for="rg">RG / Órgão Emissor</label>
                <input type="text" class="form-input" id="rg" placeholder="Ex: 00.000.000-0 SSP/UF">
              </div>
            </div>
          </section>

          <!-- SEÇÃO 02: ENDEREÇO & CONTATOS -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">02.</span>
              <h2>Endereço Residencial & Meios de Contato</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-7">
                <label class="form-label" for="endereco">Endereço (Rua, Número, Complemento, Bairro)</label>
                <input type="text" class="form-input" id="endereco" placeholder="Logradouro, nº, apto/bloco e bairro">
              </div>
              <div class="form-group col-3">
                <label class="form-label" for="cidade">Cidade / UF</label>
                <input type="text" class="form-input" id="cidade" placeholder="Ex: São Paulo / SP">
              </div>
              <div class="form-group col-2">
                <label class="form-label" for="cep">CEP</label>
                <input type="text" class="form-input" id="cep" placeholder="00000-000" maxlength="9" oninput="mascaraCEP(this)">
              </div>

              <div class="form-group col-4">
                <label class="form-label" for="telefone">Telefone / WhatsApp Principal</label>
                <input type="tel" class="form-input" id="telefone" placeholder="(00) 00000-0000" maxlength="15" oninput="mascaraTelefone(this)">
              </div>
              <div class="form-group col-8">
                <label class="form-label" for="email">E-mail para Contato</label>
                <input type="email" class="form-input" id="email" placeholder="exemplo@email.com">
              </div>
            </div>
          </section>

          <!-- SEÇÃO 03: CONTATO EMERGENCIAL -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">03.</span>
              <h2>Contato Emergencial (Em caso de necessidade clínica)</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-5">
                <label class="form-label" for="contato_emergencial">Nome do Contato Emergencial</label>
                <input type="text" class="form-input" id="contato_emergencial" placeholder="Nome da pessoa responsável ou de apoio">
              </div>
              <div class="form-group col-3">
                <label class="form-label" for="grau_parentesco">Grau de Parentesco / Vínculo</label>
                <input type="text" class="form-input" id="grau_parentesco" placeholder="Ex: Cônjuge, Mãe, Amigo(a)">
              </div>
              <div class="form-group col-4">
                <label class="form-label" for="telefone_emergencia">Telefone de Contato Emergencial</label>
                <input type="tel" class="form-input" id="telefone_emergencia" placeholder="(00) 00000-0000" maxlength="15" oninput="mascaraTelefone(this)">
              </div>
            </div>
          </section>

          <!-- SEÇÃO 04: HISTÓRICO CLÍNICO & TERAPÊUTICO -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">04.</span>
              <h2>Histórico Clínico, Terapêutico & Acompanhamento</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-6">
                <label class="form-label" for="como_conheceu">Como conheceu o atendimento / Indicação?</label>
                <input type="text" class="form-input" id="como_conheceu" placeholder="Ex: Indicação médica, conhecido, internet">
              </div>
              <div class="form-group col-6">
                <label class="form-label">Data de Início das Sessões</label>
                <input type="text" class="form-input" id="data_inicio_sessao" placeholder="DD / MM / AAAA" maxlength="10" oninput="mascaraData(this)">
              </div>

              <!-- Psicanálise Anterior -->
              <div class="form-group col-4">
                <label class="form-label">Já realizou psicanálise ou terapia?</label>
                <div class="options-group">
                  <label class="option-item"><input type="radio" name="ja_fez_terapia" value="nao" checked> Não</label>
                  <label class="option-item"><input type="radio" name="ja_fez_terapia" value="sim"> Sim</label>
                </div>
              </div>
              <div class="form-group col-8">
                <label class="form-label" for="detalhe_terapia">Se sim: Há quanto tempo? Abordagem / Experiência anterior?</label>
                <input type="text" class="form-input" id="detalhe_terapia" placeholder="Ex: Fiz análise por 2 anos com linha freudiana">
              </div>

              <!-- Medicações -->
              <div class="form-group col-4">
                <label class="form-label">Faz uso de medicação contínua?</label>
                <div class="options-group">
                  <label class="option-item"><input type="radio" name="faz_uso_medicacao" value="nao" checked> Não</label>
                  <label class="option-item"><input type="radio" name="faz_uso_medicacao" value="sim"> Sim</label>
                </div>
              </div>
              <div class="form-group col-8">
                <label class="form-label" for="qual_medicacao">Se sim: Qual(is) medicamento(s), dosagem e tempo de uso?</label>
                <input type="text" class="form-input" id="qual_medicacao" placeholder="Ex: Antidepressivo / Ansiolítico (nome e dosagem)">
              </div>

              <!-- Acompanhamento Médico -->
              <div class="form-group col-4">
                <label class="form-label">Possui acompanhamento médico?</label>
                <div class="options-group">
                  <label class="option-item"><input type="radio" name="acompanhamento_medico" value="nao" checked> Não</label>
                  <label class="option-item"><input type="radio" name="acompanhamento_medico" value="sim"> Sim</label>
                </div>
              </div>
              <div class="form-group col-8">
                <label class="form-label" for="detalhe_medico">Se sim: Especialidade, médico(a) responsável e frequência?</label>
                <input type="text" class="form-input" id="detalhe_medico" placeholder="Ex: Psiquiatra / Clínico Geral - Consultas periódicas">
              </div>
            </div>
          </section>

          <!-- SEÇÃO 05: QUEIXA PRINCIPAL / SÍNTESE ANALÍTICA -->
          <section class="section-block" style="margin-bottom:0;">
            <div class="section-title">
              <span class="section-num">05.</span>
              <h2>Queixa Principal / Motivo da Busca pelo Atendimento (Síntese)</h2>
            </div>
            <div class="clinical-note-box">
              <textarea class="form-input" id="queixa_principal" rows="3" placeholder="Breve relato da demanda espontânea e sentimentos relatados pelo(a) analisando(a) no primeiro contato com a clínica..."></textarea>
            </div>
          </section>
        </div>

        <!-- Rodapé Folha 1 -->
        <footer class="page-footer">
          <div class="footer-left">
            <span class="footer-badge"></span>
            <span>RB Psicanálise • Prontuário Clínico & Admissão • Sigilo e Confidencialidade Absoluta</span>
          </div>
          <div class="footer-right">
            Página 1 de 2
          </div>
        </footer>

      </div>
    </article>


    <!-- ========================================== -->
    <!-- PÁGINA 2: SAÚDE, ENQUADRE E TERMO          -->
    <!-- ========================================== -->
    <article class="a4-page">
      <div class="page-frame"></div>
      <div class="page-content">

        <div>
          <!-- Cabeçalho Compacto Página 2 -->
          <header class="header-compact">
            <div class="logo-mini">
              <img src="data:image/png;base64,{logo_b64}" alt="Logotipo RB Psicanálise" onerror="this.src='Logotipo minimalista de Psicanálise.png'">
              <span class="compact-title">RB Psicanálise • Setting & Termo</span>
            </div>
            <div class="patient-badge">
              <span>Analisando(a):</span>
              <input type="text" id="header_page2_paciente" placeholder="Nome do paciente" readonly>
            </div>
          </header>

          <!-- SEÇÃO 06: CONDIÇÕES DE SAÚDE RELEVANTES -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">06.</span>
              <h2>Condições de Saúde Relevantes & Informações Complementares</h2>
            </div>
            <div class="clinical-note-box">
              <div style="font-size:0.71rem; color:#475569; margin-bottom:5px; font-weight:500;">
                Assinale ou descreva condições físicas, históricas ou psíquicas importantes (doenças crônicas, cirurgias recentes, distúrbios do sono, histórico de crises, restrições ou alergias):
              </div>
              <textarea class="form-input" id="condicoes_saude" rows="4" placeholder="Descreva com detalhes quaisquer condições de saúde relevantes para o contexto analítico e suporte clínico..."></textarea>
            </div>
          </section>

          <!-- SEÇÃO 07: ENQUADRE ANALÍTICO (SETTING) -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">07.</span>
              <h2>Enquadre do Atendimento (Setting Psicanalítico)</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-3">
                <label class="form-label">Frequência Semanal</label>
                <select class="form-input" id="frequencia">
                  <option value="1x por semana">1x por semana</option>
                  <option value="2x por semana">2x por semana</option>
                  <option value="A combinar">A combinar</option>
                </select>
              </div>
              <div class="form-group col-3">
                <label class="form-label">Duração da Sessão</label>
                <input type="text" class="form-input" id="duracao" value="50 minutos">
              </div>
              <div class="form-group col-3">
                <label class="form-label">Honorários Acordados</label>
                <input type="text" class="form-input" id="honorarios" placeholder="R$ por sessão">
              </div>
              <div class="form-group col-3">
                <label class="form-label">Formato</label>
                <select class="form-input" id="formato_atendimento">
                  <option value="Presencial">Presencial</option>
                  <option value="Online">Online</option>
                  <option value="Híbrido">Híbrido</option>
                </select>
              </div>
            </div>
          </section>

          <!-- SEÇÃO 08: TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">08.</span>
              <h2>Termo de Consentimento Livre, Esclarecido e Sigilo Profissional</h2>
            </div>

            <div class="consent-box">
              <h3>Acordo Terapêutico e Responsabilidade Mútua</h3>
              
              <div class="consent-clauses">
                <div class="clause-item">
                  <span>•</span>
                  <div><strong>1. Da Natureza do Atendimento:</strong> O trabalho psicanalítico fundamenta-se na livre associação de ideias, escuta clínica qualificada e investigação dos processos inconscientes, visando à elaboração de sofrimentos psíquicos e ampliação do autoconhecimento. Trata-se de processo singular, sem promessas de resultados imediatos ou curas pré-fixadas.</div>
                </div>

                <div class="clause-item">
                  <span>•</span>
                  <div><strong>2. Do Rigoroso Sigilo Profissional:</strong> Todas as informações, relatos, conteúdos e registros clínicos compartilhados durante as sessões estão resguardados por absoluto sigilo ético e profissional, sendo vedada sua divulgação a terceiros sem prévia autorização expressa do(a) analisando(a), ressalvadas as hipóteses legais e de risco iminente à integridade física do paciente ou de outrem.</div>
                </div>

                <div class="clause-item">
                  <span>•</span>
                  <div><strong>3. Das Regras de Enquadre, Pontualidade e Faltas:</strong> O horário das sessões é reservado com exclusividade ao(à) analisando(a). Eventuais cancelamentos ou remarcações devem ser comunicados com antecedência mínima de 24 (vinte e quatro) horas, resguardando-se as regras previamente pactuadas sobre manutenção ou reposição da sessão.</div>
                </div>

                <div class="clause-item">
                  <span>•</span>
                  <div><strong>4. Da Possibilidade de Interrupção ou Encerramento:</strong> O processo analítico é pautado pela autonomia de ambas as partes. O(a) analisando(a) tem o pleno direito de interromper ou encerrar o tratamento a qualquer momento, recomendando-se a realização de sessão prévia de encerramento para elaboração e fechamento clínico do ciclo.</div>
                </div>
              </div>

              <div class="consent-declaration">
                "Declaro para os devidos fins que fui devidamente informado(a), compreendo com clareza a natureza do atendimento psicanalítico, a abrangência do sigilo profissional, as regras de enquadre e a possibilidade mútua de interrupção. Concordo integralmente com os termos e condições aqui estabelecidos."
              </div>
            </div>
          </section>

          <!-- SEÇÃO 09: ASSINATURAS E FORMALIZAÇÃO -->
          <section class="signatures-block">
            <div class="local-date-wrap">
              <span>Local e Data:</span>
              <input type="text" id="local_cidade" value="São Paulo / SP" style="width: 140px;">,
              <input type="text" id="data_dia" placeholder="dia" style="width: 32px;"> de 
              <input type="text" id="data_mes" placeholder="mês" style="width: 95px;"> de 20<input type="text" id="data_ano" placeholder="26" style="width: 28px;">.
            </div>

            <div class="sign-row">
              <div class="sign-col">
                <div class="sign-line"></div>
                <div class="sign-title" id="sign_paciente_nome">Assinatura do(a) Analisando(a)</div>
                <div class="sign-sub">Paciente ou Responsável Legal</div>
                <div class="sign-meta" id="sign_cpf_paciente">CPF: ___________________________</div>
              </div>
              <div class="sign-col">
                <div class="sign-line"></div>
                <div class="sign-title">Assinatura do(a) Psicanalista</div>
                <div class="sign-sub">RB Psicanálise • Prática Clínica</div>
                <div class="sign-meta">Registro / CBO ou Sociedade Psicanalítica</div>
              </div>
            </div>
          </section>
        </div>

        <!-- Rodapé Folha 2 -->
        <footer class="page-footer">
          <div class="footer-left">
            <span class="footer-badge"></span>
            <span>RB Psicanálise • Termo de Consentimento e Enquadre Analítico • Documento Confidencial</span>
          </div>
          <div class="footer-right">
            Página 2 de 2
          </div>
        </footer>

      </div>
    </article>

  </main>

  <!-- Scripts Interativos -->
  <script>
    function sincronizarNome(val) {{
      const nomeLimpo = val.trim();
      document.getElementById('header_page2_paciente').value = nomeLimpo || '';
      document.getElementById('sign_paciente_nome').innerText = nomeLimpo ? nomeLimpo.toUpperCase() : 'ASSINATURA DO(A) ANALISANDO(A)';
    }}

    function mascaraData(i) {{
      let v = i.value.replace(/\\D/g, "");
      if (v.length > 4) {{
        v = v.replace(/^(\\d{{2}})(\\d{{2}})(\\d{{0,4}}).*/, "$1/$2/$3");
      }} else if (v.length > 2) {{
        v = v.replace(/^(\\d{{2}})(\\d{{0,2}}).*/, "$1/$2");
      }}
      i.value = v;
    }}

    function calcularIdadePorTexto(dataStr) {{
      if (!dataStr || dataStr.length < 10) return;
      const partes = dataStr.split('/');
      if (partes.length === 3) {{
        const dia = parseInt(partes[0], 10);
        const mes = parseInt(partes[1], 10) - 1;
        const ano = parseInt(partes[2], 10);
        const nasc = new Date(ano, mes, dia);
        const hoje = new Date();
        let idade = hoje.getFullYear() - nasc.getFullYear();
        const m = hoje.getMonth() - nasc.getMonth();
        if (m < 0 || (m === 0 && hoje.getDate() < nasc.getDate())) {{
          idade--;
        }}
        if (idade >= 0 && idade < 125) {{
          document.getElementById('idade').value = idade + ' anos';
        }}
      }}
    }}

    function mascaraCPF(i) {{
      let v = i.value.replace(/\\D/g, "");
      v = v.replace(/(\\d{{3}})(\\d)/, "$1.$2");
      v = v.replace(/(\\d{{3}})(\\d)/, "$1.$2");
      v = v.replace(/(\\d{{3}})(\\d{{1,2}})$/, "$1-$2");
      i.value = v;
      if (v) {{
        document.getElementById('sign_cpf_paciente').innerText = 'CPF: ' + v;
      }} else {{
        document.getElementById('sign_cpf_paciente').innerText = 'CPF: ___________________________';
      }}
    }}

    function mascaraCEP(i) {{
      let v = i.value.replace(/\\D/g, "");
      v = v.replace(/^(\\d{{5}})(\\d)/, "$1-$2");
      i.value = v;
    }}

    function mascaraTelefone(i) {{
      let v = i.value.replace(/\\D/g, "");
      if (v.length > 10) {{
        v = v.replace(/^(\\d\\d)(\\d{{5}})(\\d{{4}}).*/, "($1) $2-$3");
      }} else if (v.length > 5) {{
        v = v.replace(/^(\\d\\d)(\\d{{4}})(\\d{{0,4}}).*/, "($1) $2-$3");
      }} else if (v.length > 2) {{
        v = v.replace(/^(\\d\\d)(\\d{{0,5}}).*/, "($1) $2");
      }}
      i.value = v;
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      const hoje = new Date();
      document.getElementById('data_dia').value = String(hoje.getDate()).padStart(2, '0');
      const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
      document.getElementById('data_mes').value = meses[hoje.getMonth()];
      document.getElementById('data_ano').value = String(hoje.getFullYear()).slice(-2);
      
      const formatHoje = String(hoje.getDate()).padStart(2, '0') + '/' + String(hoje.getMonth() + 1).padStart(2, '0') + '/' + hoje.getFullYear();
      if (!document.getElementById('data_inicio_topo').value) {{
        document.getElementById('data_inicio_topo').value = formatHoje;
      }}
      if (!document.getElementById('data_inicio_sessao').value) {{
        document.getElementById('data_inicio_sessao').value = formatHoje;
      }}
    }});

    function preencherExemplo() {{
      document.getElementById('prontuario').value = '0142/2026';
      document.getElementById('nome_completo').value = 'Mariana Vasconcelos Ribeiro';
      sincronizarNome('Mariana Vasconcelos Ribeiro');
      document.getElementById('data_nascimento').value = '14/08/1989';
      document.getElementById('idade').value = '37 anos';
      document.getElementById('estado_civil').value = 'Casado(a)';
      document.getElementById('profissao').value = 'Diretora de Recursos Humanos';
      document.getElementById('escolaridade').value = 'Pós-Graduação / Especialização';
      document.getElementById('cpf').value = '234.567.890-12';
      document.getElementById('sign_cpf_paciente').innerText = 'CPF: 234.567.890-12';
      document.getElementById('rg').value = '38.912.450-X SSP/SP';
      document.getElementById('endereco').value = 'Alameda dos Jacarandás, 840, Apto 112 - Jardins';
      document.getElementById('cidade').value = 'São Paulo / SP';
      document.getElementById('cep').value = '01423-001';
      document.getElementById('telefone').value = '(11) 98765-4321';
      document.getElementById('email').value = 'mariana.vasconcelos@exemplo.com.br';
      
      document.getElementById('contato_emergencial').value = 'Carlos Eduardo Ribeiro';
      document.getElementById('grau_parentesco').value = 'Cônjuge';
      document.getElementById('telefone_emergencia').value = '(11) 99123-8877';

      document.getElementById('como_conheceu').value = 'Indicação da Dra. Beatriz (Psiquiatra)';
      
      const radioTerapia = document.querySelectorAll('input[name="ja_fez_terapia"]');
      radioTerapia[1].checked = true;
      document.getElementById('detalhe_terapia').value = 'Psicoterapia comportamental em 2022 durante 1 ano';

      const radioMed = document.querySelectorAll('input[name="faz_uso_medicacao"]');
      radioMed[1].checked = true;
      document.getElementById('qual_medicacao').value = 'Escitalopram 15mg (manhã) para controle de ansiedade';

      const radioAcomp = document.querySelectorAll('input[name="acompanhamento_medico"]');
      radioAcomp[1].checked = true;
      document.getElementById('detalhe_medico').value = 'Dra. Beatriz Helena (Psiquiatra - CRM 142.890) consultas periódicas';

      document.getElementById('queixa_principal').value = 'Sensação de sobrecarga crônica, crises de ansiedade em momentos de tomada de decisão executiva e busca por maior autoconhecimento e elaboração de lutos recentes.';
      document.getElementById('condicoes_saude').value = 'Hipertensão arterial leve compensada sob acompanhamento médico; sem histórico de cirurgias recentes ou internações. Relato de insônia inicial em períodos de alta demanda.';
      document.getElementById('honorarios').value = 'R$ 280,00';

      alert('Exemplo completo preenchido com sucesso! Clique em \"Imprimir / Gerar PDF\" para conferir a diagramação.');
    }}

    function salvarRascunho() {{
      const inputs = document.querySelectorAll('input, select, textarea');
      const dados = {{}};
      inputs.forEach(el => {{
        if (el.id) {{
          dados[el.id] = el.type === 'radio' ? el.checked : el.value;
        }}
      }});
      localStorage.setItem('rascunho_rb_psicanalise', JSON.stringify(dados));
      alert('Rascunho salvo no navegador com sucesso!');
    }}

    function limparCampos() {{
      if (confirm('Deseja realmente limpar todos os campos da ficha?')) {{
        const inputs = document.querySelectorAll('input:not([type="radio"]), textarea');
        inputs.forEach(el => el.value = '');
        const selects = document.querySelectorAll('select');
        selects.forEach(el => el.selectedIndex = 0);
        sincronizarNome('');
        document.getElementById('sign_cpf_paciente').innerText = 'CPF: ___________________________';
      }}
    }}
  </script>
</body>
</html>
'''

with open('ficha_protocolo_atendimento.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo final ficha_protocolo_atendimento.html atualizado!')
