import requests,os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

VERDE = "\033[32m"
ROJO = "\033[31m"

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

system_prompt = """
Eres ChefAI, un agente especializado en recetas, nutrición, ingredientes y cocina.
Solo responde sobre recetas, nutrición, ingredientes y cocina.
Siempre usa tus herramientas cuando la respuesta requiera datos reales y específicos (por ejemplo, macronutrientes de un alimento o recetas con un ingrediente).
Si el usuario pregunta por una lista de alimentos con un nutriente (ej. Vitamina C), tu respuesta debe incluir una lista concisa y variada de 5 a 10 elementos conocidos, sin elaboraciones excesivas ni repeticiones, directamente en el primer mensaje.
Cuando el usuario pida recetas, *primero* muestra la lista completa de recetas encontrada por la herramienta `busqueda_recetas`. *Luego*, y solo después de mostrar las recetas, pregunta si desea información nutricional de un ingrediente específico.
Evita dar consejos médicos precisos (solo recomendación general).
"""

SPANISH_TO_ENGLISH_FOOD = {
    "manzana": "apple",
    "pollo": "chicken",
    "arroz": "rice",
    "platano": "banana",
    "huevo": "egg",
    "leche": "milk",
    "pan": "bread",
    "queso": "cheese",
    "pescado": "fish",
    "carne": "meat",
    "patata": "potato",
    "zanahoria": "carrot",
    "tomate": "tomato",
    "cebolla": "onion",
    "ajo": "garlic",
    "pasta": "pasta",
    "naranja": "orange",
    "limon": "lemon",
    "brocoli": "broccoli",
    "espinaca": "spinach",
    "palta": "avocado",
    "cerdo": "pork",
    "ternera": "beef",
    "cordero": "lamb",
    "camaron": "shrimp",
    "salmon": "salmon",
    "atun": "tuna",
    "fresa": "strawberry",
    "uva": "grape",
    "pera": "pear",
    "sandia": "watermelon",
    "melon": "melon",
    "nueces": "nuts",
    "almendras": "almonds",
    "cacahuetes": "peanuts",
    "lentejas": "lentils",
    "garbanzos": "chickpeas",
    "frijoles": "beans",
    "yogur": "yogurt",
    "mantequilla": "butter",
    "aceite de oliva": "olive oil",
    "azucar": "sugar",
    "sal": "salt",
    "pimienta": "pepper",
}

