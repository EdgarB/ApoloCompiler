#Librerias
import sys;
import os;
import pymunk;
import time;
import pyglet;
import math as math;
from classes.pila import Pila
from pymunk.pyglet_util import DrawOptions

#Arreglos que almacenan informacion
liMemGlobal = [];
liMemLocal = [];
liMemTemporal = [];
liMemCte = [];
liMemFig = [];

#Indices con la que comiienza la memoria virtual de cada lista
iComienzoMemGlobal = 1000;
iComienzoMemLocal = 21000;
iComienzoMemTemporal = 41000;
iComienzoMemCte = 61000;
iComienzoMemFig = 81000;

#Pilas para mantener estados de saltos (recursividad)
pilaEstadosCuad = Pila();
pilaMemoriaLocalLim = Pila();
pilaMemoriaTempLim = Pila();
liLocal = None;
liTemp = None;


#Arreglo con informacion de caudruplos
liCuadruplos = [];

#Apuntador para leer cuadruplos
iApuntadorCuads = 0;

#VAriables para pyglet y Pymunk
ventana = None;
espacio = None;



#Inicializando valores por defecto pygles y Pymunk
espacio = pymunk.Space();
espacio.gravity = 0,-1000;

#Funcion para encontrar si la variable es un string
def encontrarDobleEncomillado(line):
    cantidadDobleComillas = 0;
    for character in line:
        if character == '"':
            cantidadDobleComillas += 1;

    if cantidadDobleComillas == 2:
        return True;
    else:
        return False;
def encontrarPunto(linea):

    for c in linea:
        if c == '.':
            return True;

    return False;

#Leer archivo de cuadruplos y de constantes, guardarlos en sus arreglos
# correspondientes.
if __name__ == '__main__':
    colores = ["rojo", "verde", "azul", "amarillo", "rosa", "violeta"];
    tiposFigura = ["cuadrado", "triangulo", "circulo", "linea"];
    lenInp = len(sys.argv);
    if (lenInp > 1):
        archivoCuads = sys.argv[1];
        if(lenInp > 2):
            archivoCte = sys.argv[2];
        else:
            archivoCte = "const.o";
    else:
        archivoCuads = "cuad.o"
        archivoCte = "const.o"


    with open(archivoCuads) as f:
        for line in f:
            cuad = line.replace('\n','').split(",");
            liCuadruplos.append(cuad);
            #print(cuad);

    with open(archivoCte) as f:
        for line in f:

            line = line.replace('\n','');

            if line == "Verdadero" or line == "verdadero" or line == "True" or line == "true":
                line = True;
            elif line in colores or line in tiposFigura:
                line = line;
            elif line == "Falso" or line == "falso" or line == "False" or line == "false":
                line = False;
            elif encontrarDobleEncomillado(line) == True:
                line = line.replace('"','');
            elif encontrarPunto(line) == True:
                line = float(line);
            else:
                line = int(line);

            liMemCte.append(line);
            #print(line);


