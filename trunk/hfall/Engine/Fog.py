from pyglet.gl import *

class Fog():
    """
    For light effects.
    
    """
    def __init__(self):
        rFogMode = [ GL_EXP, GL_EXP2, GL_LINEAR ]
        rFogColor= [0.5, 0.5, 0.5, 1.0]
	self.FogFilter = 2
	self.FogMode = (GLuint * 3)(*rFogMode)
	self.FogColor = (GLfloat * 4)(*rFogColor)
        glFogi(GL_FOG_MODE, self.FogMode[self.FogFilter]);
        glFogfv(GL_FOG_COLOR, self.FogColor)
        glFogf(GL_FOG_DENSITY, 0.35)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogf(GL_FOG_START, 1.0)
        glFogf(GL_FOG_END, 5.0)

        
    """def FEnable():
    
        glEnable(GL_FOG)

    def FDisable():
    
        glDisable(GL_FOG)

    """
