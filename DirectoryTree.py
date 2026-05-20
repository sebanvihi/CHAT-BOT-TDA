class DirectoryNode:
    def __init__(self, name, is_category=True, bot_node=None):
        self.name = name
        self.is_category = is_category
        self.bot_node = bot_node
        self.children = []

class DirectoryTree:
    def __init__(self):
        self.root = DirectoryNode("root", True)

    def mkdir(self, path, name):
        if not name or not path:
            raise ValueError("Ruta y nombre son obligatorios.")
        node = self._navigate(path)
        if not node.is_category:
            raise ValueError("La ruta no es una categoria.")
        for child in node.children:
            if child.name == name:
                raise ValueError("El directorio ya existe.")
        node.children.append(DirectoryNode(name, True))

    def add_bot(self, path, bot_node):
        if not bot_node or not path:
            raise ValueError("Ruta y bot son obligatorios.")
        node = self._navigate(path)
        if not node.is_category:
            raise ValueError("La ruta no es una categoria.")
        for child in node.children:
            if child.name == bot_node.botName:
                raise ValueError("El bot ya existe en este directorio.")
        node.children.append(DirectoryNode(bot_node.botName, False, bot_node))

    def _navigate(self, path):
        if path in ("/", "root"):
            return self.root
        parts = [p for p in path.split("/") if p and p != "root"]
        current = self.root
        for part in parts:
            found = False
            for child in current.children:
                if child.name == part and child.is_category:
                    current = child
                    found = True
                    break
            if not found:
                raise ValueError(f"Ruta no encontrada: {part}")
        return current

    def tree(self, node=None, level=0):
        if node is None:
            node = self.root
        prefix = "  " * level + "|-- " if level > 0 else ""
        tipo = "[C]" if node.is_category else f"[B: {node.bot_node.id}]"
        print(f"{prefix}{node.name} {tipo}")
        for child in node.children:
            self.tree(child, level + 1)
