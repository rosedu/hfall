import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine/")

from pyglet.gl import *
from Object import *
from Matrix import *

class Camera(Object):
    """
    For Camera control.
    
    """
    def __init__(self, posx, posy, posz):
        self.modelView = Matrix4()
        self.position = Vector3(posx, posy, posz)
        self.modelView[0][3] = posx
        self.modelView[1][3] = -posy
        self.modelView[2][3] = posz
        self.modelView[0][0] = -1
        self.modelView[1][1] = 1
        self.modelView[2][2] = -1
        self.modelView[3][3] = 1
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrix(self.modelView)

    def translate(self, tranx, trany, tranz):
        self.position += Vector3(tranx, trany, tranz)
        m = Matrix4([1, 0, 0, -tranx, \
            			   0, 1, 0, -trany, \
        			   0, 0, 1, -tranz, \
        			   0, 0, 0, 1]);
        glMatrixMode(GL_MODELVIEW)
        self.modelView *= m;
        glLoadMatrix(self.modelView)
