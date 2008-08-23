"""
Hammerfall Terrain class.

"""

__version__ = '0.4'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet
from pyglet.gl import *

class Terrain:
    """
    The Terrain class used for rendering the terrain.

    """

    def __init__(self, heights=[0]*16*16, size=16, dx=1, dz=1, cx=0, cz=0):
        self.H = heights
        self.H[2]=1
        self.H[5]=2
        self.H[8]=-1
        self.size = size
        self.xmin = cx - (size / 2)
        self.zmin = cz - (size / 2)
        if size % 2 == 0:
            self.xmin += (float(dx) / 2)
            self.zmin += (float(dz) / 2)
        self.dx = dx
        self.dz = dz
        self.visible = False

    def render(self):
        glBegin(GL_QUADS)
        glColor3f(0,1,0)
        for i in range(len(self.H)-self.size):
            if (i + 1) % self.size != 0:
                x = (i % self.size) * self.dx + self.xmin
                z = (i / self.size) * self.dz + self.zmin
                glVertex3f(x, self.H[i], z)
                glVertex3f(x, self.H[i + self.size], z + self.dz)
                glVertex3f(x + self.dx, self.H[i + self.size + 1], z + self.dz)
                glVertex3f(x + self.dx, self.H[i + 1], z)
        glEnd()
