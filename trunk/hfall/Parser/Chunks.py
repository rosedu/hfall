import _3DS

class ChunkHeader:
    pass
class TextureChunk:
    pass

class MaterialChunk:
    def __init__(self):
        self.textureMap1 = None
        self.bumpMap = None

class MaterialGroupChunk:
    pass

class FacesChunk:
    pass

class TextureInfoChunk:
    pass

class MeshData:
    def __init__(self, coordinates = None, faces = None):
        self.coordinates = coordinates
        self.faces = faces
    pass

class SpotLightChunk:
    pass

class LightChunk:
    pass

class CameraChunk:
    pass

class MeshChunk:
    pass

class ObjectChunk:
    pass

