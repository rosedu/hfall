"""
Matrix math
"""
import math

import Vector

class Matrix3:
    """
    3x3 matrix
    """
    def __init__(self, vals = 9*[0]):
        self._m = [3*[0], 3*[0], 3*[0]]
        if len(vals) == 3:
            if isinstance(vals[0], Vector.Vector3):
                for key in range(3):
                    self.setRow(key, vals[key])
            elif len(vals[0]) == 3:
                for i in range(3):
                    for j in range(3):
                        self._m[i][j] = vals[i][j]
            else:
                raise TypeError("Invalid argument in matrix")
        elif len(vals) == 9:
            self._m[0][0] = vals[0]
            self._m[0][1] = vals[1]
            self._m[0][2] = vals[2]
            self._m[1][0] = vals[3]
            self._m[1][1] = vals[4]
            self._m[1][2] = vals[5]
            self._m[2][0] = vals[6]
            self._m[2][1] = vals[7]
            self._m[2][2] = vals[8]
        else:
            raise TypeError("Invalid argument in matrix")

    def __add__(self, other):
        return Matrix3([self._m[0][0] + other._m[0][0],\
                       self._m[0][1] + other._m[0][1],\
                       self._m[0][2] + other._m[0][2],\
                       self._m[1][0] + other._m[1][0],\
                       self._m[1][1] + other._m[1][1],\
                       self._m[1][2] + other._m[1][2],\
                       self._m[2][0] + other._m[2][0],\
                       self._m[2][1] + other._m[2][1],\
                       self._m[2][2] + other._m[2][2]])

    def __sub__(self, other):
        return Matrix3([self._m[0][0] - other._m[0][0],\
                       self._m[0][1] - other._m[0][1],\
                       self._m[0][2] - other._m[0][2],\
                       self._m[1][0] - other._m[1][0],\
                       self._m[1][1] - other._m[1][1],\
                       self._m[1][2] - other._m[1][2],\
                       self._m[2][0] - other._m[2][0],\
                       self._m[2][1] - other._m[2][1],\
                       self._m[2][2] - other._m[2][2]])

    def __neg__(self):
        return Matrix3([-self._m[0][0], -self._m[0][1], -self._m[0][2],\
                       -self._m[1][0], -self._m[1][1], -self._m[1][2],\
                       -self._m[2][0], -self._m[2][1], -self._m[2][2]])

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            c = Matrix3()
            for i in range(3):
                for j in range(3):
                    s = 0
                    for k in range(3):
                        s += self._m[i][k] * self._m[k][j]
                    c._m[i][j] = s
            return c
        elif isinstance(other, Vector.Vector3):
            v = Vector.Vector3()
            for i in range(3):
                s = 0
                for j in range(3):
                    s += self._m[i][j] * other[j]
                v[i] = s
            return v
        else:
            return Matrix3([self._m[0][0] * other,\
                           self._m[0][1] * other,\
                           self._m[0][2] * other,\
                           self._m[1][0] * other,\
                           self._m[1][1] * other,\
                           self._m[1][2] * other,\
                           self._m[2][0] * other,\
                           self._m[2][1] * other,\
                           self._m[2][2] * other])

    def __div__(self, other):
        return Matrix3([self._m[0][0] / other,\
                       self._m[0][1] / other,\
                       self._m[0][2] / other,\
                       self._m[1][0] / other,\
                       self._m[1][1] / other,\
                       self._m[1][2] / other,\
                       self._m[2][0] / other,\
                       self._m[2][1] / other,\
                       self._m[2][2] / other])

    def __rmul__(self, other):
        return Matrix3([self._m[0][0] * other,\
                       self._m[0][1] * other,\
                       self._m[0][2] * other,\
                       self._m[1][0] * other,\
                       self._m[1][1] * other,\
                       self._m[1][2] * other,\
                       self._m[2][0] * other,\
                       self._m[2][1] * other,\
                       self._m[2][2] * other])

    def __eq__(self, other):
        return self._m == other._m

    def __ne__(self, other):
        return self._m != other._m

    @staticmethod
    def identity():
        return Matrix3([1, 0, 0, 0, 1, 0, 0, 0, 1])

    def transpose(self):
        t = Matrix3()
        for i in range(3):
            for j in range(3):
                t._m[i][j] = self._m[j][i]
        return t

    def adjoint(self):
        return Matrix3([self._m[1][1] * self._m[2][2] - self._m[1][2] * self._m[2][1],\
                       -self._m[0][1] * self._m[2][2] + self._m[0][2] * self._m[2][1],\
                       self._m[0][1] * self._m[1][2] - self._m[0][2] * self._m[1][1],\
                       -self._m[1][0] * self._m[2][2] + self._m[1][2] * self._m[2][0],\
                       self._m[0][0] * self._m[2][2] - self._m[0][2] * self._m[2][0],\
                       -self._m[0][0] * self._m[1][2] + self._m[0][2] * self._m[1][0],\
                       self._m[1][0] * self._m[2][1] - self._m[1][1] * self._m[2][0],\
                       -self._m[0][0] * self._m[2][1] + self._m[0][1] * self._m[2][0],\
                       self._m[0][0] * self._m[1][1] - self._m[0][1] * self._m[1][0]])

    def inverse(self):
        return self.adjoint()/self.determinant()

    def orthonormalize(self):
        i_l =1 / math.sqrt(self._m[0][0] * self._m[0][0] +\
                           self._m[1][0] * self._m[1][0] +\
                           self._m[2][0] * self._m[2][0])
        self._m[0][0] *= i_l
        self._m[1][0] *= i_l
        self._m[2][0] *= i_l
        self._m[0][2] = self._m[1][0] * self._m[2][1] - self._m[2][0] * self._m[1][1]
        self._m[1][2] = self._m[2][0] * self._m[0][1] - self._m[0][0] * self._m[2][1]
        self._m[2][2] = self._m[0][0] * self._m[1][1] - self._m[1][0] * self._m[0][1]
        i_l =1 / math.sqrt(self._m[0][2] * self._m[0][2] +\
                           self._m[1][2] * self._m[1][2] +\
                           self._m[2][2] * self._m[2][2])
        self._m[0][2] *= i_l
        self._m[1][2] *= i_l
        self._m[2][2] *= i_l
        self._m[0][1] = self._m[1][2] * self._m[2][0] - self._m[2][2] * self._m[1][0]
        self._m[1][1] = self._m[2][2] * self._m[0][0] - self._m[0][2] * self._m[2][0]
        self._m[2][1] = self._m[0][2] * self._m[1][0] - self._m[1][2] * self._m[0][0]
        i_l =1 / math.sqrt(self._m[0][1] * self._m[0][1] +\
                           self._m[1][1] * self._m[1][1] +\
                           self._m[2][1] * self._m[2][1])
        self._m[0][1] *= i_l
        self._m[1][1] *= i_l
        self._m[2][1] *= i_l        

    def determinant(self):
        return self._m[0][0] * self._m[1][1] * self._m[2][2] +\
               self._m[0][1] * self._m[1][2] * self._m[2][0] +\
               self._m[0][2] * self._m[1][0] * self._m[2][1] -\
               self._m[0][2] * self._m[1][1] * self._m[2][0] -\
               self._m[0][1] * self._m[1][0] * self._m[2][2] -\
               self._m[0][0] * self._m[1][2] * self._m[2][1]

    def getRow(self, key):
        if key >= 0 and key <=2:
            return Vector.Vector3(self._m[key][0],\
                                  self._m[key][1],\
                                  self._m[key][2])
        else: raise IndexError("bad row index")

    def getColumn(self, key):
        if key >= 0 and key <=2:
            return Vector.Vector3(self._m[0][key],\
                                  self._m[1][key],\
                                  self._m[2][key])
        else: raise IndexError("bad column index")

    def getDiag(self):
        return Vector.Vector3(self._m[0][0],\
                              self._m[1][1],\
                              self._m[2][2])

    def setRow(self, key, vector):
        if key >= 0 and key <=2:
            if isinstance(vector, Vector.Vector3):
                self._m[key][0] = vector.x
                self._m[key][1] = vector.y
                self._m[key][2] = vector.z
            else: raise TypeError("wanted Vector3 for setRow")
        else: raise IndexError("bad column index")

    def setColumn(self, key, vector):
        if key >= 0 and key <=2:
            if isinstance(vector, Vector.Vector3):
                self._m[0][key] = vector.x
                self._m[1][key] = vector.y
                self._m[2][key] = vector.z
            else: raise TypeError("wanted Vector3 for setColumn")
        else: raise IndexError("bad column index")

    def setDiag(self, vector):
        if isinstance(vector, Vector.Vector3):
            self._m[0][0] = vector.x
            self._m[1][1] = vector.y
            self._m[2][2] = vector.z
        else: raise TypeError("wanted Vector3 for setDiag")

    def __str__(self):
        return '|' + str(self._m[0][0]) + ' ' + str(self._m[0][1]) + ' ' + str(self._m[0][2]) + '|\n' +\
               '|' + str(self._m[1][0]) + ' ' + str(self._m[1][1]) + ' ' + str(self._m[1][2]) + '|\n' +\
               '|' + str(self._m[2][0]) + ' ' + str(self._m[2][1]) + ' ' + str(self._m[2][2]) + '|'


