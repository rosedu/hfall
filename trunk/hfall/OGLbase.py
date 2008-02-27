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

    # here we should define different functions to change OpenGL state machine
    # status
    # to do : those functions, after we done 2 and while working on 3
    def translate_to(self, position):

    def render
