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

        points = [ 0.000000, -12.431658,  0.000000,\
                  8.287742,  -9.265973,  0.000000,\
                 -4.143871,  -9.265973,  7.177396,\
                 -4.143871,  -9.265973, -7.177396,\
                  9.265973,  -4.143871,  7.177396,\
                  9.265973,  -4.143871, -7.177396,\
                -10.848792,  -4.143871,  4.435805,\
                  1.582819,  -4.143871, 11.613271,\
                  1.582819,  -4.143871,-11.613271,\
                -10.848792,  -4.143871, -4.435874,\
                 10.848792,   4.143871,  4.435874,\
                 10.848792,   4.143871, -4.435874,\
                 -9.265973,   4.143871,  7.177396,\
                 -1.582819,   4.143871, 11.613271,\
                 -1.582819,   4.143871,-11.613271,\
                 -9.265973,   4.143871, -7.177396,\
                  4.143871,   9.265973,  7.177396,\
                  4.143871, 9.265973, -7.177396,\
                 -8.287742, 9.265973, 0.000000,\
                  0.000000, 12.431658, 0.000000]
        ppoints = (GLfloat * len(points))(*points)
        colors = [0.5,0.5,0, 0,0,1, 0,1,0, 0,1,1, 1,0,0, 1,0,1, 1,1,0, 1,0.5,0.5]
        pcolors = (GLfloat * len(colors))(*colors)
        self._vertexes = ppoints

        faces = [4,7,2,\
                  1,4,2,\
                  0,1,2,\
                  6,9,3,\
                  2,6,3,\
                  0,2,3,\
                  8,5,1,\
                  3,8,1,\
                  0,3,1,\
                 11,10,4,\
                  5,11,4,\
                  1,5,4,\
                  13,12,6,\
                  7,13,6,\
                  2,7,6,\
                  15,14,8,\
                  9,15,8,\
                  3,9,8,\
                  16,13,7,\
                  10,16,7,\
                  4,10,7,\
                  14,17,11,\
                  8,14,11,\
                  5,8,11,\
                  18,15,9,\
                  12,18,9,\
                  6,12,9,\
                  17,19,16,\
                  11,17,16,\
                  10,11,16,\
                  16,19,18,\
                  13,16,18,\
                  12,13,18,\
                  18,19,17,\
                  15,18,17,\
                  14,15,17]

        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, None, GL_TRIANGLES))

        
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

render = hfall.Render.Render(800, 600, posx = 10, posy = 0, posz = -50)
hfk.insert(drawer())
hfk.insert(render)
# hfk.insert(Console(render))
hfk.run()
