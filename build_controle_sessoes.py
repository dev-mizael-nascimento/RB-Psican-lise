# -*- coding: utf-8 -*-
import os

with open('logo_base64.txt', 'r', encoding='utf-8-sig') as f:
    logo_b64 = f.read().strip()

rows_html = ""
for i in range(1, 17):
    num = f"{i:02d}"
    rows_html += f'''
              <tr data-row="{i}">
                <td class="col-num">{num}</td>
                <td><input type="text" class="tbl-input text-center" id="data_{i}" placeholder="DD/MM/AAAA" maxlength="10" oninput="mascaraData(this)"></td>
                <td><input type="text" class="tbl-input text-center" id="hora_{i}" placeholder="HH:MM" maxlength="5" oninput="mascaraHora(this)"></td>
                <td>
                  <select class="tbl-select status-presenca" id="comp_{i}" onchange="atualizarResumo(); estilizarSelect(this)">
                    <option value="">—</option>
                    <option value="Sim">Sim</option>
                    <option value="Não">Não</option>
                  </select>
                </td>
                <td>
                  <select class="tbl-select status-pagamento" id="pag_{i}" onchange="atualizarResumo(); estilizarSelect(this)">
                    <option value="">—</option>
                    <option value="Pago">Pago</option>
                    <option value="Pendente">Pendente</option>
                  </select>
                </td>
                <td><input type="text" class="tbl-input" id="obs_{i}" placeholder="Anotações clínicas ou financeiras da sessão..."></td>
              </tr>'''