class Matrix4:
    """
    4x4 matrix
    """
    def __init__(self, vals = 16*[0]):
        self._m = [4*[0], 4*[0], 4*[0], 4*[0]]
        if len(vals) == 4:
            if isinstance(vals[0], Vector.Vector4):
                for key in range(4):
                    self.setRow(key, vals[key])
            elif len(vals[0]) == 4:
                for i in range(4):
                    for j in range(4):
                        self._m[i][j] = vals[i][j]
            else:
                raise TypeError("Invalid argument in matrix")
        elif len(vals) == 16:
            self._m[0][0] = vals[0]
            self._m[0][1] = vals[1]
            self._m[0][2] = vals[2]
            self._m[0][3] = vals[3]
            self._m[1][0] = vals[4]
            self._m[1][1] = vals[5]
            self._m[1][2] = vals[6]
            self._m[0][3] = vals[7]
            self._m[2][0] = vals[8]
            self._m[2][1] = vals[9]
            self._m[2][2] = vals[10]
            self._m[2][3] = vals[11]
            self._m[2][0] = vals[12]
            self._m[2][1] = vals[13]
            self._m[2][2] = vals[14]
            self._m[2][3] = vals[15]
        else:
            raise TypeError("Invalid argument in matrix")

    def __add__(self, other):
        return Matrix4([self._m[0][0] + other._m[0][0],\
                       self._m[0][1] + other._m[0][1],\
                       self._m[0][2] + other._m[0][2],\
                       self._m[0][3] + other._m[0][3],\
                       self._m[1][0] + other._m[1][0],\
                       self._m[1][1] + other._m[1][1],\
                       self._m[1][2] + other._m[1][2],\
                       self._m[1][3] + other._m[1][3],\
                       self._m[2][0] + other._m[2][0],\
                       self._m[2][1] + other._m[2][1],\
                       self._m[2][2] + other._m[2][2],\
                       self._m[2][3] + other._m[2][3],\
                       self._m[3][0] + other._m[3][0],\
                       self._m[3][1] + other._m[3][1],\
                       self._m[3][2] + other._m[3][2],\
                       self._m[3][3] + other._m[3][3]])

    def __sub__(self, other):
        return Matrix4([self._m[0][0] - other._m[0][0],\
                       self._m[0][1] - other._m[0][1],\
                       self._m[0][2] - other._m[0][2],\
                       self._m[0][3] - other._m[0][3],\
                       self._m[1][0] - other._m[1][0],\
                       self._m[1][1] - other._m[1][1],\
                       self._m[1][2] - other._m[1][2],\
                       self._m[1][3] - other._m[1][3],\
                       self._m[2][0] - other._m[2][0],\
                       self._m[2][1] - other._m[2][1],\
                       self._m[2][2] - other._m[2][2],\
                       self._m[2][3] - other._m[2][3],\
                       self._m[3][0] - other._m[3][0],\
                       self._m[3][1] - other._m[3][1],\
                       self._m[3][2] - other._m[3][2],\
                       self._m[3][3] - other._m[3][3]])

    def __neg__(self):
        return Matrix4([-self._m[0][0], -self._m[0][1], -self._m[0][2], -self._m[0][3],\
                       -self._m[1][0], -self._m[1][1], -self._m[1][2], -self._m[1][3],\
                       -self._m[2][0], -self._m[2][1], -self._m[2][2], -self._m[2][3],\
                       -self._m[3][0], -self._m[3][1], -self._m[3][2], -self._m[3][3]])

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            c = Matrix4()
            for i in range(4):
                for j in range(4):
                    s = 0
                    for k in range(4):
                        s += self._m[i][k] * self._m[k][j]
                    c._m[i][j] = s
            return c
        else:
            return Matrix4([self._m[0][0] * other,\
                           self._m[0][1] * other,\
                           self._m[0][2] * other,\
                           self._m[0][3] * other,\
                           self._m[1][0] * other,\
                           self._m[1][1] * other,\
                           self._m[1][2] * other,\
                           self._m[1][3] * other,\
                           self._m[2][0] * other,\
                           self._m[2][1] * other,\
                           self._m[2][2] * other,\
                           self._m[2][3] * other,\
                           self._m[3][0] * other,\
                           self._m[3][1] * other,\
                           self._m[3][2] * other,\
                           self._m[3][3] * other])

    def __div__(self, other):
        return Matrix4([self._m[0][0] / other,\
                        self._m[0][1] / other,\
                        self._m[0][2] / other,\
                        self._m[0][3] / other,\
                        self._m[1][0] / other,\
                        self._m[1][1] / other,\
                        self._m[1][2] / other,\
                        self._m[1][3] / other,\
                        self._m[2][0] / other,\
                        self._m[2][1] / other,\
                        self._m[2][2] / other,\
                        self._m[2][3] / other,\
                        self._m[3][0] / other,\
                        self._m[3][1] / other,\
                        self._m[3][2] / other,\
                        self._m[3][3] / other])

    def __rmul__(self, other):
        return Matrix4([self._m[0][0] * other,\
                        self._m[0][1] * other,\
                        self._m[0][2] * other,\
                        self._m[0][3] * other,\
                        self._m[1][0] * other,\
                        self._m[1][1] * other,\
                        self._m[1][2] * other,\
                        self._m[1][3] * other,\
                        self._m[2][0] * other,\
                        self._m[2][1] * other,\
                        self._m[2][2] * other,\
                        self._m[2][3] * other,\
                        self._m[3][0] * other,\
                        self._m[3][1] * other,\
                        self._m[3][2] * other,\
                        self._m[3][3] * other])

    def __eq__(self, other):
        return self._m == other._m

    def __ne__(self, other):
        return self._m != other._m

    @staticmethod
    def identity():
        return Matrix4([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

    def transpose(self):
        t = Matrix4()
        for i in range(4):
            for j in range(4):
                t._m[i][j] = self._m[j][i]
        return t

    def adjoint(self):
        """return Matrix3([self._m[1][1] * self._m[2][2] - self._m[1][2] * self._m[2][1],\
                       -self._m[0][1] * self._m[2][2] + self._m[0][2] * self._m[2][1],\
                       self._m[0][1] * self._m[1][2] - self._m[0][2] * self._m[1][1],\
                       -self._m[1][0] * self._m[2][2] + self._m[1][2] * self._m[2][0],\
                       self._m[0][0] * self._m[2][2] - self._m[0][2] * self._m[2][0],\
                       -self._m[0][0] * self._m[1][2] + self._m[0][2] * self._m[1][0],\
                       self._m[1][0] * self._m[2][1] - self._m[1][1] * self._m[2][0],\
                       -self._m[0][0] * self._m[2][1] + self._m[0][1] * self._m[2][0],\
                       self._m[0][0] * self._m[1][1] - self._m[0][1] * self._m[1][0]])"""
        raise NotImplemented("n.i.y.")

    def inverse(self):
        return self.adjoint()/self.determinant()

    def orthonormalize(self):
        raise NotImplemented("n.i.y")      

    def determinant(self):
        "return self._m[0][0] * self._m[1][1] * self._m[2][2] +\
               self._m[0][1] * self._m[1][2] * self._m[2][0] +\
               self._m[0][2] * self._m[1][0] * self._m[2][1] -\
               self._m[0][2] * self._m[1][1] * self._m[2][0] -\
               self._m[0][1] * self._m[1][0] * self._m[2][2] -\
               self._m[0][0] * self._m[1][2] * self._m[2][1]"
        raise NotImplemented("n.i.y")

    def getRow(self, key):
        if key >= 0 and key <=3:
            return Vector.Vector4(self._m[key][0],\
                                  self._m[key][1],\
                                  self._m[key][2],\
                                  self._m[key][3])
        else: raise IndexError("bad row index")

    def getColumn(self, key):
        if key >= 0 and key <=3:
            return Vector.Vector4(self._m[0][key],\
                                  self._m[1][key],\
                                  self._m[2][key],\
                                  self._m[3][key])
        else: raise IndexError("bad column index")

    def getDiag(self):
        return Vector.Vector3(self._m[0][0],\
                              self._m[1][1],\
                              self._m[2][2],\
                              self._m[3][3])

    def setRow(self, key, vector):
        if key >= 0 and key <=3:
            if isinstance(vector, Vector.Vector4):
                self._m[key][0] = vector.x
                self._m[key][1] = vector.y
                self._m[key][2] = vector.z
                self._m[key][3] = vector.w
            else: raise TypeError("wanted Vector4 for setRow")
        else: raise IndexError("bad column index")

    def setColumn(self, key, vector):
        if key >= 0 and key <=3:
            if isinstance(vector, Vector.Vector4):
                self._m[0][key] = vector.x
                self._m[1][key] = vector.y
                self._m[2][key] = vector.z
                self._m[3][key] = vector.w
            else: raise TypeError("wanted Vector4 for setColumn")
        else: raise IndexError("bad column index")

    def setDiag(self, vector):
        if isinstance(vector, Vector.Vector4):
            self._m[0][0] = vector.x
            self._m[1][1] = vector.y
            self._m[2][2] = vector.z
            self._m[3][3] = vector.w
        else: raise TypeError("wanted Vector4 for setDiag")

    def __str__(self):
        return '|' + str(self._m[0][0]) + ' ' + str(self._m[0][1]) + ' ' + str(self._m[0][2]) + ' ' + str(self._m[0][3]) + '|\n' +\
               '|' + str(self._m[1][0]) + ' ' + str(self._m[1][1]) + ' ' + str(self._m[1][2]) + ' ' + str(self._m[0][3]) + '|\n' +\
               '|' + str(self._m[2][0]) + ' ' + str(self._m[2][1]) + ' ' + str(self._m[2][2]) + ' ' + str(self._m[0][3]) + '|\n' +\
               '|' + str(self._m[3][0]) + ' ' + str(self._m[3][1]) + ' ' + str(self._m[3][2]) + ' ' + str(self._m[0][3]) + '|'
