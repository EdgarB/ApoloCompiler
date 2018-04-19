from collections import OrderedDict


class TablaSimbolos(object):
    def __init__(self, padre, nombre): # parent scope and symbol table name
        self.simbolos = {}
        self.nombre = nombre
        self.padre = padre

    def insertar(self, simbolo): # put variable symbol or fundef under <name> entry
        if self.simbolos.__contains__(simbolo.nombre):
            return False
        else:
            self.simbolos[simbolo.nombre]= simbolo
            return True

    def obtener(self, nombre): # get variable symbol or fundef from <name> entry
        if self.simbolos.__contains__(nombre):
            return self.simbolos[nombre]
        #elif self.padre:
        #    return self.padre;
        else:
            return None

    def existe(self, nombre):
        return self.simbolos.__contains__(nombre)

    def obtenerAlcancePadre(self):
        return self.padre


class Simbolo:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
    def imprimir(self):
        print("")

class SimboloVariable(Simbolo):
    def __init__(self, nombre, tipo, indice):
        self.nombre =  nombre;
        self.tipo = tipo;
        self.valor = None;
        self.dirMem = indice;
    def imprimir(self):
        if(self.nombre is not None):
            print("nombre: " + self.nombre);

        if(self.tipo is not None):
            print("tipo: " + self.tipo);

        if(self.valor is not None):
            print("valor: " + self.valor);

        if(self.dirMem is not None):
            print("Dir mem: " + str(self.dirMem));

class SimboloFuncion(Simbolo):
    def __init__(self, nombre, tipo, comienzo):
        self.nombre = nombre
        self.tipo = tipo
        self.tablaVariables = None
        self.bCreaTabla  = True  #Booleano true -> puede crear tabla ; False -> No puede crear tabla de variables
        self.parametros = [];
        self.cantParametros = 0;
        self.cantVarLocales = 0;
        self.procComienzo = comienzo;



class SimboloFigura(Simbolo):
    def  __init__(self, nombre, tipo, medida, friccion, masa, rebote, movible, color, indice):
        self.nombre = nombre;
        self.tipo = tipo;
        self.medida = medida;
        self.friccion = friccion;
        self.masa = masa;
        self.rebote = rebote;
        self.movible = movible;
        self.color = color;
        self.dirMem = indice;

    def imprimir(self):
        if(self.nombre is not None):
            print("nombre: " + self.nombre)
        if(self.tipo is not None):
            print("tipo: " + self.tipo)
        if(self.medida is not None):
            print("medida: " + str(self.medida))
        if(self.friccion is not None):
            print("friccion: " + str(self.friccion))
        if(self.masa is not None):
            print("masa: " + str(self.masa))
        if(self.rebote is not None):
            print("rebote: " + str(self.rebote))
        if(self.movible is not None):
            print("movible: " + str(self.movible))
        if(self.color is not None):
            print("color: " + self.color)
