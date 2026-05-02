from ErrorNode import ErrorNode;
class ErrorLogManager:
    def __init__(self):
        self.head = None;
        self.end = None;
    
    def logError(self,errorCode,errorMsg):
        errorNode = ErrorNode(errorCode,errorMsg);
        if not self.head:
            self.head = self.end = errorNode;
        else:
            self.end.next = errorNode;
            self.end = errorNode;
    
    def showErrors(self):
        current = self.head;
        if not self.head:
            print("NO SE ENCUENTRA ERRORES")
            return
        while current:
            print(f"FECHA Y HORA: {current.dateError:<30s} CODIGO: {current.errorCode:.10d} DESCRIPCION: {current.shortDescription}")
            current = current.next;
            return;