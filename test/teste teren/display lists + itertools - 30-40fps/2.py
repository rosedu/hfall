import pyglet
import array
import ctypes
import itertools
from pyglet import window
from pyglet import clock
from pyglet.gl import *

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4, 
                    depth_size=16, double_buffer=True,)
    w = window.Window(resizable=True, config=config, fullscreen=False)
except window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    w = window.Window(resizable=True, fullscreen=False)

zoom = -150
pressed = False
xrot = -80
zrot = 0
size = 128
width = 100

@w.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)

@w.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global zoom
    zoom -= scroll_y
    
@w.event
def on_mouse_press(x, y, button, modifiers):
    global pressed
    pressed = button == pyglet.window.mouse.LEFT
    
@w.event
def on_mouse_release(x, y, button, modifiers):
    global pressed
    pressed = not (button == pyglet.window.mouse.LEFT)
    
@w.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global xrot, zrot
    zrot -= dx * 0.3
    xrot += dy * 0.3

def setup():
    glClearColor(0.7, 0.7, 1.0, 1.0)
    glClearDepth(1.0)
    glClearStencil(0)
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
    ##loading terrain data
    global hmap
    hmap = size * size * [0]
    ##hmap[12] = 23
    ##hmap[23] = 34
    ##hmap[34] = -4

def drawterrain():
    vlen = float(width) / size
    vert = [array.array('f', itertools.repeat(0.0, size))
			for i in range(size)]
    vert[15][1] = 12
    vert[15][2] = 12
    vert[15][3] = 12
    vert[15][4] = 15
    vert[15][5] = 20
    vert[15][6] = 21
    vert[15][7] = 14
    vert[15][8] = 4
    vert[15][9] = -2
    vert[16][1] = 12 + 3
    vert[16][2] = 12 -2
    vert[16][3] = 12 +1
    vert[16][4] = 15 +0.5
    vert[16][5] = 20 +5
    vert[16][6] = 21 -23
    vert[16][7] = 14 -2
    vert[16][8] = 4 -1
    vert[16][9] = -2 +2
    glPushMatrix()
    glTranslatef(-width / 2, -width / 2, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.5, 0.5)
    for y in range(1, size):
	for x in range(1, size):
            glVertex3f(x * vlen, y * vlen, vert[x][y])
            glVertex3f((x-1) * vlen, (y-1) * vlen, vert[x-1][y-1])
            glVertex3f(x * vlen, (y-1) * vlen, vert[x][y-1])

            glVertex3f(x * vlen, y * vlen, vert[x][y])
            glVertex3f((x-1) * vlen, y * vlen, vert[x-1][y])
            glVertex3f((x-1) * vlen, (y-1) * vlen, vert[x-1][y-1])
    glEnd()
    glPopMatrix()

def tcompile():
    global list
    list = glGenLists(1)
    glNewList(list, GL_COMPILE)
    drawterrain()
    glEndList()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)	
    glLoadIdentity()
    glTranslatef(0.0, -2, zoom)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(zrot, 0, 0, 1)
    global list
    glCallList(list)

setup()
tcompile()
while not w.has_exit:
    dt = clock.tick()
    w.dispatch_events()
    draw()
    print clock.get_fps(),
    w.flip()
