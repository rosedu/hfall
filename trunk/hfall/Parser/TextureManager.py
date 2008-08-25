from Texture import Texture

class TextureManager:

    def __init__(self):
        self.textures = {}

    def get(self, name):
        if not self.textures[name]:
            return self.loadFromFile(name)
        texture = self.textures[name]
        if not texture.inRAM:
            texture.loadImage()
        if not texture.inVRAM and texture.inRAM:
            texture.loadFromRam()
        if not texture.inVRAM:
            return None
        return texture

    def loadFromFile(self, name):
        texture = Texture(name)
        if texture.loadImage():
            return texture
        else: return None
        
    def add(self, texture):
        self.textures[texture.name] = texture

    def size(self):
        return len(self.textures)
    
