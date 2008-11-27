import sys
sys.path.insert(0, "../Engine")
sys.path.insert(0, "..")

from Vector import Vector3
from Matrix import Matrix4
from math import *
from pyglet.gl import *
from glcalls import *

def invMatrix(m):
    inv = Matrix4()
    inv[0][0] = m[0][0]
    inv[0][1] = m[1][0]
    inv[0][2] = m[2][0]
    inv[1][0] = m[0][1]
    inv[1][1] = m[1][1]
    inv[1][2] = m[2][1]
    inv[2][0] = m[0][2]
    inv[2][1] = m[1][2]
    inv[2][2] = m[2][2]
    
    inv[0][3] = -m[0][0]*m[0][3] - m[0][1]*m[1][3] - m[0][2]*m[2][3]
    inv[1][3] = -m[1][0]*m[0][3] - m[1][1]*m[1][3] - m[1][2]*m[2][3]
    inv[2][3] = -m[2][0]*m[0][3] - m[2][1]*m[1][3] - m[2][2]*m[2][3]

class Object:

    def __init__(self, _type, _name):
        self.modelView = Matrix4.identity()
        self.projection = Matrix4.identity()
        self.type = _type
        self.name = _name
        """
        what type of object this is : model, camera, light source
        """
    def setModelView(self):
        glLoadMatrix(self.modelView)

    def setProjectio(self):
        glMatrixMode(GL_PROJECTION)
        glLoadMatrix(self.projection)
        glMatrixMode(GL_MODELVIEW)

    def multModelView(self):
        glMultMatrix(self.modelView)

    def getInvModelView(self):
        return invMatrix(modelview)

    def getInvProjection(self):
        return invMatrix(projection)

    def scale(self, vector):
        x = vector[0]
	y = vector[1]
	z = vector[2]
        m = Matrix4([x, 0, 0, 0,
                    0, y, 0, 0,
		    0, 0, z, 0,
		    0, 0, 0, 1])
			   
	self.modelView *= m

    def translate(self, x, y, z):
        m = Matrix4([1, 0, 0, x,
		    0, 1, 0, y,
		    0, 0, 1, z,
		    0, 0, 0, 1])
			   
	self.modelView *= m

    def rotate(self, vector, angle):
        x = vector[0]
	y = vector[1]
	z = vector[2]
	c = cos(angle)
	s = sin(angle)
	
        m = Matrix4([x*x*(1-c)+c,    y*x*(1-c)+z*s, x*z*(1-c)-y*s, 0,
                     x*y*(1-c)-z*s,  y*y*(1-c)+c,   y*z*(1-c)+x*s, 0,
		     x*z*(1-c)+y*s,  y*z*(1-c)-x*s, z*z*(1-c)+c,   0,
		     0,		     0,		    0,		   1])
			   
	self.modelView *= m

    def lookAt(self, target, up):
        f = target
        f.normalize()
	_up = up
	_up.normalize()
	s = f.crossProduct(_up)
	u = s.crossProduct(f)
	
	m = Matrix4([s[0], u[0], -f[0], 0,
		     s[1], u[1], -f[1], 0,
		     s[2], u[2], -f[2], 0,
		     0,	   0,	  0,    1])
			   
	self.projection *= m

	
