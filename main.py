import os
import json
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def obtener_5_noticias():
    prompt = """
    Busca las 5 noticias de negocios, economía y mercados más importantes del día en español.
    
    Responde ÚNICAMENTE con un JSON válido con esta estructura exactas (sin markdown ni texto extra):
    {
        "noticias": [
            {
                "titulo": "Título de la noticia",
                "fuente": "Medio o Fuente",
                "resumen": "Resumen ejecutivo en dos oraciones.",
                "impacto": "Alcista / Bajista / Neutral",
                "sectores": ["Sector A", "Sector B"]
            }
        ]
    }
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(texto_limpio)

def generar_html(data):
    noticias = data.get("noticias", [])
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    cards_html = ""
    for i, item in enumerate(noticias, 1):
        sectores = ", ".join(item.get("sectores", []))
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="badge">{item.get('impacto', 'Neutral')}</span>
                <span class="source">{item.get('fuente', 'N/A')}</span>
            </div>
            <h2>{i}. {item.get('titulo')}</h2>
            <p class="summary">{item.get('resumen')}</p>
            <div class="card-footer">
                <strong>Sectores:</strong> {sectores}
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>What's Happening Today?</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 40px; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 10px; color: #38bdf8; }}
        .timestamp {{ color: #94a3b8; font-size: 0.9rem; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 20px; border: 1px solid #334155; }}
        .card-header {{ display: flex; justify-space-between; align-items: center; margin-bottom: 12px; }}
        .badge {{ background: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }}
        .source {{ color: #94a3b8; font-size: 0.85rem; }}
        h2 {{ font-size: 1.25rem; margin: 0 0 12px 0; color: #f1f5f9; }}
        .summary {{ color: #cbd5e1; line-height: 1.6; margin-bottom: 16px; }}
        .card-footer {{ font-size: 0.85rem; color: #64748b; border-top: 1px solid #334155; padding-top: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 What's Happening Today?</h1>
            <p class="timestamp">Última actualización: {fecha_actual} (Argentina)</p>
        </header>
        <main>
            {cards_html}
        </main>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    data = obtener_5_noticias()
    generar_html(data)
