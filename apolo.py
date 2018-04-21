import sys;
import os;
import ply.yacc as yacc;
import ply.lex as lex;
from classes.tablaSimbolos import TablaSimbolos
from classes.tablaSimbolos import SimboloVariable
from classes.tablaSimbolos import SimboloFuncion
from classes.tablaSimbolos import SimboloFigura
from classes.tablaSimbolos import TablaSimbolos
from classes.tablaSimbolos import SimboloVariable
from classes.tablaSimbolos import SimboloFuncion
from classes.tablaSimbolos import SimboloFigura
from classes.pila import Pila
from classes.MemoriaDisponible import MemoriaDisponible
from collections import OrderedDict

reserved = {
    'entero' : 'ENTERO',
    'flotante' : 'FLOTANTE',
    'booleano' : 'BOOLEANO',
    'variables' : 'VARIABLES',
    'programa' : 'PROGRAMA',
    'texto' : 'TEXTO',
    'lista' : 'LISTA',
    'figuras' : 'FIGURAS',
    'imprimir' : 'IMPRIMIR',
    'medida' : 'MEDIDA',
    'friccion' : 'FRICCION',
    'rebote' : 'REBOTE',
    'regresar' : 'REGRESAR',
    'void' : 'VOID',
    'dibujar' : 'DIBUJAR',
    'dibujarLinea' : 'DIBUJAR_LINEA',
    'ciclo' : 'CICLO',
    'si' : 'SI',
    'siNo' : 'SI_NO',
    'cuadrado' : 'CUADRADO',
    'circulo' : 'CIRCULO',
    'triangulo' : 'TRIANGULO',
    'linea' : 'LINEA',
    'pantalla' : 'PANTALLA',
    'apolo' : 'APOLO',
    'movible' : 'MOVIBLE',
    'rojo' : 'ROJO',
    'verde' : 'VERDE',
    'azul' : 'AZUL',
    'amarillo' : 'AMARILLO',
    'rosa' : 'ROSA',
    'violeta' : 'VIOLETA',
    'gravedad' : 'GRAVEDAD',
    'color' : 'COLOR',
    'masa' : 'MASA',
    'verdadero' : 'VERDADERO',
    'falso' : 'FALSO',
    'funciones' : 'FUNCIONES'
    };

tokens = ['ID',
          'CTE_I',
          'CTE_F',
          'CTE_STRING',
          'SEMICOLON',
          'COLON',
          'COMMA',
          'L_PAREN',
          'R_PAREN',
          'L_BRACKETS',
          'R_BRACKETS',
          'L_BRACES',
          'R_BRACES',
          'PLUS_OP',
          'MINUS_OP',
          'TIMES_OP',
          'DIV_OP',
          'N_EQUAL_OP',
          'EQUAL_OP',
          'PLUS_EQUAL_OP',
          'MINUS_EQUAL_OP',
          'ASSIGN_OP',
          'BIGGER_THAN',
          'LESS_THAN',
          'BIGGER_EQUAL_THAN',
          'LESS_EQUAL_THAN',
          'AND',
          'OR'
] + list(reserved.values());


################################################################################
################################################################################
# Regular expression rules for simple tokens
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACKETS = r'\['
t_R_BRACKETS = r'\]'
t_L_BRACES = r'\{'
t_R_BRACES = r'\}'

################################################################################
################################################################################

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\v\f\r'

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    global idActual;
    tokensValues = [x.lower()  for x in reserved.keys()]
    if t.value in reserved.keys():
        t.type = reserved[t.value];
        t.value = t.value.lower();

    else:
        idActual = t.value;

    return t;

def t_CTE_F(t):
    r'[0-9]+\.[0-9]'
    t.value = float(t.value)
    return t

