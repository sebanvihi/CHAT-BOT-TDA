class StateNode:
    def __init__(self,model,systemInstruction,nextN):
        self.model = model;
        self.systemInstruction = systemInstruction;
        self.next = nextN;