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

        points = [-46.798, 23.399, 21.2281,\
            -32.646, 23.399, 15.8224,\
            -53.874, 35.655, 15.8224,\
            -53.874, 11.143, 15.8224,\
            -30.9756, 35.655, 7.07599,\
            -30.9756, 11.143, 7.07599,\
            -65.3232, 30.9735, 7.07599,\
            -44.0952, 43.2296, 7.07599,\
            -44.0952, 3.56842, 7.07599,\
            -65.3232, 15.8244, 7.07599,\
            -28.2728, 30.9736, -7.076,\
            -28.2728, 15.8244, -7.076,\
            -62.6204, 35.655, -7.076,\
            -49.5008, 43.2296, -7.076,\
            -49.5008, 3.56842, -7.076,\
            -62.6204, 11.143, -7.076,\
            -39.722, 35.655, -15.8224,\
            -39.722, 11.143, -15.8224,\
            -60.95, 23.399, -15.8224,\
            -46.798, 23.399, -21.22811]
        ppoints = (GLfloat * len(points))(*points)
        colors = [0.5,0.5,0, 0,0,1, 0,1,0, 0,1,1, 1,0,0, 1,0,1, 1,1,0, 1,0.5,0.5]
        pcolors = (GLfloat * len(colors))(*colors)
        self._vertexes = ppoints

        faces = [0,1,4,7,2,0,2,6,9,3,0,3,8,5,1,1,5,11,10,4,2,7,13,12,6,3,9,15,14,8,\
                 4,10,16,13,7,5,8,14,17,11,6,12,18,15,9,10,11,17,19,16,12,13,16,19,18,\
                 14,15,18,19,17]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, None, GL_LINE_STRIP))

        
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
