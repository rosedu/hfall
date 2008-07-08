"""
Hamerfall Vertex class. This class holds information about each vertex
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

class Mesh:
    """
    This is pur Vertex class. Basically it includes the position, the
    colour, the texture coordinate and the normal vector asociated to
    each vertex. It is not compulsory to have all of them defined for a
    set of vertices from one model. If one of them is not defined it is
    replaced with None.

    """

    
    def __init__(self, fac, vert, mats):
        self.faces = fac
        self.vertices = vert
        self.materials = mats