def getValor(iDirMem, topLocal = None, topTemp = None):

    global liMemGlobal;
    global liMemLocal;
    global liMemTemporal;
    global liMemCte;
    global liMemFig;

    global iComienzoMemGlobal;
    global iComienzoMemLocal;
    global iComienzoMemTemporal;
    global iComienzoMemCte;
    global iComienzoMemFig;
    global pilaMemoriaTempLim;
    global pilaMemoriaLocalLim;
    iDirMem = str(iDirMem);
    if(iDirMem[0]  == "("):
        limiteInd = len(iDirMem) - 1;
        iDirMem = getValor(iDirMem[1:limiteInd]);
    iDirMem = int(iDirMem);

    #Checar que no se None antes de hacer el return


    if(iDirMem < iComienzoMemLocal): #Global
        temporal = liMemGlobal[iDirMem - iComienzoMemGlobal];
        if temporal != None:
            return temporal;
        else:
            print("Error: Variable global no inicializada.");
            return None;
    elif(iDirMem < iComienzoMemTemporal): #Local
        if(topLocal == None):
            valPilaMemLocal = pilaMemoriaLocalLim.top();
        else:
            valPilaMemLocal = topLocal;

        if (valPilaMemLocal is None):
            temporal = liMemLocal[iDirMem - iComienzoMemLocal];
            if temporal != None:
                return temporal;
            else:
                print("Error: Variable local no inicializada.");
                return None;
        else:
            indTemp = valPilaMemLocal[0];

            #print(indTemp + iDirMem - iComienzoMemTemporal);
            temporal = liMemLocal[indTemp + (iDirMem - iComienzoMemLocal)];
            if temporal != None:
                return temporal;
            else:
                print("Error: Variable local no inicializada.");
                return None;

    elif(iDirMem < iComienzoMemCte): #Temporal
        if(topTemp == None):
            valPilaMemTemporal = pilaMemoriaTempLim.top();
        else:
            valPilaMemTemporal = topTemp;

        if (valPilaMemTemporal is None):
            temporal = liMemTemporal[iDirMem - iComienzoMemTemporal];
        
            if temporal != None:
                return temporal;
            else:
                #print(iDirMem);
                print("Error: Variable temporal no inicializada.");
                return None;
        else:
            indTemp = valPilaMemTemporal[0];

            temporal = liMemTemporal[indTemp + (iDirMem - iComienzoMemTemporal)];


            if temporal != None:
                return temporal;
            else:
                print("Error: Variable temporal no inicializada.");
                return None;

    elif(iDirMem < iComienzoMemFig): #Cte
        temporal = liMemCte[iDirMem - iComienzoMemCte];
        if temporal != None:
            return temporal;
        else:
            print("Error: Variable constante no inicializada.");
            return None;
    else: #Figura
        temporal = liMemFig[iDirMem - iComienzoMemFig];
        if temporal != None:
            return temporal;
        else:
            print("Error: Variable de figura no inicializada.");
            return None;

def setValor(iDirMem, valor, topLocal = None, topTemp = None):

    global liMemGlobal;
    global liMemLocal;
    global liMemTemporal;
    global liMemCte;
    global liMemFig;

    global iComienzoMemGlobal;
    global iComienzoMemLocal;
    global iComienzoMemTemporal;
    global iComienzoMemCte;
    global iComienzoMemFig;

    global pilaMemoriaTempLim;
    global pilaMemoriaLocalLim;

    iDirMem = str(iDirMem);
    if(iDirMem[0]  == "("):
        limiteInd = len(iDirMem) - 1;
        iDirMem = getValor(iDirMem[1:limiteInd]);
    iDirMem = int(iDirMem);

    if(iDirMem < iComienzoMemLocal): #Global
        iSize = len(liMemGlobal);
        if iSize < iDirMem + 1:
            while(iSize < iDirMem + 1):
                liMemGlobal.append(None);
                iSize += 1;
        liMemGlobal[iDirMem - iComienzoMemGlobal] = valor;
    elif(iDirMem < iComienzoMemTemporal): #Local
        if(topLocal == None):
            valPilaMemLocal = pilaMemoriaLocalLim.top();
        else:
            valPilaMemLocal = topLocal;

        if(valPilaMemLocal is None):
            iDirMem = (iDirMem - iComienzoMemLocal);
        else:
            iDirMem = valPilaMemLocal[0] + (iDirMem - iComienzoMemLocal);


        iSize = len(liMemLocal);
        if iSize <  iDirMem + 1:
            while(iSize < iDirMem + 1):
                liMemLocal.append(None);
                iSize += 1;

        liMemLocal[iDirMem] = valor;
    elif(iDirMem < iComienzoMemCte): #Temporal
        if(topTemp == None):
            valPilaMemTemporal = pilaMemoriaTempLim.top();
        else:
            valPilaMemTemporal = topTemp;

        if(valPilaMemTemporal is None):
            iDirMem = (iDirMem - iComienzoMemTemporal);
        else:
            iDirMem = valPilaMemTemporal[0] + (iDirMem - iComienzoMemTemporal);
        iSize = len(liMemTemporal);

        if iSize < iDirMem + 1:
            while(iSize < iDirMem + 1):
                liMemTemporal.append(None);
                iSize += 1;
        liMemTemporal[iDirMem] = valor;
    elif(iDirMem < iComienzoMemFig): #Cte
        iSize = len(liMemCte);
        if iSize < iDirMem:
            while(iSize < iDirMem):
                liMemCte.append(None);
                iSize += 1;
        liMemCte[iDirMem - iComienzoMemCte] = valor;
    else: #Figura
        iSize = len(liMemFig);
        if iSize < iDirMem + 1:
            while(iSize < iDirMem + 1):
                liMemFig.append(None);
                iSize += 1;
        liMemFig[iDirMem - iComienzoMemFig] = valor;

