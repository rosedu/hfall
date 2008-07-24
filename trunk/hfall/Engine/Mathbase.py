"""
Hamerfall mathematics utility. This classes implement some very useful
mathematic concepts, especially from analitic geometry. This classes
can be used by all other classes.

"""

from math import sqrt

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

class Vector2D:
    """
    A useful class for two dimensional geometry. Mainly it represents
    a two dimensional vector though it can be used to represent any pair
    of number that should be passed and treated as a one (complex numbers
    for example or position of points).

    """
    # TODO: nothing useful for me yet
    pass


class Vector3D:
    """
    A useful class for three dimensional geometry. It represents a three
    dimensional vector or a position in the 3D space.

    """

    # TODO: a type enforcing, we don't need a list to be passed as argument
    # to our vector. It is a nonsense to have such a thing.
    
    def __init__(self, x=0, y=0, z=0):
        """Vector3D initialitzation"""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """Vector3D addition"""
        #return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
	self.x+=other.x
	self.y+=other.y
	self.z+=other.z

    # TODO: define other methods as is this one
    
    def Norm3D(self):
  	norm = sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
	if norm == 0:
	    self.x = 0
	    self.y = 0
	    self.z = 0
	else:
  	    self.x = 1.0*self.x/norm
	    self.y = 1.0*self.y/norm
	    self.z = 1.0*self.z/norm

    def __multiply_scalar__(self,factor):
        """scalar element"""
	self.x *=factor
	self.y *=factor
	self.z *=factor

class Quaternion:
    """
    A useful class for operations with quaternions. Useful for storing
    efficiently information about rotations in 3D space. It may be
    assimilated as a 4 dimensional vector but there are some theoretic
    aspects that need to be taken into account before doing that.

    """
    # TODO: nothing useful for me yet
