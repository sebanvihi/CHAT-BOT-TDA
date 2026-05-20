class DecisionNode:
    def __init__(self, condition=None, suffix=None, left=None, right=None):
        self.condition = condition
        self.suffix = suffix
        self.left = left
        self.right = right

class DecisionTree:
    def __init__(self):
        self.root = self._build_default_tree()

    def _build_default_tree(self):
        leaf1 = DecisionNode(suffix="[Responde en tono formal y tecnico.]")
        leaf2 = DecisionNode(suffix="[Responde de manera concisa y directa.]")
        leaf3 = DecisionNode(suffix="[Explica paso a paso con ejemplos.]")
        leaf4 = DecisionNode(suffix="[Responde de manera amistosa y relajada.]")

        node2 = DecisionNode(condition=lambda ctx: "error" in ctx.lower() or "fallo" in ctx.lower(), left=leaf1, right=leaf3)
        node3 = DecisionNode(condition=lambda ctx: len(ctx.split()) < 5, left=leaf2, right=leaf4)

        root = DecisionNode(condition=lambda ctx: "sistema" in ctx.lower() or "codigo" in ctx.lower(), left=node2, right=node3)
        return root

    def evaluate(self, context_msg):
        current = self.root
        while current and current.condition:
            try:
                if current.condition(context_msg):
                    current = current.left
                else:
                    current = current.right
            except Exception:
                current = current.right
        return current.suffix if current else ""
