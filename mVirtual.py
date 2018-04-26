#Librerias
import sys;
import os;
import pymunk;
import time;
import pyglet;
from classes.pila import Pila

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

#Leer archivo de cuadruplos y de constantes, guardarlos en sus arreglos
# correspondientes.
if __name__ == '__main__':

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
            elif line == "Falso" or line == "falso" or line == "False" or line == "false":
                line = False;
            elif encontrarDobleEncomillado(line) == True:
                line = line.replace('"','');
            elif line.find(".") == 1:
                line = float(line);
            else:
                line = int(line);

            liMemCte.append(line);
            #print(line);


def getValor(iDirMem):

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
        valPilaMemLocal = pilaMemoriaLocalLim.top();
        if (valPilaMemLocal is None):
            temporal = liMemLocal[iDirMem - iComienzoMemLocal];
            if temporal != None:
                return temporal;
            else:
                print("Error: Variable local no inicializada.");
                return None;
        else:

            temporal = liMemLocal[valPilaMemLocal[0] + (iDirMem - iComienzoMemLocal)];
            if temporal != None:
                return temporal;
            else:
                print("Error: Variable local no inicializada.");
                return None;

    elif(iDirMem < iComienzoMemCte): #Temporal
        valPilaMemTemporal = pilaMemoriaTempLim.top();
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
            #print(indTemp);
            #print(iDirMem);
            #print(indTemp + (iDirMem - iComienzoMemTemporal))
            temporal = liMemTemporal[valPilaMemTemporal[0] + (iDirMem - iComienzoMemTemporal)];
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

def setValor(iDirMem, valor):

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

        valPilaMemLocal = pilaMemoriaLocalLim.top();
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
        valPilaMemTemporal = pilaMemoriaTempLim.top();
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

    instruccion = tempCuad[0];
    #print(instruccion);
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


        cantVL = len(liMemLocal);
        cantVT = len(liMemTemporal);

        pilaMemoriaLocalLim.push([cantVL, cantVL + varLocales]);
        pilaMemoriaTempLim.push([cantVT, cantVT + varTemps]);
        iApuntadorCuads += 1;
    elif(instruccion == "param"):
        numeroParam = int(tempCuad[3]) - 1;
        indValorParam = tempCuad[1];

        valorParam = getValor(indValorParam);
        if valorParam == None:
            print("Debug error: Primer parametro de la instruccion param no tiene un valor.")
            break;

        setValor(str(numeroParam + 21000), valorParam);
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
        liMemTemporal = liMemTemporal[0 : pilaMemoriaTempLim.top()[0]];
        liMemLocal = liMemLocal[0 : pilaMemoriaLocalLim.top()[0]];
        pilaMemoriaLocalLim.pop();
        pilaMemoriaTempLim.pop();
        iApuntadorCuads = pilaEstadosCuad.top();
        pilaEstadosCuad.pop();
    elif(instruccion == "goto"):
        Operando1 = tempCuad[3];
        iApuntadorCuads = int(Operando1);
    elif(instruccion == "gosub"):
        operando = tempCuad[3];
        pilaEstadosCuad.push(iApuntadorCuads + 1);
        iApuntadorCuads = int(operando);








    tempCuad = liCuadruplos[iApuntadorCuads];
