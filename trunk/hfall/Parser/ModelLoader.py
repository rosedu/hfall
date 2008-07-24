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

    def loadModel(self, filename):
        if not self.parser.parseFile(filename):
            return False
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
                    triangles = Mesh.Triangles([], self.materialMng.get(group.materialName), [])
                    for i in group.faces:
                        triangles.faces += m.data.faces.faces[i]
                        triangles.normals += 9*[0]
                    mesh.triangles.append(triangles)
            """to be deleted when we have normals"""
            number_of_vertices = len(mesh.vertices) / 3
            
            def get_normal(v, v1, v2):
                vv1 = v1[:]
                vv1[0] = vv1[0] - v[0]
                vv1[1] = vv1[1] - v[1]
                vv1[2] = vv1[2] - v[2]
                
                vv2 = v2[:]
                vv2[0] = vv2[0] - v[0]
                vv2[1] = vv2[1] - v[1]
                vv2[2] = vv2[2] - v[2]

                n = MathBase.cross_product(vv1,vv2)
                n = MathBase.normalize(n)

                return n
            
            for triangle in mesh.triangles:
                i = 0
                while i < len(triangle.faces):
                    v = mesh.vertices[3*triangle.faces[i]:3*(triangle.faces[i]+1)]
                    v1 = mesh.vertices[3*triangle.faces[i+1]:3*(triangle.faces[i+1]+1)]
                    v2 = mesh.vertices[3*triangle.faces[i+2]:3*(triangle.faces[i+2]+1)]
                    n = get_normal(v, v1, v2)
                    print n
                    print triangle.normals
                    triangle.normals[3*triangle.faces[i]] += n[0]
                    triangle.normals[3*triangle.faces[i]+1] += n[1]
                    triangle.normals[3*triangle.faces[i]+2] += n[2]
                    
                    v,v1,v2 = v1,v2,v
                    n = get_normal(v, v1, v2)
                    triangle.normals[3*triangle.faces[i+1]] += n[0]
                    triangle.normals[3*triangle.faces[i+1]+1] += n[1]
                    triangle.normals[3*triangle.faces[i+1]+2] += n[2]

                    v,v1,v2 = v1,v2,v
                    n = get_normal(v, v1, v2)
                    triangle.normals[3*triangle.faces[i+2]] += n[0]
                    triangle.normals[3*triangle.faces[i+2]+1] += n[1]
                    triangle.normals[3*triangle.faces[i+2]+2] += n[2]
                    
                    i = i + 3
                for i in range(number_of_vertices):
                    count = triangle.faces.count(i)
                    if count != 0:
                        triangle.normals[3*i] /= count
                        triangle.normals[3*i+1] /= count
                        triangle.normals[3*i+2] /= count
                        n = triangle.normals[3*i:3*(i+1)]
                        n = MathBase.normalize(n)
                        triangle.normals[3*i:3*(i+1)] = n
                #for i in range(number_of_vertices):    
            """---"""
            mesh.init()
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
