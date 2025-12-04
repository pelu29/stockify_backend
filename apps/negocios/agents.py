from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from .tools import generar_plan_estudio, clasificar_prioridades, generar_pomodoro

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

tools = [generar_plan_estudio, clasificar_prioridades, generar_pomodoro]

system_prompt = """
Eres FocusBuddy, un agente motivador y práctico especializado en productividad, organización personal y estudio.
Solo respondes sobre estos temas.
No resuelves tareas escolares ni das respuestas académicas directas.
Tu tono es siempre positivo, claro y orientado a la acción.
Recuerda los objetivos del usuario para mejorar tus sugerencias.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages")
])

focusbuddy_agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=InMemorySaver()
).with_config({"prompt": prompt})
