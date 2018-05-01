import os;
import sys;
import pymunk;
import time;
import pyglet;
from math import sqrt;
from pymunk.pyglet_util import DrawOptions

window = pyglet.window.Window(1280,720, "Pymunk test", resizable=False);
options = DrawOptions()


space = pymunk.Space();
space.gravity = 0, -1000;
x = 25.0;
y = int(25.0);
poly = pymunk.Poly.create_box(None, size=(x,y));
poly.color = (0, 255, 0, 255);
moment = pymunk.moment_for_poly(10,poly.get_vertices())
print(moment)
body = pymunk.Body(1,moment, pymunk.Body.DYNAMIC);
poly.body = body
body.position = 640,700;

valMedida = 30;
valPosX = 100;
valPosY = 800;
valMasa = 5;
valMovible =  pymunk.Body.DYNAMIC;
valFriccion = 0.5;
valColor = "rojo";
bT = sqrt((valMedida * valMedida) - ((valMedida * valMedida)/4));
A = (valPosX - (valMedida/2), valPosY - (bT/2));
B = (valPosX + (valMedida/2), valPosY - (bT/2));
C = (valPosX, valPosY + (bT/2));
colores = {"rojo": (255, 117,117, 255), "verde":(117, 255, 151, 255), "azul" : (117,220, 255,255), "amarillo":(248,255,117,255), "rosa":(255,117,165,255), "violeta":(188,117,255,255)};
trianguloForma = pymunk.Poly(None, (A,B,C));

trianguloMomento = pymunk.moment_for_poly(valMasa,trianguloForma.get_vertices());
trianguloCuerpo = pymunk.Body(valMasa,trianguloMomento, valMovible);

trianguloForma.friction = valFriccion; #Coeficiente de friccion de 0.0 a 1.0
trianguloCuerpo.position = valPosX, valPosY;
trianguloForma.body = trianguloCuerpo;
trianguloForma.color = colores[valColor];

space.add(trianguloCuerpo, trianguloForma);

space.add(body, poly);
body = None;
poly = None;

@window.event
def on_draw():
    window.clear();
    space.debug_draw(options);

def update(dt):
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60);
    pyglet.app.run();
