"""
Geometrical Objects classes for later use
"""

__version__ = '0.1'
__author__ = 'Razvan Ghitulete (razvan.ghitulete@gmail.com)'


class Point:
    def __init__(self, x, y, z,):
        self.x = x
        self.y = y
        self.z = z

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Plane:
    def __init__(self, normal, a):
        self.normal = normal
        self.a = a
        
