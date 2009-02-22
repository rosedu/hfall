"""
Hammerfall Terrain class.

WARNING: This module has OpenGL calls which will be removed in the future.

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import array
import itertools

import pyglet
from pyglet.gl import *

import base

class HeightField:
    """
    This class is used to represent the height field in a easy to use and
    access structure.

    """
    def __init__(self, size = 64):
        """
        size represents the height field resolution
        
        """
        self.size = size + 1
        self.vert = [array.array('f', \
                                 itertools.repeat(0.0,\
                                                  self.size))\
                     for i in range(self.size)]
        self.min = 0
        self.max = 0

    def raiseHeight(self, x, y, delta):
        """
        Use this to modifiy the height of the terrain in a specific point
        
        """
        raise NotImplementedError("not implemented yet")

    def lowerHeight(self, x, y, delta):
        """
        Use this to modify the height of the terrain in a specific point
        
        """
        raise NotImplementedError("not implemented yet")

    def setHeight(self, x, y, height):
        """
        Use this to modify the height of the terrain in a specific point
        
        """
        x = x % self.size
        y = y % self.size
        self.vert[x][y] = height

    def bounds(self):
        """
        Use this to find the extremes of this height field
        
        """
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

    def __init__(self, width = 100, hfield = HeightField(size=64),\
                 x_origin = 0, y_origin = 0):
        """
        size - the width of the patch, in tiles (heightfield resolution)
        width - the width of the patch, in real units
        hfield - the height field of the patch

        """
        self.size = hfield.size - 1
        self.width = width
        self._hf = hfield
        self.x = x_origin
        self.y = y_origin
        self.stride = float(self.width) / self.size
        self.visible = True
        self.vertexList = pyglet.graphics.vertex_list_indexed((self.size + 1)\
                                                              ** 2,\
                                TerrainPatch.buildList(self.size +1),\
                                ('v3f/static', TerrainPatch.buildVert(\
                                    self._hf, self.size + 1, self.stride)),
                                ('c3B/static', ((128, 128, 128) * \
                                                ((self.size + 1) ** 2))))
        
    @staticmethod
    def buildList(size):
        l = []
        for i in range(size + 1, size ** 2):
            if i % size != 0:
                l.extend([i, i - size - 1, i - size, i, i - 1, i - size - 1])
        return l

    @staticmethod
    def buildVert(hf, size, stride):
        l = []
        for y in range(size):
            for x in range (size):
                l.extend([x * stride, hf.vert[x][y], y * stride])
        return tuple(l)

    def render(self):
##        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if self.visible == True:
            glPushMatrix()
            glTranslatef(self.x, 0, self.y)
            self.vertexList.draw(GL_TRIANGLES)
            glPopMatrix()

class Terrain (base.Task):
    """
    We will represent the terrain as another task for debugging purposes and
    more.
    
    """
    def __init__(self, render):
        self.render = render
        self._patch = []
        self.enabled = False

    def start(self, kernel):
        """Starting the Terrain module"""
        kernel.log.msg('Ground for action set.')
        self.enabled = True
        def terrainRender():
            if self.enabled == True:
                for tpatch in self._patch:
                    tpatch.render()
                    pass
        self.render.addRenderingFunction(kernel, terrainRender)

    def stop(self, kernel):
        """Stoping the Terrain module"""
        kernel.log.msg('No more ground.')

    def pause(self, kernel):
        """Pausing the Terrain module"""
        self.enabled = False

    def resume(self, kernel):
        """Resuming the Terrain module"""
        self.enabled = True

    def run(self, kernel):
        """Running the Terrain module - rendering the Terrain"""
        pass
    
    def name(self):
        """Name of the Terrain module"""
        return 'Terrain'

    def cullPatches(self):
        raise NotImplementedError("culling not implemented")

    def addPatch(self, kernel, patch):
        if isinstance(patch, TerrainPatch):
            self._patch.append(patch)
            kernel.log.msg('Patch ' + str(len(self._patch)) + ' added.')
        else:
            raise TypeError("Invalid terrain patch submitted")
