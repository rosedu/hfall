"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

from base import Task
from pyglet import window
from Console import Console
from pyglet import font 
from pyglet import image
from pyglet.gl import *
from Sprite import Sprite
import Mathbase

class Model2D:
    """
    A basic class for any 2D object.

    """
    
    def __init__(self,  x, y, w=2.0, h=2.0, color=(0.0, 0.0, 0.0, 0.0)):
        """
        Model2D class initialization.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        self.x = x
        self.y = y
        self.xx = x + w
        self.yy = y + h
        self.color = color
	
"""
Collection of Event Overrides
"""
global_render = None
global_UI = None

def on_key_press(symbol,modifiers):
	print("Key was pressed!")
	if symbol==window.key.ESCAPE:
		global_render.w.has_exit = True
	elif symbol==window.key.U:
		global_UI.unload_full_text()
		global_UI.unload_full_2DUI()
	elif symbol==window.key.L:
		global_UI.load_full_text()
		global_UI.load_full_2DUI()
	elif symbol==window.key.A:
		global_render.ogl.translate(Mathbase.Vector3D(0,-1,-1))
		

class UI(Task):
  	""" 
	  Contains UI elements including console interaction
	"""

	"""
		External variable list:
		 - surface (Render)
  		 - console (Console)
  	"""
	_width_pt = 0
	_height_pt = 0
	_2Dlist = []
	_textlist = []

	def x_topt(self,x):
		return x*self._width_pt/self.surface.width - self._width_pt/2	

	def y_topt(self,y):
  		return -1.0*y*self._height_pt/self.surface.height + 1.0*self._height_pt/2

	def px_topt(self,px):
  		return 1.0*px/86

	def __init__(self,render):
	  	#Gain access to render
	  	self.surface = render
		global global_render 
		global_render = render
		global global_UI
		global_UI = self

		self._height_pt = 7 
		self._width_pt = 9.2 

		#Load some rectangles/text
		self.testing()

		self.load_full_2DUI()
  		self.load_full_text()

		#Load key events
  		self.surface.w.on_key_press = on_key_press
		
	def load_full_2DUI(self):
	  	for graphic in self._2Dlist:
			self.surface.add2D(graphic)
	
	def unload_full_2DUI(self):
	  	for graphic in self._2Dlist:
			self.surface.rem2D(graphic)
	
	def load_full_text(self):
  		for text in self._textlist:
			self.surface.addtext(text)

  	def unload_full_text(self):
  		for text in self._textlist:
			self.surface.remtext(text)
	
	def load_2DUI(self,x):
  		self._2Dlist.append(x)

  	def unload_2DUI(self,x):
  		self._2Dlist.remove(x)
	
	def load_text(self,x):
	  	self._textlist.append(x)
	
	def unload_text(self,x):
	  	self._textlist.remove(x)


	def start(self,kernel):
	  	pass

	def stop(self,kernel):
	  	pass

	def pause(self,kernel):
	  	pass

	def resume(self,kernel):
	  	pass

	def run(self,kernel):
	  	#Render text
	  	pass
	
	def name(self):
	  	return "UI Process" 
	
	def testing(self):

		self.console_bck = Model2D(self.x_topt(0),self.y_topt(140),\
		    self.px_topt(global_render.width), \
  		    self.px_topt(140),(0.7,0.7,0.9))
		self._2Dlist.append(self.console_bck)

  		self.console = Console()
  		self.console.enable()
  		ft = font.load('Times New Roman',6)
	  	self._textlist.append(font.Text(ft,"console",self.x_topt(0),\
		      self.y_topt(500),0,(0,0.6,0.6,255),0))
		pic = image.load("symbol.jpg")
		width, height = pic.width,pic.height
		subimage = pic.get_region(0, 0, 10, height)
  		self.surface.addgr(pic)
  		sprite = Sprite(-2,-2)
  		


