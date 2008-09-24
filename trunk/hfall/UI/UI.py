"""
Hammerfall user interface module. Useful for rendering menus, buttons,
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
import Wires
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
                mat_proj = (GLdouble * 16)()
                mat_model = (GLdouble * 16)()
                mat_view = (GLint* 4)()
                glGetDoublev(GL_PROJECTION_MATRIX,mat_proj)
                glGetDoublev(GL_MODELVIEW_MATRIX,mat_model)
                glGetIntegerv(GL_VIEWPORT,mat_view)
                world_x = (GLdouble * 1)()
                world_y = (GLdouble * 1)()
                world_z = (GLdouble * 1)()
		world_x2 = (GLdouble * 1)()
		world_y2 = (GLdouble * 1)()
		world_z2 = (GLdouble * 1)()
                if gluUnProject(x,y,-5,mat_model,mat_proj,mat_view,\
                     world_x,world_y,world_z) == GLU_FALSE:
                        print "Error in UI.on_mouse_press - projection results" + \
                              "are not valid"
		if gluUnProject(x,y,5,mat_model,mat_proj,mat_view,\
		     world_x2,world_y2,world_z2) == GLU_FALSE:
		        print "Error in UI.on_mouse_press - projection results" + \
			      "are not valid"
		# Folosim ecuatiile parametrice ale dreptei in spatiu 
		factor = 100
		x1 = world_x[0] + factor * (world_x2[0]-world_x[0])
		x2 = world_x[0] - factor * (world_x2[0]-world_x[0])
		y1 = world_y[0] + factor * (world_y2[0]-world_y[0])
		y2 = world_y[0] - factor * (world_y2[0]-world_y[0])
		z1 = world_z[0] + factor * (world_z2[0]-world_z[0])
		z2 = world_z[0] - factor * (world_z2[0]-world_z[0])
  		
		global_render.line_manager.add(Wires.Line(x1,y1,z1,z2,y2,z2))
                global_UI.refresh_world_coords(world_x[0],world_y[0],world_z[0])
        
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
	else:
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
   	if global_UI.input_handler=="Console":
   		global_UI.console.read_hold(keyboard)
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

		

		#Load events
  		self.surface.w.on_key_press = on_key_press
		self.surface.w.on_mouse_motion = on_mouse_motion
		self.surface.w.on_mouse_drag = on_mouse_drag
		self.surface.w.on_mouse_press = on_mouse_press

		#Control goes to engine
		self.f_header = font.load("Helvetica",18)
		self.f_small = font.load("Helvetica",12)
		self.f_large = font.load("Helvetica",22)

                #Load some rectangles/text
		self.testing()
		
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
		self.add_world_coords()
		self.loaded_UI = True
		self.console = Console(400,200,self.C_GRAY,self.C_LIGHTGRAY,self.C_YELLOW,self.C_RED)

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
		self.console.shutdown()
	  	pass

	def pause(self,kernel):
	  	pass

	def resume(self,kernel):
	  	pass

	def run(self,kernel):
                check_keyboard(self.keyboard)
		self.refresh_fps()
		self.console.input_clock()
	  	pass
	
	def name(self):
	  	return "UI Process"

	def switch_focus(self,target=""):
                self.unload_2Dtext(self.current_text)
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
		    global_render.w.width-20,global_render.w.height-60,\
		    halign=font.Text.RIGHT,\
		    valign = font.Text.TOP,color = self.C_YELLOW)
		self.load_2Dtext(self.fps)

        def add_world_coords(self):
                self.world_coords = font.Text(self.f_small,"",\
                        global_render.w.width-20,global_render.w.height-90,\
                        halign=font.Text.RIGHT,\
                        valign = font.Text.TOP,color = self.C_YELLOW)
                self.load_2Dtext(self.world_coords)

        def refresh_world_coords(self,x,y,z):
                self.world_coords.text = "COORDS=("+str(x)+","+str(y)+","+str(z)+")"
                
	def refresh_fps(self):
	  	self.fps.text = "fps : %d" % (global_render.fps)

	def testing(self):
		self.text = font.Text(self.f_large,"Hammerfall Graphics Engine",\
		    global_render.w.width-20,global_render.w.height-20,halign = font.Text.RIGHT,\
		    valign = font.Text.TOP,color = (1,1,1,1))
		global_render.addtext(self.text)
  		pass

class LightWidget:
    """
    Base class for all OpenGL debugging LightWidgets
    """

    def __init__(self, x, y, width, height, font_name='Helvetica', size=10,\
                  bck_color = (0.9,0.9,0.9,1.0), text_color = (0.0,0.0,0.0,1.0)):
        """
        Initialize all the default widget properties like position,
        size, background and foreground color, and other generic
        properties
        """
        #Ortho coords
        self._x, self._y = x,y
        
        #Ortho dimensions
        self._width, self._height = width, height
        
        #Font loader
        self._size = size
        self._font = font.load(font_name,size)
        
        #Other properties
        self._line_color = bck_color
        self._text_color = text_color
        self._loaded = False
        
        self._line = Sprite.Sprite(self._x, self._y, self._width,\
                            self._height, None, self._line_color)
        self._text = font.Text(self._font, "", self._x, self._y,\
                                halign = font.Text.LEFT, \
                                valign = font.Text.BOTTOM, \
                                color = self._text_color)
    
    def load(self,text_loader,sprite_loader):
        """ 
        Load all the widget components into the UI (Receiver)
        """
        if self._loaded == False:
            text_loader(self._text)
            sprite_loader(self._line)
            self._loaded = True
        
    def unload(self,text_unloader,sprite_unloader):
        """
        Unload all the widget components from the UI (Receiver)
        """
        if self._loaded == True:
            text_unloader(self._text)
            sprite_unloader(self._line)
            self._loaded = False
            
    def position(self, x, y):
        """
        Change the widget position in an orthographic projection
        """
        self._x = x
        self._y = y
        self._line.refresh(self._x, self._y, self._width,\
                            self._height)
        
    def size(self, width, height):
        """
        Change the widget size in an orthographic projection
        """
        self._width = width
        self._height = height
        self._line.refresh(self._x, self._y, self._width,\
                           self._height)
        		
class LightInputBox(LightWidget):
    #System independent OpenGL driven lightweight InputBox
    #Uses pyglet
    
    def __init__(self, *params):
        LightWidget.__init__(self, *params)
        self.init_valid_chars()
	self.max_line_length = 80
	self.base_text = ""
        
    def init_valid_chars(self):
        self._charset = CharSet()
        self._submit_key = key.ENTER
        self._delete_key = key.BACKSPACE
        self._left_key = key.LEFT
        self._right_key = key.RIGHT
    
    def text(self):
    	"""
        This function ignores the cursor, it should always be used
        when retrieving the text string
        """
        return self._text.text[:self.__cursor_position] + \
        	self._text.text[self.__cursor_position+1:]
     
    def set_text(self, new_text):
    	self._text.text = self.base_text + new_text
    	self.reset_cursor()
        
    def default(self,def_text):
        self._text.text = def_text + self._text.text
	self.base_text = def_text
    
    def input(self, symbol, modifiers):
    	self._text.text = self.text()
      	if symbol == key.DELETE:
		self._text.text = self.base_text 
		self.reset_cursor()
        if symbol == self._delete_key:
       		if modifiers & key.MOD_CTRL:
       			self.delete(5)
       		else:
		  	self.delete(1)
		  	
	if symbol == self._left_key:
		if modifiers & key.MOD_CTRL:
			self.cursor_left(5)
		else:
			self.cursor_left(1)
		
	if symbol == self._right_key:
		if modifiers & key.MOD_CTRL:
			self.cursor_right(5)
		else:
			self.cursor_right(1)
		
	if symbol == self._submit_key and len(self._text.text)>len(self.base_text):
	  	command_text = self._text.text
		self._text.text = self.base_text
		self.reset_cursor()
  		return command_text
  		
        if len(self._text.text)==self.max_line_length:
		return
		
	if symbol not in self._charset.valid_chars:
	   	print("Unknown keypress")
	   	return

        new_char = self._charset.valid_chars[symbol]
        if modifiers & key.MOD_SHIFT:
		new_char = new_char.swapcase()
		if symbol in self._charset.shift_chars:
			new_char = self._charset.shift(symbol)
	if modifiers & key.MOD_CAPSLOCK:
	        new_char = new_char.swapcase()
	        
	if len(new_char)>0:
  		self._text.text = self._text.text[:self.__cursor_position] + \
  			    new_char + self._text.text[self.__cursor_position:]
  		self.__cursor_position += 1
  		
  		
  	self.paint_cursor()
	

    #Input box functions
    def delete(self,char_number):
      	max_delete = self.__cursor_position - len(self.base_text)
	if max_delete > char_number:
	      max_delete = char_number
	if max_delete > 0:
	      self._text.text = self._text.text[0:(self.__cursor_position - max_delete)] + \
	      			self._text.text[self.__cursor_position:]
	      self.__cursor_position -= max_delete
    
    def submit(self, symbol, modifiers):
        return self._text.text
        self._text.text = ""
        
    #Cursor functions
    def set_clock(self, ticks=60):
        """
        Enables the cursor and all the necessary variables
        __cursor_state = True     visible cursor
        __cursor_state = False    invisible cursor
        """
    	self.__time = ticks
    	self.__clock = ticks
    	self.__cursor_state = True
    	self.__cursor_position = len(self._text.text)
    	self.__cursor_char = "|"
    	#self.__text_buffer = self.text()
    	self.paint_cursor()
    	
    def clock(self):
    	self.__clock -= 1
    	if self.__clock == 0:
    	    self.__clock = self.__time
    	    self.switch_cursor_state()
     
    def switch_cursor_state(self):
        self.__cursor_state = not self.__cursor_state
        
    def cursor_left(self, distance):
    	if self.__cursor_position  < distance + len(self.base_text):
    	    self.__cursor_position = len(self.base_text)
    	else:
    	    self.__cursor_position -= distance
    	return self.__cursor_position
    	    
    def cursor_right(self, distance):
    	if len(self._text.text) - self.__cursor_position < distance:
    	    self.__cursor_position = len(self._text.text)
    	else:
    	    self.__cursor_position += distance
    	return self.__cursor_position
    	
    def reset_cursor(self):
    	self.__cursor_position = len(self._text.text)
    	#self.__text_buffer = self.text()
    	
    def paint_cursor(self):
    	"""
    	Add the cursor to the text string
    	"""
    	self._text.text = self._text.text[:self.__cursor_position] + \
    		self.__cursor_char + \
    		self._text.text[self.__cursor_position:]

class LightTextBox(LightWidget):
    
    def __init__(self, *params):
        LightWidget.__init__(self,*params)
        self.__max_lines = self._height / (int(self._size*1.2))
        self.__line_count = 0
        self.__errors = False
        pass

    #Text addition methods:
    
    def text(self,new_text):
        self._text.text = new_text

    def append(self,app_text):
    	if __line_count + self._text.text.count("\n") > self.__max_lines:
    	    self.error("Too many lines, append failed")
    	    return
        self._text.text.append(app_text)
        self.__line_count += self._text.text.count("\n")

    def add_line_before(self, txt):
    	#TODO multiple line addition
    	if self.__line_count + 1 > self.__max_lines:
    	    self.error("Too many lines, add_line_before failed")
	self._text.text = txt + "\n" + self._text.text
	__line_count += 1
	
    def add_line_after(self, txt):
    	#TODO multiple line addition
    	if self.__line_count + 1 > self.__max_lines:
    	    self.error("Too many lines, add_line_after failed")
    	self._text.text = self._text.text + "\n" + txt
    	self.__line_count +=1
    	
    def force_line_after(self, txt):
    	if self.__line_count + 1 > self.__max_lines:
    	    self.error("Forced add : line dropped")
    	    #drop the first line
    	    self._text.text = self._text.text[self._text.text.find("\n")+1:]
    	    self.__line_count -= 1
    	#delete any existing newlines, testing phase
    	timeout = 10
    	while txt.find("\n")>=0 and timeout>0:
    		pos = txt.find("\n")
    		txt = txt[:pos] + txt[pos+1:]
    		timeout -=1
    	if timeout==0:
    		self.force_line_after("Parse malfunction")
    	self._text.text = self._text.text + "\n" + txt
    	self.__line_count += 1
    	
    #Line number methods
    
    def set_max_lines(self,max_lines):
    	self.__max_lines = max_lines
    	
    def get_max_lines(self):
    	return self.__max_lines
   
    def get_line_count(self):
        return self.__line_count
    	
    #Error detection methods
    
    def error(self,err_msg):
    	if self.__errors == False:
            self.__errors = True
            self.__error_log = []
        self.__error_log.append(err_msg)
    
    
    
class CharSet:
    #storage class for character sets

    def shift(self,symbol):
      	if symbol in self.shift_chars:
		return self.valid_chars[self.shift_chars[symbol]]
  

    def __init__(self):
        valid = {} 
        valid[key.A] = 'a'
        valid[key.B] = 'b'
        valid[key.C] = 'c'
        valid[key.D] = 'd'
        valid[key.E] = 'e'
        valid[key.F] = 'f'
        valid[key.G] = 'g'
        valid[key.H] = 'h'
        valid[key.I] = 'i'
        valid[key.J] = 'j'
        valid[key.K] = 'k'
        valid[key.L] = 'l'
        valid[key.M] = 'm'
        valid[key.N] = 'n'
        valid[key.O] = 'o'
        valid[key.P] = 'p'
        valid[key.Q] = 'q'
        valid[key.R] = 'r'
        valid[key.S] = 's'
        valid[key.T] = 't'
        valid[key.U] = 'u'
        valid[key.V] = 'v'
        valid[key.W] = 'w'
        valid[key.X] = 'x'
        valid[key.Y] = 'y'
        valid[key.Z] = 'z'
        valid[key._1] = '1'
        valid[key._2] = '2'
        valid[key._3] = '3'
        valid[key._4] = '4'
        valid[key._5] = '5'
        valid[key._6] = '6'
        valid[key._7] = '7'
        valid[key._8] = '8'
        valid[key._9] = '9'
        valid[key._0] = '0'
        valid[key.PERIOD] = '.'
        valid[key.BRACKETLEFT] = '['
        valid[key.BRACKETRIGHT] = ']'
        valid[key.SPACE] = ' '
        valid[key.COMMA] = ','
        valid[key.PARENLEFT] = '('
        valid[key.PARENRIGHT] = ')'
        valid[key.BRACELEFT] = '{'
        valid[key.BRACERIGHT] = '}'
        valid[key.GREATER] = '>'
        valid[key.LESS] = '<'
        valid[key.BACKSPACE] = ''
        valid[key.ENTER] = ''
        valid[key.DELETE] = ''
        valid[key.EQUAL] = '='
        valid[key.PLUS] = '+'
        valid[key.UNDERSCORE] = '_'
        valid[key.MINUS] = '-'
        valid[key.NUM_MULTIPLY] = '*'
        valid[key.APOSTROPHE] = '\''
        valid[key.DOUBLEQUOTE] = '"'
        valid[key.DOLLAR] = '$'
        valid[key.SLASH] = '/'
        valid[key.QUESTION] = '?'
        valid[key.UP] = ''
        valid[key.DOWN] = ''
        valid[key.RIGHT] = ''
        valid[key.LEFT] = ''
	valid[key.LCTRL] = ''
	valid[key.RCTRL] = ''
	valid[key.LSHIFT] = ''
	valid[key.RSHIFT] = ''
	valid[key.BACKSLASH] = '\\'
	valid[key.TAB] = '\t'
        self.valid_chars = valid

        shift = {}
        shift[key._9] = key.PARENLEFT
        shift[key._0] = key.PARENRIGHT
        shift[key.PERIOD] = key.GREATER
        shift[key.COMMA] = key.LESS
        shift[key.BRACKETLEFT] = key.BRACELEFT
        shift[key.BRACKETRIGHT] = key.BRACERIGHT
        shift[key.EQUAL] = key.PLUS
        shift[key.MINUS] = key.UNDERSCORE
        shift[key._8] = key.NUM_MULTIPLY
        shift[key.APOSTROPHE] = key.DOUBLEQUOTE
        shift[key._4] = key.DOLLAR
        shift[key.BACKSLASH] = key.BACKSLASH #Incorrect, but couldn't find "|" key
        shift[key.SLASH] = key.QUESTION
        self.shift_chars = shift
        
