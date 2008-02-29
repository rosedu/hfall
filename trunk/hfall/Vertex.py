"""
Hamerfall Vertex class. This class holds information about each vertex
used to draw our models to screen. 

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import Mathbase

class Vertex:
    """
    This is pur Vertex class. Basically it includes the position, the
    colour, the texture coordinate and the normal vector asociated to
    each vertex. It is not compulsory to have all of them defined for a
    set of vertices from one model. If one of them is not defined it is
    replaced with None.

    """

    def __init__(self, position, color=None, texture=None, normal=None):
        """
        Our Vertex constructor. The only compulsory argument is the one
        representing the position of the vertex. All other arguments may
        miss but some of them will surely be passed.
            position - the position of the vertex. It should be a list
                       containing 2, 3 or 4 floating point values
                       depending on the type of the vertex.
            color - the color of the vertex. It shoud be a list
                    containing 3 or 4 floating point values, depending
                    on usage of the alpha channel.
            texture - the textures coordinates of the vertex. It should
                      be a list with one or two floating points values.
            normal - the normal vector on the vertex. It is computed as
                     the average of the normal of the surounding faces
                     if the vertex. This computation should be done
                     before passing it as an argument to this function.
                     This class does not hold information regardin the
                     surrounding vertices and that means that it is
                     impossible to do this calculation here.
        If one of the arguments does not follow the format needed we
        replace it with None. If the position does not respect one of
        the valid formats an exception shall be thrown

        """
        # TODO: to do the verifications for the formats
        self.position = position
        self.color = color
        self.texture = texture
        self.normal = normal
