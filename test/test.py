import pyglet
from pyglet.gl import *
from pyglet import window

import numpy
import ctypes
from numpy import array

try:
    config = Config(sample_buffers = 1, samples = 4, depth_size = 16,\
                          double_buffer = True, fullscreen = False)
    w = window.Window(resizable = True, fullscreen = False, config=config)
except window.NoSuchConfigException:
    w = window.Window(resizable = True, fullscreen = False)

@w.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if height == 0:
        height = 1
    gluPerspective(60.0, width / float(height), .1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
        
# finalizing the initialization
glClearColor(0.0, 0.0, 0.0, 0.0)
glShadeModel(GL_SMOOTH)
glClearDepth(1.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_ARRAY)
#glEnable(GL_VERTEX_ARRAY)
glEnableClientState(GL_VERTEX_ARRAY)
glDepthFunc(GL_LEQUAL)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

points = [0,0,0, 1,0,0, 1,1,0, 0,1,0]
ppoints = (GLfloat * len(points))(*points)
colors = [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]
pcolors = (GLfloat * len(colors))(*colors)
#indices = array( range(len(points)), 'i')
#cindices = numpy.ascontiguousarray(indices)

while not w.has_exit:
    w.dispatch_events()
    w.clear()

    #OGL code
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 0, pcolors)
    glVertexPointer(3, GL_FLOAT, 0, ppoints)
    #print cpoints.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    #print cindices
    #glVertexPointer(4, GL_FLOAT, 0, points)
    #glVertexPointer(4, GL_FLOAT, 0, cpoints.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
    #glEnableClientState(GL_VERTEX_ARRAY);
    #glDrawElements(GL_QUADS, 4, GL_UNSIGNED_BYTE, cindices.ctypes.data_as(ctypes.POINTER(ctypes.c_int)))
    glDrawArrays(GL_QUADS, 0, len(ppoints))
    
    
    #end here
    
    w.flip()



