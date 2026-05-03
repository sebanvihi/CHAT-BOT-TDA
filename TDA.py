from ErrorLogManager import ErrorLogManager
logger = ErrorLogManager()

class Message:
    def __init__(self, user, text):
        self.user = user  
        self.text = text
        self.next = None  

class Cola:
    def __init__(self, max):
        self.max = max
        self.first = None   
        self.last = None  
        self.n = 0       

    def void(self):
        return self.first is None
    
    def full(self):
        return self.n == self.max
        
    def enqueue(self, user, text):
        message = Message(user, text)
        if self.full():
            logger.logError(202, f"Desbordamiento de cola: Se eliminó mensaje antiguo para liberar espacio.")
            self.first = self.first.next
            self.n -= 1
        if self.void():
            self.first = message
            self.last = message
        else:
            self.last.next = message
            self.last = message
            self.n += 1

