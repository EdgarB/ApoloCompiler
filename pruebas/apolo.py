import sys
import os
import ply.yacc as yacc
import ply.lex as lex
from classes.tablaSimbolos import TablaSimbolos
from classes.tablaSimbolos import SimboloVariable
from classes.tablaSimbolos import SimboloFuncion
from classes.tablaSimbolos import SimboloFigura
##########################################################################################################
# Luis Alfonso Rojo Sanchez, A01113049
# Edgar Daniel Bustillos Rivera,A01113146
##########################################################################################################
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


#Funciones - Para checar si ya fueron declaradas previamente -> Redifinicion
def checarDefFunc():
  global tablaDeSimbolos
  global idActual
  return tablaDeSimbolos.existe(idActual);

def checarDefVar():
    global tablaDeSimbolos
    global alcanceActual
    global idActual
    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);

    return simboloFunc.tablaVariables.existe(idActual)

#Regresando si el parametro ya fue definido con anterioridad

# true -> Ya fue declarado
# false -> no ha sido declarado
def checarDefParamFunc():
    global tablaDeSimbolos
    global idActual
    global alcanceActual
    bRetorno = False
    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    if simboloFunc == None :
        #error
        print("")
    else:
        bRetorno = simboloFunc.parametros.__contains__(idActual);
    return bRetorno

def checarDefFigura():
    global tablaDeSimbolos
    global idActual
    return tablaDeSimbolos.obtener("_figuras").tablaVariables.existe(idActual)
##########################################################################################################
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
    'sino' : 'SI_NO',
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
    'falso' : 'FALSO'
    }

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
          'LESS_THAN'
] + list(reserved.values())
##########################################################################################################
##########################################################################################################
##########################################################################################################
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
t_PLUS_OP = r'\+'
t_MINUS_OP = r'\-'
t_TIMES_OP = r'\*'
t_DIV_OP = r'/'
t_N_EQUAL_OP = r'\!\='
t_EQUAL_OP = r'\=\='
t_PLUS_EQUAL_OP = r'\+\='
t_MINUS_EQUAL_OP = r'\-\='
t_ASSIGN_OP = r'\='
t_BIGGER_THAN = r'\>'
t_LESS_THAN = r'\<'

##########################################################################################################
##########################################################################################################
##########################################################################################################


def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    global idActual
    if t.value.lower() in reserved.keys():
        t.value = t.value.lower();
        t.type = reserved[t.value];
    else:

        idActual = t.value;

    return t;

def t_CTE_F(t):
    r'[0-9]+\.[0-9]'
    return t

def t_CTE_I(t):
    r'[0-9]+'
    return t

def t_CTE_STRING(t):
    r'\".*\"'
    return t

##########################################################################################################
##########################################################################################################
##########################################################################################################
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\v\f\r\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

##########################################################################################################
##########################################################################################################
##########################################################################################################
#GRAMATICAS LIBRES DE CONTEXTO

def p_programa(t):
    '''
    programa : PROGRAMA creaTablaFunc ID agregaGlobalTabla SEMICOLON variablesAuxiliar pantallaAuxiliar figurasAuxiliar gravedadAuxiliar funcionesAuxiliar apoloAuxiliar
    '''
    for x in tablaDeSimbolos.simbolos:
        print("***************************************************************")
        print(x)
        print("-")
        if(tablaDeSimbolos.simbolos[x].tablaVariables is not None):
            for y in tablaDeSimbolos.simbolos[x].tablaVariables.simbolos:
                tablaDeSimbolos.simbolos[x].tablaVariables.simbolos[y].imprimir()
                print("\n")
        print("-")
        for z in tablaDeSimbolos.simbolos[x].parametros:
            print(z)
        print("\n")
    print("***************************************************************")
    print("Programa aceptado!\n")

def p_listaVar(t):
    '''
    listaVar : empty
    '''
    global tipoActual
    tipoActual = "lista"

def p_apoloTablaFunc(t):
    '''
    apoloTablaFunc : empty
    '''
    global alcanceActual
    global tipoActual
    alcanceActual = "apolo"
    tipoActual = None


def p_creaTablaFunc(t):
  '''
    creaTablaFunc : empty
  '''
  global tablaDeSimbolos
  tablaDeSimbolos = TablaSimbolos(None, "_global");


