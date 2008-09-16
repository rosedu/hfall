from Texture import Texture
from Image import *

class TextureManager:

    def __init__(self):
        self.textures = {}
        self.images = {}

    def get(self, name):
        if name not in self.textures:
            return None
        texture = self.textures[name]
        if not texture.glID:
            return self.loadTexture(name, texture.target, texture.parameters, texture.settings)
        return texture

    def loadTexture(self, name, target, param = Texture.Parameters(), settings = Texture.Settings()):
        if name in self.textures:
            return self.textures[name]
        if name not in self.images:
            return None
        image = self.images[name]
        self.textures[name] = texture = Texture.create(name, image.data, image.width, image.height,
                                                       target, image.textureFormat, param, settings)
        return texture

    def loadImage(self, name, filepath, format = None):
        if name in self.images:
            return self.images[name]
        image = Image(filepath, format)
        if image.data:
            self.images[name] = image
            return image
        else: return None
        
    def add(self, name, image, texture):
        self.textures[name] = texture
        self.images[name] = image

    def deleteFromVRAM(self, name):
        if name in self.textures:
            if self.textures[name].glID:
                self.textures[name].delete()

    def deleteFromRAM(self, name):
        if name in self.images:
            del self.images[name]

    def delete(self, name):
        self.deleteFromVRAM(name)
        self.deleteFromRAM(name)

    def size(self):
        return len(self.textures)
    
