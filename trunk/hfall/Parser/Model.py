"""
Hamerfall Model class. This class holds information about each model
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

import Mesh

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
        # glPushMatrix();
        
        for mesh in self.meshes:
            mesh.render(rnd)

        
