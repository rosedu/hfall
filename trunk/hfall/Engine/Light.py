import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine/")

from pyglet.gl import *
from Object import *
from Matrix import *

class Light(Object):
    """
    For light effects.
    
    """
    def __init__(self, lightSource, rLightAmbient,\
                 rLightDiffuse, rLightPosition):
        self.lightSource = lightSource
        self.modelView = Matrix4();
        self.modelView[0][3] = rLightPosition[0]
        self.modelView[1][3] = rLightPosition[1]
        self.modelView[2][3] = rLightPosition[2]
        self.modelView[0][0] = 1;
        self.modelView[1][1] = 1;
        self.modelView[2][2] = 1;
        self.modelView[3][3] = 1;
	self.LightAmbient = (GLfloat * 4)(*rLightAmbient)
	self.LightDiffuse = (GLfloat * 4)(*rLightDiffuse)
	self.LightPosition = (GLfloat * 4)(*rLightPosition)
        glLightfv(self.lightSource, GL_AMBIENT, self.LightAmbient)
        glLightfv(self.lightSource, GL_DIFFUSE, self.LightDiffuse)
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)
	spot_direction = [- self.LightPosition[0], - self.LightPosition[1],\
                          - self.LightPosition[2], 0.0]
	self.spotDirection = (GLfloat * 4)(*spot_direction)
	glLightf(self.lightSource, GL_SPOT_CUTOFF, 45.0)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, self.spotDirection)
	print(self.modelView);
        #to be deleted later
        self.q = gluNewQuadric()

    def __del__(self):
        gluDeleteQuadric(self.q)
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.LightPosition[0] / self.LightPosition[3],\
                     self.LightPosition[1] / self.LightPosition[3],\
                     self.LightPosition[2] / self.LightPosition[3])
        gluSphere(self.q, 1, 12, 12)
        glPopMatrix()
        #until here - replace in draw with pass
        
    def LEnable(self):
        glEnable(self.lightSource)

    def LDisable(self):
        glDisable(self.lightSource)

    def LPosition(self):
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)
