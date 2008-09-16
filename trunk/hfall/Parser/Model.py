"""
Hamerfall Model class. This class holds information about each model
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

import Mesh
import pyglet
from pyglet.gl import *

class Model:
    """
    This is our Model class. It contains the perspective and
    the meshes matrix that form the model.

    """

    
    def __init__(self, mes, matrix, name):
        """
        meshes  - the actual meshes that form the model and that
                  are given to be render to OpenGL
        matrix4 - the perspective matrix
        """
        self.meshes = mes
        self.matrix4 = matrix
        self.name = name

    def render(self, rnd):
        self.matrix4 = [1, 0, 0, 0,\
                        0, 1, 0, 0,\
                        0, 0, 1, 0,\
                        100, 0, 0, 1]
        self.matrix4 = (GLfloat *len(self.matrix4))(*self.matrix4)
        print "Matrix:\n",self.matrix4[0:4],"\n",self.matrix4[4:8],"\n",self.matrix4[8:12],"\n",self.matrix4[12:16],"\n"
        glPushMatrix();
        glMultMatrixf(self.matrix4)
        for mesh in self.meshes:
            mesh.render(rnd)
        glPopMatrix()
        
