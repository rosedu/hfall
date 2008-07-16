"""
Hammerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.1'
__author__ = 'Alex Eftimie (alexeftimie@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
from pyglet import font
import base
import Render
import UI
from Sprite import Sprite
from pyglet.window import key

class Console():
    """
    The Console class. It represents one of the most important tasks in
    the game.

    """
    #Public variables
    hidden = False 
    enabled = False 
    bottom_left_y = 0
    bottom_left_x = 0
    size = 13
    lines = []
    texts = []
    valid_chars = {} 
    shift_pairs = {} 
    registered_functions = {} 
    input_line = ""
    prompt = ">>>"

    #Constants
    MAX_CHARS = 80 
    MAX_LINES = 10
    CON_STAY = 0
    CON_PUSH = 1
		
    def __init__(self,width,height,c_back,c_line,c_text,c_comm):
        """
        About constructor.
        
        """
	self.enabled = True
	self.con_font = font.load('Verdana',self.size)
	self.c_back = c_back
	self.c_line = c_line
	self.c_text = c_text
	self.c_comm = c_comm

	self.init_valid_chars()
	
	#Create background
	self.bottom_left_y = UI.global_render.w.height - height
	self.bottom_left_x = 0 
	self.background = Sprite(self.bottom_left_x,self.bottom_left_y,\
	   UI.global_render.w.width,height,None,c_back) 
	self.lineground = Sprite(self.bottom_left_x,self.bottom_left_y,\
	    UI.global_render.w.width,self.size+3,None,c_line)
	UI.global_UI.load_2DUI(self.background)
  	UI.global_UI.load_2DUI(self.lineground)

	self.init_lines()
  	self.hide()

    def enable(self):
        self.enabled = True 

    def disable(self):
        self.enabled = False

    def toggle_visible(self):
      	if self.hidden:
		self.show()
	else:
	  	self.hide()

    def hide(self):
      	if self.hidden == True:
		return
      	self.hidden = True 
	#Tell the UI to unload all console data
	UI.global_UI.unload_2Dtext(self.input_text)
  	UI.global_UI.unload_2DUI(self.background)
  	UI.global_UI.unload_2DUI(self.lineground)
  	for line in self.lines:
		UI.global_UI.unload_2Dtext(line)	
  	self.disable()

    def show(self):
      	if self.hidden == False:
		return
        self.hidden = False
	UI.global_UI.load_2Dtext(self.input_text)
  	UI.global_UI.load_2DUI(self.background)
  	UI.global_UI.load_2DUI(self.lineground)
  	for line in self.lines:
		UI.global_UI.load_2Dtext(line)	
	self.enable()

    def init_lines(self):
        self.input_line = self.prompt
	self.input_text = font.Text(self.con_font,self.input_line,self.bottom_left_x+4,\
	    self.bottom_left_y, halign = font.Text.LEFT, valign = font.Text.BOTTOM, \
	    color = self.c_comm)
	UI.global_UI.load_2Dtext(self.input_text)

	self.lines = []
	for iter in range(self.MAX_LINES):
  		self.lines.append(font.Text(self.con_font,"",self.bottom_left_x+4,\
	      		self.bottom_left_y + (self.size+3)*(iter+1),halign=font.Text.LEFT,\
	  		valign = font.Text.BOTTOM, color = self.c_text))		

	for line in self.lines:
	   	UI.global_UI.load_2Dtext(line)
  		
	
        
    def refresh_lines(self,action):
        if action == self.CON_STAY:
        	self.input_text.text = self.input_line
	elif action == self.CON_PUSH:
	        self.push_line(self.input_line)
		self.input_line = self.prompt 
		self.input_text.text = self.input_line

    def push_line(self,txt):
        for iter in range(self.MAX_LINES-1,0,-1):
	  	self.lines[iter].text = self.lines[iter-1].text
	self.lines[0].text = txt

    def read(self,symbol,modifiers):
      	if self.enabled == False:
		return
      	if symbol == key.DELETE:
		self.input_line = self.prompt 
		self.refresh_lines(self.CON_STAY)
        if symbol == key.BACKSPACE and len(self.input_line)>len(self.prompt):
		self.input_line = self.input_line[0:(len(self.input_line)-1)]
		self.refresh_lines(self.CON_STAY)
		return

	if symbol == key.ENTER and len(self.input_line)>len(self.prompt):
		self.parse_command()
  		self.refresh_lines(self.CON_PUSH)
  		return

        if len(self.input_line)==self.MAX_CHARS:
		return

        new_char = self.valid_chars[symbol]
        if modifiers & key.MOD_SHIFT:
		new_char = new_char.swapcase()
		if symbol in self.shift_chars:
			new_char = self.shift(symbol)
	if modifiers & key.MOD_CAPSLOCK:
	        new_char = new_char.swapcase()
	       
  	self.input_line = self.input_line + new_char 
	self.refresh_lines(self.CON_STAY)
  	
    def shift(self,symbol):
	return self.valid_chars[self.shift_chars[symbol]]


    def parse_command(self):
      	command = self.input_line
	token_list = []
	
  	pass
	
    def register_command(self,func,func_str):
      	registered_functions[func_str] = func

    def init_valid_chars(self):
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
	self.valid_chars = valid

	shift = {}
	shift[key._9] = key.PARENLEFT
	shift[key._0] = key.PARENRIGHT
	shift[key.PERIOD] = key.GREATER
	shift[key.COMMA] = key.LESS
	shift[key.BRACKETLEFT] = key.BRACELEFT
	shift[key.BRACKETRIGHT] = key.BRACERIGHT
	self.shift_chars = shift

