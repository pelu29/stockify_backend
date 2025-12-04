from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
import requests
import time
import os

load_dotenv()

# MODELO LLM --------------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ No se encontró GROQ_API_KEY en el .env")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

#TIME OUT --------------------------------------------------------------------------------
def _safe_post(url, headers, payload, retries=2, timeout=10):
    for i in range(retries):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))

# TOOL 1: GENERAR PITCH ------------------------------------------------------------------------
@tool(description="Genera un pitch corto, creativo y persuasivo para un producto o idea.")
def generate_pitch(product_name: str, key_benefits: str, target_audience: str) -> str:
    """
    Genera un pitch profesional basado en:
    - product_name: Nombre del producto o idea
    - key_benefits: Beneficios clave separados por comas
    - target_audience: Público objetivo
    """

    prompt = f"""
        Eres un experto en ventas y copywriting. 
        Tu tarea es generar un pitch breve, persuasivo y memorable.

        Producto: {product_name}
        Público objetivo: {target_audience}
        Beneficios clave: {key_benefits}

        Requisitos del pitch:
        - Debe sonar profesional pero atractivo.
        - Tiene que adaptarse al tipo de audiencia.
        - No debe ser genérico.
        - Puede incluir metáforas leves o frases memorables (no exagerar).
        - Duración máxima: 2 a 3 líneas.
        - Tono consultivo y orientado a valor.

        Ahora genera el pitch.
    """

    response = llm.invoke(prompt)
    return response.content.strip()

# TOOL 2: ANALIZAR CLIENTE OBJETIVO ------------------------------------------------------------------------
@tool(description="Analiza el cliente objetivo según industria y tipo de producto.")
def analyze_target(industry: str, product_type: str, additional_details: str) -> str:
    """
    industry: B2B, B2C, B2B2C, B2G o P2P
    product_type: Tipo de producto (app, SaaS, servicio, herramienta...)
    additional_details: Detalles adicionales del proyecto o producto
    """

    prompt = f"""
        Eres un consultor experto en análisis de público objetivo.

        Analiza el cliente ideal para:
        - Industria: {industry}
        - Tipo de producto: {product_type}
        - Detalles extra: {additional_details}

        Devuelve un análisis claramente estructurado con:
        1. Segmento de cliente ideal
        2. Necesidades principales del segmento
        3. Motivaciones de compra
        4. Canales ideales para llegar a ellos
        5. Mensaje clave recomendado
        6. Riesgos o desafíos comerciales
        7. Estrategia recomendada

        Ajusta el análisis según:
        - B2B → empresas, gerentes, decisiones basadas en ROI
        - B2C → consumidores, emociones, conveniencia
        - B2B2C → empresas + clientes finales
        - B2G → procesos públicos, licitaciones, burocracia
        - P2P → usuarios individuales conectándose entre sí
    """

    response = llm.invoke(prompt)
    return response.content

# TOOL 3: TENDENCIAS DE MERCADO -----------------------------------------------------------------------------------
@tool(description="Analiza tendencias e insights de mercado usando DataForSEO SERP (vía RapidAPI).")
def market_trends(keyword: str, language: str = "English", location: str = "United States") -> str:
    """
    keyword: Tema, producto, marca o concepto a investigar.
    language: Idioma de búsqueda (ej: 'English', 'Spanish', 'French').
    location: Ubicación geográfica (ej: 'London,England,United Kingdom').
    """

    url = "https://dataforseo-dataforseo-rank-tracker-and-serp-v1.p.rapidapi.com/v3/serp/google/organic/live/advanced"

    payload = [
        {
            "depth": 10,
            "keyword": keyword,
            "language_name": language,
            "location_name": location
        }
    ]

    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", ""),
        "x-rapidapi-host": "dataforseo-dataforseo-rank-tracker-and-serp-v1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        data = _safe_post(url, headers, payload)
        items = (
            data.get("tasks", [{}])[0]
                .get("result", [{}])[0]
                .get("items", [])
        )

        if not items:
            return f"No se encontraron datos relevantes para '{keyword}'."

        # Interpretación del SERP para un insight más profesional
        insights = []

        for item in items[:10]:
            title = item.get("title", "Sin título")
            url_ = item.get("url", "Sin URL")
            snippet = item.get("description", "Sin descripción")

            insights.append(
                f"- **{title}**\n  - URL: {url_}\n  - Insight: {snippet}"
            )

        interpreted = (
            "• Si predominan artículos informativos → oportunidad de contenido SEO.\n"
            "• Si dominan comparadores → mercado competitivo con evaluación activa.\n"
            "• Si aparecen noticias → tendencia reciente o cambios del sector.\n"
        )

        final_text = f"""
        ### 🔍 Tendencias para: **{keyword}**

        **Idioma:** {language}  
        **Ubicación:** {location}  

        ### 📊 Principales resultados SERP (Top 10):
        {chr(10).join(insights)}

        ### 💡 Interpretación sugerida:
        {interpreted}
        """

        return final_text.strip()

    except Exception as e:
        return f"Error al consultar DataForSEO: {str(e)}"

# PLANER --------------------------------------------------------------------------------
class Plan(BaseModel):
    usar_api: bool = Field(description="Si es necesario llamar a la API de tendencias.")
    keyword: str = Field(description="Keyword principal detectada.", default="")
    instrucciones: str = Field(description="Explicación del plan.")

planner_prompt = """
Eres un PLANIFICADOR experto en ventas y marketing. 
Tu trabajo es LEER la solicitud del usuario y devolver un PLAN en formato JSON.

REGLAS:
1. Activa "usar_api": true cuando la consulta incluya:
   - mercado
   - tendencias
   - SEO
   - Google
   - palabras clave
   - volumen de búsqueda
   - SERP
   - competencia
   - keywords

2. Usar "usar_api" siempre estara en true. No preguntes al usuario por eso, simepre asume que es necesario.

3. Responde SIEMPRE en JSON válido.
"""

planner = create_agent(
    model=llm,
    tools=[],  # EL PLANNER NO EJECUTA HERRAMIENTAS
    system_prompt=planner_prompt
)

# CREAR AGENTE CON HERRAMIENTAS ------------------------------------------------------------------------
worker = create_agent(
    model=llm,
    tools=[generate_pitch, analyze_target, market_trends],
    checkpointer=InMemorySaver(),
    system_prompt=(
    "Eres un agente especializado en ventas, negocios, marketing y estrategias. "
    "Recibes un objeto PLAN generado por el planner. "
    "Debes condiderar que PLAN.usar_api es true cuando se hable de tendencias de mercado, usa la herramienta 'market_trends'. "
    "No preguntes al usuario si quieres usar la herramienta, simplemente úsala cuando PLAN.usar_api sea true. "
    "No inventes datos de mercado bajo ninguna circunstancia."
)
)

# WORKFLOW DEL AGENTE ------------------------------------------------------------------------
workflow = StateGraph(dict)

workflow.add_node(
    "planner", 
    lambda s: {
        "plan": (lambda p: (p.update({"usar_api": True}) or p))(
            json.loads(
                planner.invoke({"messages": [s["messages"][-1]]})["messages"][-1].content
            )
        ),
        "messages": s["messages"]
    }
)
workflow.add_node(
    "ejecutar_worker",
    lambda s: worker.invoke({
        "messages": s["messages"],
        "plan": s["plan"]   # ← le pasamos el plan al agente
    })
)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "ejecutar_worker")
workflow.add_edge("ejecutar_worker", END)

graph = workflow.compile()
# Ahora 'graph' puede ser importado y usado en views.py