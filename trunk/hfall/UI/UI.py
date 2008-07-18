"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.3'
__author__ = 'Sergiu Costea (sergiu.costea@gmail.com)'


import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
from base import Task
from pyglet import window
from pyglet.window import *
import Console
import Sprite
from pyglet import font 
from pyglet import image
from pyglet.gl import *
import Mathbase
from Console import Console

"""
Collection of Event Overrides
"""
global_render = None
global_UI = None

def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
  	factor=3
  	if global_UI.mouse_enabled==True and buttons==window.mouse.RIGHT:
		global_render.rotate(factor,0,0,dx)
  		pass
	if global_UI.mouse_enabled==True and buttons==window.mouse.LEFT:
	  	global_render.rotate(factor,-dy,dx,0)


def on_mouse_motion(x,y,dx,dy):
  	factor=1
  	#if global_UI.mouse_enabled==True:
	#	global_render.rotate(factor,-dy,dx,0)
  	
def on_key_press(symbol,modifiers):
	if global_UI.input_handler == "Engine":
                engine_get(symbol,modifiers)
        elif global_UI.input_handler == "Console":
                console_get(symbol,modifiers)
        else:
                game_get(symbol,modifiers)

def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT and modifiers & key.LCTRL:
                print "Combo pressed!"
                
def engine_get(symbol,modifiers):
	if symbol==window.key.ESCAPE:
		global_render.w.has_exit = True
	elif symbol==window.key.TAB:
		if global_UI.loaded_UI:
			global_UI.unload_full_2DUI()
		else:
			global_UI.load_full_2DUI()
	elif symbol==window.key.A:
		global_render.ogl.translate(Mathbase.Vector3D(0,-1,-1))
        elif symbol==window.key.QUOTELEFT:
                global_UI.switch_focus()
  	elif symbol==window.key.M:
  		global_UI.mouse_enabled = not global_UI.mouse_enabled
	elif symbol==window.key.F2:
	  	global_UI.console.toggle_visible()
        elif symbol==window.key.X:
                global_render.enableaxis = not global_render.enableaxis
		
def console_get(symbol,modifiers):
        if symbol==window.key.QUOTELEFT:
                global_UI.switch_focus()
        elif symbol==window.key.ESCAPE:
                global_UI.switch_focus()
	elif symbol==window.key.F2:
	       	global_UI.console.toggle_visible()
	elif symbol in global_UI.console.valid_chars:
	        global_UI.console.read(symbol,modifiers)

def game_get(symbol,modifiers):
        pass

def check_keyboard(keyboard):
  	if global_UI.input_handler=="Engine":
        	if keyboard[key.W]:
                	global_render.transz+=1
        	elif keyboard[key.S]:
                	global_render.transz-=1
        	elif keyboard[key.A]:
                	global_render.transx+=1
        	elif keyboard[key.D]:
                	global_render.transx-=1
   		elif keyboard[key.Q]:
   			global_render.transy+=1
   		elif keyboard[key.E]:
   			global_render.transy-=1
