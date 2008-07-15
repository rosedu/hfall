"""
Hamerfall Mesh class. This class holds information about each mesh
used to draw our models to screen. 

"""

__version__ = '0.001'
__author__ = 'Andrei Buhaiu(andreibuhaiu@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
import pyglet
import ctypes
from pyglet.gl import *
from OGLbase import OGL as RenderDevice

class Mesh:

    class Triangles:
    
        def __init__(self, faces, material):
            self.faces = faces
            self.material = material
        
    """
    This is our Model class. It includes the faces, vertices, materials,
    persepctive matrix, colors and draw mode of each mesh.

    """

    
    def __init__(self, vert, texels, tri, matrix, color = None, draw_mode = GL_TRIANGLES):
        
        """
        faces       - the faces formed with the vertices
        vertices    - the actual vertices that give the mesh
        materials   - the materials that are used for each mesh
        matrix4     - the perspective matrix
        colors      - the color that we use if there's no material given
        mode        - the draw mode for OpenGL this can be GL_TRIANGLES,
                      GL_QUADS, and so forth

        """

        self.vertices = vert
        self.texels = texels
        self.triangles = tri
        self.matrix4 = matrix
        self.colors = color
        self.mode = draw_mode

    def init(self):
        colors = (len(self.vertices))* [1, 1, 1]
        pcolors = (GLfloat *len(colors))(*colors)
        pvertices = (GLfloat * len(self.vertices))(*self.vertices)
        ptexels = (GLfloat *len(self.texels))(*self.texels)
        for i in range(0, len(self.triangles)):
            pfaces = (GLuint * len(self.triangles[i].faces))(*self.triangles[i].faces)
            self.triangles[i].faces = pfaces
        self.vertices = pvertices
        self.colors = pcolors
        self.texels = ptexels

    def render(self, renderDevice):
        renderDevice.pushMatrix()
        renderDevice.colorPointer(self.colors)
        renderDevice.vertexPointer(self.vertices)
        renderDevice.TexCoordPointer(self.texels)
        for faces in self.triangles:
            renderDevice.setTexture(faces.material)
            renderDevice.DrawElements(faces.faces, self.mode)
        renderDevice.popMatrix()
        
