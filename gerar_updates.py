import os
from datetime import datetime

ADDON_DIR = "Addon"
OUTPUT_FILE = "MegaCastleCraftUpdates.html"

def obter_arquivos_addon():
    if not os.path.exists(ADDON_DIR):
        os.makedirs(ADDON_DIR)
        return []

    arquivos = []
    for nome_arquivo in os.listdir(ADDON_DIR):
        if nome_arquivo.endswith(".mcaddon") or nome_arquivo.endswith(".zip") or nome_arquivo.endswith(".mcpack"):
            caminho_completo = os.path.join(ADDON_DIR, nome_arquivo)
            tempo_modificacao = os.path.getmtime(caminho_completo)
            data_str = datetime.fromtimestamp(tempo_modificacao).strftime('%d/%m/%Y')
            arquivos.append({
                "nome": nome_arquivo,
                "caminho": f"{ADDON_DIR}/{nome_arquivo}",
                "mtime": tempo_modificacao,
                "data": data_str
            })

    # Ordena do arquivo mais recente para o mais antigo
    arquivos.sort(key=lambda x: x["mtime"], reverse=True)
    return arquivos

def gerar_html_updates():
    arquivos = obter_arquivos_addon()

    cards_html = ""
    if not arquivos:
        cards_html = """
        <article class="update-card">
          <p style="text-align: center; color: #888;">Nenhum arquivo de addon encontrado na pasta /Addon.</p>
        </article>
        """
    else:
        for idx, item in enumerate(arquivos):
            e_recente = (idx == 0)
            badge = '<span class="badge badge-latest">Mais Recente</span>' if e_recente else '<span class="badge badge-old">Versão Anterior</span>'
            card_class = "update-card latest" if e_recente else "update-card"
            nome_versao = item["nome"].replace(".mcaddon", "").replace("_", " ")

            cards_html += f"""
      <article class="{card_class}">
        <div class="update-header">
          <div class="update-version">
            {nome_versao}
            {badge}
          </div>
          <div class="update-date">
            <svg class="icon" viewBox="0 0 24 24"><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/></svg>
            Atualizado em: {item["data"]}
          </div>
        </div>

        <div class="update-body">
          <div class="update-section-title">
            <svg class="icon" style="color: var(--mc-green);" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
            Detalhes do Pacote
          </div>
          <ul>
            <li>
              <svg class="icon bullet-icon" style="color: var(--mc-green);" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              Arquivo oficial para Minecraft Bedrock Edition.
            </li>
          </ul>
        </div>

        <div class="download-box">
          <a href="{item["caminho"]}" class="download-link" download="{item["nome"]}">
            <svg class="icon" viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
            Baixar {item["nome"]}
          </a>
          <span class="file-info">Download Direto</span>
        </div>
      </article>
"""

    conteudo_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atualizações - Mega Castle Craft (MCC)</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400&family=Press+Start+2P&display=swap" rel="stylesheet">

  <style>
    :root {{
      --mc-green: #388e3c;
      --mc-green-hover: #4caf50;
      --mc-card-bg: rgba(18, 18, 18, 0.90);
      --mc-border: #444444;
      --mc-gold: #ffb703;
      --mc-blue: #2196f3;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      color: #f1f1f1;
      font-family: 'Noto Sans', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 15px;
      position: relative;
      background-color: #0d0d0d;
      overflow-x: hidden;
    }}

    .bg-image {{
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: url('bg.jpg') no-repeat center center / cover;
      filter: blur(10px) brightness(0.4);
      transform: scale(1.05);
      z-index: -1;
    }}

    .back-btn {{
      position: fixed; top: 20px; left: 20px;
      background: rgba(18, 18, 18, 0.85);
      border: 2px solid var(--mc-gold);
      border-radius: 50%; width: 48px; height: 48px;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; color: var(--mc-gold);
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
      transition: all 0.3s ease; z-index: 100;
      text-decoration: none;
    }}

    .back-btn:hover {{
      transform: scale(1.1);
      background: var(--mc-gold);
      color: #0d0d0d;
    }}

    .mc-container {{
      max-width: 850px; width: 100%;
      background: var(--mc-card-bg);
      border: 2px solid var(--mc-border);
      border-radius: 12px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
      padding: 40px 30px;
      backdrop-filter: blur(8px);
      margin-top: 10px;
    }}

    .header {{
      text-align: center;
      margin-bottom: 35px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 25px;
    }}

    .logo {{
      max-width: 300px; width: 100%; height: auto;
      filter: drop-shadow(0 8px 10px rgba(0,0,0,0.8));
      margin: 0 auto; display: block;
    }}

    .page-title {{
      font-family: 'Press Start 2P', monospace;
      font-size: 0.95rem;
      color: var(--mc-gold);
      margin-top: 20px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
      text-transform: uppercase;
    }}

    .icon {{
      width: 18px; height: 18px;
      fill: currentColor; display: inline-block;
      vertical-align: middle;
    }}

    .updates-list {{ display: flex; flex-direction: column; gap: 25px; }}

    .update-card {{
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-left: 5px solid var(--mc-gold);
      border-radius: 8px; padding: 25px;
    }}

    .update-card.latest {{
      border-left-color: var(--mc-green);
      background: rgba(0, 0, 0, 0.6);
      box-shadow: 0 0 20px rgba(56, 142, 60, 0.15);
    }}

    .update-header {{
      display: flex; justify-content: space-between;
      align-items: center; flex-wrap: wrap; gap: 10px;
      margin-bottom: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      padding-bottom: 12px;
    }}

    .update-version {{
      font-family: 'Press Start 2P', monospace;
      font-size: 0.85rem; color: #ffffff;
      display: flex; align-items: center; gap: 10px;
    }}

    .badge {{
      font-family: 'Noto Sans', sans-serif;
      font-size: 0.7rem; font-weight: bold;
      padding: 3px 8px; border-radius: 4px;
      text-transform: uppercase;
    }}

    .badge-latest {{ background: var(--mc-green); color: #fff; }}
    .badge-old {{ background: #444; color: #aaa; }}

    .update-date {{ font-size: 0.8rem; color: #888; display: flex; align-items: center; gap: 6px; }}

    .update-body {{ margin-bottom: 20px; }}

    .update-section-title {{
      font-size: 0.85rem; font-weight: bold;
      color: var(--mc-gold); margin: 12px 0 8px 0;
      display: flex; align-items: center; gap: 8px;
    }}

    .update-body ul {{ list-style: none; padding-left: 5px; }}
    .update-body li {{
      font-size: 0.9rem; color: #ccc; margin-bottom: 6px;
      display: flex; align-items: flex-start; gap: 8px;
    }}

    .bullet-icon {{ margin-top: 3px; flex-shrink: 0; }}

    .download-box {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px dashed rgba(255, 255, 255, 0.15);
      padding: 12px 18px; border-radius: 6px;
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 10px;
    }}

    .download-link {{
      color: var(--mc-green-hover); font-weight: bold;
      text-decoration: none; font-size: 0.88rem;
      display: inline-flex; align-items: center; gap: 8px;
    }}

    .download-link:hover {{ color: #ffffff; text-decoration: underline; }}
    .file-info {{ font-size: 0.75rem; color: #777; }}

    @media (max-width: 600px) {{
      .mc-container {{ padding: 25px 15px; }}
      .download-box {{ flex-direction: column; align-items: flex-start; }}
    }}
  </style>
</head>
<body>

  <div class="bg-image"></div>

  <a href="index.html" class="back-btn" title="Voltar ao início">
    <svg class="icon" style="width:22px; height:22px;" viewBox="0 0 24 24">
      <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
    </svg>
  </a>

  <main class="mc-container">
    <header class="header">
      <img src="logo.png" alt="Logo Mega Castle Craft" class="logo">
      <h1 class="page-title">Histórico de Updates</h1>
    </header>

    <div class="updates-list">
{cards_html}
    </div>
  </main>

</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(conteudo_completo)

if __name__ == "__main__":
    gerar_html_updates()