class UI(Task):
  	""" 
	  Contains UI elements including console interaction
	"""

	"""
		External variable list:
		 - surface (Render)
  		 - console (Console)
  	"""
	_2Dlist = []
	_textlist = []
	_frozen = False
	input_handler = ""
	console_text = None
	engine_text = None
	game_text = None
	current_text = None
	keyboard = None
	mouse_enabled = True
	loaded_UI = False
	console = None

	#Fonts & UI Elements
	f_header = None
	f_small = None
	f_large = None

	#Colors
	C_WHITE = (1,1,1,1)
  	C_YELLOW = (1,1,0,1)
  	C_GRAY = (0.5,0.5,0.5,1)
  	C_LIGHTGRAY = (0.8,0.8,0.8,1)
  	C_RED = (1,0,0,1)

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

		#Load events
  		self.surface.w.on_key_press = on_key_press
		self.surface.w.on_mouse_motion = on_mouse_motion
		self.surface.w.on_mouse_drag = on_mouse_drag
		self.surface.w.on_mouse_press = on_mouse_press

		#Control goes to engine
		self.f_header = font.load("Helvetica",18)

  		self.console_text = font.Text(self.f_header,"Console Mode",\
		    global_render.w.width-20,20,halign=font.Text.RIGHT,\
		    valign = font.Text.BOTTOM,color = self.C_WHITE)
  		self.engine_text = font.Text(self.f_header,"Engine Mode",\
		    global_render.w.width-20,20,halign=font.Text.RIGHT,\
		    valign = font.Text.BOTTOM,color = self.C_WHITE)
  		self.current_text = self.engine_text
		self.load_2Dtext(self.current_text)
  		self.switch_focus("Engine")

		self.add_fps()
		self.loaded_UI = True
		self.console = Console(0,200,self.C_GRAY,self.C_LIGHTGRAY,self.C_YELLOW,self.C_RED)

                self.keyboard = key.KeyStateHandler()
                global_render.w.push_handlers(self.keyboard)
                
  		self.load_full_2DUI()
  		
  		
	def load_full_2DUI(self):
                if self._frozen == False:
                        return
	  	for graphic in self._2Dlist:
			self.surface.add2D(graphic)
		for text in self._textlist:
			self.surface.addtext(text)
		self._frozen = False
		self.loaded_UI = True
	
	def unload_full_2DUI(self):
                if self._frozen == True:
                        return
	  	for graphic in self._2Dlist:
			self.surface.rem2D(graphic)
		for text in self._textlist:
			self.surface.remtext(text)
		self._frozen = True
		self.loaded_UI = False
	
	def load_2DUI(self,x):
                if self._frozen == False:
                        self.surface.add2D(x)
  		self._2Dlist.append(x)

  	def unload_2DUI(self,x):
                if self._frozen == False:
                        self.surface.rem2D(x)
  		self._2Dlist.remove(x)
             
	def load_2Dtext(self,x):
                if self._frozen == False:
                        self.surface.addtext(x)
  		self._textlist.append(x)

  	def unload_2Dtext(self,x):
                if self._frozen == False:
                        self.surface.remtext(x)
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
                check_keyboard(self.keyboard)
		self.refresh_fps()
	  	pass
	
	def name(self):
	  	return "UI Process"

	def switch_focus(self,target=""):
                self.unload_2Dtext(self.current_text)
                print "Old: "+ self.input_handler
                if target=="Engine":
                        self.input_handler = "Engine"
                elif target=="Game":
                        self.input_handler = "Game"
                elif target=="Console":
                        self.input_handler = "Console"
                elif target!="":
                        pass
                        kernel.log.error("Unknown focus switch parameter: " + \
                                        target)
                elif self.input_handler == "Console":
                        self.input_handler = "Engine"
                elif self.input_handler == "Engine":
                        self.input_handler = "Console"
                else:
                        kernel.log.error("Warning - unsafe focus switch" + \
                                         " operation not completed.")
                        pass
                print "New: " + self.input_handler
                
                if self.input_handler=="Engine":
                        self.current_text = self.engine_text
                        self.load_2Dtext(self.current_text)
                elif self.input_handler=="Console":
                        self.current_text= self.console_text
                        self.load_2Dtext(self.current_text)
                elif self.game_text!= None:
                        self.current_text = self.game_text
                        self.load_2Dtext(self.current_text)
                        
	def add_fps(self):
  		self.fps = font.Text(self.f_header,global_render.fps,\
		    25,60,halign=font.Text.LEFT,\
		    valign = font.Text.BOTTOM,color = self.C_YELLOW)
		self.load_2Dtext(self.fps)

	def refresh_fps(self):
	  	self.fps.text = "fps : %d" % (global_render.fps)

	def testing(self):
  		self.helv = font.load('Helvetica',22)
		self.text = font.Text(self.helv,"Hammerfall Graphics Engine",\
		    20,20,halign = font.Text.LEFT,\
		    valign = font.Text.BOTTOM,color = (1,1,1,1))
		global_render.addtext(self.text)
  		pass
		
