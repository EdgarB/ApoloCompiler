class Cuadruplo(object):
    def __init__(self, operator,leftOperand, rightOperand, result):
        self.operator = operator;
        self.leftOperand = leftOperand;
        self.rightOperand = rightOperand;
        self.result = result;
        
    def __init__(self):
        self.operator = None;
        self.leftOperand = None;
        self.rightOperand = None;
        self.result = None;

    def getOperator(self):
        return self.operator;

    def getLeftOperand(self):
        return self.leftOperand;

    def getRightOperand(self):
        return self.rightOperand;

    def getResult(self):
        return self.result;

    def setOperator(self, operator):
        self.operator = operator;

    def setLeftOperand(self, leftOperand):
        self.leftOperand = leftOperand;

    def setRightOperand(self, rightOperand):
        self.rightOperand = rightOperand;

    def setResult(self, result):
        self.result = result;