def p_agregaGlobalTabla(t):
    '''
      agregaGlobalTabla : empty
    '''
    global idActual
    global nombrePrograma
    global tablaDeSimbolos
    global tipoActual

    nombrePrograma = idActual;

    tablaDeSimbolos.insertar(SimboloFuncion("global", tipoActual))


def p_asignarAlcance(t):
  '''
    asignarAlcance : empty
  '''
  global idActual
  global alcanceActual

  alcanceActual = idActual;

def p_creaTablaVar(t):
    '''
        creaTablaVar : empty
    '''
    global alcanceActual
    global simboloAlcance
    global tablaDeSimbolos

    simboloAlcance = tablaDeSimbolos.obtener(alcanceActual)
    if simboloAlcance == None :
        #Generar error funcion no existe
        print("Funcion " + idActual + " inexistente" )
    elif simboloAlcance.bCreaTabla : #Checa si esta siendo llamada y no siendo declarada la funcion
        simboloAlcance.tablaVariables = TablaSimbolos(alcanceActual,"vars")

def p_agregaVarTabla(t):
    '''
    agregaVarTabla : empty
    '''
    global tablaDeSimbolos
    global idActual
    global tipoActual
    global alcanceActual

    simboloFunc = tablaDeSimbolos.obtener(alcanceActual)
    if(simboloFunc == None):
        print("simboloFuncion " + alcanceActual + " no existe")#error esa funcion no existe
    elif(simboloFunc.bCreaTabla):
        tablaVars = simboloFunc.tablaVariables
        if(tablaVars != None): #Debe de existir, si no algo hicimos mal en el codigo
            if(checarDefVar()):
                print("Error: Variable " + idActual + " redefinida, cambiar nombre variable")#Ya esta definida la variable
            elif(checarDefParamFunc()):
                print("Error: Variable " + idActual + " redefinida en encabezado de los parametros, de la funcion " + alcanceActual )#Ya esta definida la variable
            else:
                tablaVars.insertar(SimboloVariable(idActual,tipoActual))
        else:
            print("Algo salio mal, checar que la regla para crear tabla de variables esta en las producciones correspondientes")


def p_agregaFuncTabla(t):
  '''
    agregaFuncTabla : empty
  '''
  global idActual
  global tipoActual
  tablaDeSimbolos.insertar(SimboloFuncion(idActual, tipoActual))

def p_agregaParamFunc(t):
    '''
    agregaParamFunc : empty
    '''
    global alcanceActual
    global idActual
    global tipoActual
    global tablaDeSimbolos

    simboloFunc = tablaDeSimbolos.obtener(alcanceActual);
    if(simboloFunc == None):
        print("")#Error funcion no existe
    elif(True is not checarDefParamFunc()):
        simboloFunc.parametros[idActual] = SimboloVariable(idActual, tipoActual)
    else:
        print("error: Redeficion de variable en " + alcanceActual + ", con la variable " + idActual)#error variable ya definida en parametros

def p_permiteCrearTablaVars(t):
    '''
    permiteCrearTablaVars : empty
    '''
    global alcanceActual
    global tablaDeSimbolos

    tablaDeSimbolos.obtener(alcanceActual).bCreaTabla = True

def p_denegaCrearTablaVars(t):
    '''
    denegaCrearTablaVars : empty
    '''
    global alcanceActual
    global tablaDeSimbolos

    tablaDeSimbolos.obtener(alcanceActual).bCreaTabla = False

def p_variablesAuxiliar(t):
  '''
  variablesAuxiliar : variables
  | empty
  '''

def p_pantallaAuxiliar(t):
  '''
  pantallaAuxiliar : pantalla
  | empty
  '''

def p_figurasAuxiliar(t):
  '''
  figurasAuxiliar : figuras
  | empty
  '''

def p_gravedadAuxiliar(t):
  '''
  gravedadAuxiliar : gravedad
  | empty
  '''
def p_funcionesAuxiliar(t):
    '''
    funcionesAuxiliar : funciones
    | empty
    '''

def p_apoloAuxiliar(t):
    '''
    apoloAuxiliar : APOLO apoloTablaFunc bloque
    '''

