import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine/")

from pyglet.gl import *
from Object import *
from Matrix import *
from math import *

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

    def rotate(self, vx, vy, vz, angle):
        '''
        v = Vector3(vx, vy, vz)
        print v
        v.normalize()
        c = cos(angle)
        s = sin(angle)
        r = 12 * [0]
        r[0] = v.x*v.x*(1-c) + c
        r[1] = v.y*v.x*(1-c) + v.z*s
        r[2] = v.x*v.z*(1-c) - v.y*s
        r[3] = r[0] * self.position.x + r[1] * self.position.y + r[2]*self.position.z - self.position.x

        r[4] = v.x*v.y*(1-c) - v.z*s
        r[5] = v.y*v.y*(1-c) + c
        r[6] = v.y*v.z*(1-c) + v.x*s
        r[7] = r[4] * self.position.x + r[5] * self.position.y + r[6]*self.position.z - self.position.y

        r[8] = v.x*v.z*(1-c) + v.y*s
        r[9] = v.y*v.z*(1-c) - v.x*s
        r[10] = v.z*v.z*(1-c) + c
        r[11] = r[8] * self.position.x + r[9] * self.position.y + r[10]*self.position.z - self.position.z
        m = Matrix4([r[0], r[1], r[2],  r[3],  \
			   r[4], r[5], r[6],  r[7],  \
			   r[8], r[9], r[10], r[11], \
			   0,	 0,	   0,	  1]);
        self.modelView *= m;
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrix(self.modelView)
        '''
        glTranslatef(-self.position.x, -self.position.y,-self.position.z)
        glRotatef(angle, vx, vy, vz)
        glTranslatef(self.position.x, self.position.y, self.position.z)
        self.modelView = glGetMatrix(GL_MODELVIEW_MATRIX)

