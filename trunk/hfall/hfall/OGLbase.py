"""
Hamerfall OpenGL class. This class initializes the OpenGL interface and
then draws vertices and lines to the screen, after changing properly the
state of the OpenGL finite-state machine. Also this module contains all
code needed to initialize pygame and use it.

"""

__version__ = '0.2'
__author__ = 'Maruseac Mihai (mihai.maruseac@gmail.com)'

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import Mathbase
import Vertex


class OGL:
    """
    This is the class that encapsulates all OpenGL API calls. All acces
    to the OpenGL interface should be done using this class.

    """

    def __init__(self, width, height, video_flags, near=0.1, far=100.0, \
                 clearcolor=(0.0, 0.0, 0.0, 0.0)):
        """
        OpenGL and pygame initialization.
            width - the width of the game window
            height - the height of the game window
            video_flags - consult pygame documentation for those
            near - near distance. All objects closer to the camera than
                    this distance will not be rendered
            far - far distance. All objects farther to the camera than
                    this distance will not be rendered
            clearcolor - the color used for clearing the buffer. Mainly
                    it represents the background color when nothing
                    is drawn over the entire window.

        """
        self._clearcolor=clearcolor
        pygame.init()
        pigame.display.set_mode((width, height), video_flags)

        # resizing
        if height == 0:
            height = 1
        if near == 0.0:
            near = 0.1 # tricks to prevent division by 0
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0 * width / height, near, far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # finalizing the initialization
        glShadeModel(GL_SMOOTH)
        glClearColor(self._clearcolor)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    # here we should define different functions to change OpenGL state
    # machine status. We should built functions to incrementally change
    # the status (like translate) or that change from the start the
    # status (translate to). Also we will need functions to save a state
    # and revert to it after a given period of time.
    # TODO: those functions, after we done 2 and while working on 3
    
    def translate_to(self, position):
        """
        Translates all points with the position vector, starting from
        the identity position - the position that OpenGL state machine
        starts with.

        """
        glLoadIdentity()
        glTranslatef(position.x, position.y, position.z)

    def translate(self, position):
        """
        Does an incremental translation. Translates the current axes by
        the position vector.

        """
        glTranslatef(position.x, position.y, position.z)
        
    def render(self, mode, vertexes):
        """
        The render function of the OpenGL.
            mode - one of the OpenGL drawing primitives
            vertexes - a list containing all the vertices to be drawn on
                       screen in proper order. All elements in the list
                       should be of Vertex type

        """
        # TODO: a verification for the vertexes list's elements format
        glBegin(mode)
        for vertex in vertexes:
            if vertex.color is not None:
                if len(vertex.color) == 3:
                    glColor3f(vertex.color[0], vertex.color[1], vertex.color[2])
                else:
                    glColor4f(vertex.color[0], vertex.color[1], vertex.color[2],\
                              vertex.color[3])
            if vertex.texture is not None:
                if len(vertex.texture) == 1:
                    glTexCoord1f(vertex.texture[0])
                else:
                    glTexCoord2f(vertex.texture[0], vertex.texture[1])
            if vertex.normal is not None:
                glNormal3f(vertex.normal.x, vertex.normal.y, vertex.normal.z)
            if len(vertex.position) == 2:
                glVertex2f(vertex.position[0], vertex.position[1])
            elif len(vertex.position) == 3:
                glVertex3f(vertex.position[0], vertex.position[1],\
                           vertex.position[2])
            else:
                glVertex4f(vertex.position[0], vertex.position[1],\
                           vertex.position[2], vertex.position[3])
        glEnd()
        
