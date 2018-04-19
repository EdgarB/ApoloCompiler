class MemoriaDisponible :
    def __init__(self):
        self.memoria = [];
        self.length = 0;

    def getNext(self):
        registro = {"type" : "registro", "value" : self.length};
        self.memoria.append(None);
        self.length = self.length + 1;

        return registro;

    def getLength(self):
        return self.length;
