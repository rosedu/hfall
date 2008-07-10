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
from hfall.Console import Console
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe=100
        self._vertexes = []
        self._faces = []
        self.mesh = []
        self.model = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        points = [1, 1, -1,\
                  -1, 1, -1,\
                  -1, 1, 1,\
                  1, 1, 1,\
                  1, -1, 1,\
                  -1, -1, 1,\
                  -1, -1, -1,\
                  1, -1, -1]
        ppoints = (GLfloat * len(points))(*points)
        colors = [0.5,0.5,0, 0,0,1, 0,1,0, 0,1,1, 1,0,0, 1,0,1, 1,1,0, 1,0.5,0.5]
        pcolors = (GLfloat * len(colors))(*colors)
        self._vertexes = ppoints

        faces = [0,1,2,3, 4,5,6,7, 3,2,5,4, 7,6,1,0, 2,1,6,5, 0,3,4,7]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors, GL_QUADS))

        
        self.model = hfall.Model.Model(self.mesh, None)
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

render = hfall.Render.Render(800, 600)
hfk.insert(drawer())
hfk.insert(render)
# hfk.insert(Console(render))
hfk.run()
