class Pila:
    def __init__(self):
        self.items = [];
        self.length = 0;
    def top(self):
        if(not self.isEmpty()):
            return self.items[len(self.items) - 1];
        else:
            return None;
    def isEmpty(self):
        if(len(self.items) <= 0):
            return True;
        else:
            return False;

    def pop(self):
        if(self.length > 0):
            self.items.pop();
            self.length -= 1;

    def push(self, item):
        self.length += 1;
        self.items.append(item);
        #print(str(self.items));
