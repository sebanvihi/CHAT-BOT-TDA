from ErrorNode import ErrorNode
from BTree import BTree

class ErrorLogManager:
    def __init__(self):
        self.head = None
        self.end = None
        self.b_tree = BTree(3)
    
    def logError(self, errorCode, errorMsg):
        errorNode = ErrorNode(errorCode, errorMsg)
        if not self.head:
            self.head = self.end = errorNode
        else:
            self.end.next = errorNode
            self.end = errorNode
        self.b_tree.insert(errorNode.dateError, f"[{errorNode.errorCode}] {errorNode.shortDescription}")
    
    def showErrors(self):
        current = self.head
        if not self.head:
            print("NO SE ENCUENTRA ERRORES")
            return
        while current:
            print(f"FECHA Y HORA: {current.dateError:<30s} CODIGO: {str(current.errorCode):.10s} DESCRIPCION: {current.shortDescription}")
            current = current.next
        return

    def log_range(self, start_time, end_time):
        resultados = self.b_tree.log_range(start_time, end_time)
        if not resultados:
            print("No hay errores en el rango indicado.")
            return
        for timestamp, val in resultados:
            print(f"FECHA Y HORA: {timestamp:<30s} LOG: {val}")