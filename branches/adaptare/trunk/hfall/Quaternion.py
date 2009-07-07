"""
Quaternion math
"""
import math
from pyglet.gl import *

import Matrix
import Vector

class Quaternion:
    """
    Quaternion usefull stuff
    """
    def __init__(self, *args):
        if len(args) == 4:
            # 4 real values
            self.x = args[1]
            self.y = args[2]
            self.z = args[3]
            self.w = args[0]
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Quaternion):
                self.x = arg.x
                self.y = arg.y
                self.z = arg.z
                self.w = arg.w
            elif isinstance(arg, Matrix.Matrix3):
                raise NotImplemented("Not implemented yet")
            elif isinstance(arg, Matrix.Matrix4):
                raise NotImplemented("Not implemented yet")
            else:
                raise TypeError("Invalid argument")
        else:
            raise TypeError("Invalid argument")
                

    def __add__(self, other):
        return Qauternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    def __sub__(self, other):
        return Quaternion(self.w - other.w,
                          self.x - other.x,
                          self.y - other.y,
                          self.z - other.z)

    def __neg__(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(\
                other.w * self.w - other.x * self.x -\
                    other.y * self.y - other.z * self.z,\
                self.y * other.z - self.z * other.y +\
                    self.w * other.x + self.x * other.w,\
                self.z * other.x - self.x * other.z +\
                    self.w * other.y + self.y * other.w,\
                self.x * other.y - self.y * other.x +\
                    self.w * other.z + self.z * other.w)
        else:
            return Quaternion(self.w * other,
                              self.x * other,
                              self.y * other,
                              self.z * other)


    def __eq__(self, other):
        return (self.x == other.x and \
                self.y == other.y and \
                self.z == other.z and \
                self.w == other.w)

    def __ne__(self, other):
        return (not (self == other))

    def __getitem__(self, key):
        if key == 0: return self.w
        elif key == 1: return self.x
        elif key == 2: return self.y
        elif key == 3: return self.w
        else: raise IndexError("bad Quaternion index");

    def __setitem__(self, key, val):
        if key == 0: self.w = val
        elif key == 1: self.x = val
        elif key == 2: self.y = val
        elif key == 3: self.z = val
        else: raise IndexError("bad Quaternion index");

    def length(self):
        x = self.x ** 2
        y = self.y ** 2
        z = self.z ** 2
        w = self.w ** 2
        return math.sqrt(x + y + z +w)

    def normalize(self):
        l = self.length()
        self.x /= l
        self.y /= l
        self.w /= l
        self.z /= l

    def __str__(self):
        return '[ w = ' + str(self.w) +\
               '; v = (' + str(self.x) +\
               ' ' + str(self.y) + \
               ' ' + str(self.z) + ')]'

    def fromMatrix(self, matrix4or3):
        pass

    def toMatrix3(self):
        pass

    def toMatrix4(self):
        pass

    def fromEuler(self, vectororvals):
        pass

    def toEuler(self):
        pass

    def LERP(self, undefined):
        pass

    def SLERP(self, undefined):
        pass
