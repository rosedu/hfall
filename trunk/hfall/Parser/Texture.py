from Image import Image
from pyglet.gl import *
import os

class Texture:
    def __init__(self, name = None):
        self.name = name
        self.normalMap = False
        self.image = None
        self.inRAM = False
        self.inVRAM = False
	self.id = (GLuint)(*[])

    def loadImage(self):
        if os.path.exists(self.name):
            self.image = Image(self.name)
            if self.normalMap:
                self.image.computeNormalMap(scaleHeightByNz = True)
            self.image.convert("RGBA")
        else:
            print "Could not find ", self.name
        if not self.image:
            return False
        self.inRAM = True
        return True

    def loadFromRam(self):
	glGenTextures(1, self.id)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT) 
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)

        data = self.image.get_data()
        pdata = (GLubyte * len(data))(*data)
        glTexImage2D(GL_TEXTURE_2D,0,4,self.image.width,self.image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,pdata)
        gluBuild2DMipmaps(GL_TEXTURE_2D,4,self.image.width,self.image.height,GL_RGBA,GL_UNSIGNED_BYTE,pdata)
        self.inVRAM = True
