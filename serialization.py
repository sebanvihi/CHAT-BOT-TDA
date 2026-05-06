import json

def serializar(manager, ruta_archivo):
    data_final = {"chatbots": []}
   
    actual_bot = manager.head
    while actual_bot:
        bot_dict = {
            "id": actual_bot.id,
            "botName": actual_bot.botName,
            "model": actual_bot.model,
            "apiKey": actual_bot.apiKey,
            "systemInstruction": actual_bot.systemInstruction,
            "mensajes": [],
            "historial_estados": [] 
        }
        
       
        actual_msg = actual_bot.messageQueue.first
        while actual_msg:
            bot_dict["mensajes"].append({
                "user": actual_msg.user,
                "text": actual_msg.text
            })
            actual_msg = actual_msg.next
            
        
        actual_estado = actual_bot.undoStack.top
        while actual_estado:
            bot_dict["historial_estados"].append({
                "model": actual_estado.model,
                "systemInstruction": actual_estado.systemInstruction
            })
            actual_estado = actual_estado.next
            
        data_final["chatbots"].append(bot_dict)
        actual_bot = actual_bot.next

def obtener_ruta():
    try:
        with open("config.txt", "r") as f:
            return f.read().strip() # Lee la ruta del JSON desde el archivo
    except FileNotFoundError:
        # Si no existe el config, registras el error en el Módulo 5
        logger.logError(404, "Archivo de configuración config.txt no encontrado")
        return "respaldo.json"

    # 4. Guardar en el archivo JSON físico[cite: 1]
    with open(ruta_archivo, 'w') as f:
        json.dump(data_final, f, indent=4)
    print("Sistema guardado exitosamente.")