def p_variables(t):
  '''
  variables : VARIABLES creaTablaVar variablesAuxiliar1 ID agregaVarTabla variablesAuxiliar2 SEMICOLON variablesAuxiliar3
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

def p_retorno(t):
  '''
  retorno : REGRESAR retornoAuxiliar1 SEMICOLON
  '''

def p_retornoAuxiliar1(t):
  '''
  retornoAuxiliar1 : var_cte
  | sp_cte
  '''

def p_funciones(t):
  '''
  funciones : funcionesAuxiliar1 ID asignarAlcance agregaFuncTabla L_PAREN tipo ID agregaParamFunc funcionesAuxiliar2 R_PAREN L_BRACES  funcionesAuxiliar3 funcionesAuxiliar4  R_BRACES
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

def p_tipo(t):
  '''
  tipo : ENTERO
  | FLOTANTE
  | BOOLEANO
  | TEXTO
  '''
  global tipoActual
  tipoActual = t[1];

def p_tipo_lista(t):
  '''
  tipo_lista : LISTA listaVar tipo L_BRACKETS CTE_I R_BRACKETS
  '''
  global tipoActual
  tipoActual = "lista " + tipoActual

def p_estatuto(t):
  '''
  estatuto : asignacion SEMICOLON
  | condicion
  | escritura
  | ciclo
  | dibujar
  | llamada SEMICOLON
  | retorno
  | incremento SEMICOLON
  '''

def p_bloque(t):
  '''
  bloque : L_BRACES  bloqueAuxiliar1 R_BRACES
  '''


def p_bloqueAuxiliar1(t):
    '''
    bloqueAuxiliar1 : empty
    | estatuto bloqueAuxiliar1
    '''


def p_incremento(t):
  '''
  incremento : ID incrementoAuxiliar1 exp
  '''

def p_incrementoAuxiliar1(t):
  '''
  incrementoAuxiliar1 : PLUS_EQUAL_OP
  | MINUS_EQUAL_OP
  '''

def p_asignacion(t):
  '''
  asignacion : ID ASSIGN_OP asignacionAuxiliar1
  '''

def p_asignacionAuxiliar1(t):
  '''
  asignacionAuxiliar1 : expresion
  | lista_cte
  | sp_cte
  '''

def p_escritura(t):
  '''
  escritura : IMPRIMIR L_PAREN escrituraAuxiliar1 escrituraAuxiliar2 R_PAREN SEMICOLON
  '''

def p_escrituraAuxiliar1(t):
  '''
  escrituraAuxiliar1 : expresion
  | sp_cte
  '''

def p_escrituraAuxiliar2(t):
  '''
  escrituraAuxiliar2 : COMMA expresion escrituraAuxiliar2
  | COMMA sp_cte escrituraAuxiliar2
  | empty
  '''

def p_expresion(t):
  '''
  expresion : exp expresionAuxiliar1
  '''


def p_expresionAuxiliar1(t):
  '''
  expresionAuxiliar1 : expresionAuxiliar2 exp
  | empty
  '''

def p_expresionAuxiliar2(t):
  '''
  expresionAuxiliar2 : N_EQUAL_OP
  | EQUAL_OP
  | BIGGER_THAN
  | LESS_THAN
  '''

def p_ciclo(t):
  '''
  ciclo : CICLO L_PAREN asignacion SEMICOLON expresion SEMICOLON incremento R_PAREN bloque
  '''

def p_condicion(t):
  '''
  condicion : SI L_PAREN expresion R_PAREN bloque condicionAuxiliar1 SEMICOLON
  '''

def p_condicionAuxiliar1(t):
  '''
  condicionAuxiliar1 : SI_NO bloque
  | empty
  '''

def p_exp(t):
  '''
  exp : termino expAuxiliar1
  '''
def p_expAuxiliar1(t):
    '''
    expAuxiliar1 : MINUS_OP exp
    | PLUS_OP exp
    | empty
    '''
def p_termino(t):
  '''
  termino : factor terminoAuxiliar1
  '''

def p_terminoAuxiliar1(t):
    '''
    terminoAuxiliar1 : DIV_OP termino
    | TIMES_OP termino
    | empty
    '''

