from langchain_core.tools import tool

@tool
def generar_plan_estudio(horas_disponibles: int) -> str:
    """Crea un plan de estudio según las horas disponibles"""
    bloques = horas_disponibles // 2
    return f"Puedes hacer {bloques} bloques de estudio de 2 horas cada uno."

@tool
def clasificar_prioridades(tareas: list[str]) -> list[str]:
    """Ordena tareas por urgencia (simulado: primero las que contienen 'urgente')"""
    return sorted(tareas, key=lambda x: "urgente" in x.lower(), reverse=True)

@tool
def generar_pomodoro(ciclos: int) -> str:
    """Genera un esquema Pomodoro según número de ciclos"""
    return f"{ciclos} ciclos de 25 minutos de trabajo y 5 minutos de descanso."
