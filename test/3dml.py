import sys
import pyglet
from pyglet.gl import *
sys.path.insert(0, "../trunk")
import numpy
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
        self.mesh = None
        self.model = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        points = [0,1,0,-1,-1,1,1,-1,1,1,-1,-1,-1,-1,-1]
        ppoints = (GLfloat * len(points))(*points)
        faces = [0, 1, 2, 0,2,3,0,3,4,0,4,1]
        pfaces = (GLuint * len(faces))(*faces)

        self._vertexes = ppoints
        self._faces = pfaces
        self.mesh = hfall.Mesh.Mesh(self._faces, self._vertexes, None, None)
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
