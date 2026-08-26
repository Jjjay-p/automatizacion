import os
import json
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def buscar_y_analizar_noticias():
    prompt = """
    Analiza la situación actual de los mercados financieros y de negocios en español.
    Genera un informe con una noticia o tendencia clave del mercado.
    
    Responde ÚNICAMENTE con un JSON válido con esta estructura exacta (sin markdown ni texto extra):
    {
        "titulo": "Título descriptivo de la noticia",
        "fuente": "Medio o Sector",
        "resumen": "Resumen ejecutivo en dos oraciones",
        "impacto": "Alcista / Bajista / Neutral",
        "sectores_afectados": ["Sector A", "Sector B"],
        "repercusiones": ["Efecto 1", "Efecto 2"]
    }
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(texto_limpio)

def guardar_informe(data):
    fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nombre_archivo = f"reporte_{fecha_str}.md"
    
    sectores = ", ".join(data.get('sectores_afectados', []))
    repercusiones = "\n".join([f"- {r}" for r in data.get('repercusiones', [])])
    
    contenido_markdown = f"""# 📊 Alerta de Mercado & Análisis IA
**Fecha:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

### 📰 {data.get('titulo', 'Informe de Mercado')}
- **Fuente:** {data.get('fuente', 'N/A')}
- **Impacto:** `{data.get('impacto', 'Neutral')}`
- **Sectores Afectados:** {sectores}

---

### 📝 Resumen Ejecutivo
{data.get('resumen', '')}

---

### ⚡ Posibles Repercusiones
{repercusiones}
"""
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_markdown)
    
    print(f"Informe guardado exitosamente: {nombre_archivo}")

if __name__ == "__main__":
    data = buscar_y_analizar_noticias()
    guardar_informe(data)
