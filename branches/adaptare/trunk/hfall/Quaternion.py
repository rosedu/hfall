"""
Quaternion math
"""
import math
from pyglet.gl import *

class Quaternion:
    """
    Quaternion usefull stuff
    """
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x,
                       self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x,
                       self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vector3) == True:
            return Vector2(self.x * other.x,
                           self.y * other.y)
        else:
            return Vector2(self.x * other,
                           self.y * other)

    def __div__(self, other):
        if isinstance(other, Vector3) == True:
            return Vector2(self.x / other.x,
                           self.y / other.y)
        else:
            return Vector2(self.x / other,
                           self.y / other)

    def __rmul__(self, other):
        return Vector2(other * self.x,
                       other * self.y)

    def __eq__(self, other):
        return (self.x == other.x and \
                self.y == other.y)

    def __ne__(self, other):
        return (not (self == other))

    def __getitem__(self, key):
        if key == 0: return self.x
        elif key == 1: return self.y
        else: raise IndexError("bad Vector2 index");

    def __setitem__(self, key, val):
        if key == 0: self.x = val
        elif key == 1: self.y = val
        else: raise IndexError("bad Vector2 index");

    def length(self):
        return math.sqrt(self.dotProduct(self))

    def distance(self, other):
        raise NotImplemented("no specs provided");

    def crossProduct(self, other):
        raise NotImplemented("Not defined");

    def dotProduct(self, other):
        return self.x * other.x +\
               self.y * other.y

    def normalize(self):
        l = self.length()
        self.x /= l
        self.y /= l

    def __str__(self):
        return '[' + str(self.x) +\
               ' ' + str(self.y) + ']'

    def length(self):
        return math.sqrt(self.dotProduct(self))

    def distance(self, other):
        raise NotImplemented("no specs provided");

    def crossProduct(self, other):
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def dotProduct(self, other):
        return self.x * other.x +\
               self.y * other.y +\
               self.z * other.z

    def normalize(self):
        #import traceback
        #traceback.print_stack()
        l = self.length()
        self.x /= l
        self.y /= l
        self.z /= l

    def __str__(self):
        return '[' + str(self.x) +\
               ' ' + str(self.y) +\
               ' ' + str(self.z) + ']'

    def asDouble(self):
        m = (GLint*4)(*[])
        m[0] = int(self.x)
        m[1] = int(self.y)
        m[2] = int(self.z)
        m[3] = int(self.w)
        return m
