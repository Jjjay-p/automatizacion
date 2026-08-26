import os
import json
from datetime import datetime
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def buscar_y_analizar_noticias():
    prompt = """
    Busca las noticias financieras, de negocios y mercado más importantes y recientes en español.
    Selecciona la noticia más relevante del momento y genera un análisis de mercado estructurado.
    
    Responde ÚNICAMENTE con un JSON válido usando este formato exacto:
    {
        "titulo": "Título descriptivo de la noticia",
        "fuente": "Nombre del medio o URL",
        "resumen": "Resumen ejecutivo en 2 o 3 oraciones",
        "impacto": "Alcista / Bajista / Neutral",
        "sectores_afectados": ["Sector A", "Sector B"],
        "repercusiones": ["Efecto a corto/largo plazo 1", "Efecto a corto/largo plazo 2"]
    }
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}],
            response_mime_type="application/json",
            temperature=0.2
        ),
    )
    
    return json.loads(response.text)

def guardar_informe(data):
    fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nombre_archivo = f"reporte_{fecha_str}.md"
    
    sectores = ", ".join(data['sectores_afectados'])
    repercusiones = "\n".join([f"- {r}" for r in data['repercusiones']])
    
    contenido_markdown = f"""# 📊 Alerta de Mercado & Análisis IA
**Fecha:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

### 📰 {data['titulo']}
- **Fuente:** {data['fuente']}
- **Sentimiento / Impacto:** `{data['impacto']}`
- **Sectores Afectados:** {sectores}

---

### 📝 Resumen Ejecutivo
{data['resumen']}

---

### ⚡ Posibles Repercusiones de Mercado
{repercusiones}
"""
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_markdown)
        
    print(f"Informe guardado con éxito en {nombre_archivo}")

if __name__ == "__main__":
    try:
        data = buscar_y_analizar_noticias()
        guardar_informe(data)
    except Exception as e:
        print(f"Error procesando la noticia: {e}")