def t_CTE_I(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'\".*\"'
    t.value = str(t.value)
    #print(t.value);
    return t


def t_N_EQUAL_OP(t):
    r'\!\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_EQUAL_OP(t):
    r'\=\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_PLUS_EQUAL_OP(t):
    r'\+\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_MINUS_EQUAL_OP(t):
    r'\-\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_BIGGER_EQUAL_THAN(t):
    r'\>\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_LESS_EQUAL_THAN(t):
    r'\<\='
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_AND(t):
    r'\&\&'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_OR(t):
    r'\|\|'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_PLUS_OP(t):
    r'\+'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_MINUS_OP(t):
    r'\-'
    global operadorActual
    operadorActual = t.value;
    #print(operadorActual);
    return t;

def t_TIMES_OP(t):
    r'\*'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_DIV_OP(t):
    r'/'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_ASSIGN_OP(t):
    r'\='
    global operadorActual;
    operadorActual = t.value;
    #print(operadorActual);
    return t;

def t_BIGGER_THAN(t):
    r'\>'
    global operadorActual;
    operadorActual = t.value;
    return t;

def t_LESS_THAN(t):
    r'\<'
    global operadorActual;
    operadorActual = t.value;
    return t;


################################################################################

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1;

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print(t);
    t.lexer.skip(1)
################################################################################
################################################################################

#     VARIABLES GLOBALES     ###################################################
#TABLA DE SIMBOLOS
tablaDeSimbolos = None;
idActual = None;
alcanceActual = "global";
tipoActual = None;
nombrePrograma = None;

#Figuras
medidaFigActual = None;
friccionFigActual = None;
masaFigActual = None;
reboteFigActual = None;
movibleFigActual = None;
colorFigActual = None;

#Operadores
operadorActual = None;

#Variables necesarias para realizar cuadruplos en Asignacion, Lista_cte
valorActual = None # Esta variable es para guardar el valor de la ultima constante leida
listaTemp = None

#Cubo semantico y compatibilidad de tipos
listaDeCuadruplos = [];
pilaOperandos = Pila();
pilaOperadores = Pila();
pilaTipos = Pila();
memRegistros = MemoriaDisponible();
signoActual = None;

#Condiciones
contadorCuadruplos = 0; #Cada vez que se agrega un cuadruplo se debe de aumentar uno a este contador
pilaSaltosPendientes = Pila();

#Modulos
contadorVariables = 0;
contadorParametros = 0;
apuntadorFuncion = None;

#Constantes y direcciones de Memoria
tablaMemCte = OrderedDict();
#DIRECCIONS MEMORIA
# 1000 - 20999 -> Global
indiceGlobal = 1000;
limMemGlobal = 20999;
# 21000 - 40999 -> Local
indiceLocal = 21000;
limMemLocal = 40999;
# 41000 - 60999 -> Temporal
indiceTemporal = 41000;
limMemTemporal = 60999;
# 61000 - 80999 -> CTE
indiceCTE = 61000;
limMemCTE = 80999;
# 81000 - 100999
indiceFigura = 81000;
limMemFigura = 100999;



#LISTAS
contadorIndice = 0;

longLista = 0;

traductorValoresCubo = {
  0 :  "error",
  1 : "int",
  2 : "float",
  3 : "string",
  4 : "bool",
  5 : "lista int",
  6 : "lista float",
  7 : "lista string",
  8 : "lista bool",
  9 : "nothing"
}

traductorIndicesOperandosCubo = {
    "int" : 0,
    "entero" : 0,
    "float" : 1,
    "flotante" : 1,
    "string" : 2,
    "texto" : 2,
    "bool" : 3,
    "booleano" : 3,
    "lista int" : 4,
    "lista float" : 5,
    "lista string" : 6,
    "lista bool" : 7,
    "nothing" : 8
}

traductorIndicesOperadoresCubo = {
    "+" : 0,
    "-" : 1,
    "*" : 2,
    "/" : 3,
    "+=" : 4,
    "-=" : 5,
    "=" : 6,
    ">" : 7,
    "<" : 8,
    "==" : 9,
    "!=" : 10
}

# [tipo][tipo][operador] = tipo retorno
cuboSemantico = [
        [
            [1, 1, 1, 2, 9, 9, 9, 4, 4, 4, 4],
            [2, 2, 2, 2, 9, 9, 9, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ],
        [
            [2, 2, 2, 2, 9, 9, 9, 4, 4, 4, 4],
            [2, 2, 2, 2, 9, 9, 9, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 3, 0, 9, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 9, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 5, 0, 9, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 5, 0, 9, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 5, 0, 9, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 5, 0, 9, 0, 0, 4, 4]

        ]
    ];

"""
 0 -> error
 1 -> int
 2 -> float
 3 -> string
 4 -> bool
 5 -> lista int
 6 -> lista float
 7 -> lista string
 8 -> lista bool
 9 -> nothing

indices  -> cubo - 1

0 -> +
1 -> -
2 -> *
3 -> /
4 -> +=
5 -> -=
6 -> =
7 -> >
8 -> <
9 -> ==
10 -> !=

"""

#     FUNCIONES     ############################################################

# imprimirError
# En construccion
def imprimirError(error, linea):
    global idActual;
    global alcanceActual;

    if(linea is not None):
        print("Error en linea " + str(linea) + ":");
    else:
        print("Error:");

    if(error == 0):
        #Error: Variable no definida
        print("Variable " + idActual + " llamada en " + alcanceActual + " no definida previamente.");
    elif(error == 1):
        print("Funcion " + idActual + " llamada en " + alcanceActual + " no fue declarada previamente.");
    elif(error == 2):
        print("Redeficion de la figura " + idActual + ".");
    elif(error == 3):
        print("Atributo repetido en la figura " + idActual + ".");
    elif(error == 4):
        #Error: El atributo escrito no es un atributo valido en la definicion de la figura
        print("Atributo inexistente en la figura " + idActual + ".");
    elif(error == 5):
        print("Figura " + idActual + " inexistente.");
    elif(error == 6):
        print("Operacion entre operandos no compatible.");
    elif(error == 7):
        print("Los valores a utilizar dentro de la funcion PANTALLA deben ser numeros solamente.");
    elif(error == 8):
        print("dibujar solo acepta figuras que no sean de tipo linea.");
    elif(error == 9):
        print("dibujarLinea solo acepta figuras que sean de tipo linea.");
    elif(error == 10):
        print("Los tipos de datos no coinciden.");
    elif(error == 11):
         #Error cantidad de parametros en llamada a funcion no coinciden
         print("Cantidad de parametros en llamada a funcion no coincide con su declaracion.");
    elif(error == 12):
        #Error retorno en funcion VOID
        print("Estatuto retorno definido en funcion de tipo VOID.");
    elif(error == 13):
        print("Indice fuera de rango.");
    elif(error == 14):
        print("Variable " + idActual + " redefinida en la declaracion de los parametros de la funcion " + alcanceActual + ".");
    elif(error == 15):
        print("Variable " + idActual + " declarada en " + alcanceActual + " redefinida.");
    elif(error == 16):
        print("Limite de memoria alcanzado");
# checarDefFunc
#   Descripcion: Checa que el nombre de la funcion recien declarada no haya sido
#       declarado anteriormente en la tabla de funciones global
#       (en la variable tablaDeSimbolos).
#   Retorno: Si encuentra que el id ya habia sido declarado regresa VERDADERO,
#       Si no, regresa FALSO.
def checarDefFunc():
  global tablaDeSimbolos
  global idActual
  return tablaDeSimbolos.existe(idActual);

# checarDefVar
#   Descripcion: Checa que la variable recien definida no haya sido definida
#       anteriormente dentro del alcance que se encuentra.
#   Retorno: Regresa VERDADERO si la variable ya habia sido declarada con
#       anterioridad. Si no, regresa FALSO.
def checarDefVar():
    global tablaDeSimbolos;
    global alcanceActual;
    global idActual;

    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    bRetorno = False;
    if(simboloFunc is not None and simboloFunc.tablaVariables is not None):
        bRetorno = simboloFunc.tablaVariables.existe(idActual);
        if(bRetorno is not True):
            simboloFunc = tablaDeSimbolos.obtener("global");
            if(simboloFunc is not None and simboloFunc.tablaVariables is not None):
                return simboloFunc.tablaVariables.existe(idActual);
            else:
                return False;
        else:
            return True;
    elif(alcanceActual is not "global"):
        simboloFunc = tablaDeSimbolos.obtener("global");
        if(simboloFunc is not None and simboloFunc.tablaVariables is not None):
            return simboloFunc.tablaVariables.existe(idActual);
        else:
            return False;
    else:
        return False;

# checarDefParamFunc
#   Descripcion: Checa si el nombre del parametro recien definido no ha sido
#       Definido anteriormente como parte de la funcion donde acaba de ser
#       declarada la el id de la variable siendo checada.
#   Retorno: Regresa VERDADERO si encontro que el id de la varaiable definida
#       ya habia sido definida anteriormente.
def checarDefParamFunc():
    global tablaDeSimbolos;
    global idActual;
    global alcanceActual;
    bRetorno = False;
    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    if simboloFunc == None :
        #error
        imprimirError(1,None);
    else:
        vTemp = simboloFunc.parametros;
        for x in vTemp:
            if(x[0] == idActual):
                bRetorno = True;
                break;
    return bRetorno;

# checarDefFunc
#   Descripcion: Checa si ya se utilizo el id de la figura recien declarada
#       la declaracion de otra figura.
#   Retorno: Regresa VERDADERO si el id siendo evaluado ya fue utilizado en la
#       declaracion de otra figura.
def checarDefFigura():
    global tablaDeSimbolos
    global idActual
    return tablaDeSimbolos.obtener("_figuras").tablaVariables.existe(idActual)

def imprimirContenidoTablaSimbolos(tablaSimb):
    for x in tablaSimb.simbolos:
        print("**************************************************************");
        print(x);
        print("-");
        if(tablaSimb.simbolos[x].tablaVariables is not None):
            for y in tablaSimb.simbolos[x].tablaVariables.simbolos:
                tablaSimb.simbolos[x].tablaVariables.simbolos[y].imprimir();
                print("\n");
        print("-");
        for z in tablaSimb.simbolos[x].parametros:
            print(z);
        print("\n");
    print("**************************************************************");

def obtenerContSimb(id):
    global tablaDeSimbolos;
    global alcanceActual;
    simbFunAct = tablaDeSimbolos.obtener(alcanceActual);
    if(simbFunAct != None):
        if(simbFunAct.tablaVariables != None):
            simbVar = simbFunAct.tablaVariables.obtener(id);
            if(simbVar != None):
                return simbVar;
            else:
                simbFunAct = tablaDeSimbolos.obtener("global");
                if(simbFunAct.tablaVariables != None):
                    simbVar = simbFunAct.tablaVariables.obtener(id);
                    return simbVar;
                else:
                    return None;
        else:
            simbFunAct = tablaDeSimbolos.obtener("global");
            if(simbFunAct.tablaVariables != None):
                simbVar = simbFunAct.tablaVariables.obtener(id);
                return simbVar;
            else:
                return None;
    else:
        simbFunAct = tablaDeSimbolos.obtener("global");
        if(simbFunAct.tablaVariables != None):
            simbVar = simbFunAct.tablaVariables.obtener(id);
            return simbVar;
        else:
            return None;
################################################################################
################################################################################

#     PROGRAMA     #############################################################

def p_programa(t):
    '''
        programa : PROGRAMA creaTablaFunc  ID agregaGlobalTabla  SEMICOLON variablesAuxiliar pantallaAuxiliar figurasAuxiliar gravedadAuxiliar agregarGoToApolo funcionesAuxiliar apoloAuxiliar
        '''
    global tablaDeSimbolos;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    imprimirContenidoTablaSimbolos(tablaDeSimbolos);
    print("Cant cuads (real) -> " + str(len(listaDeCuadruplos)));
    print("Cant cuads (contador) -> " + str(contadorCuadruplos));
    print("Programa compilado correctamente");

def p_variablesAuxiliar(t):
    '''
        variablesAuxiliar : creaTablaVar variables
        | empty
        '''

def p_pantallaAuxiliar(t):
    '''
        pantallaAuxiliar : pantalla
        | empty agregarCuadDefectoPantalla
        '''

def p_figurasAuxiliar(t):
    '''
        figurasAuxiliar : figuras
        | empty
        '''

def p_gravedadAuxiliar(t):
    '''
        gravedadAuxiliar : gravedad
        | empty agregarCuadDefectoGravedad
        '''
def p_funcionesAuxiliar(t):
    '''
        funcionesAuxiliar : FUNCIONES funciones
        | empty
        '''

def p_apoloAuxiliar(t):
    '''
        apoloAuxiliar : APOLO apoloTablaFunc agregaFuncTabla creaTablaVar bloque
    '''
    global listaDeCuadruplos;
    global contadorCuadruplos;

    listaDeCuadruplos.append(["END",None, None,None])
    contadorCuadruplos +=1;
################################################################################

# Puntos neuralgicos para cuadruplos

# Expresiones

# Punto 1
def p_agregarIdHaciaPilas(t):
    '''
        agregarIdHaciaPilas : empty
    '''
    global idActual;
    global tipoActual;
    global pilaOperandos;
    global pilaOperadores;
    global tablaDeSimbolos;
    global alcanceActual;

    #Asumiendo que ya se checo que existiera la variable declarada
    varTemp1 = tablaDeSimbolos.obtener(alcanceActual);


    if(varTemp1 is None):
        varAux = tablaDeSimbolos.obtener("global");
        varAux2 = varAux.tablaVariables.obtener(idActual);
        if(varAux2 is not None):
            #Variable es global
            #print(idActual + " : " + str(varAux2.valor));
            pilaOperandos.push(varAux2.dirMem);
            pilaTipos.push(varAux2.tipo);
    else:
        varTemp2 = varTemp1.tablaVariables;
        if(varTemp2 is  None or varTemp2.obtener(idActual) is None):
            varAux = tablaDeSimbolos.obtener("global");
            varAux2 = varAux.tablaVariables.obtener(idActual);
            if(varAux2 is not None):
                pilaOperandos.push(varAux2.dirMem);
                pilaTipos.push(varAux2.tipo);
                #print(idActual + " : " +str(varAux2.nombre));
        else:
            varTemp2 = varTemp2.obtener(idActual);
            pilaOperandos.push(varTemp2.dirMem);
            pilaTipos.push(varTemp2.tipo);
            #print(idActual + " : " + str(varTemp2.nombre));

# Punto 2 y 3 y 8
def p_agregarOperador(t):
    '''
        agregarOperador : empty
    '''
    global operadorActual;
    global pilaOperadores;
    """
    if(operadorActual == '+'):
        pilaOperadores.push('+');
    elif(operadorActual == '-'):
        pilaOperadores.push('-');
    elif(operadorActual == '*'):
        pilaOperadores.push('*');
    elif(operadorActual == '/'):
        pilaOperadores.push('/');
    elif(operadorActual == '>'):
        pilaOperadores.push('>');
    elif(operadorActual == '<'):
        pilaOperadores.push('<');
    elif(operadorActual == '>='):
        pilaOperadores.push('>=');
    elif(operadorActual == '<='):
        pilaOperadores.push('<=');
    elif(operadorActual == '!='):
        pilaOperadores.push('!=');
    elif(operadorActual == '=='):
        pilaOperadores.push('==');
    elif(operadorActual == '&&'):
        pilaOperadores.push('&&');
    elif(operadorActual == '||'):
        pilaOperadores.push('||');
    elif(operadorActual == '='):
        pilaOperadores.push('=');
    """
    pilaOperadores.push(operadorActual);
    #print("--PILA OPERADORE-- ",  pilaOperadores.items);

# Punto 4
def p_compSemMasMenosYGenCuad(t):
    '''
        compSemMasMenosYGenCuad : empty
    '''
    global pilaOperandos;
    global pilaOperadores;
    global pilaTipos;
    global cuboSemantico;
    global memRegistros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global liMemTemporal;
    varTemp =  pilaOperadores.top();
    if(varTemp is not None and (varTemp == '+' or varTemp == '-')):

        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();

        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();

        operandoIzquierdo = pilaOperandos.top();
        pilaOperandos.pop();

        tipoIzquierdo = pilaTipos.top();
        pilaTipos.pop();

        operador = varTemp;
        pilaOperadores.pop();

        tipoResultado = cuboSemantico[traductorIndicesOperandosCubo[tipoIzquierdo]][traductorIndicesOperandosCubo[tipoDerecho]][traductorIndicesOperadoresCubo[operador]]
        #print("MAS MENOS : " + str(operandoIzquierdo) + " " + str(operador) + " " + str(operandoDerecho));
        #print("MAS MENOS: " + str(tipoIzquierdo) + " " + str(operador) + " " + str(tipoDerecho));
        if(tipoResultado != 0):
            if(indiceTemporal < limMemTemporal):
                cuadruplo = [operador, operandoIzquierdo, operandoDerecho, indiceTemporal];


                listaDeCuadruplos.append(cuadruplo);
                pilaOperandos.push(indiceTemporal);
                tipoResultado = traductorValoresCubo[tipoResultado];
                pilaTipos.push(tipoResultado);

                indiceTemporal += 1;
                contadorCuadruplos += 1;
            else:
                imprimirError(16, None);

        else:

            imprimirError(6, t.lineno(1));

# Punto 5
def p_comprobarSemanticaPorEntre(t):
    '''
        comprobarSemanticaPorEntre : empty
    '''
    global pilaOperandos;
    global pilaOperadores;
    global pilaTipos;
    global cuboSemantico;
    global memRegistros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global liMemTemporal;
    varTemp = pilaOperadores.top();
    if(varTemp is not None and (varTemp == '*' or varTemp == '/')):
        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();

        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();

        operandoIzquierdo = pilaOperandos.top();
        pilaOperandos.pop();

        tipoIzquierdo = pilaTipos.top();
        pilaTipos.pop();

        operador = pilaOperadores.top();
        pilaOperadores.pop();

        tipoResultado = cuboSemantico[traductorIndicesOperandosCubo[tipoIzquierdo]][traductorIndicesOperandosCubo[tipoDerecho]][traductorIndicesOperadoresCubo[operador]]
        #print("POR ENTRE : " + str(operandoIzquierdo) + " " + str(operador) + " " + str(operandoDerecho));
        #print("POR ENTRE: " + str(tipoIzquierdo) + " " + str(operador) + " " + str(tipoDerecho));
        if(tipoResultado != 0):
            if(indiceTemporal < limMemTemporal):
                cuadruplo = [operador, operandoIzquierdo, operandoDerecho, indiceTemporal];


                listaDeCuadruplos.append(cuadruplo);
                pilaOperandos.push(indiceTemporal);
                tipoResultado = traductorValoresCubo[tipoResultado];
                pilaTipos.push(tipoResultado);

                indiceTemporal += 1;
                contadorCuadruplos += 1;
            else:
                imprimirError(16,None);

        else:

            imprimirError(6, t.lineno(1));

#Punto 6
def p_agregarPisoFalso(t):
    '''
        agregarPisoFalso : empty
    '''
    global pilaOperadores;
    pilaOperadores.push('(');

#Punto 7
def p_eliminarPisoFalso(t):
    '''
        eliminarPisoFalso : empty
    '''
    global pilaOperadores;
    pilaOperadores.pop();

#Punto 8
#Es el punto 3

#Punto 9
#Punto neuralgico para comprobar semantica y generar cuadruplo de los operadores
#'<', '>', '<=', '>=', '!=', '=='
def p_comprobarSemanticaOperadoresRelacionales(t):
    '''
        comprobarSemanticaOperadoresRelacionales : empty
    '''
    global pilaOperandos;
    global pilaOperadores;
    global pilaTipos;
    global cuboSemantico;
    global memRegistros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global liMemTemporal;
    varTemp = pilaOperadores.top();

    if(varTemp is not None and (varTemp == '>' or varTemp == '<' or varTemp == '<=' or varTemp == '>=' or varTemp == '!=' or varTemp == '==')):

        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();

        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();

        operandoIzquierdo = pilaOperandos.top();
        pilaOperandos.pop();

        tipoIzquierdo = pilaTipos.top();
        pilaTipos.pop();

        operador = pilaOperadores.top();
        pilaOperadores.pop();

        ind1 = traductorIndicesOperandosCubo[tipoIzquierdo];
        ind2 = traductorIndicesOperandosCubo[tipoDerecho];
        ind3 = traductorIndicesOperadoresCubo[operador];
        tipoResultado = cuboSemantico[ind1][ind2][ind3];
        #print("RELACIONALES : " + str(operandoIzquierdo) + " " + str(operador) + " " + str(operandoDerecho));
        #print("RELACIONALES: " + str(tipoIzquierdo) + " " + str(operador) + " " + str(tipoDerecho));
        if(tipoResultado != 0):
            if(indiceTemporal < limMemTemporal):
                cuadruplo = [operador, operandoIzquierdo, operandoDerecho, indiceTemporal];

                listaDeCuadruplos.append(cuadruplo);
                pilaOperandos.push(indiceTemporal);
                tipoResultado = traductorValoresCubo[tipoResultado];
                pilaTipos.push(tipoResultado);

                indiceTemporal += 1;
                contadorCuadruplos += 1;
            else:
                imprimirError(16, None);

        else:
            imprimirError(6, t.lineno(1));
#Punto 10
#Punto neuralgico para comprobar semantica y generar cuadruplo de los operadores '&&' y '||'
def p_compSemYGenCuadYO(t):
    '''
        compSemYGenCuadYO : empty
    '''
    global pilaOperandos;
    global pilaOperadores;
    global pilaTipos;
    global cuboSemantico;
    global memRegistros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global liMemTemporal;
    varTemp = pilaOperadores.top();

    if(varTemp is not None and (varTemp == '&&' or varTemp == '||')):
        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();

        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();

        operandoIzquierdo = pilaOperandos.top();
        pilaOperandos.pop();

        tipoIzquierdo = pilaTipos.top();
        pilaTipos.pop();

        operador = pilaOperadores.top();
        pilaOperadores.pop();

        tipoResultado = cuboSemantico[traductorIndicesOperandosCubo[tipoIzquierdo]][traductorIndicesOperandosCubo[tipoDerecho]][traductorIndicesOperadoresCubo[operador]];
        #print("AND OR : " + str(operandoIzquierdo) + " " + str(operador) + " " + str(operandoDerecho));
        #print("AND OR: " + str(tipoIzquierdo) + " " + str(operador) + " " + str(tipoDerecho));
        if(tipoResultado != 0):
            if(indiceTemporal < limMemTemporal):
                cuadruplo = [operador, operandoIzquierdo, operandoDerecho, indiceTemporal];
                indiceTemporal += 1;
                listaDeCuadruplos.append(cuadruplo);
                pilaOperandos.push(resultado);
                tipoResultado = traductorValoresCubo[tipoResultado];
                pilaTipos.push(tipoResultado);

                contadorCuadruplos += 1;
            else:
                imprimirError(16, None);
        else:
            imprimirError(6, t.lineno(1));

#Puntos neuralgicos para cuadruplos en asignacion

#1 Es la de agregarIdHaciaPilas

#2 Reutilizar punto de agregarOperador en expresion
#3 Agrega operando
def p_agregarOperando(t):
    '''
        agregarOperando : empty
    '''
    global pilaOperandos;
    global valorActual;
    global pilaTipos;
    global tablaMemCte;
    global indiceCTE;
    global limMemCTE;

    if(isinstance(valorActual, bool)):
        pilaTipos.push("bool");
        if(valorActual in tablaMemCte):
            pilaOperandos.push(tablaMemCte[valorActual]);
        else:
            if(indiceCTE < limMemCTE):
                pilaOperandos.push(indiceCTE);
                tablaMemCte[valorActual] = indiceCTE;
                indiceCTE += 1;
            else:
                imprimirError(16, None);



    elif(isinstance(valorActual, str)):

        pilaTipos.push("string");
        if(valorActual in tablaMemCte):
            pilaOperandos.push(tablaMemCte[valorActual]);
        else:
            if(indiceCTE < limMemCTE):
                pilaOperandos.push(indiceCTE);
                tablaMemCte[valorActual] = indiceCTE;
                indiceCTE += 1;
            else:
                imprimirError(16, None);
    else:
        print("tipo: " + str(type(valorActual)));


#4
def p_agregarCuadYCompSemAsignacion(t):
    '''
    agregarCuadYCompSemAsignacion : empty
    '''
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaOperadores;
    global pilaTipos;
    global pilaOperandos;
    global cuboSemantico;
    global traductorValoresCubo;
    global traductorIndicesOperandosCubo;
    global traductorIndicesOperadoresCubo;
    global alcanceActual;
    global indiceTemporal;
    global liMemTemporal;
    #print("ASIGNACION");
    #print(pilaTipos.items);
    #print(pilaOperandos.items);
    #print(pilaOperadores.items);
    #print(pilaOperadores.top());
    #print("ENDASIGNACION");
    varOpTop = pilaOperadores.top();
    if(varOpTop == '=' or varOpTop == '+=' or varOpTop == '-='):
        #print("entro igual");
        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();

        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();

        operandoIzquierdo = pilaOperandos.top();
        pilaOperandos.pop();

        tipoIzquierdo = pilaTipos.top();
        pilaTipos.pop();

        operador = pilaOperadores.top();
        pilaOperadores.pop();


        #print("ASIGNACION: " + str(operandoIzquierdo) + " " + str(operador) + " " + str(operandoDerecho));
        #print("ASIGNACION: " + str(tipoIzquierdo) + " " + str(operador) + " " + str(tipoDerecho));
        tipoResultado = cuboSemantico[traductorIndicesOperandosCubo[tipoIzquierdo]][traductorIndicesOperandosCubo[tipoDerecho]][traductorIndicesOperadoresCubo[operador]];

        if(tipoResultado != 0):
            #print("wooo");

            if(tipoIzquierdo == "integer" or tipoIzquierdo == "int" or tipoIzquierdo == "entero"):
                if(indiceTemporal < limMemTemporal):

                    cuad = ["cast", operandoDerecho, "int", indiceTemporal];
                    listaDeCuadruplos.append(cuad);

                    cuadruplo = [operador, indiceTemporal, None, operandoIzquierdo];

                    contadorCuadruplos += 1;
                    indiceTemporal += 1;
                else:
                    imprimirError(16, None);
            elif(tipoIzquierdo == "float" or  tipoIzquierdo == "flotante"):
                if(indiceTemporal < limMemTemporal):
                    cuad = ["cast", operandoDerecho, "float", indiceTemporal];
                    listaDeCuadruplos.append(cuad);

                    cuadruplo = [operador, indiceTemporal, None, operandoIzquierdo];

                    contadorCuadruplos += 1;
                    indiceTemporal += 1;
                else:
                    imprimirError(16, None);
            else:
                cuadruplo = [operador, operandoDerecho, None, operandoIzquierdo];

            listaDeCuadruplos.append(cuadruplo);
            contadorCuadruplos += 1;

        else:
            imprimirError(6, t.lineno(1));


#Puntos neuralgicos para pantalla y pantallaAuxiliar
#Pantalla
def p_agregarCuadYCompSemPantalla(t):
    '''
    agregarCuadYCompSemPantalla : empty
    '''
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaOperadores;
    global pilaTipos;
    global pilaOperandos;


    operandoDerecho = pilaOperandos.top();
    pilaOperandos.pop();

    tipoDerecho = pilaTipos.top();
    pilaTipos.pop();

    operandoIzquierdo = pilaOperandos.top();
    pilaOperandos.pop();

    tipoIzquierdo = pilaTipos.top();
    pilaTipos.pop();

    if((tipoDerecho == "int" or tipoDerecho == "Entero" or tipoDerecho == "float" or tipoDerecho == "flotante") and (tipoIzquierdo == "int" or tipoIzquierdo == "Entero" or tipoIzquierdo == "float" or tipoIzquierdo == "flotante")):
        #Crear cuadruplo
        cuadruplo = ["pantalla", operandoIzquierdo, operandoDerecho, None];
        listaDeCuadruplos.append(cuadruplo);
        contadorCuadruplos += 1;
    else:
        imprimirError(7,None);

#Pantalla auxiliar (valores por defecto)
def p_agregarCuadDefectoPantalla(t):
    '''
    agregarCuadDefectoPantalla : empty
    '''

    global listaDeCuadruplos;
    global contadorCuadruplos;
    cuadruplo = ["pantalla", 100, 100, None];
    listaDeCuadruplos.append(cuadruplo);
    contadorCuadruplos += 1;


#Puntos neuralgicos para gravedad y gravedadAuxiliar
#Gravedad
def p_agregarCuadYCompSemGravedad(t):
    '''
    agregarCuadYCompSemGravedad : empty
    '''
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaOperadores;
    global pilaTipos;
    global pilaOperandos;


    operandoDerecho = pilaOperandos.top();
    pilaOperandos.pop();

    tipoDerecho = pilaTipos.top();
    pilaTipos.pop();

    operandoIzquierdo = pilaOperandos.top();
    pilaOperandos.pop();

    tipoIzquierdo = pilaTipos.top();
    pilaTipos.pop();

    if((tipoDerecho == "int" or tipoDerecho == "Entero" or tipoDerecho == "float" or tipoDerecho == "flotante") and (tipoIzquierdo == "int" or tipoIzquierdo == "Entero" or tipoIzquierdo == "float" or tipoIzquierdo == "flotante")):
        #Crear cuadruplo
        cuadruplo = ["gravedad", operandoIzquierdo, operandoDerecho, None];
        listaDeCuadruplos.append(cuadruplo);
        contadorCuadruplos += 1;
    else:
        imprimirError(7,None);

#Gravedad auxiliar (valores por defecto)
def p_agregarCuadDefectoGravedad(t):
    '''
    agregarCuadDefectoGravedad : empty
    '''

    global listaDeCuadruplos;
    global contadorCuadruplos;
    cuadruplo = ["gravedad", 0, -9.81, None];
    listaDeCuadruplos.append(cuadruplo);
    contadorCuadruplos += 1;

#Cuadruplos Escritura
#Agregar cuadruplo de Escritura cuando se tiene expresion como atributo
def p_agregarCuadEScrituraExpresion(t):
    '''
    agregarCuadEScrituraExpresion : empty
    '''
    global pilaOperandos;
    global pilaTipos;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    #(pilaOperandos.items);
    aux = pilaOperandos.top();
    pilaOperandos.pop();
    pilaTipos.pop();
    if(aux is not None):
        cuadruplo = ["imprimir", aux, None, None];
        listaDeCuadruplos.append(cuadruplo);
        contadorCuadruplos += 1;

#Agregar cuadruplo de Escritura cuando se tiene string o bool como parametro
def p_agregarCuadEscrituraSPCTE(t):
    '''
    agregarCuadEscrituraSPCTE : empty
    '''
    global valorActual;
    global listaDeCuadruplos;
    global contadorCuadruplos;

    if(valorActual is not None):
        cuadruplo = ["imprimir", valorActual, None, None];
        listaDeCuadruplos.append(cuadruplo);
        contadorCuadruplos += 1;

#Cuadruplos dibujarLinea y dibujar
#Agregar operando dibujarLinea
def p_agregarOperadorDibujarLinea(t):
    '''
    agregarOperadorDibujarLinea : empty
    '''
    global pilaOperadores;

    pilaOperadores.push("dibujarLinea");

#Agregar operando dibujar
def p_agregarOperadorDibujar(t):
    '''
    agregarOperadorDibujar : empty
    '''
    global pilaOperadores;

    pilaOperadores.push("dibujar");

#agregarCuadDibujarGen
def p_agregarCuadDibujarGen(t):
    '''
    agregarCuadDibujarGen : empty
    '''
    global pilaOperadores;
    global pilaOperandos;
    global pilaTipos;
    global listaDeCuadruplos;
    global contadorCuadruplos;

    varTemp = pilaOperadores.top();
    if(varTemp == "dibujar"):
        pilaOperadores.pop();
        param2 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        param1 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        idFigura = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop()


        cuad = ["dibujar",idFigura, param1, param2];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

    elif(varTemp == "dibujarLinea"):
        pilaOperadores.pop();

        param4 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        param3 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        param2 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        param1 = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();

        idFigura = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop()

        cuad = ["dibujarLinea", idFigura, param1, param2];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        cuad = ["dibujarLinea", idFigura, param3, param4];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

#Puntos neuralgicos condicion
#1
def p_generarCuadCondicionGotoFIf(t):
    '''
    generarCuadCondicionGotoFIf : empty
    '''
    global pilaTipos;
    global pilaOperandos;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaSaltosPendientes;
    exp_tipo = pilaTipos.top();
    pilaTipos.pop();
    if(exp_tipo == 'bool' or exp_tipo == 'booleano'):
        result = pilaOperandos.top();
        pilaOperandos.pop();
        pilaTipos.pop();
        cuad = ["gotof", result,None];
        listaDeCuadruplos.append(cuad);
        pilaSaltosPendientes.push(contadorCuadruplos);
        contadorCuadruplos += 1;
    else:
        #Imprimir error de type missmatch
        imprimirError(10, None);
#2
def p_llenarGotof(t):
    '''
    llenarGotof : empty
    '''
    global pilaSaltosPendientes;
    global listaDeCuadruplos;
    global contadorCuadruplos;

    end = pilaSaltosPendientes.top();
    pilaSaltosPendientes.pop();

    listaDeCuadruplos[end].append(contadorCuadruplos);

#3
def p_generarCuadCondicionGotoFElse(t):
    '''
    generarCuadCondicionGotoFElse : empty
    '''
    global pilaSaltosPendientes;
    global listaDeCuadruplos;
    global contadorCuadruplos;

    cuad = ["goto",None, None];
    listaDeCuadruplos.append(cuad);
    contadorCuadruplos += 1;

    falso = pilaSaltosPendientes.top();
    pilaSaltosPendientes.pop();

    pilaSaltosPendientes.push(contadorCuadruplos - 1);

    listaDeCuadruplos[falso].append(contadorCuadruplos);


#Puntos neuralgicos para cuadruplos de ciclos
#1
#Cuando termina de ejecutarse el bloque dentro del ciclo, este debe regresar a
# una posicion donde empieza a ejecutarse la expresion del ciclo, este punto neuralgico
# es para definir ese punto.
def p_agregarAPilaSaltosRegresoCiclo(t):
    '''
    agregarAPilaSaltosRegresoCiclo : empty
    '''
    global pilaSaltosPendientes;
    global contadorCuadruplos;
    pilaSaltosPendientes.push(contadorCuadruplos);

#2
def p_generarCuadCondCiclo(t):
    '''
    generarCuadCondCiclo : empty
    '''
    global contadorCuadruplos;
    global listaDeCuadruplos;
    global pilaOperandos;
    global pilaTipos;
    global pilaSaltosPendientes;

    exp_tipo = pilaTipos.top();
    pilaTipos.pop();

    if(exp_tipo == "bool" or exp_tipo == "booleano"):
        resultado = pilaOperandos.top();
        pilaOperandos.pop();

        cuad = ["gotof", resultado, None];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        pilaSaltosPendientes.push(contadorCuadruplos - 1);

    else:
        imprimirError(10, None);
#3
def p_generarCuadRetCiclo(t):
    '''
    generarCuadRetCiclo : empty
    '''
    global contadorCuadruplos;
    global listaDeCuadruplos;
    global pilaSaltosPendientes;

    gotof = pilaSaltosPendientes.top();
    pilaSaltosPendientes.pop();

    cicloComienzo = pilaSaltosPendientes.top();
    pilaSaltosPendientes.pop();


    cuadRegreso = ["goto", None, None, cicloComienzo];

    listaDeCuadruplos.append(cuadRegreso);
    contadorCuadruplos += 1;

    listaDeCuadruplos[gotof].append(contadorCuadruplos);


#Puntos neuralgicos para retorno
def p_genCuadRetorno(t):
    '''
    genCuadRetorno : empty
    '''
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaOperadores;
    global pilaTipos;
    global pilaOperandos;
    global alcanceActual;
    global tablaDeSimbolos;

    opRet = pilaOperadores.top()
    pilaOperadores.pop();
    if(opRet == "retorno"):
        thisFunc = tablaDeSimbolos.obtener(alcanceActual);
        tipoRes = pilaTipos.top();
        pilaTipos.pop();
        if(thisFunc.tipo == tipoRes):
            #(pilaOperandos.items);
            resultado = pilaOperandos.top();
            pilaOperandos.pop();
            #("TIPO FUNCION -> " + str(tipoRes) + " - " + str(resultado));
            cuad = ["return", resultado, None,None ];
            listaDeCuadruplos.append(cuad);
            contadorCuadruplos += 1;
        else:
            imprimirError(10,None);

# Checar si el retorno esta en una funcion que regrese algo
def p_checarRetorno(t):
    '''
    checarRetorno : empty
    '''
    global alcanceActual;
    global tablaDeSimbolos;

    varFunc = tablaDeSimbolos.obtener(alcanceActual);
    if(varFunc.tipo == "void"):
        imprimirError(12);


def p_agregarOperadorRetorno(t):
    '''
    agregarOperadorRetorno : empty
    '''
    global pilaOperadores;
    pilaOperadores.push("retorno");

#Punts neuralgics declaracion llamada ( la mayoria estan en otra poosicion)

def p_agregarOperandoVoid(t):
    '''
    agregarOperandoVoid : empty
    '''
    global pilaOperandos;
    global pilaTipos;

    pilaOperandos.push(None);
    pilaTipos.push("void");

#Puntos neuralgicos llamda de funcion

#Verificar que la funcion exista
def p_checarSiExisteFuncion(t):
    '''
    checarSiExisteFuncion : empty
    '''
    if(checarDefFunc() is False):
        imprimirError(1, None);

#Generar accion ERA
def p_generarAccionERA(t):
    '''
    generarAccionERA : empty
    '''
    global contadorParametros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global idActual;
    global apuntadorFuncion;
    global tablaDeSimbolos;

    apuntadorFuncion = tablaDeSimbolos.obtener(idActual);
    cuad = ["era", idActual, None, None];
    listaDeCuadruplos.append(cuad);
    contadorCuadruplos += 1;
    contadorParametros = 1;

def p_generarAccionParam(t):
    '''
    generarAccionParam : empty
    '''
    global contadorParametros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global idActual;
    global pilaOperandos;
    global pilaTipos;
    global apuntadorFuncion;


    argumento = pilaOperandos.top();
    pilaOperandos.pop();

    argTipo = pilaTipos.top();
    pilaTipos.pop();

    if(contadorParametros > apuntadorFuncion.cantParametros):
         #Error cantidad de parametros en llamada a funcion no coinciden
         imprimirError(11, None);
    elif(argTipo != apuntadorFuncion.parametros[contadorParametros - 1][1]):
        #Error type missmatch
        imprimirError(10, None);
        #print("func - " + str(argTipo) + " = " + str(apuntadorFuncion.parametros[contadorParametros - 1][1]));
    else:
        cuad = ["param", argumento, None, contadorParametros];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;
        contadorParametros += 1;

def p_generarAccionGoSub(t):
    '''
    generarAccionGoSub : empty
    '''
    global contadorParametros;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global apuntadorFuncion;


    if(contadorParametros - 1 != apuntadorFuncion.cantParametros):
        #Error cantidad de parametros en llamada a funcion no coinciden
        imprimirError(11, None);
    else:
        cuad = ["gosub", apuntadorFuncion.nombre, None, apuntadorFuncion.procComienzo];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;
        contadorParametros = 1;
        apuntadorFuncion = None;
################################################################################

# checarSiExisteFiguraId
#
def p_checarSiExisteFiguraIdYAgregarAPila(t):
    '''
    checarSiExisteFiguraId : empty
    '''
    global tablaDeSimbolos;
    global pilaOperadores;
    global pilaOperandos;
    global pilaTipos;



    figTemp = tablaDeSimbolos.obtener("_figuras").tablaVariables.obtener(idActual);
    if(figTemp is None):
        imprimirError(5, t.lineno(0));
    else:
        opTemp = pilaOperadores.top();
        if(opTemp == "dibujar" and figTemp.tipo == "linea"):
            #Imprimir error de tipo de figura incorrecto no se esperaba una linea
            imprimirError(8,None);
        elif(opTemp == "dibujarLinea" and figTemp.tipo != "linea"):
            #imprimir error de tipo de figura incorrecto, se esperaba una linea
            imprimirError(9,None);
        else:
            pilaOperandos.push(figTemp.dirMem);
            pilaTipos.push(figTemp.tipo);
# listaVar
#    Descripcion: Asigna el tipo actual y el valor de lista.
def p_listaVar(t):
    '''
    listaVar : empty
    '''
    global tipoActual;
    tipoActual = "lista"

# variables
#   Descripcion: Asigna como el alcance actual todo todo lo que esta dentro de
#       de la funcion principal apolo.
def p_apoloTablaFunc(t):
    '''
    apoloTablaFunc : empty
    '''
    global idActual;
    global alcanceActual;
    global tipoActual;
    global pilaSaltosPendientes;
    global listaDeCuadruplos;

    alcanceActual = "apolo"
    tipoActual = "void"
    idActual = "apolo"

    indice = pilaSaltosPendientes.top();
    pilaSaltosPendientes.pop();

    listaDeCuadruplos[indice].append(contadorCuadruplos);

#agregargotoApolo
def p_agregarGoToApolo(t):
    '''
        agregarGoToApolo : empty
    '''

    global listaDeCuadruplos;
    global contadorCuadruplos;
    global pilaSaltosPendientes;
    listaDeCuadruplos.append(["goto", "apolo", None]);
    pilaSaltosPendientes.push(contadorCuadruplos);
    contadorCuadruplos += 1;
# creaTablaFunc
#   Descripcion: Crea la tabla de simbolos global (Tabla de funciones)
def p_creaTablaFunc(t):
  '''
    creaTablaFunc : empty
  '''
  global tablaDeSimbolos;

  tablaDeSimbolos = TablaSimbolos(None, "_global");


# agregaGlobalTabla:
#   Descripcion: Agrega el registro para las variables globales en la tabla de
#       funciones.
def p_agregaGlobalTabla(t):
    '''
      agregaGlobalTabla : empty
    '''
    global idActual
    global nombrePrograma
    global tablaDeSimbolos
    global tipoActual
    global contadorCuadruplos;
    global alcanceActual;

    nombrePrograma = idActual;

    tablaDeSimbolos.insertar(SimboloFuncion("global", tipoActual, contadorCuadruplos));
    alcanceActual = "global";

# asignarAlcance
#   Descripcion: Asigna el alcance actual segun el ultimo registro leido de la
#       tabla de funciones
def p_asignarAlcance(t):
  '''
    asignarAlcance : empty
  '''
  global idActual
  global alcanceActual

  alcanceActual = idActual;

# creaTablaVar
#   Descripcion: Crea la tabla de variables para el ultimo registro leido
#       de la tabla de funciones leido.
def p_creaTablaVar(t):
    '''
        creaTablaVar : empty
    '''
    global alcanceActual
    global simboloAlcance
    global tablaDeSimbolos
    global contadorVariables

    simboloAlcance = tablaDeSimbolos.obtener(alcanceActual)
    if simboloAlcance == None :
        #Generar error funcion no existe
        #print("Error: ");
        #print("Funcion " + idActual + " inexistente" );
        imprimirError(1, None);
    else: #Checa si esta siendo llamada y no siendo declarada la funcion
        #print("Se creo tabla " + alcanceActual);
        simboloAlcance.tablaVariables = TablaSimbolos(alcanceActual,"vars");
        contadorVariables = 0;

#
#
def p_checarDefID(t):
    '''
        checarDefID : empty
    '''
    global idActual;

    if(not checarDefVar()):
        imprimirError(0, t.lineno(1));

# agregaVarTabla
# Descripcion: Se ingresa a la tabla de variables local de la funcion las
#       variables con su respectivo tipo, en dado caso que la variable
#       tratandose de agregar no haya sido definida previamente.

def p_agregaVarTabla(t):
    '''
    agregaVarTabla : empty
    '''
    global tablaDeSimbolos
    global idActual
    global tipoActual
    global alcanceActual
    global contadorVariables;
    global indiceLocal;
    global indiceGlobal;
    global longLista;
    global limMemLocal;
    global limMemGlobal;
    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);

    if(simboloFunc == None):
        #print("simboloFuncion " + alcanceActual + " no existe")#error esa funcion no existe
        imprimirError(1, None);
    elif(simboloFunc.bCreaTabla):
        tablaVars = simboloFunc.tablaVariables
        if(tablaVars != None): #Debe de existir, si no algo hicimos mal en el codigo
            if(checarDefVar()):
                imprimirError(15, None);
            elif(checarDefParamFunc()):
                imprimirError(14, None); #Ya esta definida la variable
            else:

                contadorVariables += 1;
                if(alcanceActual == "global"):
                    temp = tipoActual.split();
                    if(temp[0] == "lista"):
                        if(indiceGlobal < limMemGlobal):
                            simbVar = SimboloVariable(idActual,tipoActual,indiceGlobal, longLista);
                            tablaVars.insertar(simbVar);
                            indiceGlobal += longLista;
                        else:
                            imprimirError(16, None);


                    else:
                        if(indiceGlobal < limMemGlobal):
                            simbVar = SimboloVariable(idActual,tipoActual,indiceGlobal, None);
                            tablaVars.insertar(simbVar);
                            indiceGlobal += 1;
                        else:
                            imprimirError(16, None);




                else:
                    temp = tipoActual.split();
                    if(temp[0] == "lista"):
                        if(indiceLocal < limMemLocal):
                            simbVar = SimboloVariable(idActual,tipoActual,indiceLocal, longLista);
                            tablaVars.insertar(simbVar);
                            indiceLocal += longLista;
                        else:
                            imprimirError(16, None);


                    else:
                        if(indiceLocal < limMemLocal):
                            simbVar = SimboloVariable(idActual,tipoActual,indiceLocal, None);
                            tablaVars.insertar(simbVar);
                            indiceLocal += 1;
                        else:
                            imprimirError(16, None);




        else:
            print("Algo salio mal, checar que la regla para crear tabla de variables esta en las producciones correspondientes")


# agregaFuncTabla
#   Descripcion: Agrega el registro de la funcion a la tabla de funciones global.
def p_agregaFuncTabla(t):
  '''
    agregaFuncTabla : empty
  '''
  global idActual;
  global tipoActual;
  global contadorCuadruplos;
  tablaDeSimbolos.insertar(SimboloFuncion(idActual, tipoActual, contadorCuadruplos));


# agregaParamFunc
#   Descripcion: Agrega los parametros al registro de la funcion correspondiente,
#       si el ID del parametro no ha sido registrado previamente.
def p_agregaParamFunc(t):
    '''
    agregaParamFunc : empty
    '''
    global alcanceActual;
    global idActual;
    global tipoActual;
    global tablaDeSimbolos;
    global indiceLocal;
    global limMemLocal;

    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    if(simboloFunc == None):
        imprimirError(1, None);#Error funcion no existe
    elif(True is not checarDefParamFunc()):
        encabezadoParam = [idActual, tipoActual];
        simboloFunc.parametros.append(encabezadoParam);
        simboloFunc.cantParametros += 1;
        temp = tipoActual.split();
        if(temp[0] == "lista"):
            if(indiceLocal < limMemLocal):
                simbVar = SimboloVariable(idActual,tipoActual,indiceLocal, longLista);
                simboloFunc.tablaVariables.insertar(simbVar);
                indiceLocal += longLista;
            else:
                impmrimirError(16,None);
        else:
            if(indiceLocal < limMemLocal):
                simbVar = SimboloVariable(idActual,tipoActual,indiceLocal, None);
                simboloFunc.tablaVariables.insertar(simbVar);
                indiceLocal += 1;
            else:
                imprimirError(16, None);

    else:
        imprimirError(15, None);#error variable ya definida en parametros

def p_liberaTablaVars(t):
    '''
    liberaTablaVars : empty
    '''
    global alcanceActual;
    global indiceLocal;
    global tablaDeSimbolos;
    global contadorVariables;
    global contadorCuadruplos;
    global listaDeCuadruplos;
    global indiceTemporal;
    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    if(simboloFunc == None):
        imprimirError(1); #Error funcion no existe
    else:
        simboloFunc.tablaVariables = None;
        simboloFunc.cantVarLocales = contadorVariables;
        cuad = ["endproc", None, None, None];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        indiceLocal = 21000;
        indiceTemporal = 41000;


def p_creaFigFuncSimb(t):
  '''
    creaFigFuncSimb : empty
  '''
  global tablaDeSimbolos;
  global alcanceActual;
  global contadorCuadruplos;

  alcanceActual = "_figuras"
  tablaDeSimbolos.insertar(SimboloFuncion("_figuras", None, contadorCuadruplos))
  tablaDeSimbolos.obtener("_figuras").tablaVariables = TablaSimbolos(None, "vars")

def p_checarFiguraId(t):
    '''
    checarFiguraId : empty
    '''
    if(checarDefFigura()):
        imprimirError(2, t.lineno(1));

def p_creaFigVar(t):
    '''
    creaFigVar : empty
    '''
    global tablaDeSimbolos;
    global idActual;
    global medidaFigActual;
    global friccionFigActual;
    global masaFigActual;
    global reboteFigActual;
    global movibleFigActual;
    global colorFigActual;
    global indiceFigura;
    global limMemFigura
    if(not checarDefFigura()):
        if(indiceFigura < limMemFigura):
            figura = SimboloFigura(idActual, tipoActual, medidaFigActual, friccionFigActual, masaFigActual, reboteFigActual, movibleFigActual, colorFigActual, indiceFigura);
            indiceFigura += 1;
            varsFigTabla = tablaDeSimbolos.obtener("_figuras").tablaVariables.insertar(figura)


            medidaFigActual = None;
            friccionFigActual = None;
            masaFigActual = None;
            reboteFigActual = None;
            movibleFigActual = None;
            colorFigActual = None;
        else:
            imprimirError(16, None);

#     VARIABLES     ############################################################
def p_variables(t):
  '''
  variables : VARIABLES  variablesAuxiliar1 ID agregaVarTabla variablesAuxiliar2 SEMICOLON variablesAuxiliar3
  '''

def p_variablesAuxiliar1(t):
  '''
  variablesAuxiliar1 : tipo
  | tipo_lista
  '''

def p_variablesAuxiliar2(t):
  '''
  variablesAuxiliar2 : COMMA ID agregaVarTabla variablesAuxiliar2
  | empty
  '''

def p_variablesAuxiliar3(t):
  '''
  variablesAuxiliar3 : variablesAuxiliar1 ID agregaVarTabla variablesAuxiliar2 SEMICOLON variablesAuxiliar3
  | empty
  '''



#     TERMINO     ##############################################################
def p_termino(t):
  '''
  termino : factor comprobarSemanticaPorEntre terminoAuxiliar1
  '''

def p_terminoAuxiliar1(t):
    '''
    terminoAuxiliar1 : operadorEntre agregarOperador termino
    | operadorPor agregarOperador termino
    | empty
    '''

#     RETORNO     ##############################################################
def p_retorno(t):
  '''
  retorno : REGRESAR checarRetorno agregarOperadorRetorno retornoAuxiliar1 SEMICOLON genCuadRetorno
  '''

def p_retornoAuxiliar1(t):
  '''
  retornoAuxiliar1 : expresion
  | sp_cte agregarOperando
  | empty agregarOperandoVoid
  '''

#     PANTALLA     #############################################################
def p_pantalla(t):
  '''
  pantalla : PANTALLA L_PAREN exp COMMA exp R_PAREN SEMICOLON agregarCuadYCompSemPantalla
  '''


#     GRAVEDAD     #############################################################
def p_gravedad(t):
  '''
  gravedad : GRAVEDAD L_PAREN exp COMMA exp R_PAREN SEMICOLON agregarCuadYCompSemGravedad
  '''


#     FUNCIONES     ############################################################
def p_funciones(t):
  '''
  funciones : funcionesAuxiliar1 ID asignarAlcance agregaFuncTabla creaTablaVar L_PAREN tipo ID agregaParamFunc funcionesAuxiliar2 R_PAREN L_BRACES  funcionesAuxiliar3 funcionesAuxiliar4 R_BRACES liberaTablaVars
  '''
def p_funcionesAuxiliar1(t):
  '''
  funcionesAuxiliar1 : tipo
  | VOID
  '''

def p_funcionesAuxiliar2(t):
  '''
  funcionesAuxiliar2 :  COMMA tipo ID agregaParamFunc funcionesAuxiliar2
  | empty
  '''

def p_functionsAuxiliar3(t):
    '''
    funcionesAuxiliar3 : variables
    | empty
    '''


def p_funcionesAuxiliar4(t):
    '''
    funcionesAuxiliar4 :  estatuto funcionesAuxiliar4
    | empty
    '''



#     FIGURAS     ##############################################################
def p_figuras(t):
  '''
  figuras : FIGURAS creaFigFuncSimb asignarAlcance figura ID checarFiguraId L_BRACES figura_atributos figura_atributosAuxiliar2 R_BRACES creaFigVar figurasAuxiliar1 SEMICOLON
  '''

def p_figurasAuxiliar1(t):
  '''
  figurasAuxiliar1 : COMMA figura ID checarFiguraId L_BRACES figura_atributos figura_atributosAuxiliar2 R_BRACES creaFigVar figurasAuxiliar1
  | empty
  '''


#     FIGURA     ###############################################################
def p_figura(t):
  '''
  figura : CUADRADO
  | CIRCULO
  | TRIANGULO
  | LINEA
  '''
  global tipoActual
  tipoActual = t[1]

#     FIGURA_ATRIBUTOS    ######################################################
def p_figura_atributos(t):
    '''
    figura_atributos : MEDIDA COLON CTE_I
    | figura_atributosAuxiliar1 COLON CTE_F
    | MOVIBLE COLON cte_bool
    | COLOR COLON color_cte
    '''
    global medidaFigActual
    global friccionFigActual
    global masaFigActual
    global reboteFigActual
    global movibleFigActual
    global colorFigActual
    if(t[1] == 'medida'):
        if(medidaFigActual == None):
            medidaFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    elif(t[1] == 'friccion'):
        if(friccionFigActual ==  None):
            friccionFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    elif(t[1] == 'masa'):
        if(masaFigActual == None):
            masaFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    elif(t[1] == 'rebote'):
        if(reboteFigActual == None):
            reboteFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    elif(t[1] == 'movible'):
        if(movibleFigActual == None):
            movibleFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    elif(t[1] == 'color'):
        if(colorFigActual == None):
            colorFigActual = t[3]
        else:
            #Crashealo
            imprimirError(3, t.lineno(1));
    else:
        imprimirError(4, t.lineno(1));

def p_figura_atributosAuxiliar1(t):
  '''
  figura_atributosAuxiliar1 : FRICCION
  | MASA
  | REBOTE
  '''
  t[0] = t[1]

def p_figura_atributosAuxiliar2(t):
  '''
  figura_atributosAuxiliar2 : COMMA figura_atributos figura_atributosAuxiliar2
  | empty
  '''

#     EXP    ###################################################################
def p_exp(t):
  '''
  exp : termino compSemMasMenosYGenCuad expAuxiliar1
  '''

def p_expAuxiliar1(t):
    '''
    expAuxiliar1 : operadorMenos agregarOperador exp
    | operadorMas agregarOperador exp
    | empty
    '''

#     ESTATUTO     #############################################################
def p_estatuto(t):
  '''
  estatuto : asignacion SEMICOLON
  | condicion
  | escritura
  | ciclo
  | dibujar
  | llamada SEMICOLON
  | incremento SEMICOLON
  | retorno
  '''

#     DIBUJAR     ##############################################################
def p_dibujar(t):
  '''
  dibujar : dibujarAuxiliar1 COMMA exp COMMA exp R_PAREN SEMICOLON agregarCuadDibujarGen
  '''

def p_dibujarAuxiliar1(t):
  '''
  dibujarAuxiliar1 : DIBUJAR agregarOperadorDibujar L_PAREN ID checarSiExisteFiguraId
  | DIBUJAR_LINEA agregarOperadorDibujarLinea L_PAREN ID checarSiExisteFiguraId COMMA exp COMMA exp
  '''


#     CICLO     ################################################################
def p_ciclo(t):
  '''
  ciclo : CICLO L_PAREN asignacion SEMICOLON agregarAPilaSaltosRegresoCiclo expresion SEMICOLON generarCuadCondCiclo incremento R_PAREN bloque generarCuadRetCiclo
  '''

#     CONDICION     ###########################################################
def p_condicion(t):
  '''
  condicion : SI L_PAREN expresion R_PAREN generarCuadCondicionGotoFIf bloque condicionAuxiliar1 SEMICOLON llenarGotof
  '''

def p_condicionAuxiliar1(t):
  '''
  condicionAuxiliar1 : SI_NO generarCuadCondicionGotoFElse bloque
  | empty
  '''



#     BLOQUE     ###############################################################

def p_bloque(t):
  '''
  bloque : L_BRACES  bloqueAuxiliar1 R_BRACES
  '''


def p_bloqueAuxiliar1(t):
    '''
    bloqueAuxiliar1 : empty
    | estatuto bloqueAuxiliar1
    '''

#     INCREMENTO     ##########################################################
def p_incremento(t):
  '''
  incremento : ID checarDefID agregarIdHaciaPilas incrementoAuxiliar1 agregarOperador exp agregarCuadYCompSemAsignacion
  '''

def p_incrementoAuxiliar1(t):
  '''
  incrementoAuxiliar1 : PLUS_EQUAL_OP
  | MINUS_EQUAL_OP
  '''
  global operadorActual;
  ### DEBUG: operador += no esta siendo agregado
  #print("OPERADOR INCREMENTO: " + t[1]);
  operadorActual = t[1];

#     ASIGNACION    ##########################################################
def p_asignacion(t):
  '''
  asignacion : asignacionAuxiliar2   ASSIGN_OP agregarOperadorAsignacion asignacionAuxiliar1
  '''
  if(checarDefVar() is False):
      imprimirError(0, t.lineno(1));

def p_agregarOperadorAsignacion(t):
    '''
    agregarOperadorAsignacion : empty
    '''
    global operadorActual;
    global pilaOperadores;
    #print("OPERADOR ASIGNACION!!!!!!!!!")
    pilaOperadores.push('=');
    #print("WWWWWWWWWWWAAAAT");
def p_asignacionAuxiliar1(t):
  '''
  asignacionAuxiliar1 : expresion agregarCuadYCompSemAsignacion
  | lista_cte
  | sp_cte agregarOperando agregarCuadYCompSemAsignacion
  '''
def p_asignacionAuxiliar2(t):
    '''
    asignacionAuxiliar2 : ID checarDefID agregarIdHaciaPilas
    | elemArr
    '''
#   LLAMADA ELEM ARREGLO ####################################################
def p_elemArr (t):
    '''
    elemArr : ID checarDefID agregarIdHaciaPilas agregarLongLista L_BRACKETS exp R_BRACKETS agregarCuadsElemArr
    '''

def p_agregarCuadsElemArr(t):
    '''
    agregarCuadsElemArr : empty
    '''
    global pilaOperandos;
    global pilaTipos;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global longLista;
    global tablaMemCte;
    global indiceCTE;
    global limMemCTE;
    global liMemTemporal;
    indice = pilaOperandos.top();
    pilaOperandos.pop()

    indiceTipo = pilaTipos.top();
    pilaTipos.pop();

    lista = pilaOperandos.top();
    pilaOperandos.pop();



    listaTipo = pilaTipos.top();
    pilaTipos.pop();
    print(str(listaTipo));
    contTipo = listaTipo.split();
    if(indiceTemporal < limMemTemporal):
        cuad = ["cast", indice, "int",indiceTemporal];
        indiceTemporal += 1;

        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        cuad = ["ver", indiceTemporal - 1, 0, longLista - 1];
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        if(lista in tablaMemCte):
            dirBLista = tablaMemCte[lista];
        else:
            if(indiceCTE < limMemCTE):
                tablaMemCte[lista] = indiceCTE;
                dirBLista = indiceCTE;

                indiceCTE += 1;
            else:
                imprimirError(16, None);


        cuad = ["+", dirBLista, indiceTemporal - 1, indiceTemporal];
        indiceTemporal += 1;
        listaDeCuadruplos.append(cuad);
        contadorCuadruplos += 1;

        dirLista = "(" + str(indiceTemporal - 1) + ")";
        pilaOperandos.push(dirLista);
        pilaTipos.push(contTipo[1]);
    else:
        imprimirError(16, None);

def p_agregarLongLista(t):
    '''
    agregarLongLista : empty
    '''
    global idActual;
    global longLista;
    simbArr = obtenerContSimb(idActual);
    longLista = simbArr.dim;





#    ESCRITURA    ###########################################################
def p_escritura(t):
  '''
  escritura : IMPRIMIR L_PAREN escrituraAuxiliar1 escrituraAuxiliar2 R_PAREN SEMICOLON
  '''

def p_escrituraAuxiliar1(t):
  '''
  escrituraAuxiliar1 : expresion agregarCuadEScrituraExpresion
  | sp_cte agregarCuadEscrituraSPCTE
  '''

def p_escrituraAuxiliar2(t):
  '''
  escrituraAuxiliar2 : COMMA escrituraAuxiliar1 escrituraAuxiliar2
  | empty
  '''




#     LLAMADA     ##############################################################
def p_llamada(t):
  '''
  llamada : ID checarSiExisteFuncion generarAccionERA L_PAREN llamadaAuxiliar1 R_PAREN generarAccionGoSub
  '''


def p_llamadaAuxiliar1(t):
    '''
    llamadaAuxiliar1 : llamadaAuxiliar2 generarAccionParam llamadaAuxiliar3
    | empty
    '''

def p_llamadaAuxiliar2(t):
  '''
  llamadaAuxiliar2 : exp
  | sp_cte agregarOperando
  '''

def p_llamadaAuxiliar3(t):
  '''
  llamadaAuxiliar3 : COMMA llamadaAuxiliar2 generarAccionParam llamadaAuxiliar3
  | empty
  '''
#

#     EXPRESION     ############################################################

def p_expresion(t):
  '''
  expresion : exp expresionAuxiliar1
  '''

def p_expresionAuxiliar1(t):
  '''
  expresionAuxiliar1 : expresionAuxiliar2 agregarOperador exp comprobarSemanticaOperadoresRelacionales expresionAuxiliar3
  | empty
  '''

def p_expresionAuxiliar2(t):
  '''
  expresionAuxiliar2 : N_EQUAL_OP
  | EQUAL_OP
  | BIGGER_THAN
  | LESS_THAN
  | BIGGER_EQUAL_THAN
  | LESS_EQUAL_THAN
  '''

  t[0] = t[1];

def p_expresionAuxiliar3(t):
    '''
    expresionAuxiliar3 : expresionAuxiliar4 agregarOperador expresion compSemYGenCuadYO
    | empty
    '''

def p_expresionAuxiliar4(t):
    '''
    expresionAuxiliar4 : operadorY
    | operadorO
    '''


#     FACTOR     ###############################################################


def p_factor(t):
  '''
  factor : L_PAREN  agregarPisoFalso expresion R_PAREN eliminarPisoFalso
  | factorAuxiliar1 factorAuxiliar3 factorAuxiliar4
  | factorAuxiliar3
  '''


def p_factorAuxiliar1(t):
  '''
  factorAuxiliar1 : PLUS_OP
  | MINUS_OP
  '''
  global signoActual;

  signoActual = t[1];

def p_factorAuxiliar2(t):
    '''
    factorAuxiliar2 : CTE_I
    | CTE_F
    '''
    global signoActual;
    global pilaOperandos;
    global pilaTipos;
    global alcanceActual;
    global indiceCTE;
    global tablaMemCte;
    global limMemCTE;



    if(t[1] in tablaMemCte):
        pilaOperandos.push(tablaMemCte[t[1]]);
    else:
        if(indiceCTE < limMemCTE):

            tablaMemCte[t[1]] = indiceCTE;
            pilaOperandos.push(indiceCTE);
            indiceCTE += 1;
        else:
            imprimirError(16, None);




    if(isinstance(t[1], float)):
        pilaTipos.push('float');
    else:
        pilaTipos.push('int');

    t[0] = t[1];

def p_factorAuxiliar3(t):
    '''
    factorAuxiliar3 : factorAuxiliar2
    | ID checarDefID agregarIdHaciaPilas
    | llamada
    | elemArr
    '''

def p_factorAuxiliar4(t):
    '''
    factorAuxiliar4 : empty
    '''
    global signoActual;
    global pilaOperandos;
    global pilaTipos;
    global alcanceActual;
    global traductorValoresCubo;
    global traductorIndicesOperandosCubo;
    global traductorIndicesOperadoresCubo;
    global cuboSemantico;
    global listaDeCuadruplos;
    global contadorCuadruplos;
    global indiceTemporal;
    global tablaMemCte;
    global indiceCTE;
    global limMemCTE;
    global liMemTemporal;
    if(signoActual != None and signoActual == "-"):
        signoActual = None;
        operandoDerecho = pilaOperandos.top();
        pilaOperandos.pop();


        tipoDerecho = pilaTipos.top();
        pilaTipos.pop();


        ind1 = traductorIndicesOperandosCubo["entero"];
        ind2 = traductorIndicesOperandosCubo[tipoDerecho];
        ind3 = traductorIndicesOperadoresCubo["*"]
        returnType = cuboSemantico[ind1][ind2][ind3];
        if(returnType != 0):
            if(indiceTemporal < limMemTemporal):
                if(-1  in tablaMemCte):
                    cuad = ["*",tablaMemCte[-1], operandoDerecho, indiceTemporal];
                else:
                    if(indiceCTE < limMemCTE):
                        cuad = ["*", indiceCTE, operandoDerecho, indiceTemporal];
                        tablaMemCte[-1] = indiceCTE;
                        indiceCTE += 1;
                    else:
                        imprimirError(16, None);


                pilaOperandos.push(indiceTemporal);
                pilaTipos.push(traductorValoresCubo[returnType]);
                listaDeCuadruplos.append(cuad);
                indiceTemporal += 1;
                contadorCuadruplos += 1;
            else:
                imprimirError(16,None);
        else:
            imprimirError(10, None);



#     LISTA CONSTANTE     ######################################################
def p_lista_cte(t):
  '''
  lista_cte : reiniciarContadorIndices L_BRACKETS  lista_cteAuxiliar1 comprobarTipoElem lista_cteAuxiliar2 R_BRACKETS p_sacarListaPilaOperandos
  '''
  t[0] = [];

def p_lista_cteAuxiliar1(t):
  '''
  lista_cteAuxiliar1 : exp
  | sp_cte agregarOperando
  '''

def p_lista_cteAuxiliar2(t):
  '''
  lista_cteAuxiliar2 : COMMA comprobarIndices lista_cteAuxiliar1 comprobarTipoElem lista_cteAuxiliar2
  | empty
  '''
def p_comprobarTipoElem(t):
    '''
    comprobarTipoElem : empty
    '''

    global pilaOperandos;
    global pilaTipos;
    global listaDeCuadruplos;
    global contadorIndice;
    global contadorCuadruplos;
    global traductorIndicesOperandosCubo;

    elem = pilaOperandos.top();
    pilaOperandos.pop();

    tipoElem = pilaTipos.top();
    pilaTipos.pop();

    lista = pilaOperandos.top();
    tipoLista = pilaTipos.top();

    temp = tipoLista.split();
    listaTipoTrad = traductorIndicesOperandosCubo[temp[1]];
    elemTipoTrad = traductorIndicesOperandosCubo[tipoElem];

    if(listaTipoTrad != elemTipoTrad):
        #No coinciden los tipos, ERROR!
        #print(str(temp) + " - " + str(tipoElem));
        imprimirError(10,None);
    else:
        #Coinciden los tipos
        #Agregar cuadruplo
        dir = lista + contadorIndice;
        cuad = ["=", elem, None, dir];
        listaDeCuadruplos.append(cuad);
        contadorIndice += 1;
        contadorCuadruplos += 1;

def p_comprobarIndices(t):
    '''
    comprobarIndices : empty
    '''
    global contadorIndice;
    global longLista;

    if(contadorIndice >= longLista):
        #print("Comprobando indices)
        imprimirError(13, None);
        #Error indice fuera de rango

def p_reiniciarContadorIndices(t):
    '''
    reiniciarContadorIndices : empty
    '''
    global contadorIndice;
    global pilaTipos;
    global idActual;
    global alcanceActual;
    global tablaDeSimbolos;
    global longLista;
    temp = pilaTipos.top();
    temp2 = temp.split();
    if(temp2[0] != "lista"):
        #error tipos no coinciden!
        imprimirError(10,None);
    else:
        contadorIndice = 0;






def p_sacarListaPilaOperandos(t):
    '''
    p_sacarListaPilaOperandos : empty
    '''
    global pilaOperandos;
    global pilaTipos;
    global pilaOperadores;

    pilaOperadores.pop();
    pilaOperandos.pop();
    pilaTipos.pop();

#     TIPO LISTA     ##########################################################

def p_tipo_lista(t):
  '''
  tipo_lista : LISTA listaVar tipo L_BRACKETS CTE_I R_BRACKETS
  '''
  global tipoActual;
  global longLista;

  tipoActual = "lista " + tipoActual
  longLista = t[5];


#     TIPO      ###############################################################
def p_tipo(t):
  '''
  tipo : ENTERO
  | FLOTANTE
  | BOOLEANO
  | TEXTO
  '''
  global tipoActual
  tipoActual = t[1];

#     COLOR CONSTANTE    #######################################################
def p_color_cte(t):
  '''
  color_cte : ROJO
  | VERDE
  | AZUL
  | AMARILLO
  | ROSA
  | VIOLETA
  '''
  t[0] = t[1]


#     CONSTANTE ESPECIAL     ###################################################
def p_sp_cte(t):
  '''
  sp_cte : CTE_STRING
  | cte_bool
  '''
  global valorActual;
  valorActual = t[1];
  """
  if(valorActual is not True and valorActual is not False):
      print();
      print("**************************");
      print(valorActual);
      print("**************************");
  """
  #print("t[1] = " + str(type(t[1])));
  t[0] = t[1];

#     CONSTANTE BOOLEANA     ###################################################
def p_cte_bool(t):
    '''
    cte_bool : VERDADERO
    | FALSO
    '''
    global valorActual;
    valorActual = t[1];

    if(t[1] == "verdadero"):
        t[0] = True;
    else:
        t[0] = False;

"""
#     CONSTANTE VARIABLES     ##################################################
def p_var_cte(t):
  '''
  var_cte : CTE_I
  | ID checarDefID
  | CTE_F
  | llamada
  '''
"""
#     PRODUCCIONES PARA LOS OPERADORES #########################################
"""
    + - * / && ||
"""

def p_operadorMas(t):
    '''
    operadorMas : PLUS_OP
    '''
    global operadorActual;
    operadorActual = t[1];
    t[0] = t[1];

def p_operadorMenos(t):
    '''
    operadorMenos : MINUS_OP
    '''
    global operadorActual;
    operadorActual = t[1];

    t[0] = t[1];

def p_operadorPor(t):
    '''
    operadorPor : TIMES_OP
    '''
    global operadorActual;
    operadorActual = t[1];

def p_operadorEntre(t):
    '''
    operadorEntre : DIV_OP
    '''
    global operadorActual;
    operadorActual = t[1];

def p_operadorY(t):
    '''
    operadorY : AND
    '''
    global operadorActual
    operadorActual = t[1]

def p_operadorO(t):
    '''
    operadorO : OR
    '''
    global operadorActual;
    operadorActual = t[1];

#     ERROR     ################################################################

def p_error(p):
    if p:
         print("Syntax error at token", p.type )
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")

#     VACIO     ################################################################
def p_empty(p):
    '''empty :'''
################################################################################
################################################################################

lexer = lex.lex();
parser = yacc.yacc();

if __name__ == '__main__':

    if (len(sys.argv) > 1):
        archivoParaLeer = sys.argv[1];

    archivo = open(archivoParaLeer, 'r');
    informacion = archivo.read();
    archivo.close();
    #lexer.input(informacion);

    parser.parse(informacion,);
    cont = 0
    for element in listaDeCuadruplos:
        print(str(cont) + " ", element);
        cont += 1;
    for key in tablaMemCte:
        print(str(key) +  " : " +str(tablaMemCte[key]));

    cuadsFile = open('cuad.o', 'w');
    for element in listaDeCuadruplos:
        cuadsFile.write(str(element[0]) + "," + str(element[1]) +"," + str(element[2]) + "," + str(element[3]) + "\n");

    cuadsFile.close();

    constFile = open('const.o', 'w');
    for key in tablaMemCte:
        constFile.write(str(key) + "\n");

    constFile.close();




    print("Parseo correcto");
