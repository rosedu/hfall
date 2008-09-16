from VertexBuffer import *
import pyglet
import array
import itertools
from pyglet.gl import *
from pyglet import window
from pyglet import clock

"""---window---"""
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

"""---globals--"""
zoom = -150
pressed = False
xrot = -80
zrot = 0
size = 128
width = 100

"""--other--"""
def setup():
    glClearColor(0.7, 0.7, 1.0, 1.0)
    glClearDepth(1.0)
    glClearStencil(0)
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    tsetup()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

def tsetup():
    global vlen
    vlen = 10 * (float(width) / size)
    vert = [array.array('f', itertools.repeat(0.0, size))
			for i in range(size)]
    vertices = [0, 0, vert[0][0]]
    colors = [1, 1, 1]
    indices = [0]
    index = 1
    for x in range(1, size):
        vertices.extend([x * vlen, 0, vert[x][0]])
        colors.extend([0.5, 0.5, 0.5])
        index = index + 1
    print "first row done", index
    for y in range(1, size):
        vertices.extend([0, y * vlen, vert[0][y]])
        colors.extend([0.5, 0.5, 0.5])
        index = index + 1
        for x in range(1, size):
            vertices.extend([x * vlen, y * vlen, vert[x][y]])
            colors.extend([0, 0, 0])
            indices.extend([index, index - size - 1, index - size,\
                            index, index - 1, index - size - 1])
            index = index + 1
    print "all done", index
    buffSize = (len(vertices) + len(colors)) * sizeof(GLfloat)
    buff = VertexBuffer(buffSize)
    global verts
    verts = VBOArray(len(vertices), GLfloat, vertices, buff)
    global cols
    cols = VBOArray(len(colors), GLfloat, colors, buff)
    buffSize = len(indices) * sizeof(GLuint)
    global fbuff
    fbuff = VertexBuffer(buffSize, target = VertexBuffer.ELEMENT_ARRAY_BUFFER)
    global vbo
    vbo = VBOArray(len(indices), GLuint, indices, fbuff)
    print "buffers created"

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)	
    glLoadIdentity()
    glTranslatef(0.0, -2, zoom)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(zrot, 0, 0, 1)
    tdraw()

def tdraw():
    verts.buffer.enable()
    glColorPointer(3, GL_FLOAT, 0, cols.pointer())
    glVertexPointer(3, GL_FLOAT, 0, verts.pointer())
    fbuff.enable()

    #glDrawRangeElements(GL_TRIANGLES, 0, size**2, size, GL_UNSIGNED_INT, vbo.pointer())
    glDrawElements(GL_TRIANGLES, size, GL_UNSIGNED_INT, vbo.pointer())
    
    verts.buffer.disable()
    fbuff.disable()

"""--main--"""
setup()
while not w.has_exit:
    dt = clock.tick()
    w.dispatch_events()
    draw()
    print clock.get_fps(),
    w.flip()
