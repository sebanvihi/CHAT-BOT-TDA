import json
from Node import Node # Importa el nodo del Módulo 1
from ProfileManager import ProfileManager
from StackManager import StackManager 
from ErrorLogManager import ErrorLogManager 
from serializacion import obtener_ruta

def cargar_datos(manager):
    try:
        with open("config.txt", "r") as config:
            ruta_json = config.read().strip()
            
        with open(ruta_json, "r") as f:
            datos = json.load(f)
            
            for bot in datos["chatbots"]:
                nuevo_bot = Node(bot["botName"], bot["model"], bot["apiKey"], bot["systemInstruction"])

                manager.insertar_final(nuevo_bot)
                
    except Exception as e:
        error_logger = ErrorLogManager()
        error_logger.logError(500, f"Fallo en persistencia: {str(e)}")
