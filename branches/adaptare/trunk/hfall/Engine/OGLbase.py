"""
Hamerfall OpenGL class. This class initializes the OpenGL interface and
then draws vertices and lines to the screen, after changing properly the
state of the OpenGL finite-state machine.

WARNING: the following files are reported to have OpenGL calls in them:
    * ./VertexBuffer.py

"""

__version__ = '0.7'
__authors__ = 'Maruseac Mihai (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)' ,\
              'Valentin Priescu (vali_shooter@yahoo.com)'
import sys
sys.path.insert(0, "..")

import pyglet

from base import kernel as hfk
from Coordinate import Coordinate
from Matrix import *
from Vector import *

class OGL:
    """
    This is the class that encapsulates all OpenGL API calls. All access
    to the OpenGL interface should be done using this class.

    """

    def __init__(self, render, width, height, near=0.1, far=100.0, fov = 60.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0)):
        """
        OpenGL and pyglet initialization.
            w - the window which provides the rendering surface
            width - the width of the game window
            height - the height of the game window
            near - minimum distance. All objects closer to the camera than
                   this distance will not be rendered
            far - maximum distance. All objects further away from the camera than
                  this distance will not be rendered
            clearcolor - the color used for clearing the buffer. Mainly
                         it represents the background color when nothing
                         is drawn over the entire window.
                    
        """
	self.far = far
	self.near = near
	self.fov = fov

        self.render = render
        self.w = render.w
        @self.w.event
        def on_resize(width, height):
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if height == 0:
                height = 1
            gluPerspective(fov, width / float(height), near, far)
            glMatrixMode(GL_MODELVIEW)
            OGL.setModelViewMatrix(render.camera.modelView)
            return pyglet.event.EVENT_HANDLED

        # finalizing the initialization
        glClearColor(clearcolor[0], clearcolor[1], clearcolor[2], \
                     clearcolor[3])
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
 	glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        hfk.log.msg('Open GL started')

    def prepareframe(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        OGL.setModelViewMatrix(self.render.camera.modelView)

    def drawAxes(self):
        pyglet.graphics.draw_indexed(12, GL_LINES, range(12),\
                        ('v3f', ( 0, 0, 0,\
                                100, 0, 0,\
                                  0, 0, 0,\
                                -100, 0, 0,\
                                  0, 0, 0,\
                                  0, 100, 0,\
                                  0, 0, 0,\
                                  0, -100, 0,\
                                  0, 0, 0,\
                                  0, 0, 100,\
                                  0, 0, 0,\
                                  0, 0, -100)),\
                        ('c3B', (255, 0, 0,\
                                 255, 0, 0,\
                                 0, 255, 255,\
                                 0, 255, 255,\
                                 0, 255, 0,\
                                 0, 255, 0,\
                                 255, 0, 255,\
                                 255, 0, 255,\
                                 0, 0, 255,\
                                 0, 0, 255,\
                                 255, 255, 0,\
                                 255, 255, 0)))

    @staticmethod
    def setModelViewMatrix(matrix):
        glMatrixMode(GL_MODELVIEW)
        OGL.oglLoadMatrix(matrix)

    @staticmethod
    def oglVertex(vector):
        if isinstance(vector, Vector2):
            glVertex2f(vector[0], vector[1])
        elif isinstance(vector, Vector3):
            glVertex3f(vector[0], vector[1], vector[2])
        elif isinstance(vector, Vector4):
            glVertex4f(vector[0], vector[1], vector[2], vector[4])
        elif isinstance(vector, list):
            if len(vector) == 2:
                glVertex2fv((GLfloat*2)(*vector))
            elif len(vector) == 3:
                glVertex3fv((GLfloat*3)(*vector))
            elif len(vector) == 4:
                glVertex4fv((GLfloat*4)(*vector))

    @staticmethod
    def oglColor(color):
        if isinstance(color, Vector3):
            glColor3f(color[0], color[1], color[2])
        elif isinstance(color, Vector4):
            glColor4f(color[0], color[1], color[2], color[3])
        elif isinstance(color, list):
            if len(color) == 3:
                glColor3fv((GLfloat*3)(*color))
            elif len(color) == 4:
                glColor4fv((GLfloat*4)(*color))

    @staticmethod
    def oglNormal(normal):
        if isinstance(normal, Vector3):
            glNormal3f(normal[0], normal[1], normal[2])
        elif isinstance(normal, list):
            if len(normal) == 3:
               glNormal3fv((GLfloat*3)(*normal))

    @staticmethod
    def oglTexCoord(tex):
        if isinstance(tex, Vector2):
            glTexCoord2f(tex[0], tex[1])
        if isinstance(tex, Vector2):
            glTexCoord3f(tex[0], tex[1], tex[2])
        if isinstance(tex, Vector2):
            glTexCoord4f(tex[0], tex[1], tex[2], tex[3])
        elif isinstance(tex, list):
            if len(tex) == 2:
                glTexCoord2fv((GLfloat*2)(*tex))
            if len(tex) == 2:
                glTexCoord3fv((GLfloat*3)(*tex))
            if len(tex) == 2:
                glTexCoord4fv((GLfloat*4)(*tex))

    @staticmethod
    def oglMultiTexCoord(unit, tex):
        if isinstance(tex, Vector2):
            glMultiTexCoord2fARB(unit, tex[0], tex[1])
        if isinstance(tex, Vector2):
            glMultiTexCoord3fARB(unit, tex[0], tex[1], tex[2])
        if isinstance(tex, Vector2):
            glMultiTexCoord4fARB(unit, tex[0], tex[1], tex[2], tex[3])
        elif isinstance(tex, list):
            if len(tex) == 2:
                glMultiTexCoord2fvARB(unit, (GLfloat*2)(*tex))
            if len(tex) == 3:
                glMultiTexCoord3fvARB(unit, (GLfloat*3)(*tex))
            if len(tex) == 4:
                glMultiTexCoord4fvARB(unit, (GLfloat*4)(*tex))

    @staticmethod
    def oglGetVector2(name):
        v = (GLfloat*4)(*[])
        glGetFloatv(name, v)
        return Vector2(v[0], v[1])

    @staticmethod
    def oglGetVector3(name):
        v = (GLfloat*4)(*[])
        glGetFloatv(name, v)
        return Vector3(v[0], v[1], v[2])

    @staticmethod
    def oglGetVector4(name):
        v = (GLfloat*4)(*[])
        glGetFloatv(name, v)
        return Vector4(v[0], v[1], v[2], v[3])

    @staticmethod
    def oglGetMatrix(name):
        m = (GLfloat*16)(*[])
        glGetFloatv(name, m)
        return Matrix4(m).transpose()

    @staticmethod
    def oglLoadMatrix(matrix4):
        m = matrix4
        if isinstance(matrix4, Coordinate):
            m = matrix4.matrix()
        elif isinstance(matrix4, list):
            m = Matrix4(matrix4)
        if isinstance(m, Matrix4):
            transp = (GLfloat * 16)(*[])
            for i in range(4):
                for j in range(4):
                    transp[4*i+j] = m[j][i]
            m = transp
        glLoadMatrixf(m)

    @staticmethod
    def oglMultMatrix(matrix4):
        m = matrix4
        if isinstance(matrix4, Coordinate):
            m = matrix4.matrix()
        elif isinstance(matrix4, list):
            m = Matrix4(matrix4)
        if isinstance(m, Matrix4):
            transp = (GLfloat * 16)(*[])
            for i in range(4):
                for j in range(4):
                    transp[4*i+j] = m[j][i]
            m = transp
        glMultMatrixf(m)

    @staticmethod
    def oglLoadInvMatrix(matrix4):
        if isinstance(matrix4, Matrix4):
            inverse = matrix4.inverse()
        if isinstance(matrix4, Coordinate):
            inverse = matrix4.inverseMatrix()
        else: inverse = matrix4
        glLoadMatrix(inverse)

    @staticmethod
    def oglMultInvMatrix(matrix4):
        if isinstance(matrix4, Matrix4):
            inverse = matrix4.inverse()
        if isinstance(matrix4, Coordinate):
            inverse = matrix4.inverseMatrix()
        else: inverse = matrix4
        glMultMatrix(inverse)

    @staticmethod
    def oglDisableAllTextures():
        if not glInfo:
            glInfo = gl_info.GLInfo()
            glInfo.set_active_context()
        
        glDisable(GL_TEXTURE_1D)
        glDisable(GL_TEXTURE_2D)
        if glInfo.have_extension("GL_EXT_texture3D"):
            glDisable(GL_TEXTURE_3D)
        if glInfo.have_extension("GL_EXT_texture_cube_map"):
            glDisable(GL_TEXTURE_CUBE_MAP_ARB)
        if glInfo.have_extension("GL_EXT_texture_rectangle"):
            glDisable(GL_TEXTURE_RECTANGLE_ARB)

    def activateOrtho(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.w.width, 0, self.w.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

    @staticmethod
    def activatePerspective():
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
