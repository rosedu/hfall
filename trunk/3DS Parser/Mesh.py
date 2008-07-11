"""
Hamerfall Mesh class. This class holds information about each mesh
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

import pyglet
from pyglet.gl import *

class Mesh:
    """
    This is our Model class. It includes the faces, vertices, materials,
    persepctive matrix, colors and draw mode of each mesh.

    """

    
    def __init__(self, fac, vert, mats, matrix, color = None, draw_mode = GL_TRIANGLES):
        
        """
        faces       - the faces formed with the vertices
        vertices    - the actual vertices that give the mesh
        materials   - the materials that are used for each mesh
        matrix4     - the perspective matrix
        colors      - the color that we use if there's no material given
        mode        - the draw mode for OpenGL this can be GL_TRIANGLES,
                      GL_QUADS, and so forth

        """
        
        self.faces = fac
        self.vertices = vert
        self.materials = mats
        self.matrix4 = matrix
        self.colors = color
        self.mode = draw_mode
