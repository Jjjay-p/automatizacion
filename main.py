import os
import json
import time
from datetime import datetime
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def obtener_5_noticias():
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    Fecha y hora actual: {ahora}.
    Busca y selecciona las 5 noticias de negocios, economía, tecnología y mercados más importantes e impactantes del momento en español.
    Asegúrate de traer novedades frescas y variadas.
    
    Responde ÚNICAMENTE con un JSON válido con esta estructura exacta (sin markdown ni texto extra):
    {{
        "noticias": [
            {{
                "titulo": "Título descriptivo de la noticia",
                "fuente": "Medio o Fuente",
                "resumen": "Resumen ejecutivo en dos oraciones detalladas.",
                "impacto": "Alcista / Bajista / Neutral",
                "sectores": ["Sector A", "Sector B"]
            }}
        ]
    }}
    """

    modelos = ['gemini-2.5-flash', 'gemini-1.5-flash']
    config = types.GenerateContentConfig(temperature=0.7)
    
    for modelo in modelos:
        try:
            print(f"Buscando noticias frescas con {modelo}...")
            chat = client.chats.create(model=modelo, config=config)
            response = chat.send_message(prompt)
            texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(texto_limpio)
        except Exception as e:
            print(f"Error con {modelo}: {e}. Reintentando...")
            time.sleep(2)
            
    raise Exception("Todos los modelos fallaron. Reintenta en unos minutos.")

def generar_html(data):
    noticias = data.get("noticias", [])
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    cards_html = ""
    for i, item in enumerate(noticias, 1):
        sectores = ", ".join(item.get("sectores", []))
        impacto = item.get('impacto', 'Neutral')
        color_badge = "#0284c7"
        if "Alcista" in impacto:
            color_badge = "#16a34a"
        elif "Bajista" in impacto:
            color_badge = "#dc2626"

        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="badge" style="background-color: {color_badge};">{impacto}</span>
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
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 10px; color: #38bdf8; }}
        .timestamp {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }}
        
        /* Botón de recarga */
        .btn-update {{
            background: #0284c7; color: white; border: none; padding: 12px 24px;
            font-size: 1rem; font-weight: bold; border-radius: 8px; cursor: pointer;
            transition: background 0.2s, transform 0.1s; display: inline-flex; align-items: center; gap: 8px;
        }}
        .btn-update:hover {{ background: #0369a1; transform: translateY(-1px); }}
        .btn-update:disabled {{ background: #475569; cursor: not-allowed; }}
        
        .card {{ background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 20px; border: 1px solid #334155; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .badge {{ color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }}
        .source {{ color: #94a3b8; font-size: 0.85rem; }}
        h2 {{ font-size: 1.25rem; margin: 0 0 12px 0; color: #f1f5f9; }}
        .summary {{ color: #cbd5e1; line-height: 1.6; margin-bottom: 16px; }}
        .card-footer {{ font-size: 0.85rem; color: #64748b; border-top: 1px solid #334155; padding-top: 12px; }}
        #status-msg {{ margin-top: 15px; font-size: 0.9rem; color: #38bdf8; display: none; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 What's Happening Today?</h1>
            <p class="timestamp">Última actualización: {fecha_actual} (hs)</p>
            <button class="btn-update" id="reloadBtn" onclick="dispararActualizacion()">
                🔄 Actualizar Noticias Ahora
            </button>
            <div id="status-msg">🚀 Generando noticias frescas... La página se recargará en 45 segundos.</div>
        </header>
        <main>
            {cards_html}
        </main>
    </div>

    <script>
        async function dispararActualizacion() {{
            const btn = document.getElementById('reloadBtn');
            const status = document.getElementById('status-msg');
            
            // Solicitamos el token en un prompt simple para no exponer claves en el repo
            const token = prompt("Ingresá tu Personal Access Token de GitHub para autorizar la actualización:");
            if (!token) return;

            btn.disabled = true;
            status.style.display = "block";

            try {{
                const response = await fetch('https://api.github.com/repos/Jjay-p/automatizacion/actions/workflows/automatizacion.yml/dispatches', {{
                    method: 'POST',
                    headers: {{
                        'Accept': 'application/vnd.github+json',
                        'Authorization': `Bearer ${{token}}`,
                    }},
                    body: JSON.stringify({{ ref: 'main' }})
                }});

                if (response.ok) {{
                    alert("¡Disparo exitoso! Esperá unos 45 segundos a que corra el script y recargá la página.");
                    setTimeout(() => {{ window.location.reload(); }}, 45000);
                }} else {{
                    alert("Error autorizando la ejecución. Verificá tu token.");
                    btn.disabled = false;
                    status.style.display = "none";
                }}
            }} catch (err) {{
                alert("Error de conexión: " + err);
                btn.disabled = false;
                status.style.display = "none";
            }}
        }}
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    data = obtener_5_noticias()
    generar_html(data)
