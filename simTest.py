import os;
import sys;
import pymunk;
import time;
import pyglet;
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
