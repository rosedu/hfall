from MaxParser import MaxParser
from Vertex import Vertex
from Mesh import Mesh
from Model import Model
from MeshMaterialGroup import MeshMaterialGroup

class ModelLoader:

    def __init__(self):
        self.parser = MaxParser()

    def loadModel(self, filename):
        if not self.parser.parseFile(filename):
            return False
        self.model = Model([], 16*[0])
        for m in self.parser.object.meshes:
            if m.type != 1:
                continue
            mesh = Mesh([], [], [], 16*[0])
            
            for i in range(0, 3):
                for j in range(0, 4):
                    mesh.matrix4[i*3+j] = m.data.matrix[i+j*3]
            
            for i in range(0, m.data.nrOfVertices):
                vertex = Vertex(m.data.vertices[i], m.data.coordinates[i])
                mesh.vertices.append(vertex)

            for face in m.data.faces.faces:
                mesh.faces.append(face)
            
            for group in m.data.faces.materialGroups:
                mat = MeshMaterialGroup(group.materialName, group.faces)
                mesh.materials.append(mat)
            self.model.meshes.append(mesh)
        return True
    
    def getModel(self):
        return self.model
