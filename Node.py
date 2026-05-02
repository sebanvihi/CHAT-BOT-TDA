from random import choice;
import string;

class Node:
    def __init__(self,botName,model,apiKey,systemInstruction):
        self.id = self.generateID();
        self.botName = botName;
        self.model = model;
        self.apiKey = apiKey;
        self.systemInstruction = systemInstruction;
        self.next = None;
        self.previous = None;
        self.undoStack = None;
        self.messageQueue = None; 

    def generateID(self):
        newId = "";
        for i in range (4):
            newId += choice(string.digits);
        newId += "-";
        for i in range(10):
            newId += choice(string.ascii_letters);
        newId += "-";
        for i in range (4):
            newId += choice(string.digits);
        return newId;
        




