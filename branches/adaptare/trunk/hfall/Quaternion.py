"""
Quaternion math
"""

__version__ = '0.1'
__authors__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)' ,\
              'Laura-Mihaela Vasilescu (vasilescu.laura@gmail.com)'

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
        trace = matrix4or3._m[0][0] + matrix4or3._m[1][1] +\ 
                matrix4or3._m[2][2] + 1
        if trace > 0:
            S = 0.5 / sqrt(trace)
            self.w = 0.25 / S
            self.x = (matrix4or3._m[2][1] - matrix4or3._m[1][2]) * S
            self.y = (matrix4or3._m[0][2] - matrix4or3._m[2][0]) * S
            self.z = (matrix4or3._m[1][0] - matrix4or3._m[0][1]) * S
        else
            maxd = matrix4or3._m[0][0]
            column = 0
            if matrix4or3._m[1][1] > maxd:
                maxd = matrix4or3._m[1][1]
                column = 1
            if matrix4or3._m[2][2] > maxd:
                maxd = matrix4or3._m[2][2]
                column = 2
                
            if column == 0:
                S = sqrt(1.0 + matrix4or3._m[0][0] - matrix4or3._m[1][1] \
                        - matrix4or3._m[2][2]) * 2
                Qx = 0.5 / S
                Qy = (matrix4or3._m[0][1] + matrix4or3._m[1][0]) / S
                Qz = (matrix4or3._m[0][2] + matrix4or3._m[2][0]) / S
                Qw = (matrix4or3._m[1][2] + matrix4or3._m[2][1]) / S
                
            if column == 1:
                S = sqrt(1.0 - matrix4or3._m[0][0] + matrix4or3._m[1][1] \
                        - matrix4or3._m[2][2]) * 2
                Qy = 0.5 / S
                Qx = (matrix4or3._m[0][1] + matrix4or3._m[1][0]) / S
                Qw = (matrix4or3._m[0][2] + matrix4or3._m[2][0]) / S
                Qz = (matrix4or3._m[1][2] + matrix4or3._m[2][1]) / S    
                
            if column == 2:
                S = sqrt(1.0 - matrix4or3._m[0][0] - matrix4or3._m[1][1] \
                        + matrix4or3._m[2][2]) * 2
                Qz = 0.5 / S
                Qw = (matrix4or3._m[0][1] + matrix4or3._m[1][0]) / S
                Qx = (matrix4or3._m[0][2] + matrix4or3._m[2][0]) / S
                Qy = (matrix4or3._m[1][2] + matrix4or3._m[2][1]) / S
            
            self.x = Qx
            self.y = Qy
            self.z = Qz
            self.w = Qw
            return self
        

    def toMatrix3(self):
        m3 = Matrix.Matrix3()
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        m3._m[0][0] = 1 - 2 * y ** 2 - 2 * z ** 2
        m3._m[0][1] = 2 * x * y - 2 * z * w
        m3._m[0][2] = 2 * x * z + 2 * y * w
        m3._m[1][0] = 2 * x * y + 2 * z * w
        m3._m[1][1] = 1 - 2 * x ** 2 - 2 * z ** 2
        m3._m[1][2] = 2 * y * z - 2 * x * w
        m3._m[2][0] = 2 * x * z - 2 * y * w
        m3._m[2][1] = 2 * y * z + 2 * x * w
        m3._m[2][2] = 1 - 2 * x ** 2 - 2 * y ** 2
        return m3
        
    def toMatrix4(self):
        m4 = Matrix.Matrix4()
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        m4._m[0][0] = 1 - 2 * y ** 2 - 2 * z ** 2
        m4._m[0][1] = 2 * x * y - 2 * z * w
        m4._m[0][2] = 2 * x * z + 2 * y * w
        m4._m[1][0] = 2 * x * y + 2 * z * w
        m4._m[1][1] = 1 - 2 * x ** 2 - 2 * z ** 2
        m4._m[1][2] = 2 * y * z - 2 * x * w
        m4._m[2][0] = 2 * x * z - 2 * y * w
        m4._m[2][1] = 2 * y * z + 2 * x * w
        m4._m[2][2] = 1 - 2 * x ** 2 - 2 * y ** 2
        m4._m[0][3] = m4._m[1][3] = m4._m[2][3] = 0
        m4._m[3][0] = m4._m[3][1] = m4._m[3][2] = 0
        m4._m[3][3] = 1
        return m4

    def fromEuler(self, vectororvals):
        pass

    def toEuler(self):
        pass

    def LERP(self, undefined):
        pass

    def SLERP(self, undefined):
        pass
        

