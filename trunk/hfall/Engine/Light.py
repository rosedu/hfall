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

        
    def LEnable(self):
    
        glEnable(self.lightSource)

    def LDisable(self):
    
        glDisable(self.lightSource)
