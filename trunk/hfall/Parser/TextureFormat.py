from switch import switch
from pyglet.gl import *

class Callable:
    def __init__(self, method):
        self.__call__ = method

class TextureFormat:
    def __init__(self):
        self.format = GL_RGB
        self.internalFormat = GL_RGB8
        self.dataFormat = GL_UNSIGNED_BYTE
        self.channels = 3

    def create(format, internal, data, channels):
        texFormat = TextureFormat()
        texFormat.format = format
        texFormat.internalFormat = internal
        texFormat.dataFormat = data
        texFormat.channels = channels
        return texFormat

    def toString(self):
        for case in switch(self.format):
            if case(GL_RGB): return "RGB"
            if case(GL_RGBA): return "RGBA"
            if case(GL_ALPHA): return "A"
            if case(GL_LUMINANCE): return "L"
            if case(GL_LUMINANCE_ALPHA): return "LA"

    def dataType(self):
        for case in switch(self.dataFormat):
            if case(GL_UNSIGNED_SHORT):
                return GLushort
            if case(GL_UNSIGNED_INT):
                return GLuint
            if case(GL_FLOAT):
                return GLfloat
            if case(GL_UNSIGNED_BYTE):
                return GLubyte
            if case(GL_BYTE):
                return GLbyte

    def fromString(string):
        for case in switch(string):
            if case("RGB"):
                return TextureFormat.create(GL_RGB, GL_RGB8, GL_UNSIGNED_BYTE, 3)
            if case("RGBA"):
                return TextureFormat.create(GL_RGBA, GL_RGBA8, GL_UNSIGNED_BYTE, 4)
            if case("A"):
                return TextureFormat.create(GL_ALPHA, GL_ALPHA8, GL_UNSIGNED_BYTE, 1)
            if case("L"):
                return TextureFormat.create(GL_LUMINANCE, GL_LUMINANCE8, GL_UNSIGNED_BYTE, 1)
            if case("LA"):
                return TextureFormat.create(GL_LUMINANCE_ALPHA, GL_LUMINANCE8_ALPHA8, GL_UNSIGNED_BYTE, 2)

    create = Callable(create)
    fromString = Callable(fromString)

            
