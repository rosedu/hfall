"""
Geometrical Objects classes for later use
"""

__version__ = '0.1'
__author__ = 'Razvan Ghitulete (razvan.ghitulete@gmail.com)'

import math
from Vector import Vector3

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def getDistance(self, a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        dz = a.z - b.z
        res = sqrt(dx*dx + dy*dy + dz*dz)
        return res

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Plane:
    def __init__(self, *args):
    	if len(args) == 3:
            #Plane determined by 3 points
            x = args[0]
            y = args[1]
            z = args[2]
            A = Vector3(x.x - y.x, x.y - y.y, x.z - y.z)
            B = Vector3(y.x - z.x, y.y - z.y, y.z - z.z)
            self.normal = normal = A.crossProduct(B)
            self.point = point = x
        elif len(args) == 2:
            self.normal = args[1]
            self.point = args[0]
        else:
            self.normal = Vector3(args[0], args[1], args[2])
       	    if args[0] != 0:
                self.point = Vector3(args[3]/args[0],0,0)
            elif args[1] != 0: 
                self.point = Vector3(0,args[3]/args[1],0)
            else:
                self.point = Vector3(0,0,args[3]/args[2])
                
class Sphere:
    #Determined by the length of the ray and the center of the sphere
    def __init__(self, ray, center):
        self.ray = ray
        self.center = center
        
class Box:
    #Determined by 4 points
    def __init__(self, *args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
        self.u = args[3]
        self.length = self.getDistance(self.x, self.y)
        self.width = self.getDistance(self.x, self.z)
        self.height = self.getDistance(self.x, self.u)

class Cylinder:
    #Determined by the supporting plane, ray and height
    def __init__(self, plane, ray, height):
        self.plane = plane
        self.ray = ray
        self.height = height