#Lector de caudruplos
tempCuad = liCuadruplos[0];
while tempCuad[0] != "END":

    #print("pila ", pilaMemoriaTempLim.items);
    #print("lista ", liMemTemporal);
    instruccion = tempCuad[0];
    #print(tempCuad);
    if(instruccion == "*"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la multiplicacion no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la multiplicacion no tiene un valor.")
            break;

        resultado = operando1 * operando2;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "+"):

        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la suma no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la suma no tiene un valor.")
            break;

        resultado = operando1 + operando2;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "-"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la resta no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la resta no tiene un valor.")
            break;

        resultado = operando1 - operando2;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "/"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la division no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la division no tiene un valor.")
            break;

        resultado = operando1 / operando2;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == ">"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la comparacion - mayor que - no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la comparacion - mayor que - no tiene un valor.")
            break;

        if operando1 > operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "<"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la comparacion - menor que - no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la comparacion - menor que - no tiene un valor.")
            break;

        if operando1 < operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);

        iApuntadorCuads += 1;
    elif(instruccion == "<="):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la comparacion - menor o igual que - no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la comparacion - menor o igual que - no tiene un valor.")
            break;

        if operando1 <= operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == ">="):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la comparacion - mayor o igual que - no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la comparacion - mayor o igual que - no tiene un valor.")
            break;

        if operando1 >= operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "=="):
        # BOOLEANO - BOOLEANO
        # FLOTANTE - FLOTANTE
        # FLOTANTE - ENTERO
        # ENTERO - FLOTANTE
        # ENTERO - ENTERO
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la igualacion no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la igualacion no tiene un valor.")
            break;

        if operando1 == operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "!="):
        # BOOLEANO - BOOLEANO
        # FLOTANTE - FLOTANTE
        # FLOTANTE - ENTERO
        # ENTERO - FLOTANTE
        # ENTERO - ENTERO
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la no equivalencia no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la no equivalencia no tiene un valor.")
            break;

        if operando1 != operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "&&"):

        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la operacion AND no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la operacion AND no tiene un valor.")
            break;

        if operando1 and operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;

    elif(instruccion == "||"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        operando2 = getValor(indOperando2);

        if operando1 == None or operando2 == None:
            if operando1 == None:
                print("Error: Operando izquierdo de la operacion OR no tiene un valor.")
            if operando2 == None:
                print("Error: Operando derecho de la operacion OR no tiene un valor.")
            break;

        if operando1 or operando2:
            resultado = True;
        else:
            resultado = False;

        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "+="):

        indOperando1 = tempCuad[1];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        resultado = getValor(indResultado);

        if operando1 == None:
            print("Error: Operando derecho del operador mas igual no tiene un valor.")
            break;
        if resultado == None:
            print("Error: Operando izquierdo del operador mas igual no tiene un valor.")
            break;

        resultado = resultado + operando1;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "-="):

        indOperando1 = tempCuad[1];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        resultado = getValor(indResultado);

        if operando1 == None:
            print("Error: Operando derecho del operador menos igual no tiene un valor.")
            break;

        resultado = resultado - operando1;
        setValor(indResultado, resultado);
        iApuntadorCuads += 1;
    elif(instruccion == "="):

        indOperando1 = tempCuad[1];

        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);

        if operando1 == None:
            print("Error: Operando derecho del operador asignacion no tiene un valor.")
            break;

        setValor(indResultado, operando1);
        iApuntadorCuads += 1;
    elif(instruccion == "pantalla"):

        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];

        operando1 = getValor(indOperando1);
        if operando1 == None:
            print("Error: Primer parametro de la funcion pantalla no tiene un valor.")
            break;

        operando2 = getValor(indOperando2);
        if operando2 == None:
            print("Error: Segundo parametro de la funcion pantalla no tiene un valor.")
            break;

        ventana = pyglet.window.Window(operando1,operando2, "Apolo", resizable=False);
        iApuntadorCuads += 1;
    elif(instruccion == "gravedad"):


        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];

        operando1 = getValor(indOperando1);
        if operando1 == None:
            print("Error: Primer parametro de la funcion gravedad no tiene un valor.")
            break;

        operando2 = getValor(indOperando2);
        if operando2 == None:
            print("Error: Segundo parametro de la funcion gravedad no tiene un valor.")
            break;

        espacio = pymunk.Space();
        espacio.gravity = operando1, operando2;
        iApuntadorCuads += 1;
    elif(instruccion == "cast"):
        indOperando1 = tempCuad[1];
        tipoCast = tempCuad[2];
        indResultado = tempCuad[3];

        operando1 = getValor(indOperando1);
        if operando1 == None:
            print("Debug error: Primer parametro de la instruccion cast no tiene un valor.")
            break;

        if(tipoCast == "int"):
            valor = int(operando1);
        elif(tipoCast == "float"):
            valor = float(operando1);

        setValor(indResultado, valor);
        iApuntadorCuads += 1;
    elif(instruccion == "era"):
        varLocales = int(tempCuad[2]);
        varTemps = int(tempCuad[3]);

        #print("lista Temporal ERA " ,liMemTemporal);
        cantVL = len(liMemLocal);
        cantVT = len(liMemTemporal);

        while(len(liMemLocal) < cantVL + varLocales):
            liMemLocal.append(None);

        while(len(liMemTemporal) < cantVT + varTemps):
            liMemTemporal.append(None);

        #print("Cant Temporal ERA " ,cantVT);
        liLocal = [cantVL, cantVL + varLocales];
        liTemp = [cantVT, cantVT + varTemps];
        iApuntadorCuads += 1;
    elif(instruccion == "ver"):
        indOperando1 = tempCuad[1];
        operando2 = int(tempCuad[2]);
        operando3 = int(tempCuad[3]);

        operando1 = getValor(indOperando1);
        if(operando1 == None):
            print("Error : indice del arreglo no tiene asignado un valor.");
            break;

        if(not (operando1 <= operando3 and operando2 <= operando1)):
            print("Error : indice del arreglo fuera del rango establecido.")
            break;





        iApuntadorCuads += 1;
    elif(instruccion == "param"):
        numeroParam = int(tempCuad[3]) - 1;
        indValorParam = tempCuad[1];

        valorParam = getValor(indValorParam);
        if valorParam == None:
            print("Debug error: parametro " + str(numeroParam + 1) + " de la instruccion param no tiene un valor.")
            print(tempCuad)
            print(numeroParam);
            print(indValorParam);
            break;
        #print(numeroParam + 21000 , "->", valorParam)
        setValor(str(numeroParam + 21000), valorParam,liLocal, liTemp);
        iApuntadorCuads += 1;
    elif(instruccion == "imprimir"):
        indOperando = tempCuad[1];
        valorOperando = getValor(indOperando);
        if(valorOperando == None):
            print("Debug error: Primer parametro de la instruccion imprimir no tiene un valor.")
            break;

        print(str(valorOperando));
        iApuntadorCuads += 1;
    elif(instruccion == "endproc"):
        #print("top temp lim" + str(pilaMemoriaTempLim.top()[0]))
        #print("Pila mem temporal top: " + str(pilaMemoriaTempLim.top()[0]));
        liMemTemporal = liMemTemporal[0 : pilaMemoriaTempLim.top()[0]];
        #print("Pila mem local top: " + str(pilaMemoriaLocalLim.top()[0]));
        liMemLocal = liMemLocal[0 : pilaMemoriaLocalLim.top()[0]];
        pilaMemoriaLocalLim.pop();
        pilaMemoriaTempLim.pop();
        iApuntadorCuads = pilaEstadosCuad.top();
        pilaEstadosCuad.pop();
    elif(instruccion == "goto"):
        Operando1 = tempCuad[3];
        iApuntadorCuads = int(Operando1);
    elif(instruccion == "gosub"):
        pilaMemoriaLocalLim.push(liLocal);
        pilaMemoriaTempLim.push(liTemp);
        operando = tempCuad[3];
        pilaEstadosCuad.push(iApuntadorCuads + 1);
        iApuntadorCuads = int(operando);
    elif(instruccion == "gotof"):
        indOperando = tempCuad[1];
        valOperando = getValor(indOperando);
        operandoSalto = int(tempCuad[3]);

        if valOperando == None:
            print("Debug error: Primer parametro de la instruccion gotof no tiene un valor.")
            break;

        if(valOperando is False):

            iApuntadorCuads = operandoSalto;
        else:

            iApuntadorCuads += 1;
    elif(instruccion == "dibujar"):
        dirBase = int(tempCuad[1]);
        indPosX = tempCuad[2];
        indPosY = tempCuad[3];

        valPosX = getValor(indPosX);
        if(valPosX == None):
            print("Debug error: Segundo parametro de la instruccion dibujar no tiene valor");
            break;

        valPosY = getValor(indPosY);
        if(valPosY == None):
            print("Debug error: Tercer parametro de la instruccion dibujar no tiene valor");
            break;

        #Tomar valores de la figura
        valTipo = getValor(dirBase);
        if(valTipo == None):
            print("Debug error: valTipo no tiene valor");
            break;

        valMedida = getValor(dirBase + 1);
        if(valMedida == None):
            print("Debug error: valMedida no tiene valor");
            break;
        valFriccion = getValor(dirBase + 2);
        if(valFriccion == None):
            print("Debug error: valFriccion no tiene valor");
            break;
        valMasa = getValor(dirBase + 3);
        if(valMasa == None):
            print("Debug error: valMasa no tiene valor");
            break;
        valRebote = getValor(dirBase + 4);
        if(valRebote == None):
            print("Debug error: valRebote no tiene valor");
            break;
        valMovible = getValor(dirBase + 5);
        if(valMovible == None):
            print("Debug error: valMovible no tiene valor");
            break;
        valColor = getValor(dirBase + 6);
        if(valColor == None):
            print("Debug error: valColor no tiene valor");
            break;

        if(valMovible):
            valMovible = pymunk.Body.DYNAMIC;
        else:
            valMovible = pymunk.Body.STATIC;
        #Crear figura y guardarla para su futuro despliegue
        if(valTipo == "cuadrado"):
            cajaForma = pymunk.Poly.create_box(None, size=(valMedida,valMedida));
            cajaMomento = pymunk.moment_for_poly(valMasa,cajaForma.get_vertices());
            cajaCuerpo = pymunk.Body(valMasa,cajaMomento, valMovible);
            if(valFriccion > 1):
                valFriccion = 1;
            cajaForma.friction = valFriccion;
            cajaCuerpo.position = valPosX, valPosY;
            cajaForma.body = cajaCuerpo

            espacio.add(cajaCuerpo, cajaForma);


        elif(valTipo == "triangulo"):
            #Generar vertices de acuerdo a lo ingresado por el usuario
            bT = math.sqrt((valMedida * valMedida) - ((valMedida * valMedida * valMedida * valMedida)/4));
            A = (valPosX - (valMedida/2), valPosY - (bT/2));
            B = (valPosX + (valMedida/2), valPosY - (bT/2));
            C = (valPosX, valPosY + (bT/2));

            trianguloForma = pymunk.Poly(None, A,B,C);

            trianguloMomento = pymunk.moment_for_poly(valMasa,trianguloForma.get_vertices());
            trianguloCuerpo = pymunk.Body(valMasa,trianguloMomento, valMovible);
            if(valFriccion > 1):
                valFriccion = 1.0;
            trianguloForma.friction = valFriccion; #Coeficiente de friccion de 0.0 a 1.0
            trianguloCuerpo.position = valPosX, valPosY;
            trianguloForma.body = trianguloCuerpo;

            espacio.add(trianguloCuerpo, trianguloForma);



        else: #circulo
            circuloMomento = pymunk.moment_for_circle(valMasa, 0, valMedida);
            circuloCuerpo = pymunk.Body(valMasa, circuloMomento);
            circuloCuerpo.position = valPosX, valPosY;
            circuloForma = pymunk.Circle(circuloCuerpo, valMedida);

            espacio.add(circuloCuerpo, circuloForma);

        iApuntadorCuads += 1;
    elif(instruccion == "dibujarLinea"):
        dirBase = int(tempCuad[1]);
        indPosX1 = tempCuad[2];
        indPosY1 = tempCuad[3];

        tempCuad = liCuadruplos[iApuntadorCuads + 1];
        indPosX2 = tempCuad[2];
        indPosY2 = tempCuad[3];

        valPosX1 = getValor(indPosX1);
        if(valPosX1 == None):
            print("Debug error: Segundo parametro de la instruccion dibujarLinea no tiene valor");
            break;

        valPosY1 = getValor(indPosY1);
        if(valPosY1 == None):
            print("Debug error: Tercer parametro de la instruccion dibujarLinea no tiene valor");
            break;

        valPosX2 = getValor(indPosX2);
        if(valPosX2 == None):
            print("Debug error: Cuarto parametro de la instruccion dibujarLinea no tiene valor");
            break;

        valPosY2 = getValor(indPosY2);
        if(valPosY2 == None):
            print("Debug error: Quinto parametro de la instruccion dibujarLinea no tiene valor");
            break;

        #Tomar valores de la figura
        valTipo = getValor(dirBase);
        if(valTipo == None):
            print("Debug error: valTipo no tiene valor");
            break;

        valMedida = getValor(dirBase + 1);
        if(valMedida == None):
            print("Debug error: valMedida no tiene valor");
            break;
        valFriccion = getValor(dirBase + 2);
        if(valFriccion == None):
            print("Debug error: valFriccion no tiene valor");
            break;
        valMasa = getValor(dirBase + 3);
        if(valMasa == None):
            print("Debug error: valMasa no tiene valor");
            break;
        valRebote = getValor(dirBase + 4);
        if(valRebote == None):
            print("Debug error: valRebote no tiene valor");
            break;
        valMovible = getValor(dirBase + 5);
        if(valMovible == None):
            print("Debug error: valMovible no tiene valor");
            break;
        valColor = getValor(dirBase + 6);
        if(valColor == None):
            print("Debug error: valColor no tiene valor");
            break;

        lineaMomento = pymunk.moment_for_segment(valMasa, (valPosX1, valPosY1), (valPosX2, valPosY2), 2);
        lineaCuerpo = pymunk.Body = pymunk.Body(valMasa, lineaMomento);
        lineaForma = pymunk.Segment(lineaCuerpo,(valPosX1, valPosY1), (valPosX2, valPosY2), 2);
        lineaCuerpo.position = valPosX, valPosY;

        espacio.add(lineaCuerpo, lineaForma);

        iApuntadorCuads += 2;


    tempCuad = liCuadruplos[iApuntadorCuads];

options = DrawOptions();
if(ventana != None):
    @ventana.event
    def on_draw():
        ventana.clear();
        espacio.debug_draw(options);

    def update(dt):
        espacio.step(dt)

if(ventana != None and tempCuad[0] == "END"):
    pyglet.clock.schedule_interval(update, 1.0/60);
    pyglet.app.run();