def p_factor(t):
  '''
  factor : L_PAREN expresion R_PAREN
  | factorAuxiliar1 var_cte
  '''


def p_factorAuxiliar1(t):
  '''
  factorAuxiliar1 : PLUS_OP
  | MINUS_OP
  | empty
  '''

def p_var_cte(t):
  '''
  var_cte : CTE_I
  | ID
  | CTE_F
  | lista_cte
  | llamada
  '''

def p_sp_cte(t):
  '''
  sp_cte : CTE_STRING
  | cte_bool
  '''
  t[0] = t[1]
def p_cte_bool(t):
    '''
    cte_bool : VERDADERO
    | FALSO
    '''
    t[0] = t[1]
def p_figuras(t):
  '''
  figuras : FIGURAS creaFigFuncSimb asignarAlcance figura ID checarFiguraId L_BRACES figura_atributos figura_atributosAuxiliar2 R_BRACES creaFigVar figurasAuxiliar1 SEMICOLON
  '''
def p_creaFigFuncSimb(t):
  '''
    creaFigFuncSimb : empty
  '''
  global tablaDeSimbolos
  global idActual
  idActual = "_figuras"
  tablaDeSimbolos.insertar(SimboloFuncion("_figuras", None))
  tablaDeSimbolos.obtener("_figuras").tablaVariables = TablaSimbolos(None, "vars")
def p_checarFiguraId(t):
    '''
    checarFiguraId : empty
    '''
    global idActual
    global tablaDeSimbolos
    if(checarDefFigura()):
        print("error: Redeficion de la figura " + idActual)
def p_creaFigVar(t):
  '''
  creaFigVar : empty
  '''
  global tablaDeSimbolos
  global idActual
  global medidaFigActual
  global friccionFigActual
  global masaFigActual
  global reboteFigActual
  global movibleFigActual
  global colorFigActual

  if(not checarDefFigura()):
      figura = SimboloFigura(idActual, tipoActual, medidaFigActual, friccionFigActual, masaFigActual, reboteFigActual, movibleFigActual, colorFigActual)
      varsFigTabla = tablaDeSimbolos.obtener("_figuras").tablaVariables.insertar(figura)

  medidaFigActual = None;
  friccionFigActual = None;
  masaFigActual = None;
  reboteFigActual = None;
  movibleFigActual = None;
  colorFigActual = None;

def p_figurasAuxiliar1(t):
  '''
  figurasAuxiliar1 : COMMA figura ID checarFiguraId L_BRACES figura_atributos figura_atributosAuxiliar2 R_BRACES creaFigVar figurasAuxiliar1
  | empty
  '''

def p_dibujar(t):
  '''
  dibujar : dibujarAuxiliar1 COMMA exp COMMA exp R_PAREN SEMICOLON
  '''

def p_dibujarAuxiliar1(t):
  '''
  dibujarAuxiliar1 : DIBUJAR L_PAREN ID
  | DIBUJAR_LINEA L_PAREN ID COMMA exp COMMA exp
  '''

def p_gravedad(t):
  '''
  gravedad : GRAVEDAD L_PAREN exp COMMA exp R_PAREN SEMICOLON
  '''

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
            print("Atributo repetido")
    elif(t[1] == 'friccion'):
        if(friccionFigActual ==  None):
            friccionFigActual = t[3]
        else:
            #Crashealo
            print("Atributo repetido")
    elif(t[1] == 'masa'):
        if(masaFigActual == None):
            masaFigActual = t[3]
        else:
            #Crashealo
            print("Atributo repetido")
    elif(t[1] == 'rebote'):
        if(reboteFigActual == None):
            reboteFigActual = t[3]
        else:
            #Crashealo
            print("Atributo repetido")
    elif(t[1] == 'movible'):
        if(movibleFigActual == None):
            movibleFigActual = t[3]
        else:
            #Crashealo
            print("Atributo repetido")
    elif(t[1] == 'color'):
        if(colorFigActual == None):
            colorFigActual = t[3]
        else:
            #Crashealo
            print("Atributo repetido")
    else:
        print("Atributo inexistente")


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

def p_figura(t):
  '''
  figura : CUADRADO
  | CIRCULO
  | TRIANGULO
  | LINEA
  '''
  global tipoActual
  tipoActual = t[1]

  t[0] = t[1]

