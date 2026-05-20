import json
from ErrorLogManager import ErrorLogManager
from ErrorNode import ErrorNode

def cargar_datos(manager):
    logger = ErrorLogManager()
    try:
        with open("config.txt", "r") as config:
            ruta_json = config.read().strip()
        with open(ruta_json, "r") as f:
            datos = json.load(f)
            for bot in datos["chatbots"]:
                manager.createProfile(
                    bot["botName"], bot["model"], bot["apiKey"], bot["systemInstruction"]
                )
                newNode = manager.end
                for msg in bot.get("mensajes", []):
                    newNode.messageQueue.enqueue(msg["user"], msg["text"])
                
                for estado in reversed(bot.get("historial_estados", [])):
                    newNode.undoStack.push(estado["model"], estado["systemInstruction"])

            for log in datos.get("auditoria", []):
                errorNode = ErrorNode(log["errorCode"], log["shortDescription"])
                errorNode.dateError = log["dateError"]
                if not manager.logger.head:
                    manager.logger.head = manager.logger.end = errorNode
                else:
                    manager.logger.end.next = errorNode
                    manager.logger.end = errorNode
                manager.logger.b_tree.insert(errorNode.dateError, f"[{errorNode.errorCode}] {errorNode.shortDescription}")

    except Exception as e:
        logger.logError(500, f"Error carga: {str(e)}")