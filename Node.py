from random import choice;
import string;

class Nodo:
    def __init__(self,botName,model,apiKey,systemInstruction):
        self.id = self.generateID(self);
        self.botName = botName;
        self.model = model;
        self.apiKey = apiKey;
        self.systemInstruction = systemInstruction;
        self.next = None;
        self.previous = None;

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




