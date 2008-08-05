from Texture import Texture
from pyglet.gl import *

class Material:
    def __init__(self, name, ambient = [0.2,0.2,0.2,0.0], diffuse = [0.2,0.2,0.2,0.0], specular = [1.0,1.0,1.0,0.0], shininess = [1.0]):
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.texture = None

    def init(self):
        self.ambient = (GLfloat * len(self.ambient))(*self.ambient)
        self.diffuse = (GLfloat * len(self.diffuse))(*self.diffuse)
        self.specular = (GLfloat * len(self.specular))(*self.specular)
        self.shininess = (GLfloat * len(self.shininess))(*self.shininess)
