import json
from ErrorLogManager import ErrorLogManager

def cargar_datos(manager):
    logger = ErrorLogManager()
    try:
        with open("config.txt", "r") as config:
            ruta_json = config.read().strip()
        with open(ruta_json, "r") as f:
            datos = json.load(f)
            for bot in datos["chatbots"]:
                manager.createProfile(bot["botName"], bot["model"], bot["apiKey"], bot["systemInstruction"])
                nuevo_nodo = manager.end
                for msg in bot.get("mensajes", []):
                    nuevo_nodo.messageQueue.enqueue(msg["user"], msg["text"])
                for estado in reversed(bot.get("historial_estados", [])):
                    nuevo_nodo.undoStack.push(estado["model"], estado["systemInstruction"])
    except Exception as e:
        logger.logError(500, f"Fallo en persistencia: {str(e)}")