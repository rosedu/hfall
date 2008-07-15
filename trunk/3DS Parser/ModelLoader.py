from MaxParser import MaxParser
from Material import Material
from Mesh import Mesh
from Model import Model
from Texture import Texture
from MeshMaterialGroup import MeshMaterialGroup
from ModelManager import ModelManager
from MaterialManager import MaterialManager
from TextureManager import TextureManager

class ModelLoader:

    def __init__(self, modelMng, matMng, texMng):
        self.parser = MaxParser()
        self.modelMng = modelMng
        self.materialMng = matMng
        self.textureMng = texMng

    def loadModel(self, filename):
        if not self.parser.parseFile(filename):
            return False
        self.modelName = filename
        self.saveMaterials()
        self.saveModel()
        return True

    def saveModel(self):
        self.model = Model([], [1, 0, 0, 0] +
                               [0, 1, 0, 0] +
                               [0, 0, 1, 0] +
                               [0, 0, 0, 1], self.modelName)
        for m in self.parser.object.meshes:
            if m.type != 1:
                continue
            mesh = Mesh([], None, None, 16*[0])
            
            # get system coordinates
            for i in range(0, 3):
                for j in range(0, 4):
                    mesh.matrix4[i*3+j] = m.data.matrix[i+j*3]
            # get vertices & texCoordinates
            for i in range(0, m.data.nrOfVertices):
                mesh.vertices += m.data.vertices[i]
                if m.data.coordinates:
                    if not mesh.texels:
                        mesh.texels = []
                    mesh.texels += m.data.coordinates[i]
            # get faces
            if m.data.faces:
                mesh.triangles = []
                for group in m.data.faces.materialGroups:
                    triangles = Mesh.Triangles([], self.materialMng.get(group.materialName))
                    for i in group.faces:
                        triangles.faces += m.data.faces.faces[i]
                    mesh.triangles.append(triangles)
            self.model.meshes.append(mesh)
        self.modelMng.add(self.model)

    def saveMaterials(self):
        for m in self.parser.object.materials:
            self.saveTextures(m)
            material = Material(m.name)
            if m.textureMap1:
                material.texture = self.textureMng.get(m.textureMap1.name)
            self.materialMng.add(material)

    def saveTextures(self, material):
        for tex in material.textures:
            texture = Texture(tex.name)
            self.textureMng.add(texture)
        
    def getModel(self):
        return self.model
