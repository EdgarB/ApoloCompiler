import sys;
import os;
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

#Arreglo con informacion de caudruplos
liCuadruplos = []

#Apuntador para leer cuadruplos
iApuntadorCuads = 0;

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
            print(cuad);

    with open(archivoCte) as f:
        for line in f:
            liMemCte.append(line);
            print(line);


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

    if(iDirMem < iComienzoMemLocal): #Global
        return liMemGlobal[iDirMem - iComienzoMemGlobal];
    elif(iDirMem < iComienzoMemTemporal): #Local
        return liMemLocal[iDirMem - iComienzoMemLocal];
    elif(iDirMem < iComienzoMemCte): #Temporal
        return liMemTemporal[iDirMem - iComienzoMemTemporal];
    elif(iDirMem < iComienzoMemFig): #Cte
        return liMemCte[iDirMem - iComienzoMemCte];
    else: #Figura
        return liMemFig[iDirMem - iComienzoMemFig];

def setValor(iDirMemoria, valor):
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

    if(iDirMem < iComienzoMemLocal): #Global
        liMemGlobal[iDirMem - iComienzoMemGlobal] = valor;
    elif(iDirMem < iComienzoMemTemporal): #Local
        liMemLocal[iDirMem - iComienzoMemLocal] = valor;
    elif(iDirMem < iComienzoMemCte): #Temporal
        liMemTemporal[iDirMem - iComienzoMemTemporal] = valor;
    elif(iDirMem < iComienzoMemFig): #Cte
        liMemCte[iDirMem - iComienzoMemCte] = valor;
    else: #Figura
        liMemFig[iDirMem - iComienzoMemFig] = valor;

#Lector de caudruplos
tempCuad = liCuadruplos[0];
while tempCuad[0] != "END":
    instruccion = tempCuad[0];
    if(instruccion == "*"):
        indOperando1 = tempCuad[1];
        indOperando2 = tempCuad[2];
        indResultado = tempCuad[3];
        """
            #Obtener si los numeros son int o float y convertilos
            operando1 = getValor(indOperando1);
            operando2 = getValor(indOperando2);
            resultado = operando1 * operando2;
            setValor(indResultado, resultado);
        """


    elif(instruccion == "+"):

    elif(instruccion == "-"):

    elif(instruccion == "/"):

    """
        >
        <
        <=
        >=
        ==
        !=
        &&
        ||
        =
        +=
        -=
    """

    iApuntadorCuads += 1;
    tempCuad = liCuadruplos[iApuntadorCuads];
