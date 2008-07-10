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

        points = [0.2000,  0.0000, 2.70000  ,    0.2000, -0.1120, 2.70000  ,    0.1120, -0.2000, 2.70000  ,
       0.0000, -0.2000, 2.70000  ,    1.3375,  0.0000, 2.53125  ,    1.3375, -0.7490, 2.53125  ,
       0.7490, -1.3375, 2.53125  ,    0.0000, -1.3375, 2.53125  ,    1.4375,  0.0000, 2.53125  ,
       1.4375, -0.8050, 2.53125  ,    0.8050, -1.4375, 2.53125  ,    0.0000, -1.4375, 2.53125  ,
       1.5000,  0.0000, 2.40000  ,    1.5000, -0.8400, 2.40000  ,    0.8400, -1.5000, 2.40000  ,
       0.0000, -1.5000, 2.40000  ,    1.7500,  0.0000, 1.87500  ,    1.7500, -0.9800, 1.87500  ,
       0.9800, -1.7500, 1.87500  ,    0.0000, -1.7500, 1.87500  ,    2.0000,  0.0000, 1.35000  ,
       2.0000, -1.1200, 1.35000  ,    1.1200, -2.0000, 1.35000  ,    0.0000, -2.0000, 1.35000  ,
       2.0000,  0.0000, 0.90000  ,    2.0000, -1.1200, 0.90000  ,    1.1200, -2.0000, 0.90000  ,
       0.0000, -2.0000, 0.90000  ,   -2.0000,  0.0000, 0.90000  ,    2.0000,  0.0000, 0.45000  ,
       2.0000, -1.1200, 0.45000  ,    1.1200, -2.0000, 0.45000  ,    0.0000, -2.0000, 0.45000  ,
       1.5000,  0.0000, 0.22500  ,    1.5000, -0.8400, 0.22500  ,    0.8400, -1.5000, 0.22500  ,
       0.0000, -1.5000, 0.22500  ,    1.5000,  0.0000, 0.15000  ,    1.5000, -0.8400, 0.15000  ,
       0.8400, -1.5000, 0.15000  ,    0.0000, -1.5000, 0.15000  ,   -1.6000,  0.0000, 2.02500  ,
      -1.6000, -0.3000, 2.02500  ,   -1.5000, -0.3000, 2.25000  ,   -1.5000,  0.0000, 2.25000  ,
      -2.3000,  0.0000, 2.02500  ,   -2.3000, -0.3000, 2.02500  ,   -2.5000, -0.3000, 2.25000  ,
      -2.5000,  0.0000, 2.25000  ,   -2.7000,  0.0000, 2.02500  ,   -2.7000, -0.3000, 2.02500  ,
      -3.0000, -0.3000, 2.25000  ,   -3.0000,  0.0000, 2.25000  ,   -2.7000,  0.0000, 1.80000  ,
      -2.7000, -0.3000, 1.80000  ,   -3.0000, -0.3000, 1.80000  ,   -3.0000,  0.0000, 1.80000  ,
      -2.7000,  0.0000, 1.57500  ,   -2.7000, -0.3000, 1.57500  ,   -3.0000, -0.3000, 1.35000  ,
      -3.0000,  0.0000, 1.35000  ,   -2.5000,  0.0000, 1.12500  ,   -2.5000, -0.3000, 1.12500  ,
      -2.6500, -0.3000, 0.93750  ,   -2.6500,  0.0000, 0.93750  ,   -2.0000, -0.3000, 0.90000  ,
      -1.9000, -0.3000, 0.60000  ,   -1.9000,  0.0000, 0.60000  ,    1.7000,  0.0000, 1.42500  ,
       1.7000, -0.6600, 1.42500  ,    1.7000, -0.6600, 0.60000  ,    1.7000,  0.0000, 0.60000  ,
       2.6000,  0.0000, 1.42500  ,    2.6000, -0.6600, 1.42500  ,    3.1000, -0.6600, 0.82500  ,
       3.1000,  0.0000, 0.82500  ,    2.3000,  0.0000, 2.10000  ,    2.3000, -0.2500, 2.10000  ,
       2.4000, -0.2500, 2.02500  ,    2.4000,  0.0000, 2.02500  ,    2.7000,  0.0000, 2.40000  ,
       2.7000, -0.2500, 2.40000  ,    3.3000, -0.2500, 2.40000  ,    3.3000,  0.0000, 2.40000  ,
       2.8000,  0.0000, 2.47500  ,    2.8000, -0.2500, 2.47500  ,    3.5250, -0.2500, 2.49375  ,
       3.5250,  0.0000, 2.49375  ,    2.9000,  0.0000, 2.47500  ,    2.9000, -0.1500, 2.47500  ,
       3.4500, -0.1500, 2.51250  ,    3.4500,  0.0000, 2.51250  ,    2.8000,  0.0000, 2.40000  ,
       2.8000, -0.1500, 2.40000  ,    3.2000, -0.1500, 2.40000  ,    3.2000,  0.0000, 2.40000  ,
       0.0000,  0.0000, 3.15000  ,    0.8000,  0.0000, 3.15000  ,    0.8000, -0.4500, 3.15000  ,
       0.4500, -0.8000, 3.15000  ,    0.0000, -0.8000, 3.15000  ,    0.0000,  0.0000, 2.85000  ,
       1.4000,  0.0000, 2.40000  ,    1.4000, -0.7840, 2.40000  ,    0.7840, -1.4000, 2.40000  ,
       0.0000, -1.4000, 2.40000  ,    0.4000,  0.0000, 2.55000  ,    0.4000, -0.2240, 2.55000  ,
       0.2240, -0.4000, 2.55000  ,    0.0000, -0.4000, 2.55000  ,    1.3000,  0.0000, 2.55000  ,
       1.3000, -0.7280, 2.55000  ,    0.7280, -1.3000, 2.55000  ,    0.0000, -1.3000, 2.55000  ,
       1.3000,  0.0000, 2.40000  ,    1.3000, -0.7280, 2.40000  ,    0.7280, -1.3000, 2.40000  ,
       0.0000, -1.3000, 2.40000 ]
        ppoints = (GLfloat * len(points))(*points)
        colors = ((len(points) // 2) + 1)* [1, 0, 0, 0, 0, 1]
        pcolors = (GLfloat * len(colors))(*colors)
        self._vertexes = ppoints

        faces = [102, 103, 104, 105,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors))

        faces = [68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83\
        , 80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors))

        faces = [12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27\
        , 24,  25,  26,  27,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors))

        faces = [96,  96,  96,  96,  97,  98,  99, 100, 101, 101, 101, 101,   0,   1,   2,   3\
        , 0,   1,   2,   3, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors))
        
        faces = [41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56\
        , 53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  28,  65,  66,  67]
        pfaces = (GLuint * len(faces))(*faces)
        self._faces = pfaces
        self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, pcolors))

        
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
