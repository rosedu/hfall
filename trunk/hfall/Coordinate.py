"""
Model coordinates and orientation
"""
import math

from Matrix import *
from Vector import Vector3

class Coordinate:
    def __init__(self, rotation = Matrix3.identity(), translation = Vector3()):
        if isinstance(rotation, list):
            rotation = Matrix3(rotation)
        if isinstance(translation, list):
            translation = Vector3(translation[0], translation[1], translation[2])
        self.rotation = rotation
        self.translation = translation

    def matrix(self):
        return Matrix4([\
            self.rotation[0][0], self.rotation[0][1], self.rotation[0][2], self.translation[0],\
            self.rotation[1][0], self.rotation[1][1], self.rotation[1][2], self.translation[1],\
            self.rotation[2][0], self.rotation[2][1], self.rotation[2][2], self.translation[2],\
            0, 0, 0, 1])

    def inverseMatrix(self):
        rotInv = self.rotation.transpose()
        trans = rotInv * (-self.translation)
        return Matrix4([\
            rotInv[0][0], rotInv[0][1], rotInv[0][2], trans[0],\
            rotInv[1][0], rotInv[1][1], rotInv[1][2], trans[1],\
            rotInv[2][0], rotInv[2][1], rotInv[2][2], trans[2],\
            0, 0, 0, 1])

    def _computeWS(self, vector):
        v1 = self.rotation * vector
        v2 = v1 + self.translation
        return Vector3(v2.x, v2.y, v2.z)
        
    def toWorldSpace(self, vectors):
        if isinstance(vectors, list):
            for vector in vectors:
                if isinstance(vector, Vector.Vector3):
                    self._computeWS(vector)
        elif isinstance(vectors, Vector.Vector3):
            self._computeWS(vectors)
        else:
            raise TypeError("not a supported type")

    def _computeOS(self, vector):
        v1 = vector - self.translation
        v2 = self.rotation * v1
        return Vector3(v2.x, v2.y, v2.z)

    def toObjectSpace(self, vectors):
        if isinstance(vectors, list):
            for vector in vectors:
                if isinstance(vector, Vector.Vector3):
                    self._computeOS(vector)
        elif isinstance(vectors, Vector.Vector3):
            self._computeOS(vectors)
        else:
            raise TypeError("not a supported type")
