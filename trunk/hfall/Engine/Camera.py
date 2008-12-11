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
        self.modelView[0][3] = -posx
        self.modelView[1][3] = -posy
        self.modelView[2][3] = posz
        self.modelView[0][0] = 1
        self.modelView[1][1] = 1
        self.modelView[2][2] = -1
        self.modelView[3][3] = 1
        self.enabled = False
        self.pitch = self.yaw = self.roll = 0;

    def enable(self):
        self.enabled = True
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrix(self.modelView)

    def disable(self):
        self.enabled = False

    def translate(self, tranx, trany, tranz):
       	self.modelView[0][3] -= tranx
       	self.modelView[1][3] -= trany
       	self.modelView[2][3] += tranz
	self.position.x = -self.modelView[0][0]*self.modelView[0][3] - self.modelView[1][0]*self.modelView[1][3] - self.modelView[2][0]*self.modelView[2][3]
	self.position.y = -self.modelView[0][1]*self.modelView[0][3] - self.modelView[1][1]*self.modelView[1][3] - self.modelView[2][1]*self.modelView[2][3]
	self.position.z = -self.modelView[0][2]*self.modelView[0][3] - self.modelView[1][2]*self.modelView[1][3] - self.modelView[2][2]*self.modelView[2][3]

        if (self.enabled):
            glMatrixMode(GL_MODELVIEW)
            glLoadMatrix(self.modelView)

    def rotate(self, vx, vy, vz, angle):
        self.yaw += vy*angle;
        self.roll += vz*angle;
        self.pitch += vx*angle;

        c1 = cos(self.pitch);
        s1 = sin(self.pitch);
        c2 = cos(-self.yaw);
        s2 = sin(-self.yaw);
        c3 = cos(self.roll);
        s3 = sin(self.roll);
                        
        X = Matrix4([1,  0,  0,  0, \
                    0,  c1, s1, 0, \
                    0, -s1, c1, 0, \
                    0,  0,  0,  1])
        Y = Matrix4([c2, 0, -s2, 0, \
                    0,  1,  0,  0, \
                    s2, 0,  c2, 0, \
                    0,  0,  0,  1])
        Z = Matrix4([c3, s3, 0, 0, \
                    -s3, c3, 0, 0, \
                    0,	0, 1, 0, \
                    0,	0, 0, 1])
        I = Matrix4 ([1, 0,  0, 0, \
                    0, 1,  0, 0, \
                    0, 0, -1, 0, 
                    0, 0,  0, 1])
                           
        self.modelView = X*Y*Z*I;

        self.modelView[0][3] = -self.position.x*self.modelView[0][0] - self.position.y*self.modelView[0][1] - self.position.z*self.modelView[0][2];
        self.modelView[1][3] = -self.position.x*self.modelView[1][0] - self.position.y*self.modelView[1][1] - self.position.z*self.modelView[1][2];
        self.modelView[2][3] = -self.position.x*self.modelView[2][0] - self.position.y*self.modelView[2][1] - self.position.z*self.modelView[2][2];

        if (self.enabled):
            glMatrixMode(GL_MODELVIEW)
            glLoadMatrix(self.modelView)

    def lookAt(self, vx, vy, vz):
        f = Vector3(vx,vy,vz) - self.position
        f.normalize()
        self.pitch = self.yaw = 0
        self.rotate(asin(f.y), atan2(f.x, f.z), 0, 1)
        if (self.enabled):
            glMatrixMode(GL_MODELVIEW)
            glLoadMatrix(self.modelView)
