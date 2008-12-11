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
    def __init__(self, lightSource, rLightSpecular , rLightAmbient,\
                 rLightDiffuse, rLightPosition, ca = 1.0, la = 0.0, qa = 0.0):
        self.lightSource = lightSource
        self.modelView = Matrix4();
        self.modelView[0][3] = rLightPosition[0]
        self.modelView[1][3] = rLightPosition[1]
        self.modelView[2][3] = rLightPosition[2]
        self.modelView[0][0] = 1
        self.modelView[1][1] = 1
        self.modelView[2][2] = 1
        self.modelView[3][3] = 1
        self.type = "Light"
        self.name = "light" + str(lightSource - GL_LIGHT0)
	self.LightAmbient = (GLfloat * 4)(*rLightAmbient)
      	self.LightSpecular = (GLfloat * 4)(*rLightSpecular)
	self.LightDiffuse = (GLfloat * 4)(*rLightDiffuse)
	self.LightPosition = (GLfloat * 4)(*rLightPosition)
	self.constantAttenuation = (GLfloat)( ca)
        self.linearAttenuation = (GLfloat)( la)
        self.quadraticAttenuation = (GLfloat)( qa )
        glLightfv(self.lightSource, GL_AMBIENT, self.LightAmbient)
        glLightfv(self.lightSource, GL_DIFFUSE, self.LightDiffuse)
        glLightfv(self.lightSource, GL_SPECULAR, self.LightSpecular)
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)
        #to be deleted later
        self.q = gluNewQuadric()

    def __del__(self):
        gluDeleteQuadric(self.q)

    def enableAttenuation(self):
        glLightfv(self.lightSource, GL_CONSTANT_ATTENUATION, self.constantAttenuation)
        glLightfv(self.lightSource, GL_LINEAR_ATTENUATION, self.linearAttenuation)
        glLightfv(self.lightSource, GL_QUADRATIC_ATTENUATION, self.quadraticAttenuation)
        
    def draw(self):
        glPushMatrix()
        glColor3f(self.LightDiffuse[0], self.LightDiffuse[1], self.LightDiffuse[2])
        glMultMatrix(self.modelView)
        gluSphere(self.q, 1, 12, 12)
        glPopMatrix()
        #until here - replace in draw with pass
        
    def LEnable(self):

        self.LPosition()
        glEnable(self.lightSource)


    def LDisable(self):
        glDisable(self.lightSource)

    def LPosition(self):
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)

class Spotlight(Light):

    def __init__(self, lightSource, rLightSpecular, rLightAmbient,\
                 rLightDiffuse, rLightPosition):
        Light.__init__(self, lightSource, rLightSpecular, rLightAmbient,\
               rLightDiffuse, rLightPosition)
        self.type = "Spotlight"
	spot_direction = [-self.LightPosition[0], -self.LightPosition[1],\
                          -self.LightPosition[2]]
        # spot_direction = [-1, -1 ,0]
	self.spotDirection = (GLfloat * 3)(*spot_direction)
	glLightf(self.lightSource, GL_SPOT_CUTOFF, 45.0)
	glLightfv(self.lightSource, GL_SPOT_DIRECTION, self.spotDirection)
	glLightf(self.lightSource, GL_SPOT_EXPONENT, 0.0);

    def LPosition(self):
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)
        glLightfv(self.lightSource, GL_SPOT_DIRECTION, self.spotDirection)
        


