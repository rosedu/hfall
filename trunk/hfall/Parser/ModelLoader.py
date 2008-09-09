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
            geom = Mesh.Geometry([], [], [])
            objectMatrix = []
            triangles = []
            # get system coordinates
            mx = m.data.matrix
            for i in range(4):
                objectMatrix += [mx[3*i], mx[3*i + 1], mx[3*i + 2], 0]
            objectMatrix[15] = 1
            
            # get vertices & texCoordinates
            geom.vertices = m.data.vertices
            if m.data.coordinates:
                geom.texCoords = m.data.coordinates
                
            # get faces
            if m.data.faces:
                geom.faces = m.data.faces.faces
                for group in m.data.faces.materialGroups:
                    faces = []
                    for i in group.faces:
                        faces += m.data.faces.faces[i]
                    triangles.append(Mesh.Triangles(faces, self.materialMng.get(group.materialName)))
                    
            mesh = Mesh(objectMatrix, geom, triangles)
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
