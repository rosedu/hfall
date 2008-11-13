"""
Hamerfall Model class. This class holds information about each model
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine/")

import Mesh
from glcalls import *
from pyglet.gl import *
from Object import *

class Model(Object):
    """
    This is our Model class. It contains the perspective and
    the meshes matrix that form the model.

    """

    
    def __init__(self, mes, name, matrix = Matrix4.identity()):
        """
        meshes  - the actual meshes that form the model and that
                  are given to be render to OpenGL
        matrix4 - the perspective matrix
        """
        self.meshes = mes
        self.type = "Model"
        self.modelView = matrix
        self.name = name

    def render(self, rnd, textured = True):
        glPushMatrix();
        glMultMatrix(self.modelView)
        for mesh in self.meshes:
            if textured: mesh.render(rnd)
            else: mesh.renderNonTextured(rnd)
        glPopMatrix()
        
