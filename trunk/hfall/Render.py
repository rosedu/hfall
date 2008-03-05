"""
Hamerfall Render class. All drawings to the screen should be done using
this class.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import time
import Vertex
import Mathbase
import OGLbase
import base
import base
from base import kernel as hfk

class Render(base.Task):
    """
    The Render class. It represents one of the most important task in
    the game.

    """
    def __init__(self, width, height, video_flags, near=0.1, far=100.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0)):
        """
        Render task initialization. It starts pygame and OpenGL behind.
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
        self.ogl=OGLbase.OGL(width, height, video_flags, near, far, clearcolor)
        hfk.log.msg('Rendering module started')

    def start(self):
        """Starting the rendering module"""
        pass

    def stop(self):
        """Stopping the rendering module"""
        hfk.log.msg('Rendering module ended')

    def pause(self):
        """Pausing the rendering module"""
        pass

    def resume(self):
        """Resuming the rendering module"""
        pass

    def run(self):
        """
        The main part of the rendering module. It is used to render all 3D
        game graphics.
        
        """
        pass
        # TODO: to be done later, after loading the model

    def name(self):
        """
        Returns the name of the task for an integration with the kernel

        """
        return 'Render'

    def Render2D():
        """
        This function is used to render any 2D graphic, mainly used for
        rendering the user interface.

        """
        pass

# TODO: not completed yet
