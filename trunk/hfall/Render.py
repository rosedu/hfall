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
        self._3dlist=[]
        self._2dlist=[]
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

    def Render2D(x, y, w=32.0, h=32.0, color=(0.0, 0.0, 0.0, 0.0)):
        """
        This function is used to render any 2D graphic, mainly used for
        rendering the user interface.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        # TODO: to save OpenGL state
        glTranslate2f(x, y)
        if len(color) == 3:
            glColor3f(color[0], color[1], color[2])
        else:
            glColor4f(color[0], color[1], color[2], color[3])
        # TODO: revert to old state
        pass

    def add2D(self, x, y, w=32.0, h=32.0, color=(0.0, 0.0, 0.0, 0.0)):
        """
        This function is used to add a 2D object to the list of the models
        to be drawn. This list keeps the models sorted by the insertion
        order. This way the last inserted object will be drawn on top of
        the others.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.
        
        """

    def add3D(self):
        """
        This function is used to add a 3D model to the list of the
        models to be drawn. This function sorts the list of 3D models
        in a way that lets all model with the same texture to be grouped.
        
        """
        pass
        # TODO: to be done later after loading the model

    def rem3D(self):
        """
        This function is used to remove a 3D object from the drawing list.
        
        """
        # TODO: to be done later after loading the model
        pass

    def rem2D(self):
        """
        This function is used to remove a 2D object from the drawing list.
        
        """
        # TODO: to be done later
        pass

    def clear3D(self):
        """
        A faster way to clear the 3D models list.
        
        """
        self._3dlist=[]

    def clear2D(self):
        """
        A faster way to clear the 2D models list.
        
        """
        self._2dlist=[]