html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ficha Individual de Controle de Sessões - RB Psicanálise</title>
  
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
      line-height: 1.35;
      padding-bottom: 70px;
    }}

    /* Barra Superior de Ferramentas */
    .action-bar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #090d16;
      color: #fff;
      padding: 10px 24px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      border-bottom: 1px solid rgba(255,255,255,0.12);
    }}

    .action-bar .brand-info {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .action-bar .brand-title {{
      font-family: 'Cinzel', serif;
      font-size: 1.05rem;
      letter-spacing: 0.12em;
      color: #f8fafc;
      font-weight: 700;
    }}

    .action-bar .brand-badge {{
      background: rgba(158, 120, 52, 0.22);
      border: 1px solid rgba(158, 120, 52, 0.6);
      color: #fde047;
      font-size: 0.7rem;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 600;
    }}

    .action-buttons {{
      display: flex;
      gap: 7px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .patient-selector {{
      background: #1e293b;
      color: #f8fafc;
      border: 1px solid #475569;
      border-radius: 6px;
      padding: 7px 10px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.8rem;
      font-weight: 500;
      outline: none;
      cursor: pointer;
      max-width: 210px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 13px;
      border-radius: 6px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.8rem;
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

    .btn-mini {{
      background: #ffffff;
      color: #334155;
      border: 1px solid #cbd5e1;
      padding: 2px 8px;
      font-size: 0.68rem;
      font-weight: 600;
      border-radius: 4px;
      cursor: pointer;
    }}
    .btn-mini:hover {{
      background: #f8fafc;
      border-color: var(--gold-dark);
      color: var(--gold-dark);
    }}

    /* Contêiner de Documentos */
    .document-wrapper {{
      max-width: 210mm;
      margin: 28px auto;
      display: flex;
      flex-direction: column;
      gap: 36px;
    }}

    /* Folha A4 */
    .a4-page {{
      background: #ffffff;
      width: 210mm;
      min-height: 297mm;
      padding: 13mm 15mm 12mm 15mm;
      margin: 0 auto;
      box-shadow: 0 12px 36px rgba(0,0,0,0.14);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-sizing: border-box;
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
      flex: 1;
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
      max-height: 76px;
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
      padding: 6px 14px;
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
      font-size: 0.77rem;
      font-weight: 600;
      border: none;
      border-bottom: 1px dotted #94a3b8;
      background: transparent;
      color: #0f172a;
      outline: none;
      font-family: inherit;
    }}

    /* Título de Seção */
    .section-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #f1f5f9;
      border-left: 3.5px solid var(--gold-dark);
      padding: 4px 9px;
      margin-bottom: 7px;
    }}

    .section-title-left {{
      display: flex;
      align-items: center;
      gap: 7px;
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

    /* Tabela de Controle de Sessões */
    .sessions-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.75rem;
      border: 1px solid #cbd5e1;
    }}

    .sessions-table thead th {{
      background: #1e293b;
      color: #f8fafc;
      font-family: 'Cinzel', serif;
      font-size: 0.67rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 6px 5px;
      border: 1px solid #334155;
      text-align: center;
    }}

    .sessions-table tbody tr:nth-child(even) {{
      background: #f8fafc;
    }}

    .sessions-table tbody td {{
      border: 1px solid #cbd5e1;
      padding: 3px 5px;
      height: 30px;
      vertical-align: middle;
    }}

    .col-num {{
      text-align: center;
      font-weight: 700;
      font-size: 0.7rem;
      color: #64748b;
      background: #f1f5f9;
      width: 44px;
    }}

    .tbl-input {{
      width: 100%;
      border: none;
      background: transparent;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.76rem;
      color: #0f172a;
      padding: 2px 4px;
      outline: none;
    }}

    .tbl-input:focus {{
      background: #fef9ee;
      border-radius: 2px;
    }}

    .text-center {{
      text-align: center;
    }}

    .tbl-select {{
      width: 100%;
      border: 1px solid transparent;
      background: transparent;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.73rem;
      font-weight: 600;
      color: #0f172a;
      padding: 2px 3px;
      text-align: center;
      text-align-last: center;
      border-radius: 3px;
      cursor: pointer;
      outline: none;
    }}

    .badge-ok {{
      background-color: #ecfdf5 !important;
      color: #065f46 !important;
      border-color: #a7f3d0 !important;
    }}

    .badge-no {{
      background-color: #fef2f2 !important;
      color: #991b1b !important;
      border-color: #fecaca !important;
    }}

    .badge-warn {{
      background-color: #fffbeb !important;
      color: #92400e !important;
      border-color: #fde68a !important;
    }}

    /* Barra de Resumo Automático */
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-top: 10px;
    }}

    .summary-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-top: 2.5px solid var(--gold-dark);
      border-radius: 3px;
      padding: 5px 8px;
      text-align: center;
    }}

    .summary-label {{
      font-size: 0.59rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 700;
      color: #64748b;
    }}

    .summary-value {{
      font-family: 'Cinzel', serif;
      font-size: 0.92rem;
      font-weight: 700;
      color: #0f172a;
      margin-top: 1px;
    }}

    /* Assinatura & Validação */
    .clinical-sign-bar {{
      margin-top: 10px;
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
      font-size: 0.73rem;
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

    /* Rodapé */
    .page-footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
      margin-top: 8px;
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

      .action-bar, .no-print {{
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
        min-height: 297mm !important;
        padding: 12mm 14mm 11mm 14mm !important;
      }}

      .page-frame {{
        border-color: #cbd5e1 !important;
      }}

      .tbl-select {{
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
        background: transparent !important;
        border-color: transparent !important;
      }}

      .tbl-input::placeholder {{
        color: transparent !important;
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
      <span class="brand-badge">Controle Individual</span>
    </div>
    <div class="action-buttons">
      <select id="lista_pacientes_salvos" class="patient-selector" onchange="carregarPacienteSelecionado(this.value)" title="Reabrir ficha de um paciente salvo">
        <option value="">📂 Reabrir Paciente Salvo...</option>
      </select>
      <button class="btn btn-dark" onclick="salvarPaciente()" title="Salvar ficha deste paciente no navegador">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
        Salvar Paciente
      </button>
      <button class="btn btn-outline" onclick="exportarArquivo()" title="Baixar arquivo .json para guardar na pasta do paciente">
        ⬇️ Baixar (.json)
      </button>
      <button class="btn btn-outline" onclick="document.getElementById('input_importar').click()" title="Reabrir um arquivo .json salvo anteriormente">
        ⬆️ Abrir (.json)
      </button>
      <input type="file" id="input_importar" accept=".json" style="display:none;" onchange="importarArquivo(event)">
      <button class="btn btn-gold" onclick="window.print()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Imprimir / PDF
      </button>
      <button class="btn btn-outline" onclick="preencherExemplo()">
        Exemplo
      </button>
      <button class="btn btn-outline" onclick="limparCampos()">
        Limpar
      </button>
    </div>
  </header>

  <!-- Folha Individual A4 -->
  <main class="document-wrapper">
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
              <h1>Ficha de Controle de Sessões</h1>
              <div class="sub-title">Acompanhamento Individual de Frequência, Pagamentos e Observações</div>
            </div>
            <div class="header-meta-bar">
              <div class="meta-item" style="flex:1;">
                <label>Paciente:</label>
                <input type="text" id="paciente_nome" placeholder="Nome completo do(a) paciente" style="width: 100%;">
              </div>
              <div class="meta-item">
                <label>Prontuário Nº:</label>
                <input type="text" id="prontuario_num" placeholder="0001/2026" style="width: 82px; text-align:center;">
              </div>
              <div class="meta-item">
                <label>Período / Ano:</label>
                <input type="text" id="mes_referencia" placeholder="2026" style="width: 88px; text-align:center;">
              </div>
            </div>
          </header>

          <!-- Título da Tabela -->
          <div class="section-title">
            <div class="section-title-left">
              <span class="section-num">01.</span>
              <h2>Registro Cronológico Individual de Sessões</h2>
            </div>
            <button type="button" class="btn-mini no-print" onclick="adicionarLinha()">+ Nova Linha</button>
          </div>

          <!-- Tabela Estruturada Individual -->
          <table class="sessions-table">
            <thead>
              <tr>
                <th style="width: 44px;">Sessão</th>
                <th style="width: 92px;">Data</th>
                <th style="width: 66px;">Horário</th>
                <th style="width: 86px;">Compareceu</th>
                <th style="width: 92px;">Pagamento</th>
                <th>Observação</th>
              </tr>
            </thead>
            <tbody id="tabela_sessoes_body">
              {rows_html}
            </tbody>
          </table>

          <!-- Resumo Automático -->
          <div class="summary-grid">
            <div class="summary-card">
              <div class="summary-label">Sessões Lançadas</div>
              <div class="summary-value" id="sum_total">0</div>
            </div>
            <div class="summary-card">
              <div class="summary-label">Compareceu (Sim)</div>
              <div class="summary-value" id="sum_sim">0</div>
            </div>
            <div class="summary-card">
              <div class="summary-label">Faltas (Não)</div>
              <div class="summary-value" id="sum_nao">0</div>
            </div>
            <div class="summary-card">
              <div class="summary-label">Pagos</div>
              <div class="summary-value" id="sum_pago">0</div>
            </div>
            <div class="summary-card">
              <div class="summary-label">Pendentes</div>
              <div class="summary-value" id="sum_pendente">0</div>
            </div>
          </div>

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
              <div class="sign-sub">RB Psicanálise • Controle Clínico</div>
            </div>
          </section>
        </div>

        <!-- Rodapé -->
        <footer class="page-footer">
          <div class="footer-left">
            <span class="footer-badge"></span>
            <span>RB Psicanálise • Controle Individual de Sessões • Documento Confidencial</span>
          </div>
          <div class="footer-right">
            Página 1 de 1
          </div>
        </footer>

      </div>
    </article>
  </main>

  <!-- Scripts Interativos: Persistência por Paciente + Exportação/Importação JSON -->
  <script>
    const STORAGE_KEY = 'rb_psicanalise_controle_pacientes_v1';
    let totalLinhas = 16;

    function mascaraData(i) {{
      let v = i.value.replace(/\\D/g, "");
      if (v.length > 4) {{
        v = v.replace(/^(\\d{{2}})(\\d{{2}})(\\d{{0,4}}).*/, "$1/$2/$3");
      }} else if (v.length > 2) {{
        v = v.replace(/^(\\d{{2}})(\\d{{0,2}}).*/, "$1/$2");
      }}
      i.value = v;
      atualizarResumo();
    }}

    function mascaraHora(i) {{
      let v = i.value.replace(/\\D/g, "");
      if (v.length > 2) {{
        v = v.replace(/^(\\d{{2}})(\\d{{0,2}}).*/, "$1:$2");
      }}
      i.value = v;
    }}

    function estilizarSelect(sel) {{
      sel.classList.remove('badge-ok', 'badge-no', 'badge-warn');
      if (sel.value === 'Sim' || sel.value === 'Pago') {{
        sel.classList.add('badge-ok');
      }} else if (sel.value === 'Não') {{
        sel.classList.add('badge-no');
      }} else if (sel.value === 'Pendente') {{
        sel.classList.add('badge-warn');
      }}
    }}

    function adicionarLinha(silencioso = false) {{
      totalLinhas++;
      const i = totalLinhas;
      const num = String(i).padStart(2, '0');
      const tbody = document.getElementById('tabela_sessoes_body');
      const tr = document.createElement('tr');
      tr.setAttribute('data-row', i);
      tr.innerHTML = `
        <td class="col-num">${{num}}</td>
        <td><input type="text" class="tbl-input text-center" id="data_${{i}}" placeholder="DD/MM/AAAA" maxlength="10" oninput="mascaraData(this)"></td>
        <td><input type="text" class="tbl-input text-center" id="hora_${{i}}" placeholder="HH:MM" maxlength="5" oninput="mascaraHora(this)"></td>
        <td>
          <select class="tbl-select status-presenca" id="comp_${{i}}" onchange="atualizarResumo(); estilizarSelect(this)">
            <option value="">—</option>
            <option value="Sim">Sim</option>
            <option value="Não">Não</option>
          </select>
        </td>
        <td>
          <select class="tbl-select status-pagamento" id="pag_${{i}}" onchange="atualizarResumo(); estilizarSelect(this)">
            <option value="">—</option>
            <option value="Pago">Pago</option>
            <option value="Pendente">Pendente</option>
          </select>
        </td>
        <td><input type="text" class="tbl-input" id="obs_${{i}}" placeholder="Anotações clínicas ou financeiras da sessão..."></td>
      `;
      tbody.appendChild(tr);
      if (!silencioso) document.getElementById('data_' + i).focus();
    }}

    function ajustarQuantidadeLinhas(qtd) {{
      while (totalLinhas < qtd) {{
        adicionarLinha(true);
      }}
    }}

    function atualizarResumo() {{
      let total = 0, sim = 0, nao = 0, pago = 0, pendente = 0;
      for (let i = 1; i <= totalLinhas; i++) {{
        const dataEl = document.getElementById('data_' + i);
        if (!dataEl) continue;
        const data = dataEl.value.trim();
        const hora = document.getElementById('hora_' + i).value.trim();
        const comp = document.getElementById('comp_' + i).value;
        const pag = document.getElementById('pag_' + i).value;
        const obs = document.getElementById('obs_' + i).value.trim();

        if (data || hora || comp || pag || obs) total++;
        if (comp === 'Sim') sim++;
        if (comp === 'Não') nao++;
        if (pag === 'Pago') pago++;
        if (pag === 'Pendente') pendente++;
      }}
      document.getElementById('sum_total').innerText = total;
      document.getElementById('sum_sim').innerText = sim;
      document.getElementById('sum_nao').innerText = nao;
      document.getElementById('sum_pago').innerText = pago;
      document.getElementById('sum_pendente').innerText = pendente;
    }}

    function coletarDadosAtuais() {{
      const sessoes = [];
      for (let i = 1; i <= totalLinhas; i++) {{
        const data = document.getElementById('data_' + i)?.value || '';
        const hora = document.getElementById('hora_' + i)?.value || '';
        const comp = document.getElementById('comp_' + i)?.value || '';
        const pag = document.getElementById('pag_' + i)?.value || '';
        const obs = document.getElementById('obs_' + i)?.value || '';
        sessoes.push({{ data, hora, comp, pag, obs }});
      }}
      return {{
        paciente_nome: document.getElementById('paciente_nome').value.trim(),
        prontuario_num: document.getElementById('prontuario_num').value.trim(),
        mes_referencia: document.getElementById('mes_referencia').value.trim(),
        local_cidade: document.getElementById('local_cidade').value.trim(),
        data_dia: document.getElementById('data_dia').value.trim(),
        data_mes: document.getElementById('data_mes').value.trim(),
        data_ano: document.getElementById('data_ano').value.trim(),
        sessoes
      }};
    }}

    function aplicarDadosNaFicha(dados) {{
      if (!dados) return;
      document.getElementById('paciente_nome').value = dados.paciente_nome || '';
      document.getElementById('prontuario_num').value = dados.prontuario_num || '';
      document.getElementById('mes_referencia').value = dados.mes_referencia || '';
      if (dados.local_cidade) document.getElementById('local_cidade').value = dados.local_cidade;
      if (dados.data_dia) document.getElementById('data_dia').value = dados.data_dia;
      if (dados.data_mes) document.getElementById('data_mes').value = dados.data_mes;
      if (dados.data_ano) document.getElementById('data_ano').value = dados.data_ano;

      const sessoes = dados.sessoes || [];
      ajustarQuantidadeLinhas(Math.max(16, sessoes.length));

      for (let i = 1; i <= totalLinhas; i++) {{
        const item = sessoes[i - 1] || {{ data: '', hora: '', comp: '', pag: '', obs: '' }};
        document.getElementById('data_' + i).value = item.data || '';
        document.getElementById('hora_' + i).value = item.hora || '';
        const comp = document.getElementById('comp_' + i);
        comp.value = item.comp || '';
        estilizarSelect(comp);
        const pag = document.getElementById('pag_' + i);
        pag.value = item.pag || '';
        estilizarSelect(pag);
        document.getElementById('obs_' + i).value = item.obs || '';
      }}
      atualizarResumo();
    }}

    function obterBancoPacientes() {{
      try {{
        return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
      }} catch (e) {{
        return {{}};
      }}
    }}

    function atualizarSeletorPacientes(selecionado = '') {{
      const banco = obterBancoPacientes();
      const select = document.getElementById('lista_pacientes_salvos');
      select.innerHTML = '<option value="">📂 Reabrir Paciente Salvo...</option>';
      Object.keys(banco).sort().forEach(nome => {{
        const opt = document.createElement('option');
        opt.value = nome;
        opt.textContent = nome;
        if (nome === selecionado) opt.selected = true;
        select.appendChild(opt);
      }});
    }}

    function salvarPaciente() {{
      const dados = coletarDadosAtuais();
      if (!dados.paciente_nome) {{
        alert('Preencha o nome do(a) paciente no cabeçalho antes de salvar.');
        document.getElementById('paciente_nome').focus();
        return;
      }}
      const banco = obterBancoPacientes();
      banco[dados.paciente_nome] = dados;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(banco));
      atualizarSeletorPacientes(dados.paciente_nome);
      alert('Ficha de "' + dados.paciente_nome + '" salva! Você poderá reabri-la a qualquer momento no menu superior.');
    }}

    function carregarPacienteSelecionado(nome) {{
      if (!nome) return;
      const banco = obterBancoPacientes();
      if (banco[nome]) {{
        aplicarDadosNaFicha(banco[nome]);
      }}
    }}

    function exportarArquivo() {{
      const dados = coletarDadosAtuais();
      const nomeBase = (dados.paciente_nome || 'paciente')
        .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
        .replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_+|_+$/g, '');
      const blob = new Blob([JSON.stringify(dados, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'controle_sessoes_' + nomeBase + '.json';
      a.click();
      URL.revokeObjectURL(url);
    }}

    function importarArquivo(event) {{
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {{
        try {{
          const dados = JSON.parse(e.target.result);
          aplicarDadosNaFicha(dados);
          if (dados.paciente_nome) {{
            const banco = obterBancoPacientes();
            banco[dados.paciente_nome] = dados;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(banco));
            atualizarSeletorPacientes(dados.paciente_nome);
          }}
        }} catch (err) {{
          alert('Não foi possível ler o arquivo selecionado. Verifique se é um arquivo .json válido desta ficha.');
        }}
      }};
      reader.readAsText(file);
      event.target.value = '';
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      const hoje = new Date();
      document.getElementById('data_dia').value = String(hoje.getDate()).padStart(2, '0');
      const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
      document.getElementById('data_mes').value = meses[hoje.getMonth()];
      document.getElementById('data_ano').value = String(hoje.getFullYear()).slice(-2);
      atualizarSeletorPacientes();
    }});

    function preencherExemplo() {{
      aplicarDadosNaFicha({{
        paciente_nome: 'Mariana Vasconcelos Ribeiro',
        prontuario_num: '0142/2026',
        mes_referencia: 'Nov / 2026',
        sessoes: [
          {{ data: '05/11/2026', hora: '14:00', comp: 'Sim', pag: 'Pago', obs: 'Sessão inicial de enquadre analítico' }},
          {{ data: '12/11/2026', hora: '14:00', comp: 'Sim', pag: 'Pago', obs: 'Associação livre sobre rotina laboral e cobranças' }},
          {{ data: '19/11/2026', hora: '14:00', comp: 'Não', pag: 'Pago', obs: 'Falta sem aviso prévio (regra das 24h aplicada)' }},
          {{ data: '26/11/2026', hora: '14:00', comp: 'Sim', pag: 'Pendente', obs: 'Acerto previsto para o dia 30/11' }}
        ]
      }});
      alert('Exemplo individual preenchido! Você pode clicar em "Salvar Paciente" ou "⬇️ Baixar (.json)" para testar a reabertura.');
    }}

    function limparCampos() {{
      if (confirm('Deseja limpar os campos da tela para iniciar um novo paciente? (Os pacientes já salvos continuam guardados no menu superior)')) {{
        aplicarDadosNaFicha({{ paciente_nome: '', prontuario_num: '', mes_referencia: '', sessoes: [] }});
        document.getElementById('lista_pacientes_salvos').value = '';
      }}
    }}
  </script>
</body>
</html>
'''

with open('ficha_controle_sessoes.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo ficha_controle_sessoes.html individual atualizado com sucesso!')
