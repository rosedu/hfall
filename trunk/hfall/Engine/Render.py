"""
Hamerfall Render class. All drawings to the screen should be done using
this class. This class also provides a context surface where drawings
could take place via OpenGL or any other rendering API.

"""

__version__ = '0.3'
__authors__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)'
import math
import pyglet
import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../UI")
from pyglet.gl import *
from pyglet import window
from pyglet import clock

import Mathbase
import OGLbase
import base
from base import kernel as hfk
# import UI

class Render(base.Task):
    """
    The Render class. It represents one of the most important task in
    the game.

    """
    
    def __init__(self, width, height, near=0.1, far=100.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0),\
                 posx = 0, posy = 0, posz = 0,\
                 raw_LightAmbient = [1.0, 1.0, 1.0, 1.0],\
               	 raw_LightDiffuse = [1.0, 1.0, 1.0, 1.0],\
                 raw_LightPosition = [0.0, -1.5, -50.0, 1.0]
                 ):
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
	self._textlist = []
	self.transx = posx;
	self.transy = posy;
        self.transz = posz;
	self.width = width
	self.height = height
	self.LighAmbient = [];
        self.LighDiffuse = [];
      	self.LighPosition = [];
	self.LightAmbient = (GLfloat * 4)(*raw_LightAmbient)
	self.LightDiffuse = (GLfloat * 4)(*raw_LightDiffuse)
	self.LightPosition = (GLfloat * 4)(*raw_LightPosition)
  	self.angle = Mathbase.Vector3D(0,0,0)

        try:
            # Try to create a window with antialising
            # TODO: add other possible config via another parameter
            config = Config(sample_buffers = 1, samples = 4, depth_size = 16,\
                          double_buffer = True)
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
  	    self.ogl.activate_perspective(self.w.width,self.w.height)
  	    self.ogl.activate_model()
            glEnable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glLightfv(GL_LIGHT1, GL_AMBIENT, self.LightAmbient)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, self.LightDiffuse)
            glLightfv(GL_LIGHT1, GL_POSITION, self.LightPosition)
            glEnable(GL_LIGHT1)

            
            # TODO: camera manipulation
            # For dodecadron testing
            point_to_translate = Mathbase.Vector3D(self.transx,\
                                self.transy, self.transz)
            self.ogl.translate( point_to_translate)
            self.ogl.rotate(self.angle.x, Mathbase.Vector3D(1,0,0)) 
            self.ogl.rotate(self.angle.y, Mathbase.Vector3D(0,1,0)) 
            self.ogl.rotate(self.angle.z, Mathbase.Vector3D(0,0,1)) 
            # TODO: 3D model drawing
            for model in self._3dlist:
                self.ogl.Render3D(model)
            # TODO: special effects here
            # TODO: save openGL state here
            for model in self._2dlist:
                self.ogl.Render2D(model)
  	    #Alien code here - text rendering
  	    self.ogl.activate_ortho(0,self.w.width,0,self.w.height)
  	    self.ogl.activate_model()
  	    for text in self._textlist:
	        text.draw()
            
            self.w.flip()
            self.fps=clock.get_fps()
            print self.fps
            "To be deleted later on, examples"
            #self._angle += 0.5
            # if self._xpos > 3 :
            #    self._xpos = -3
            # self._xpos += 0.05
            
    def rotate(self,angle,x,y,z):
         dir_to_rotate = Mathbase.Vector3D(x,y,z)
  	 dir_to_rotate.Norm3D()
	 dir_to_rotate.__multiply_scalar__(angle)
	 self.angle.__add__(dir_to_rotate)

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

    def add3D(self, model):
        """
        This function is used to add a 3D model to the list of the
        models to be drawn. This function sorts the list of 3D models
        in a way that lets all model with the same texture to be grouped.
        
        """
        self._3dlist.append(model)

    def addtext(self,text):
        self._textlist.append(text)

    def remtext(self,x):
        self._textlist.remove(x)
        pass

    def cleartext(self):
        self._textlist = []

    def rem3D(self,x):
        """
        This function is used to remove a 3D object from the drawing list.
        
        """
	self._3dlist.remove(x)
        pass

    def rem2D(self,x):
        """
        This function is used to remove a 2D object from the drawing list.
        
        """
	self._2dlist.remove(x)
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
