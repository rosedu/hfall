import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
from OGLbase import OGL as RenderDevice
from VertexBuffer import *
from pyglet.gl import *
import MathBase

class Mesh:

    class Triangles:
    
        def __init__(self, faces, material):
            self.start = min(faces)
            self.end = max(faces)
            self.material = material
            self.faces = faces
            self.size = len(faces)

    class Geometry:
        
        def __init__(self, vertices, texCoords, faces, tangents = None,
                     binormal = None, normals = None):
            
            self.vertices = vertices
            self.texCoords = texCoords
            self.faces = faces
            self.tangents = None
            self.binormals = None
            self.normals = None

        def computeTangentSpace(self):
            if not self.faces:
                return
            tbn = MathBase.computeTangentSpace(self.vertices, self.texCoords, self.faces)
            self.tangents = tbn[0]
            self.binormals = tbn[1]
            self.normals = tbn[2]

        def toList(self, data):
            p = []
            if(data):
                for i in range(len(data)):
                    p.extend(data[i])
            return p
            

    
    def __init__(self, matrix, geometry, triangles, draw_mode = GL_TRIANGLES):

        self.vertices = None
        self.normals = None
        self.texCoords = None
        self.colors = None
        self.facesBuffer = None
        self.triangles = triangles
        self.matrix4 = matrix
        self.mode = draw_mode
        self.geometry = geometry
        self.name = "None"

    def init(self):
        self.geometry.computeTangentSpace()
        vertices = self.geometry.toList(self.geometry.vertices)
        texCoords = self.geometry.toList(self.geometry.texCoords)
        normals = self.geometry.toList(self.geometry.normals)
        colors = (len(vertices))*[1, 1, 1]
        self.matrix4 = (GLfloat *len(self.matrix4))(*self.matrix4)
        triSize = len(self.geometry.faces)*3
        self.createBuffers(vertices, texCoords, normals, colors, self.triangles, triSize)

    def createBuffers(self, vertices, texCoords, normals, colors, triangles, triSize):
        buffSize = (len(vertices) + len(normals) + len(texCoords) + len(colors)) * sizeof(GLfloat)
        vertBuff = VertexBuffer(buffSize)
        self.vertices = VBOArray(len(vertices), GLfloat, vertices, vertBuff)
        self.normals = VBOArray(len(normals), GLfloat, normals, vertBuff)
        self.texCoords = VBOArray(len(texCoords), GLfloat, texCoords, vertBuff)
        self.colors = VBOArray(len(colors), GLfloat, colors, vertBuff)
        buffSize = triSize*sizeof(GLuint)
        self.facesBuffer = VertexBuffer(buffSize, target = VertexBuffer.ELEMENT_ARRAY_BUFFER)
        for triangle in triangles:
            vbo = VBOArray(len(triangle.faces), GLuint, triangle.faces, self.facesBuffer)
            triangle.faces = vbo

    def render(self, renderDevice):
        self.vertices.buffer.enable()
        renderDevice.texCoordPointer(self.texCoords.pointer(), [0, 1])
        renderDevice.colorPointer(self.colors.pointer())
        renderDevice.normalPointer(self.normals.pointer())
        renderDevice.vertexPointer(self.vertices.pointer())
        self.facesBuffer.enable()
        
        for triangle in self.triangles:
            renderDevice.configureMaterial(triangle.material)
            renderDevice.drawRangeElements(self.mode, triangle)
            glDisable(GL_TEXTURE_2D)
        
        self.vertices.buffer.disable()
        self.facesBuffer.disable()

        
        
