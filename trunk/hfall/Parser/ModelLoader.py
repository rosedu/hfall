import sys
sys.path.insert(0,"..")
import MathBase
from MaxParser import MaxParser
from Material import Material
from Mesh import Mesh
import Model
from Texture import Texture
from ModelManager import ModelManager
from MaterialManager import MaterialManager
from TextureManager import TextureManager

class ModelLoader:

    def __init__(self, modelMng, matMng, texMng):
        self.parser = MaxParser()
        self.modelMng = modelMng
        self.materialMng = matMng
        self.textureMng = texMng
        self.currentDir = "./"

    def loadModel(self, filename):
        if not self.parser.parseFile(filename):
            return False
        index = filename.rfind("/")
        if index > -1:
            self.currentDir = filename[0:index+1]
        self.modelName = filename
        self.saveMaterials()
        self.saveModel()
        return True

    def saveModel(self):
        self.model = Model.Model([], [1, 0, 0, 0] +
                               [0, 1, 0, 0] +
                               [0, 0, 1, 0] +
                               [0, 0, 0, 1], self.modelName)
        for m in self.parser.object.meshes:
            if m.type != 1:
                continue
            mesh = Mesh(16*[0], [])
            
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
                mesh.normals = MathBase.calculateNormals(m.data.vertices, m.data.faces.faces)
                for group in m.data.faces.materialGroups:
                    triangles = Mesh.Triangles([], self.materialMng.get(group.materialName))
                    for i in group.faces:
                        triangles.faces += m.data.faces.faces[i]
                    mesh.triangles.append(triangles)
            mesh.init()
            self.model.meshes.append(mesh)
        self.modelMng.add(self.model)

    def saveMaterials(self):
        _dir = self.currentDir
        for m in self.parser.object.materials:
            self.saveTextures(m)
            material = Material(m.name)
            material.ambient = m.ambientColor + [0]
            material.diffuse = m.diffuseColor + [0]
            material.specular = m.specularColor + [0]
            if m.textureMap1:
                material.texture = self.textureMng.get(_dir+m.textureMap1.name)
            if m.bumpMap:
                material.bump = self.textureMng.get(_dir+m.bumpMap.name)
            material.init()
            self.materialMng.add(material)

    def saveTextures(self, material):
        _dir = self.currentDir
        for tex in material.textures:
            texture = Texture(_dir + tex.name)
            #if material.bumpMap and texture.name == _dir+material.bumpMap.name:
            #    texture.normalMap = True
            self.textureMng.add(texture)
        
    def getModel(self):
        return self.model
