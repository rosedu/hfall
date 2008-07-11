import sys
import pyglet
from pyglet.gl import *
sys.path.insert(0, "../trunk")
import ctypes
import hfall.base
import hfall.OGLbase
import hfall.UI
import hfall.Render
import hfall.Vertex
import hfall.Mesh
import hfall.Model
import hfall.ModelLoader
from hfall.Console import Console
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe = 100
        self._vertexes = []
        self._faces = []
        # self.mesh = []
        self.model = None
        self.Loader = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        
        # ppoints = (GLfloat * len(points))(*points)
        # pcolors = (GLfloat * len(colors))(*colors)
        # self._vertexes = ppoints
        # pfaces = (GLuint * len(faces))(*faces)
        # self._faces = pfaces
        # self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, None, GL_TRIANGLES))

        Loader = hfall.ModelLoader.ModelLoader()
        Loader.loadModel("test.3ds")
        self.model = Loader.getModel()
        for i in range(0,len(self.model.meshes)):
            self.model.meshes[i].vertices = (GLfloat * len(self.model.meshes[i].vertices))(*self.model.meshes[i].vertices)
            self.model.meshes[i].faces = (GLuint * len(self.model.meshes[i].faces))(*self.model.meshes[i].faces)

        # self.model = hfall.Model.Model(self.mesh, None)
        render.add3D(self.model)

    def stop(self, kernel):
        pass

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        #self._maxframe-=1
        #print "Frame: ",self._maxframe
        if (self._maxframe<0):
            kernel.shutdown()

    def name(self):
        return "drawer"

render = hfall.Render.Render(800, 600, posx = 10, posy = 0, posz = -50)
hfk.insert(drawer())
hfk.insert(render)
# hfk.insert(Console(render))
hfk.run()
