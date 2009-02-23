"""
Hamerfall Render class. All drawings to the screen should be done using
this class. This class also provides a context surface where drawings
could take place via OpenGL or any other rendering API. Thus, this module
MUST not contain (and will NOT contain) any OpenGL call (excluding the call
which constructs the OpenGL renderer).

This class must be informed of every instance to be drawn on the screen. Any
2D or 3D object, any model or any point, any modifications of the camera, etc.
must be done using ONLY this class. There are helper classes around but their
instances should not exist outside of the Render.

"""

__version__ = '0.7'
__authors__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)'
import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet import clock
from pyglet import font

import base
import OGLbase
import Camera

class Render(base.Task):
    """
    The Render class. It represents one of the most important task in
    the game.

    """
    
    def __init__(self, width, height, near=0.1, far=100.0, fov=60.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0),\
                 posx = 0, posy = 0, posz = 0):
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
        self.enableAxes = True
        self._dfcts = [] # a list of drawing functions - affected by perspective
        self._dofcts = [] # ortho drawing functions
        try:
            # Try to create a window with antialising
            # TODO: add other possible config via another parameter
            config = Config(sample_buffers = 1, samples = 4, depth_size = 16,\
                          double_buffer = True)
            self.w = window.Window(resizable = True, fullscreen = False,\
                                   config=config, visible = False)
        except window.NoSuchConfigException:
            self.w = window.Window(resizable = True, fullscreen = False,\
                                   visible = False)

        self.ogl = OGLbase.OGL(self, width, height, near, far, fov,\
                               clearcolor)
        self.camera = Camera.Camera(posx,posy,posz)
        self.camera.enable()
        self.batch = pyglet.graphics.Batch()

    def start(self, kernel):
        """Starting the rendering module"""
        kernel.log.msg('Rendering module started')
        self.w.set_visible()

##        @self.w.event
##        def on_draw():
##            self.run(kernel)
##
##        pyglet.app.run()

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
        game graphics. This function is also called at every redraw of the
        application window.
        
        """

        if self.w.has_exit: # exiting totally
            print 'ESC-ing'
            kernel.log.msg('Application ending')
            kernel.shutdown()
        else:
            self.w.dispatch_events()
            #REMEMBER!!!!:
            # NO OPENGL CALLS ARE ALLOWED
            # OUTSIDE OF OGLbase MODULE!!!
            #BEHAVE ACCORDINGLY!!!
            self.ogl.prepareframe() #this will set the viewport to be
                                        # identical to the camera's one
            if self.enableAxes:
                self.ogl.drawAxes()

            for drawingfunction in self._dfcts:
                drawingfunction()

            self.ogl.activateOrtho()
            for drawingfunction in self._dofcts:
                drawingfunction()
            self.batch.draw()
            self.ogl.activatePerspective()

            self.w.flip()

    def name(self):
        """
        Returns the name of the task for an integration with the kernel

        """
        return 'Render'

    def addRenderingFunction(self, kernel, f):
        self._dfcts.insert(0, f)
        kernel.log.msg('Rendering function ' + f.func_name + ' was added to ' +\
                       'the front of the rendering functions list. (' +\
                       str(len(self._dfcts)) + ')')

    def removeRenderingFunction(self, kernel, f):
        if f in self._dfcts:
            self._dfcts.remove(f)
            kernel.log.msg('Rendering function ' + f.func_name + \
                           ' was removed from the rendering functions list. ('\
                           + str(len(self._dfcts)) + ')')

    def addOrthoRenderingFunction(self, kernel, f):
        self._dofcts.insert(0, f)
        kernel.log.msg('Orthographic rendering function ' + f.func_name + \
                       ' was added to the front of the rendering functions' +\
                       ' list. (' + str(len(self._dofcts)) + ')')

    def removeOrthoRenderingFunction(self, kernel, f):
        if f in self._dfcts:
            self._dofcts.remove(f)
            kernel.log.msg('Orthographic rendering function ' + f.func_name + \
                           ' was removed from the rendering functions list. ('\
                           + str(len(self._dofcts)) + ')')

