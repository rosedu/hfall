"""
Hamerfall Render class. All drawings to the screen should be done using
this class. This class also provides a context surface where drawings
could take place via OpenGL or any other rendering API.

"""

__version__ = '0.3'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet import clock
import Vertex
import Mathbase
import OGLbase
import base
from base import kernel as hfk
import UI

class Render(base.Task):
    """
    The Render class. It represents one of the most important task in
    the game.

    """
    
    def __init__(self, width, height, near=0.1, far=100.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0)):
        """
        Render task initialization. It starts pyglet and OpenGL.
            width - the width of the game window
            height - the height of the game window
            near - near distance. All objects closer to the camera than
                    this distance will not be rendered
            far - far distance. All objects farther to the camera than
                    this distance will not be rendered
            clearcolor - the color used for clearing the buffer. Mainly
                    it represents the background color when nothing
                    is drawn over the entire window.

        """
        self._3dlist = []
        self._2dlist = []
        self._angle = 0;
        self._xpos = -1;
        try:
            # Try to create a window with antialising
            # TODO: add other possible config via another parameter
            config = Config(sample_buffers = 1, samples = 4, depth_size = 16,\
                          double_buffer = True, fullscreen = False)
            self.w = window.Window(resizable = True, fullscreen = True, config=config)
        except window.NoSuchConfigException:
            self.w = window.Window(resizable = True, fullscreen = True)
        self.ogl = OGLbase.OGL(self.w, width, height, near, far, clearcolor)
                
    def start(self, kernel):
        """Starting the rendering module"""
        kernel.log.msg('Rendering module started')

    def stop(self, kernel):
        """Stopping the rendering module"""
        kernel.log.msg('Rendering module ended')

    def pause(self, kernel):
        """Pausing the rendering module"""
        pass

    def resume(self, kernel):
        """Resuming the rendering module"""
        pass

    def run(self, kernel):
        """
        The main part of the rendering module. It is used to render all 3D
        game graphics.
        
        """
        if self.w.has_exit:
            # TODO: add a possibility to run kernel modules after the window
            # is closed
            kernel.shutdown()
        else:
            dt=clock.tick()
            self.w.dispatch_events()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            
            # TODO: camera manipulation
            point_to_translate = Mathbase.Vector3D(self._xpos, 0, -6)
            self.ogl.translate( point_to_translate)
            direction_to_rotate = Mathbase.Vector3D(0, 1 ,0)
            self.ogl.rotate(self._angle, direction_to_rotate) 
            # TODO: 3D model drawing
            for vertex in self._3dlist:
                self.ogl.render(GL_TRIANGLES, vertex)
            # TODO: special effects here
            # TODO: save openGL state here
            for model in self._2dlist:
                self.ogl.Render2D(model)
            
            self.w.flip()
            self.fps=clock.get_fps()
            print self.fps
            self._angle += 0.2
            if self._xpos > 3 :
                self._xpos = -3
            self._xpos += 0.05
    def name(self):
        """
        Returns the name of the task for an integration with the kernel

        """
        return 'Render'

    def add2D(self, model):
        """
        This function is used to add a 2D object to the list of the models
        to be drawn. This list keeps the models sorted by the insertion
        order. This way the last inserted object will be drawn on top of
        the others.
            model - the two dimensional object to be added
        
        """
        self._2dlist.append(model)

    def add3D(self, vertexes):
        """
        This function is used to add a 3D model to the list of the
        models to be drawn. This function sorts the list of 3D models
        in a way that lets all model with the same texture to be grouped.
        
        """
        self._3dlist.append(vertexes)
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
