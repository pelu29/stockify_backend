from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

#Definicion de Tools Locales
@tool("generar_rutinas",description="Genera rutinas de acuerdo al nivel del usuario")
def generar_rutinas(nivel:str)->str:
    """
    nivel : Posibles valores = 'principante', 'intermedio' o 'avanzado'

    """
    if nivel == "principiante":
        return{
            "nivel" : "principiante",
            "rutina":[
                "Sentadillas 3x12",
                "Flexiones 3x10",
                "Plancha 3x30s"
            ]
        }
    elif nivel == "intermedio":
        return {
            "nivel": "intermedio",
            "rutina": [
                "Sentadillas con peso 4x10",
                "Press banca 4x8",
                "Remo con mancuernas 4x10",
                "Plancha lateral 3x30s"
            ]
        }
    else:
        return {
            "nivel": "avanzado",
            "rutina": [
                "Sentadillas pesadas 5x5",
                "Peso muerto 5x5",
                "Dominadas lastradas 4x8",
                "Press militar 4x8",
                "Plancha con peso 3x45s"
            ]
        }

@tool("recomendar_suenio",description="Recomienda la cantidad de horas de sueño según la edad de la persona")
def recomendar_sueño(edad:int)->str:
    """
    edad : Edad de la persona en años
    """

    if edad < 1:
        return {
            "edad": edad,
            "categoria": "bebé",
            "horas_recomendadas": "14-17 horas"
        }
    elif edad <= 2:
        return {
            "edad": edad,
            "categoria": "toddler",
            "horas_recomendadas": "11-14 horas"
        }
    elif edad <= 5:
        return {
            "edad": edad,
            "categoria": "preescolar",
            "horas_recomendadas": "10-13 horas"
        }
    elif edad <= 13:
        return {
            "edad": edad,
            "categoria": "niño",
            "horas_recomendadas": "9-11 horas"
        }
    elif edad <= 17:
        return {
            "edad": edad,
            "categoria": "adolescente",
            "horas_recomendadas": "8-10 horas"
        }
    elif edad <= 64:
        return {
            "edad": edad,
            "categoria": "adulto",
            "horas_recomendadas": "7-9 horas"
        }
    else:  # 65+
        return {
            "edad": edad,
            "categoria": "adulto mayor",
            "horas_recomendadas": "7-8 horas"
        }

@tool("calcular_hidratacion",description="Calcula la cantidad de agua que debe beber una persona según su peso y edad")
def calcular_hidratacion(peso: float, edad: int)->str:
    """
    peso : Peso de la persona en kilogramos
    edad : Edad de la persona en años
    """
 
    if edad < 4:
        return {
            "edad": edad,
            "peso": peso,
            "categoria": "bebé/toddler",
            "agua_recomendada": "Consultar pediatra (recomendación individualizada)"
        }

    elif edad <= 13:
        ml_por_kg = 40
        categoria = "niño"
    elif edad <= 17:
        ml_por_kg = 45
        categoria = "adolescente"
    elif edad <= 64:
        ml_por_kg = 35
        categoria = "adulto"
    else:
        ml_por_kg = 30
        categoria = "adulto mayor"

    litros = (peso * ml_por_kg) / 1000  # convertir ml a litros

    return {
        "edad": edad,
        "peso": peso,
        "categoria": categoria,
        "agua_recomendada": f"{litros:.2f} litros por día",
        "nota": "Este cálculo es una recomendación general, puede variar según actividad física y clima."
    }


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.15
)

agente = create_agent(
    model=llm,
    tools=[generar_rutinas, recomendar_sueño, calcular_hidratacion],#
    system_prompt="Eres un asistente que solo usa sus tools configuradas para dar informacion unicamente de bienestar general, no reemplazas a un doctor",

    checkpointer=InMemorySaver()
    )

configs ={"configurable":{
            "thread_id":"1"
            }
        }


def process_instruction(content: str) -> str:
    Respuesta = agente.invoke({"messages":[{"role": "user", "content": content}]},configs)
    return Respuesta["messages"][-1].content
