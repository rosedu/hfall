from pyglet.gl import *

class Light():
    """
    For light effects.
    
    """
    def __init__(self, lightSource, rLightAmbient,\
                 rLightDiffuse, rLightPosition):
        self.lightSource = lightSource
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
        #to be deleted later
        self.q = gluNewQuadric()

    def __del__(self):
        gluDeleteQuadric(self.q)
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.LightPosition[0],\
                     self.LightPosition[1],\
                     self.LightPosition[2])
        gluSphere(self.q, 1, 12, 12)
        glPopMatrix()
        #until here - replace in draw with pass
        
    def LEnable(self):
        glEnable(self.lightSource)

    def LDisable(self):
        glDisable(self.lightSource)

    def LPosition(self):
        glLightfv(self.lightSource, GL_POSITION, self.LightPosition)
