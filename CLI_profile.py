import cohere
from ProfileManager import ProfileManager
from serialization import serializar, obtener_ruta
from deserialization import cargar_datos
from DecisionTree import DecisionTree

class AppCLI:
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.selected_node = None
        self.comandos = {
            "create": self.cmd_create,
            "list": self.cmd_list,
            "select": self.cmd_select,
            "chat": self.cmd_chat,
            "edit": self.cmd_edit,
            "delete": self.cmd_delete,
            "undo": self.cmd_undo,
            "current": self.cmd_current,
            "log": self.cmd_log,
            "save": self.cmd_save,
            "load": self.cmd_load,
            "help": self.cmd_help,
            "mkdir": self.cmd_mkdir,
            "tree": self.cmd_tree,
            "find": self.cmd_find,
            "log-range": self.cmd_log_range
        }
        self.decision_tree = DecisionTree()

    def run(self):
        self.cmd_load("")
        if not self.profile_manager.head:
            self.profile_manager.createProfile("DefaultBot", "command-light", "xVsKUv72B05xviCPtkQtEKwZaWOfT4oms8q67BH3", "You are a helpful assistant.", "root")
        print("------ GEMINI MESH (COHERE CONNECTED) ------")
        print("Escribe 'help' para ver los comandos.")
        
        while True:
            bot_actual = self.selected_node.botName if self.selected_node else "Ninguno"
            entrada = input(f"\n[Bot: {bot_actual}]> ").strip()
            
            if not entrada: continue
            if entrada.lower() in ["exit", "exit-chatbot"]:
                self.cmd_save("")
                break

            partes = entrada.split(maxsplit=1)
            comando = partes[0].lower()
            argumentos = partes[1] if len(partes) > 1 else ""

            if comando in self.comandos:
                try:
                    self.comandos[comando](argumentos)
                except Exception as e:
                    print(f"Error: {e}")
                    self.profile_manager.logger.logError("CLI_ERR", str(e))
            else:
                print("Comando no reconocido.")

    def cmd_chat(self, args):
        if not self.selected_node:
            print("Selecciona un bot primero.")
            return
        
        msg_user = args.strip('"').strip("'")
        if not msg_user: return

        try:
            co = cohere.Client(self.selected_node.apiKey)
            sufijo = self.decision_tree.evaluate(msg_user)
            prompt_final = f"{self.selected_node.systemInstruction} {sufijo}\n\nUser: {msg_user}\nChatbot:"
            response = co.chat(
                model=self.selected_node.model,
                message=prompt_final
            )
            respuesta_ai = response.text.strip()
            self.selected_node.messageQueue.enqueue("User", msg_user)
            self.selected_node.messageQueue.enqueue(self.selected_node.botName, respuesta_ai)
            print(f"\n[{self.selected_node.botName}]: {respuesta_ai}")
            
        except Exception as e:
            error_msg = f"Fallo en API Cohere: {str(e)}"
            print(error_msg)
            self.profile_manager.logger.logError("API_FAIL", error_msg)

    def cmd_help(self, args):
        print(" create              : Nuevo perfil")
        print(" list                : Ver todos")
        print(" select <id>         : Seleccionar bot")
        print(" chat \"<msj>\"        : Chat real con API")
        print(" edit <campo> <valor>: Cambiar nombre/modelo/prompt")
        print(" undo                : Restaurar config (Pila)")
        print(" current             : Ver historial (Cola)")
        print(" save / load         : Persistencia JSON")
        print(" log                 : Ver errores")

    def cmd_create(self, args):
        b = input("Nombre: ")
        m = input("Modelo (ej: command-light): ") or "command-a-03-2025"
        k = input("ApiKey (deja vacio para usar la de defecto): ") or "xVsKUv72B05xviCPtkQtEKwZaWOfT4oms8q67BH3"
        si = input("System Instruction: ")
        ruta = input("Ruta en directorio (ej: root/ventas) [root]: ") or "root"
        pid = self.profile_manager.createProfile(b, m, k, si, ruta)
        print(f"ID generado: {pid}")

    def cmd_list(self, args):
        for node in self.profile_manager:
            print(f"ID: {node.id} | Bot: {node.botName} | Modelo: {node.model}")

    def cmd_select(self, args):
        node = self.profile_manager.consultProfile(args)
        if node:
            self.selected_node = node
            print(f"Seleccionado: {node.botName}")

    def cmd_undo(self, args):
        if not self.selected_node: return
        popped = self.selected_node.undoStack.pop()
        if popped:
            self.selected_node.model = popped.model
            self.selected_node.systemInstruction = popped.systemInstruction
            print("Configuracion restaurada.")
        else: print("Pila vacia.")

    def cmd_current(self, args):
        if not self.selected_node: return
        actual = self.selected_node.messageQueue.first
        while actual:
            print(f"[{actual.user}]: {actual.text}")
            actual = actual.next

    def cmd_edit(self, args):
        if not self.selected_node: return
        partes = args.split(maxsplit=1)
        if len(partes) < 2: return
        campo, valor = partes[0].lower(), partes[1]
        if campo == "nombre": self.profile_manager.modifyProfile(self.selected_node.id, newName=valor)
        elif campo == "modelo": self.profile_manager.modifyProfile(self.selected_node.id, newModel=valor)
        elif campo == "prompt": self.profile_manager.modifyProfile(self.selected_node.id, newPrompt=valor)
        print("Editado.")

    def cmd_delete(self, args):
        if self.profile_manager.deleteProfile(args):
            print("Eliminado.")
            self.selected_node = None

    def cmd_log(self, args):
        self.profile_manager.logger.showErrors()

    def cmd_save(self, args):
        serializar(self.profile_manager, obtener_ruta())

    def cmd_load(self, args):
        cargar_datos(self.profile_manager)
        print("Datos cargados.")

    def cmd_mkdir(self, args):
        partes = args.split(maxsplit=1)
        if len(partes) < 2:
            print("Uso: mkdir <ruta_padre> <nombre_nuevo>")
            return
        self.profile_manager.dir_tree.mkdir(partes[0], partes[1])
        print("Directorio creado.")

    def cmd_tree(self, args):
        self.profile_manager.dir_tree.tree()

    def cmd_find(self, args):
        if not args:
            print("Uso: find <id>")
            return
        node = self.profile_manager.avl_tree.search(args)
        if node:
            print(f"Encontrado: {node.botName} | Modelo: {node.model}")
        else:
            print("No encontrado.")

    def cmd_log_range(self, args):
        partes = args.split(",")
        if len(partes) < 2:
            print("Uso: log-range <YYYY-MM-DD HH:MM:SS>,<YYYY-MM-DD HH:MM:SS>")
            return
        self.profile_manager.logger.log_range(partes[0].strip(), partes[1].strip())

if __name__ == "__main__":
    app = AppCLI()
    app.run()