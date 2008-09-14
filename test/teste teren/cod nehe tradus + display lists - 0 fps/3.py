import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet import clock

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4, 
                    depth_size=16, double_buffer=True,)
    w = window.Window(resizable=True, config=config, fullscreen=False)
except window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    w = window.Window(resizable=True, fullscreen=False)

@w.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)

# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)

hmap = None

m_size = 1024
s_size = 16

def setup():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 1)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
    ##loading terrain data
    global hmap
    hmap = m_size * m_size * [0]
    hmap[12] = 23
    hmap[23] = 34
    hmap[34] = -4

def H(x,y):
    x = x % m_size
    y = y % m_size
    return hmap[x + y * m_size]

def SetVertexColor(x, y):
    color = -.15 + H(x,y)/256.0
    glColor3f(0, 0, color)

def renderHM():
    X = Y = 0;
    glBegin(GL_QUADS)
    for X in range(m_size):
        for Y in range(m_size):
            x = X
            y = H(X, Y)
            z = Y
            SetVertexColor(x, z)
            glVertex3i(x, y, z)

            x = X
            y = H(X, Y + s_size)
            z = Y + s_size
            SetVertexColor(x, z)
            glVertex3i(x, y, z)

            x = X + s_size
            y = H(X + s_size, Y + s_size)
            z = Y + s_size
            SetVertexColor(x, z)
            glVertex3i(x, y, z)

            x = X + s_size
            y = H(X + s_size, Y)
            z = Y
            SetVertexColor(x, z)
            glVertex3i(x, y, z)
            
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(21, 16, 19, 0, 0, 0, 0, 1, 0)
    #glScalef()

    #renderHM()
    global list
    glCallList(list)

def tcompile():
    global list
    list= glGenLists(1)
    glNewList(list, GL_COMPILE)
    #drawterrain()
    renderHM()
    glEndList()

setup()
tcompile()
w.dispatch_events()
while not w.has_exit:
    dt = clock.tick()
    w.dispatch_events()
    draw()
    fps = clock.get_fps()
    print fps,
    w.flip()