def p_pantalla(t):
  '''
  pantalla : PANTALLA L_PAREN CTE_I COMMA CTE_I R_PAREN SEMICOLON
  '''

def p_llamada(t):
  '''
  llamada : ID L_PAREN llamadaAuxiliar1 R_PAREN
  '''

def p_llamadaAuxiliar1(t):
    '''
    llamadaAuxiliar1 : llamadaAuxiliar2 llamadaAuxiliar3
    | empty
    '''

def p_llamadaAuxiliar2(t):
  '''
  llamadaAuxiliar2 : ID
  | exp
  | sp_cte
  '''

def p_llamadaAuxiliar3(t):
  '''
  llamadaAuxiliar3 : COMMA llamadaAuxiliar2 llamadaAuxiliar3
  | empty
  '''

def p_lista_cte(t):
  '''
  lista_cte : L_BRACKETS lista_cteAuxiliar1 lista_cteAuxiliar2 R_BRACKETS
  '''

def p_lista_cteAuxiliar1(t):
  '''
  lista_cteAuxiliar1 : exp
  | sp_cte
  '''

def p_lista_cteAuxiliar2(t):
  '''
  lista_cteAuxiliar2 : COMMA lista_cteAuxiliar1 lista_cteAuxiliar2
  | empty
  '''

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

def p_empty(p):
    '''empty :'''

##########################################################################################################
##########################################################################################################
##########################################################################################################

def p_error(p):
    if p:
         print("Syntax error at token", p.type )
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")

# Build the lexer
lexer = lex.lex()

#Build the parser
parser = yacc.yacc()

# Test it out
data = '''
programa prueba;

variables entero i, b;
flotante z;
lista entero[10] d;
texto b;

pantalla(800,800);

figuras
    cuadrado miCaja{
      medida : 10,
      friccion: 0.5,
      masa: 10.0,
      rebote: 0.4,
      movible: falso,
      color : amarillo
    },
    triangulo miCaja{
        friccion: 0.5,
        masa: 10.0,
        rebote: 0.4,
        movible: falso
    };

gravedad(10,10);

entero assd(entero i, flotante j){
    variables
        entero iS;
        lista texto[10] i;

    asd = [10,10,10,10,10];
    asd = verdadero;
    asd = "asdasd";
    asd += 10;
    asd -= 5;
    asd = 10 < 20;
    si(10 < 20){
        imprimir("asdasd");
    }siNo{
    imprimir("asdasd");
    imprimir("asdasd");
    };
    asd = asd(10,10);
    asd();
}

apolo{


    asd = [10,10,10,10,10];
    asd = verdadero;
    asd = "asdasd";
    asd += 10;
    asd -= 5;
    asd = 10 < 20;
    si(10 < 20){
        imprimir("asdasd");
        si(10 < 20){
            imprimir("asdasd");
            si(10 < 20){
                imprimir("asdasd");
            }siNo{
                imprimir("asdasd");
                imprimir("asdasd");
                asd = [10,10,10,10,10];
                asd = verdadero;
                asd = "asdasd";
                asd += 10;
                asd -= 5;
                asd = 10 < 20;
            };
        }siNo{
            imprimir("asdasd");
            imprimir("asdasd");
            asd = [10,10,10,10,10];
            asd = verdadero;
            asd = "asdasd";
            asd += 10;
            asd -= 5;
            asd = 10 < 20;
            si(10*121 < 20-0.0){
                imprimir("asdasd");
            }siNo{
                imprimir("asdasd");
                imprimir("asdasd");
                asd = [10,10,10,10,10];
                asd = verdadero;
                asd = "asdasd";
                asd += 10;
                asd -= 5;
                asd = 10 < 20;
            };
        };
    }siNo{
        imprimir("asdasd");
        imprimir("asdasd");
        asd = [10,10,10,10,10];
        asd = verdadero;
        asd = "asdasd";
        asd += 10;
        asd -= 5;
        asd = 10 < 20;
    };
    asd = asd(10,10);
    asd();
    dibujar(asd, 1,2);
    dibujarLinea(asd,-1.0,-2,+3,4);
  }

'''

# Give the parser some input
parser.parse(data)

#lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
