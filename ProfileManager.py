from Node import Node;
class ProfileManager:
    def __init__(self):
        self.head = None;
        self.end = None;

    def createProfile(self,botName,model,apiKey,systemInstruction):
        newNode = Node(botName,model,apiKey,systemInstruction)
        if not self.head:
            self.head = self.end = newNode;
        else:
            self.end.next = newNode;
            newNode.previous = self.end;
            self.end = newNode;
        return newNode.id;
    
    def consultProfile(self,requiredId):
        current = self.head;
        while current:
            if current.id == requiredId:
                return current;
            current = current.next;
        return None
    
    def modifyProfile(self,requiredId,newName = None, newModel = None,newPrompt = None):
        node = self.consultProfile(requiredId);
        if node:
            if newName != None:
                node.botName = newName;
            if newModel != None:
                node.model = newModel;
            if newPrompt != None:
                node.systemInstruction = newPrompt;
            return True;
        return False;

    def deleteProfile(self,requiredId):
        node = self.consultProfile(requiredId)
        if not node:
            return False
        if node == self.head:
            self.head = node.next
        if node.previous:
            node.previous.next = node.next
        if node.next:
            node.next.previous = node.previous
        else:
            self.end = node.previous
        node.next = None
        node.previous = None
        return True
    
    def __iter__(self):
        current = self.head;
        while current:
            yield current;
            current = current.next;
