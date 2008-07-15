"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

from base import Task
from pyglet import window
from pyglet.window import *
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

def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
  	if global_UI.mouse_enabled==True:
		factor = 1
		global_render.rotate(factor,0,0,dx)
  		pass


def on_mouse_motion(x,y,dx,dy):
  	if global_UI.mouse_enabled==True:
  		factor = 1
		global_render.rotate(factor,-dy,dx,0)
  	
def on_key_press(symbol,modifiers):
	if global_UI.input_handler == "Engine":
                engine_get(symbol,modifiers)
        elif global_UI.input_handler == "Console":
                console_get(symbol,modifiers)
        else:
                game_get(symbol,modifiers)

def engine_get(symbol,modifiers):
	if symbol==window.key.ESCAPE:
		global_render.w.has_exit = True
	elif symbol==window.key.U:
		global_UI.unload_full_2DUI()
	elif symbol==window.key.L:
		global_UI.load_full_2DUI()
	elif symbol==window.key.A:
		global_render.ogl.translate(Mathbase.Vector3D(0,-1,-1))
        elif symbol==window.key.QUOTELEFT:
                global_UI.switch_focus()
  	elif symbol==window.key.M:
  		global_UI.mouse_enabled = not global_UI.mouse_enabled
"""
        elif symbol==window.key.UP:
                global_render._angle+=1
        elif symbol==window.key.DOWN:
                global_render._angle-=1
        elif symbol==window.key.W:
                global_render.transz+=1
        elif symbol==window.key.S:
                global_render.transz-=1
"""
                
		
def console_get(symbol,modifiers):
        if symbol==window.key.QUOTELEFT:
                global_UI.switch_focus()
        elif symbol==window.key.ESCAPE:
                global_UI.switch_focus()


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
	_width_pt = 0
	_height_pt = 0
	_2Dlist = []
	_frozen = False
	input_handler = ""
	path_console_gr = "console.bmp"
	path_engine_gr = "engine.bmp"
	path_game_gr = ""
	console_sprite = None
	engine_sprite = None
	game_sprite = None
	current_sprite = None
	keyboard = None
	mouse_enabled = True

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

		#Load events
  		self.surface.w.on_key_press = on_key_press
		self.surface.w.on_mouse_motion = on_mouse_motion
		self.surface.w.on_mouse_drag = on_mouse_drag

		#Control goes to engine
  		self.console_sprite = Sprite(3.3,-3.3,1,0.5,self.path_console_gr)
  		self.engine_sprite = Sprite(3.3,-3.3,1,0.5,self.path_engine_gr)
  		self.load_2DUI(self.engine_sprite)
  		self.current_sprite = self.engine_sprite
  		self.switch_focus("Engine")

                self.keyboard = key.KeyStateHandler()
                global_render.w.push_handlers(self.keyboard)
                
  		self.load_full_2DUI()
  		
	def load_full_2DUI(self):
                if self._frozen == False:
                        return
	  	for graphic in self._2Dlist:
			self.surface.add2D(graphic)
		self._frozen = False
	
	def unload_full_2DUI(self):
                if self._frozen == True:
                        return
	  	for graphic in self._2Dlist:
			self.surface.rem2D(graphic)
		self._frozen = True
	
	def load_2DUI(self,x):
                if self._frozen == False:
                        self.surface.add2D(x)
  		self._2Dlist.append(x)

  	def unload_2DUI(self,x):
                if self._frozen == False:
                        self.surface.rem2D(x)
  		self._2Dlist.remove(x)
                

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
	  	pass
	
	def name(self):
	  	return "UI Process"

	def switch_focus(self,target=""):
                self.unload_2DUI(self.current_sprite)
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
                        self.current_sprite = self.engine_sprite
                        self.load_2DUI(self.current_sprite)
                elif self.input_handler=="Console":
                        self.current_sprite = self.console_sprite
                        self.load_2DUI(self.current_sprite)
                elif self.game_sprite != None:
                        self.current_sprite = self.game_sprite
                        self.load_2DUI(self.current_sprite)
                        
                        
                        
                
                        
	def testing(self):
                """
		self.console_bck = Sprite(self.x_topt(0),self.y_topt(140),\
		    self.px_topt(global_render.width), \
  		    self.px_topt(140),None,(0.3,0.3,0.7))
		self._2Dlist.append(self.console_bck)
                """
  		txt = Sprite(0,0,2,2,"test.bmp")
		self.load_2DUI(txt)
		
