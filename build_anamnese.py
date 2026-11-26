# -*- coding: utf-8 -*-
import os

with open('logo_base64.txt', 'r', encoding='utf-8-sig') as f:
    logo_b64 = f.read().strip()

html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ficha de Anamnese Clínica - RB Psicanálise</title>
  
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
      margin-bottom: 11px;
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
      max-height: 78px;
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
      justify-content: space-between;
      align-items: center;
      gap: 14px;
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
      white-space: nowrap;
    }}

    .meta-item input {{
      font-size: 0.75rem;
      font-weight: 600;
      border: none;
      border-bottom: 1px dotted #94a3b8;
      background: transparent;
      color: #0f172a;
      outline: none;
      font-family: inherit;
    }}

    /* Cabeçalho Compacto (Página 2) */
    .header-compact {{
      border-bottom: 1.5px solid var(--slate-800);
      padding-bottom: 7px;
      margin-bottom: 10px;
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
      width: 220px;
      outline: none;
      font-family: inherit;
    }}

    /* Seções Clínicas */
    .section-block {{
      margin-bottom: 9px;
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
    .col-6  {{ grid-column: span 6; }}

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
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }}

    .form-hint {{
      font-size: 0.61rem;
      font-weight: 500;
      text-transform: none;
      color: #64748b;
      font-style: italic;
      letter-spacing: 0;
    }}

    .form-input {{
      padding: 5px 8px;
      font-size: 0.78rem;
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
      line-height: 1.42;
    }}

    /* Assinatura Clínica Compacta */
    .clinical-sign-bar {{
      margin-top: 8px;
      padding-top: 8px;
      border-top: 1px dashed #cbd5e1;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 20px;
    }}

    .local-date-wrap {{
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 0.73rem;
      color: #334155;
      white-space: nowrap;
    }}

    .local-date-wrap input {{
      border: none;
      border-bottom: 1px solid #64748b;
      font-size: 0.74rem;
      font-weight: 600;
      color: #0f172a;
      padding: 1px 4px;
      text-align: center;
      outline: none;
      font-family: inherit;
    }}

    .analyst-sign {{
      width: 245px;
      text-align: center;
    }}

    .sign-line {{
      width: 100%;
      border-top: 1.2px solid #334155;
      margin-bottom: 3px;
    }}

    .sign-title {{
      font-size: 0.71rem;
      font-weight: 700;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .sign-sub {{
      font-size: 0.62rem;
      color: #64748b;
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

    /* AJUSTES PARA IMPRESSÃO / PDF (A4) */
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

      .form-input {{
        border-color: #94a3b8 !important;
        background: transparent !important;
        box-shadow: none !important;
      }}

      @page {{
        size: A4 portrait;
        margin: 0;
      }}
    }}
  </style>
</head>
<body>

  <!-- Barra de Ferramentas Superior -->
  <header class="action-bar">
    <div class="brand-info">
      <span class="brand-title">RB PSICANÁLISE</span>
      <span class="brand-badge">Ficha de Anamnese Clínica</span>
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

  <!-- Documento Principal (2 Páginas A4) -->
  <main class="document-wrapper">

    <!-- ========================================================== -->
    <!-- PÁGINA 1: DEMANDA, HISTÓRIA FAMILIAR, INFÂNCIA E ESCOLA    -->
    <!-- ========================================================== -->
    <article class="a4-page">
      <div class="page-frame"></div>
      <div class="page-content">

        <div>
          <!-- Cabeçalho Principal com Logo Centralizado -->
          <header class="header-main">
            <div class="header-logo-wrap">
              <img src="data:image/png;base64,{logo_b64}" alt="Logotipo RB Psicanálise" onerror="this.src='Logotipo minimalista de Psicanálise.png'">
            </div>
            <div class="header-center">
              <h1>Ficha de Anamnese Clínica</h1>
              <div class="sub-title">Investigação Analítica, História Subjetiva e Contexto Biográfico</div>
            </div>
            <div class="header-meta-bar">
              <div class="meta-item">
                <label>Prontuário Nº:</label>
                <input type="text" id="prontuario" placeholder="0001/2026" style="width: 82px; text-align:center;">
              </div>
              <div class="meta-item" style="flex:1;">
                <label>Analisando(a):</label>
                <input type="text" id="nome_paciente" placeholder="Nome completo do paciente" style="width: 100%;" oninput="sincronizarNome(this.value)">
              </div>
              <div class="meta-item">
                <label>Data:</label>
                <input type="text" id="data_anamnese" placeholder="DD/MM/AAAA" maxlength="10" style="width: 85px; text-align:center;" oninput="mascaraData(this)">
              </div>
            </div>
          </header>

          <!-- SEÇÃO 01: MOTIVO DA PROCURA & HISTÓRIA DA QUEIXA -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">01.</span>
              <h2>Demanda Inicial & Construção da Queixa</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="motivo_procura">
                  <span>Motivo da Procura</span>
                  <span class="form-hint">O que mobilizou a busca pelo atendimento neste momento?</span>
                </label>
                <textarea class="form-input" id="motivo_procura" rows="3" placeholder="Relato espontâneo sobre o que trouxe o(a) analisando(a) à clínica agora..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="historia_queixa">
                  <span>História da Queixa</span>
                  <span class="form-hint">Início, evolução dos sintomas, gatilhos percebidos e momentos de alívio ou agravo</span>
                </label>
                <textarea class="form-input" id="historia_queixa" rows="4" placeholder="Contextualização temporal, episódios anteriores semelhantes e impactos atuais na rotina..."></textarea>
              </div>
            </div>
          </section>

          <!-- SEÇÃO 02: HISTÓRIA FAMILIAR & DESENVOLVIMENTO INFANTIL -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">02.</span>
              <h2>Constelação Familiar & Primeiros Tempos</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="historia_familiar">
                  <span>História Familiar</span>
                  <span class="form-hint">Composição familiar, vínculos com pais/irmãos, clima afetivo, perdas ou conflitos</span>
                </label>
                <textarea class="form-input" id="historia_familiar" rows="4" placeholder="Estrutura familiar de origem e atual, figuras de referência, história psíquica na família..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="desenvolvimento_infantil">
                  <span>Desenvolvimento Infantil</span>
                  <span class="form-hint">Gestação, primeiros anos, marcos motores/fala, memórias da infância e traumas precoces</span>
                </label>
                <textarea class="form-input" id="desenvolvimento_infantil" rows="4" placeholder="Relatos sobre a infância, sono infantil, medos, brincadeiras, adaptações e separações..."></textarea>
              </div>
            </div>
          </section>

          <!-- SEÇÃO 03: ESCOLARIDADE -->
          <section class="section-block" style="margin-bottom:0;">
            <div class="section-title">
              <span class="section-num">03.</span>
              <h2>Escolaridade & Percurso Formativo</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="escolaridade_historico">
                  <span>Escolaridade</span>
                  <span class="form-hint">Trajetória escolar e acadêmica, socialização, dificuldades de aprendizagem ou mudanças</span>
                </label>
                <textarea class="form-input" id="escolaridade_historico" rows="3" placeholder="Relação com estudos, professores e colegas ao longo do ensino básico e superior..."></textarea>
              </div>
            </div>
          </section>
        </div>

        <!-- Rodapé Folha 1 -->
        <footer class="page-footer">
          <div class="footer-left">
            <span class="footer-badge"></span>
            <span>RB Psicanálise • Ficha de Anamnese Clínica • Sigilo e Confidencialidade Absoluta</span>
          </div>
          <div class="footer-right">
            Página 1 de 2
          </div>
        </footer>

      </div>
    </article>


    <!-- ========================================================== -->
    <!-- PÁGINA 2: VIDA PESSOAL, SAÚDE, HÁBITOS E OBSERVAÇÕES       -->
    <!-- ========================================================== -->
    <article class="a4-page">
      <div class="page-frame"></div>
      <div class="page-content">

        <div>
          <!-- Cabeçalho Compacto Página 2 -->
          <header class="header-compact">
            <div class="logo-mini">
              <img src="data:image/png;base64,{logo_b64}" alt="Logotipo RB Psicanálise" onerror="this.src='Logotipo minimalista de Psicanálise.png'">
              <span class="compact-title">RB Psicanálise • Anamnese Clínica</span>
            </div>
            <div class="patient-badge">
              <span>Analisando(a):</span>
              <input type="text" id="header_page2_paciente" placeholder="Nome do paciente" readonly>
            </div>
          </header>

          <!-- SEÇÃO 04: VIDA PESSOAL & RELACIONAMENTO AFETIVO -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">04.</span>
              <h2>Vida Pessoal, Social & Relacionamentos Afetivos</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="vida_pessoal">
                  <span>Vida Pessoal</span>
                  <span class="form-hint">Cotidiano, trabalho/carreira, amizades, lazer, espiritualidade e autonomia</span>
                </label>
                <textarea class="form-input" id="vida_pessoal" rows="3" placeholder="Organização da rotina atual, satisfações, pressões laborais e rede de apoio social..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="relacionamento_afetivo">
                  <span>Relacionamento Afetivo</span>
                  <span class="form-hint">Histórico amoroso, vínculo atual, padrões de escolha objetal, sexualidade e filhos</span>
                </label>
                <textarea class="form-input" id="relacionamento_afetivo" rows="3" placeholder="Qualidade dos vínculos afetivos, conflitos recorrentes, conjugalidade e vivência da sexualidade..."></textarea>
              </div>
            </div>
          </section>

          <!-- SEÇÃO 05: SAÚDE FÍSICA, MEDICAÇÕES & HÁBITOS -->
          <section class="section-block">
            <div class="section-title">
              <span class="section-num">05.</span>
              <h2>Saúde Física, Uso de Medicamentos & Hábitos de Vida</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="saude_fisica">
                  <span>Saúde Física</span>
                  <span class="form-hint">Diagnósticos clínicos, cirurgias, internações, dores crônicas e manifestações psicossomáticas</span>
                </label>
                <textarea class="form-input" id="saude_fisica" rows="3" placeholder="Estado geral de saúde, queixas corporais frequentes e acompanhamentos médicos..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="uso_medicamentos">
                  <span>Uso de Medicamentos</span>
                  <span class="form-hint">Medicações contínuas ou psiquiátricas, dosagens, tempo de uso e prescritor</span>
                </label>
                <textarea class="form-input" id="uso_medicamentos" rows="2" placeholder="Fármacos em uso atual ou recente, eventuais efeitos colaterais e adesão ao tratamento..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="habitos_vida">
                  <span>Hábitos de Vida</span>
                  <span class="form-hint">Qualidade do sono, alimentação, exercícios físicos, uso de álcool, tabaco ou outras substâncias</span>
                </label>
                <textarea class="form-input" id="habitos_vida" rows="3" placeholder="Padrões de sono/sonhos, rotina alimentar, práticas físicas e eventuais compulsões ou vícios..."></textarea>
              </div>
            </div>
          </section>

          <!-- SEÇÃO 06: EXPECTATIVAS & OBSERVAÇÕES INICIAIS -->
          <section class="section-block" style="margin-bottom:4px;">
            <div class="section-title">
              <span class="section-num">06.</span>
              <h2>Expectativas & Observações Iniciais do(a) Psicanalista</h2>
            </div>
            <div class="form-grid grid-cols-12">
              <div class="form-group col-12">
                <label class="form-label" for="expectativas">
                  <span>Expectativas</span>
                  <span class="form-hint">O que o(a) analisando(a) espera alcançar com o processo psicanalítico?</span>
                </label>
                <textarea class="form-input" id="expectativas" rows="2" placeholder="Objetivos conscientes, fantasias sobre a análise e disposição para o trabalho analítico..."></textarea>
              </div>
              <div class="form-group col-12">
                <label class="form-label" for="observacoes_iniciais">
                  <span>Observações Iniciais</span>
                  <span class="form-hint">Impressões clínicas, postura, discurso, transferência inicial e pontos de atenção</span>
                </label>
                <textarea class="form-input" id="observacoes_iniciais" rows="4" placeholder="Anotações reservadas ao(à) analista sobre a escuta inicial, afetos predominantes e encaminhamentos..."></textarea>
              </div>
            </div>
          </section>

          <!-- Validação / Local e Data -->
          <section class="clinical-sign-bar">
            <div class="local-date-wrap">
              <span>Local e Data:</span>
              <input type="text" id="local_cidade" value="São Paulo / SP" style="width: 105px;">,
              <input type="text" id="data_dia" placeholder="dia" style="width: 24px;"> de
              <input type="text" id="data_mes" placeholder="mês" style="width: 75px;"> de 20<input type="text" id="data_ano" placeholder="26" style="width: 22px;">.
            </div>
            <div class="analyst-sign">
              <div class="sign-line"></div>
              <div class="sign-title">Psicanalista Responsável</div>
              <div class="sign-sub">RB Psicanálise • Registro Clínico</div>
            </div>
          </section>
        </div>

        <!-- Rodapé Folha 2 -->
        <footer class="page-footer">
          <div class="footer-left">
            <span class="footer-badge"></span>
            <span>RB Psicanálise • Ficha de Anamnese Clínica • Documento Estritamente Confidencial</span>
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
      document.getElementById('header_page2_paciente').value = val.trim();
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

    window.addEventListener('DOMContentLoaded', () => {{
      const hoje = new Date();
      document.getElementById('data_dia').value = String(hoje.getDate()).padStart(2, '0');
      const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
      document.getElementById('data_mes').value = meses[hoje.getMonth()];
      document.getElementById('data_ano').value = String(hoje.getFullYear()).slice(-2);

      const formatHoje = String(hoje.getDate()).padStart(2, '0') + '/' + String(hoje.getMonth() + 1).padStart(2, '0') + '/' + hoje.getFullYear();
      if (!document.getElementById('data_anamnese').value) {{
        document.getElementById('data_anamnese').value = formatHoje;
      }}

      const salvo = localStorage.getItem('rascunho_rb_anamnese');
      if (salvo) {{
        try {{
          const dados = JSON.parse(salvo);
          Object.keys(dados).forEach(id => {{
            const el = document.getElementById(id);
            if (el && dados[id] !== undefined) el.value = dados[id];
          }});
          sincronizarNome(document.getElementById('nome_paciente').value || '');
        }} catch (e) {{}}
      }}
    }});

    function preencherExemplo() {{
      document.getElementById('prontuario').value = '0142/2026';
      document.getElementById('nome_paciente').value = 'Mariana Vasconcelos Ribeiro';
      sincronizarNome('Mariana Vasconcelos Ribeiro');

      document.getElementById('motivo_procura').value = 'Sensação persistente de esgotamento emocional, episódios de ansiedade diante de demandas profissionais e dificuldade em dizer não nas relações familiares.';
      document.getElementById('historia_queixa').value = 'Os sintomas intensificaram-se há cerca de 8 meses após promoção no trabalho e falecimento da avó materna. Relata angústia matinal frequente e sensação de nunca corresponder às próprias exigências.';
      document.getElementById('historia_familiar').value = 'Filha mais velha de dois irmãos. Pai exigente e pouco expressivo afetivamente; mãe acolhedora, porém ansiosa. Mantém vínculo próximo com a família de origem, embora sinta peso excessivo no papel de cuidadora.';
      document.getElementById('desenvolvimento_infantil').value = 'Desenvolvimento motor e de linguagem dentro do esperado. Relata infância marcada por grande responsabilidade precoce e medo noturno até os 9 anos após separação temporária dos pais.';
      document.getElementById('escolaridade_historico').value = 'Excelente desempenho acadêmico durante toda a vida escolar; perfeccionismo acentuado em provas e apresentações. Graduou-se em Administração com pós-graduação em Gestão de Pessoas.';
      document.getElementById('vida_pessoal').value = 'Rotina intensa de 10h diárias de trabalho. Pouco tempo reservado para lazer espontâneo; mantém pequeno círculo de amigas de longa data.';
      document.getElementById('relacionamento_afetivo').value = 'Casada há 6 anos, sem filhos. Relacionamento estável e companheiro, com redução recente da libido associada ao cansaço e à tensão constante.';
      document.getElementById('saude_fisica').value = 'Hipertensão arterial leve controlada e episódios esporádicos de gastrite nervosa e tensão cervical em semanas de maior estresse.';
      document.getElementById('uso_medicamentos').value = 'Escitalopram 15mg/dia pela manhã (prescrição psiquiátrica há 6 meses) e Losartana 50mg/dia.';
      document.getElementById('habitos_vida').value = 'Sono fragmentado (desperta por volta das 3h com pensamentos acelerados). Alimentação regular; caminhadas 2x por semana. Consumo social moderado de vinho aos finais de semana.';
      document.getElementById('expectativas').value = 'Compreender a origem de sua autocrítica severa, elaborar o luto recente e construir limites mais saudáveis sem culpa.';
      document.getElementById('observacoes_iniciais').value = 'Discurso organizado, fluido e com boa capacidade associativa. Demonstra forte racionalização como defesa frente ao afeto de tristeza. Boa abertura inicial para o enquadre analítico.';

      alert('Exemplo completo de anamnese preenchido! Clique em "Imprimir / Gerar PDF (A4)" para visualizar.');
    }}

    function salvarRascunho() {{
      const inputs = document.querySelectorAll('input, textarea');
      const dados = {{}};
      inputs.forEach(el => {{
        if (el.id) dados[el.id] = el.value;
      }});
      localStorage.setItem('rascunho_rb_anamnese', JSON.stringify(dados));
      alert('Rascunho da anamnese salvo no navegador com sucesso!');
    }}

    function limparCampos() {{
      if (confirm('Deseja realmente limpar todos os campos da ficha de anamnese?')) {{
        document.querySelectorAll('input, textarea').forEach(el => {{
          if (el.id !== 'local_cidade' && el.id !== 'data_dia' && el.id !== 'data_mes' && el.id !== 'data_ano') {{
            el.value = '';
          }}
        }});
        localStorage.removeItem('rascunho_rb_anamnese');
        sincronizarNome('');
      }}
    }}
  </script>
</body>
</html>
'''

with open('ficha_anamnese.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo ficha_anamnese.html gerado com sucesso!')
