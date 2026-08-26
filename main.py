import os
import json
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def buscar_y_analizar_noticias():
    prompt = """
    Busca noticias financieras y de mercado relevantes recientes en español.
    Genera un análisis rápido del impacto de mercado.
    
    Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
    {
        "titulo": "Título de la noticia",
        "fuente": "Fuente o medio",
        "resumen": "Resumen de 2 oraciones",
        "impacto": "Alcista / Bajista / Neutral",
        "sectores_afectados": ["Sector 1", "Sector 2"],
        "repercusiones": ["Punto 1", "Punto 2"]
    }
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    # Limpiamos delimitadores si la IA envía bloques de código markdown
    texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(texto_limpio)

def guardar_informe(data):
    fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nombre_archivo = f"reporte_{fecha_str}.md"
    
    sectores = ", ".join(data.get('sectores_afectados', []))
    repercusiones = "\n".join([f"- {r}" for r in data.get('repercusiones', [])])
    
    contenido_markdown = f"""# 📊 Alerta de Mercado & Análisis IA
**Fecha:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

### 📰 {data.get('titulo', 'Sin título')}
- **Fuente:** {data.get('fuente', 'N/A')}
- **Impacto:** `{data.get('impacto', 'Neutral')}`
- **Sectores:** {sectores}

---

### 📝 Resumen
{data.get('resumen', '')}

---

### ⚡ Repercusiones
{repercusiones}
"""
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_markdown)
        
    print(f"Archivo generado exitosamente: {nombre_archivo}")

if __name__ == "__main__":
    # Sin try/except para que si hay error se corte e informe
    data = buscar_y_analizar_noticias()
    guardar_informe(data)
        print(f"Error procesando la noticia: {e}")
