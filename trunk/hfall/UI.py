"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

from base import Task
from pyglet import window
from Console import Console
from Sprite import Sprite
from pyglet import font 
from pyglet import image
from pyglet.gl import *
import Mathbase

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
                """
		self.console_bck = Sprite(self.x_topt(0),self.y_topt(140),\
		    self.px_topt(global_render.width), \
  		    self.px_topt(140),None,(0.3,0.3,0.7))
		self._2Dlist.append(self.console_bck)
                """
  		txt = Sprite(0,0,2,2,"test.bmp")
		self._2Dlist.append(txt)
		txt2 = Sprite(-3,-3,2,2,"test2.bmp")
		self._2Dlist.append(txt2)
		txt3 = Sprite(-2,0,1,1,"test3.bmp")
		self._2Dlist.append(txt3)
		txt4 = Sprite(1,-2.5,1,1,"test4.bmp")
		self._2Dlist.append(txt4)
		txt5 = Sprite(3,-2.5,1,1,"test5.bmp")
		self._2Dlist.append(txt5)
