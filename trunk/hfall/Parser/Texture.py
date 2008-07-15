from Image import Image
from pyglet.gl import *

class Texture:
    def __init__(self, name):
        self.name = name
        self.inRAM = False
        self.inVRAM = False

    def loadImage(self):
        self.image = Image(self.name)
        if not self.image:
            return False
        self.inRAM = True
        return True

    def loadFromRam(self):
        self.id = []
	self.id = (GLuint)(*self.id)
	glGenTextures(1, self.id)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT) 
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        pdata = (GLubyte * len(self.image.data))(*self.image.data)
        glTexImage2D(GL_TEXTURE_2D,0,4,self.image.width,self.image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,pdata)
        gluBuild2DMipmaps(GL_TEXTURE_2D,4,self.image.width,self.image.height,GL_RGBA,GL_UNSIGNED_BYTE,pdata)
        self.inVRAM = True