@tool
def consulta_nutricional(alimento: str) -> str:
    """
    Consulta la información nutricional de un alimento específico utilizando la API de USDA FoodData Central.
    Recibe el nombre de un alimento y devuelve sus macronutrientes (macros).
    """
    api_key = os.getenv("USDA_API_KEY")

    if not api_key:
        return "Error: La clave de API de USDA (USDA_API_KEY) no está configurada."

    translated_alimento = SPANISH_TO_ENGLISH_FOOD.get(alimento.lower(), alimento)

    #Buscar el alimento para obtener su fdcId
    #Priorizar tipos de datos "SR Legacy" y "Foundation" para obtener alimentos puros.
    search_urls = []
    search_urls.append(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={alimento}&dataType=SR%20Legacy,Foundation")
    if translated_alimento != alimento:
        search_urls.append(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={translated_alimento}&dataType=SR%20Legacy,Foundation")

    search_data = None
    for url in search_urls:
        try:
            search_response = requests.get(url)
            search_response.raise_for_status()
            search_data = search_response.json()
            if search_data and search_data.get("foods"):
                break # Encontró resultados, salir del bucle
        except requests.exceptions.RequestException as e:
            continue # Intentar con la siguiente URL si hay un error de conexión
        except Exception as e:
            continue

    if not search_data or not search_data.get("foods"):
        return f"No se encontró el alimento '{alimento}' en USDA FoodData Central. Intenta con otro nombre, una descripción más específica o en inglés si es posible."

    # Mejorar la selección del fdcId: buscar el alimento más relevante
    # Iterar a través de los resultados y encontrar uno que coincida mejor y sea "SR Legacy" o "Foundation"
    best_match_fdc_id = None
    for food_item in search_data["foods"]:
        description = food_item.get("description", "").lower()
        data_type = food_item.get("dataType")

        # Priorizar coincidencias exactas o casi exactas con "SR Legacy" o "Foundation"
        if data_type in ["SR Legacy", "Foundation"]:
            if (alimento.lower() in description or translated_alimento.lower() in description) and \
               ("raw" in description or "fresh" in description or "unprepared" in description or
                description == translated_alimento.lower() or description == alimento.lower()):
                best_match_fdc_id = food_item["fdcId"]
                break
        
        # Si no hay un "SR Legacy" o "Foundation" tan específico, tomar el primero de esos tipos
        if best_match_fdc_id is None and data_type in ["SR Legacy", "Foundation"]:
             best_match_fdc_id = food_item["fdcId"]
             # No romper, seguir buscando uno más específico si existe
        
        # Si no hay de tipo "SR Legacy" o "Foundation", tomar el primero que sea relevante (puede ser Branded)
        if best_match_fdc_id is None:
             best_match_fdc_id = food_item["fdcId"] # fallback a cualquier primer resultado relevante
    
    if not best_match_fdc_id:
        return f"No se pudo seleccionar un alimento relevante para '{alimento}' de los resultados de búsqueda."

    fdc_id = best_match_fdc_id

    # Obtener los detalles nutricionales usando el fdcId
    details_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={api_key}"
    
    try:
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        food_details = details_response.json()

        # Extraer macronutrientes. Los nombres de nutrientes pueden variar, buscamos los más comunes.
        # Generalmente, los nutrientes están en la lista 'foodNutrients'.
        
        nutrients = {}
        for nutrient_item in food_details.get("foodNutrients", []):
            nutrient_name = nutrient_item.get("nutrient", {}).get("name")
            unit = nutrient_item.get("nutrient", {}).get("unitName")
            amount = nutrient_item.get("amount")
            
            if nutrient_name and amount is not None:
                if "Energy" in nutrient_name and unit.lower() == "kcal":
                    nutrients["Calorías"] = f"{amount:.2f} kcal"
                elif "Protein" in nutrient_name and unit.lower() == "g":
                    nutrients["Proteínas"] = f"{amount:.2f} g"
                elif "Total lipid (fat)" in nutrient_name and unit.lower() == "g":
                    nutrients["Grasas"] = f"{amount:.2f} g"
                elif "Carbohydrate, by difference" in nutrient_name and unit.lower() == "g":
                    nutrients["Carbohidratos"] = f"{amount:.2f} g"

        if not nutrients:
            return f"No se pudo extraer información nutricional detallada para '{alimento}' (FDC ID: {fdc_id})."

        return f"Información nutricional para '{alimento}' (USDA FoodData Central): {nutrients}"

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print(f"ERROR HTTP en USDA (detalles): {status_code} - {e.response.text}")
        if status_code == 403:
            return f"Error de API de USDA (código {status_code}): Acceso denegado. Verifica tu USDA_API_KEY."
        return f"Error de API de USDA (código {status_code}): {e.response.text}"
    except requests.exceptions.RequestException as e:
        print(f"ERROR de Conexión en USDA (detalles): {e}")
        return f"Error de conexión al consultar los detalles de la API de USDA para '{alimento}': {e}"
    except Exception as e:
        print(f"ERROR Inesperado al procesar detalles de nutrición de '{alimento}': {e}")
        return f"Ocurrió un error inesperado al procesar la nutrición de '{alimento}': {e}"

@tool
def busqueda_recetas(ingredientes: List[str]) -> str:
    """
    Busca recetas basadas en un ingrediente principal utilizando la API de TheMealDB.
    Recibe una lista de ingredientes (solo se usará el primero como ingrediente principal)
    y devuelve recetas coincidentes.
    """
    #TheMealDB solo permite buscar por un ingrediente principal.
    if not ingredientes:
        return "Error: Debes proporcionar al menos un ingrediente para buscar recetas."
    
    main_ingredient = ingredientes[0]
    # Usar el mismo diccionario de traducción que para USDA
    translated_main_ingredient = SPANISH_TO_ENGLISH_FOOD.get(main_ingredient.lower(), main_ingredient)

    api_key = "1" #TheMealDB test API key

    url = f"https://www.themealdb.com/api/json/v1/{api_key}/filter.php?i={translated_main_ingredient}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        recipes_data = response.json()

        if not recipes_data or not recipes_data.get("meals"):
            return f"No se encontraron recetas con el ingrediente principal '{main_ingredient}'. Intenta con otro ingrediente."

        recipe_list = []
        for recipe in recipes_data["meals"]:
            recipe_list.append(f"- {recipe['strMeal']} (ID: {recipe['idMeal']})")
        return "Recetas encontradas (TheMealDB):\n" + "\n".join(recipe_list)

    except requests.exceptions.HTTPError as e:
        print(f"ERROR HTTP en TheMealDB: {e.response.status_code} - {e.response.text}")
        return f"Error de API de TheMealDB (código {e.response.status_code}): {e.response.text}"
    except requests.exceptions.RequestException as e:
        print(f"ERROR de Conexión en TheMealDB: {e}")
        return f"Error de conexión al consultar la API de TheMealDB para recetas: {e}"
    except Exception as e:
        print(f"ERROR Inesperado en TheMealDB: {e}")
        return f"Ocurrió un error inesperado al buscar recetas: {e}"

import json

PREFERENCES_FILE = "user_preferences.json"

def _load_preferences() -> Dict[str, List[str]]:
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, "r") as f:
            return json.load(f)
    return {"ingredientes_favoritos": [], "restricciones_alimentarias": []}

def _save_preferences(preferences: Dict[str, List[str]]):
    with open(PREFERENCES_FILE, "w") as f:
        json.dump(preferences, f, indent=4)

@tool
def guardar_preferencia(tipo: str, valor: str) -> str:
    """
    Guarda una preferencia del usuario. Puede ser un 'ingrediente_favorito' o una 'restriccion_alimentaria'.
    Ejemplo de uso: guardar_preferencia("ingrediente_favorito", "pollo")
    Ejemplo de uso: guardar_preferencia("restriccion_alimentaria", "vegano")
    """
    preferences = _load_preferences()
    if tipo == "ingrediente_favorito":
        if valor not in preferences["ingredientes_favoritos"]:
            preferences["ingredientes_favoritos"].append(valor)
            _save_preferences(preferences)
            return f"Ingrediente favorito '{valor}' guardado."
        return f"El ingrediente favorito '{valor}' ya está guardado."
    elif tipo == "restriccion_alimentaria":
        if valor not in preferences["restricciones_alimentarias"]:
            preferences["restricciones_alimentarias"].append(valor)
            _save_preferences(preferences)
            return f"Restricción alimentaria '{valor}' guardada."
        return f"La restricción alimentaria '{valor}' ya está guardada."
    else:
        return "Tipo de preferencia no válido. Usa 'ingrediente_favorito' o 'restriccion_alimentaria'."

@tool
def cargar_preferencias() -> Dict[str, List[str]]:
    """
    Carga y devuelve las preferencias guardadas del usuario (ingredientes favoritos y restricciones alimentarias).
    """
    return _load_preferences()

@tool
def calculo_estimado_calorias(alimento: str, cantidad_gramos: float) -> str:
    """
    Calcula una estimación de calorías para un alimento y cantidad dados.
    Utiliza una fórmula simple para estimar las calorías.
    """
    calorias_por_gramo_estimado = 2.0 
    calorias_totales = cantidad_gramos * calorias_por_gramo_estimado
    return f"Estimación de calorías para {cantidad_gramos:.2f}g de {alimento}: {calorias_totales:.2f} kcal."

tools = [
    consulta_nutricional,
    busqueda_recetas,
    calculo_estimado_calorias,
    guardar_preferencia,
    cargar_preferencias,
]

checkpointer = InMemorySaver()
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=checkpointer
)

def interactuar_con_chefai(user_input: str, thread_id: str = "chef_ai_session"):
    response = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        {"configurable": {"thread_id": thread_id}}
    )
    return response["messages"][-1].content

if __name__ == "__main__":
    print(VERDE+"👨‍🍳¡Hola! Soy ChefAI. ¿En qué puedo ayudarte hoy con recetas o nutrición?")
    print(VERDE+"Escribe 'salir' para terminar la conversación.")

    # Usamos un thread_id fijo para mantener la memoria a través de las interacciones
    session_thread_id = "chef_ai_session_main"

    while True:
        user_message = input(ROJO+"Tú: ")
        if user_message.lower() == 'salir':
            print(VERDE+"👋¡Adiós! Que tengas un buen día culinario.")
            break

        response = interactuar_con_chefai(user_message, session_thread_id)
        print(VERDE+f"👨‍🍳ChefAI: {response}")