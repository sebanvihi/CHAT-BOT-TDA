from Node import Node
from ErrorLogManager import ErrorLogManager

class ProfileManager:
    def __init__(self):
        self.head = None
        self.end = None
        self.logger = ErrorLogManager()

    def createProfile(self, botName, model, apiKey, systemInstruction):
        newNode = Node(botName, model, apiKey, systemInstruction)
        if not self.head:
            self.head = self.end = newNode
        else:
            self.end.next = newNode
            newNode.previous = self.end
            self.end = newNode
        return newNode.id
    
    def consultProfile(self, requiredId):
        current = self.head
        while current:
            if current.id == requiredId: return current
            current = current.next
        self.logger.logError("NOT_FOUND", requiredId)
        return None
    
    def modifyProfile(self, requiredId, newName=None, newModel=None, newPrompt=None):
        node = self.consultProfile(requiredId)
        if node:
            node.undoStack.push(node.model, node.systemInstruction)
            if newName: node.botName = newName
            if newModel: node.model = newModel
            if newPrompt: node.systemInstruction = newPrompt
            return True
        return False

    def deleteProfile(self, requiredId):
        node = self.consultProfile(requiredId)
        if not node: return False
        if node == self.head: self.head = node.next
        if node.previous: node.previous.next = node.next
        if node.next: node.next.previous = node.previous
        else: self.end = node.previous
        node.next = node.previous = None
        return True
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next