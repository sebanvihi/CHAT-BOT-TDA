import datetime;
class ErrorNode:
    def __init__(self, errorCode,description):
        self.dateError = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.errorCode = errorCode;
        self.shortDescription = description;
        self.next = None;