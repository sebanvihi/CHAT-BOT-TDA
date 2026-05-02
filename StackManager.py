from StateNode import StateNode
class StackManager:
    def __init__(self):
        self.top = None
        self.length = 0;

    def push(self,model,systemInstruction):
        newNode = StateNode(model,systemInstruction,self.top);
        self.top = newNode;
        self.length += 1; 

    def pop(self):
        if self.top is None:
            return None;
        poppedNode = self.top
        self.top = self.top.next;
        poppedNode.next = None;
        self.length -= 1;
        return poppedNode;
