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
                nuevo_bot_id = manager.createProfile(
                    bot["botName"], bot["model"], bot["apiKey"], bot["systemInstruction"]
                )
        # Aquí podrías restaurar también los mensajes y el historial si lo necesitas.
    except Exception as e:
        logger.logError(500, f"Fallo en persistencia: {str(e)}")
