"""
Hammerfall Terrain class.

"""

__version__ = '0.4'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Parser")
from VertexBuffer import *
import pyglet
from pyglet.gl import *
import array
import itertools

class HeightField:
    """
    This class is used to represent the height field in a easy to use and
    access structure.

    """
    def __init__(self, size = 64):
        self.size = size + 1
        self.vert = [array.array('f', \
                                 itertools.repeat(0.0,\
                                                  self.size))\
                     for i in range(self.size)]
        self.min = 0
        self.max = 0

    def raiseHeight(self, x, y, delta):
        raise NotImplementedError("not implemented yet")

    def lowerHeight(self, x, y, delta):
        raise NotImplementedError("not implemented yet")

    def setHeight(self, x, y, height):
        x = x % self.size
        y = y % self.size
        self.vert[x][y] = height

    def bounds(self):
        m = min(self.vert[0])
        for i in range(1, self.size):
            m = min(self.vert[i], m)
        self.min = m
        m = max(self.vert[0])
        for i in range(1, self.size):
            m = max(self.vert[i], m)
        self.max = m

class TerrainPatch:
    """
    This class is used to represent a terrain patch, allowing for different
    levels of needed terrain detail, if properly constructed.
    
    """

    def __init__(self, size = 64, width = 64, hfield = HeightField(size=64),\
                 x_origin = 0, y_origin = 0):
        """
        size - the width of the patch, in tiles (heightfield resolution)
        width - the width of the patch, in real units

        """
        self.size = size
        self.width = width
        self._hf = hfield
        self.x = x_origin
        self.y = y_origin
        self.stride = float(self.width) / size
        self.visible = False
        self.renderable = False
        self.list = 0;

    def opreparebuffers(self):
        vsize = self.size + 1
        vsize = 3 * (vsize ** 2)
        colors = vsize * [0.5] #gray color for now
        #colors = [0.5, 0.5, 0.5]
        vsize = self.size + 1
        vertices = [0, self._hf.vert[0][0], 0]
        indices = []
        index = 1
        for x in range(1, vsize):
            vertices.extend([x * self.stride, self._hf.vert[x][0], 0])
            #colors.extend([0.5, 0.5, 0.5])
            index += 1
        for y in range(1, vsize):
            vertices.extend([0, self._hf.vert[0][y], y * self.stride])
            index += 1
            for x in range(1, vsize):
                vertices.extend([x * self.stride, self._hf.vert[x][y], y * self.stride])
                #colors.extend([0.5, 0.5, 0.5])
                indices.extend([index, index - vsize - 1, index - vsize,\
                                index, index - 1, index - vsize - 1])
                index += 1
        buffSize = (len(vertices) + len(colors)) * sizeof(GLfloat)
        vbuff = VertexBuffer(buffSize)
        self.verts = VBOArray(len(vertices), GLfloat, vertices, vbuff)
        self.cols = VBOArray(len(colors), GLfloat, colors, vbuff)
        buffSize = len(indices) * sizeof(GLuint)
        self.fbuff = VertexBuffer(buffSize, target = VertexBuffer.ELEMENT_ARRAY_BUFFER)
        self.vbo = VBOArray(len(indices), GLuint, indices, self.fbuff)
        self.ilength = len(indices)
        self.imin = min(indices)
        self.imax = max(indices)
        self.renderable = True

    def makelist(self):
        glPushMatrix()
        width = self.width
        glTranslatef(-width/2, -width/2, 0)
        glBegin(GL_TRIANGLES)
        glColor3f(0.5, 0.5, 0.5)
        vlen = self.stride
        vert = self._hf.vert
        size = self.size
        for y in range(1, size):
            for x in range(1, size):
                glVertex3f(x * vlen, y * vlen, vert[x][y])
                glVertex3f((x-1) * vlen, (y-1) * vlen, vert[x-1][y-1])
                glVertex3f(x * vlen, (y-1) * vlen, vert[x][y-1])

                glVertex3f(x * vlen, y * vlen, vert[x][y])
                glVertex3f((x-1) * vlen, y * vlen, vert[x-1][y])
                glVertex3f((x-1) * vlen, (y-1) * vlen, vert[x-1][y-1])
        glEnd()
        glPopMatrix()

    def preparebuffers(self):
        #deprecated
        self.list = glGenLists(1)
        glDisable(GL_CULL_FACE)
        glNewList(self.list, GL_COMPILE)
        self.makelist()
        glEndList()
        glEnable(GL_CULL_FACE)
        print self.list
        self.renderable = True

    def makeVisible(self):
        if self.renderable == False:
            raise Exception("this terrain patch is not renderable yet, call preparebuffers")
        else:
            self.Visible = True

    def makeInvisible(self):
        self.Visible = False

    def orender(self):
	if self.Visible == True:
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            self.verts.buffer.enable()
            glColorPointer(3, GL_FLOAT, 0, self.cols.pointer())
            glVertexPointer(3, GL_FLOAT, 0, self.verts.pointer())
            self.fbuff.enable()
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisable(GL_NORMAL_ARRAY)
            glDrawRangeElements(GL_TRIANGLES, self.imin, self.imax,\
                                self.ilength, GL_UNSIGNED_INT, self.vbo.pointer())
	    self.verts.buffer.disable()
            self.fbuff.disable()
            glPopMatrix()

    def render(self):
        #deprecated
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glCallList(self.list)
        glPopMatrix()

class Terrain:
    """
    This class is used for terrain rendering.
    
    """
    def __init__(self):
        self._patch = []
        self.enabled = False

    def cullPatches(self):
        raise NotImplementedError("culling not implemented")

    def Enable(self):
        self.enabled = True

    def Disable(self):
        self.enabled = False

    def render(self):
        if self.enabled == True:
            for tpatch in self._patch:
                tpatch.orender()

    def addPatch(self, patch):
        if isinstance(patch, TerrainPatch):
            self._patch.append(patch)
        else:
            raise TypeError("Invalid terrain patch submitted")
