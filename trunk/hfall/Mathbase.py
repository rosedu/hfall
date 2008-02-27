"""
Hamerfall mathematics utility. This classes implement some very useful
mathematic concepts, especially from analitic geometry. This classes
can be used by all other classes.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

# imports here

class Vector2D:
    """
    A usefull class for two dimensional geometry. Mainly it represents
    a two dimensional vector though it can be used to represent any pair
    of number that should be passed and treated as a one (complex numbers
    for example or position of points).

    """
    # to do - nothing useful for me yet
    pass


class Vector3D:
    """
    A useful class for three dimensional geometry. It represents a three
    dimensional vector or a position in the 3D space.

    """

    # to do : a type enforcing, we don't need a list to be passed as argument
    # to our vector. It is a nonsense to have such a thing.
    
    def __init__(self, x=0, y=0, z=0):
        """Vector3D initialitzation"""
        self._x = x
        self._y = y
        self._z = z

    def __add__(self, other):
        """Vector3D addition"""
        return Vector3D(self._x + other._x, self._y + other._y, self._z + \
                        other._z)

    # to do : define other methods as is this one
    

class Quaternion:
    """
    A useful class for operations with quaternions. Useful for storing
    efficiently information about rotations in 3D space. It may be
    assimilated as a 4 dimensional vector but there are some theoretic
    aspects that need to be taken into account before doing that.

    """
    # to do - nothing useful for me yet
