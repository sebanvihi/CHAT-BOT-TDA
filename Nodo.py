from uuid import uuid4;

class Nodo:
    def __init__(self,botName,model,apiKey,systemInstruction):
        self.id = str(uuid4());
        self.botName = botName;
        self.model = model;
        self.apiKey = apiKey;
        self.systemInstruction = systemInstruction;
        self.next = None;
        self.previous = None;



