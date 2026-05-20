class AVLNode:
    def __init__(self, bot_node):
        self.bot_node = bot_node
        self.id = bot_node.id
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def insert(self, root, bot_node):
        if not root:
            return AVLNode(bot_node)
        if bot_node.id < root.id:
            root.left = self.insert(root.left, bot_node)
        elif bot_node.id > root.id:
            root.right = self.insert(root.right, bot_node)
        else:
            return root

        root.height = 1 + max(self._height(root.left), self._height(root.right))
        balance = self._balance_factor(root)

        if balance > 1 and bot_node.id < root.left.id:
            return self._rotate_right(root)
        if balance < -1 and bot_node.id > root.right.id:
            return self._rotate_left(root)
        if balance > 1 and bot_node.id > root.left.id:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)
        if balance < -1 and bot_node.id < root.right.id:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def add_bot(self, bot_node):
        self.root = self.insert(self.root, bot_node)

    def find(self, root, requiredId):
        if not root or root.id == requiredId:
            return root
        if root.id < requiredId:
            return self.find(root.right, requiredId)
        return self.find(root.left, requiredId)

    def search(self, requiredId):
        node = self.find(self.root, requiredId)
        return node.bot_node if node else None

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, requiredId):
        if not root:
            return root
        if requiredId < root.id:
            root.left = self.delete(root.left, requiredId)
        elif requiredId > root.id:
            root.right = self.delete(root.right, requiredId)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self._min_value_node(root.right)
            root.id = temp.id
            root.bot_node = temp.bot_node
            root.right = self.delete(root.right, temp.id)
        if root is None:
            return root
        root.height = 1 + max(self._height(root.left), self._height(root.right))
        balance = self._balance_factor(root)
        if balance > 1 and self._balance_factor(root.left) >= 0:
            return self._rotate_right(root)
        if balance < -1 and self._balance_factor(root.right) <= 0:
            return self._rotate_left(root)
        if balance > 1 and self._balance_factor(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)
        if balance < -1 and self._balance_factor(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)
        return root

    def remove_bot(self, requiredId):
        self.root = self.delete(self.root, requiredId)

