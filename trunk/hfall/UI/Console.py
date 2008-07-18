"""
Hammerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.2'
__author__ = 'Sergiu Costea (sergiu.costea@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
from pyglet import font
import base
import UI
from AddModel import *
from pyglet.gl import *
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
    size = 10 
    lines = []
    extended_lines = []
    extended = False
    texts = []
    mem_var = []
    valid_chars = {} 
    shift_pairs = {} 
    registered_functions = {} 
    input_line = ""
    command = ""
    prompt = ">>>"

    #Constants
    MAX_CHARS = 80 
    MAX_LINES = 0 	#changed from init
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

	self.MAX_LINES = height/(self.size+4)
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

    def get_mem(self,p):
      	if p>=len(self.mem_var) or p<0:
		self.push_line("Error - no value at index")
		return str("None")
	else:
	  	return str(self.mem_var[p])

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
    	self.extended_lines = []
        for iter in range(self.MAX_LINES):
  		self.extended_lines.append(font.Text(self.con_font,"",\
		      self.bottom_left_x+UI.global_render.w.width/2+4,\
	    	      self.bottom_left_y + (self.size+3)*(iter+1), halign=font.Text.LEFT,\
		      valign = font.Text.BOTTOM, color = self.c_text))		

    def extend_lines(self):
	for line in self.extended_lines:
	   	UI.global_UI.load_2Dtext(line)
        
    def refresh_lines(self,action):
        if action == self.CON_STAY:
        	self.input_text.text = self.input_line
	elif action == self.CON_PUSH:
	        self.push_line(self.input_line)
	        self.command = self.input_line
		self.input_line = self.prompt 
		self.input_text.text = self.input_line

    def push_line(self,txt):
	for iter in range(self.MAX_LINES-1,0,-1):
		self.extended_lines[iter].text = self.extended_lines[iter-1].text
	self.extended_lines[0].text = self.lines[-1].text
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
  		self.refresh_lines(self.CON_PUSH)
		self.parse_command()
  		return
  	if symbol == key.UP:
                self.input_line = self.command
                self.refresh_lines(self.CON_STAY)

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
      	command = self.command[3:]
	command = command.strip()
	token_list = []
	mem = self.mem_var
	while True:
	      parts = command.partition(" ")
	      aux = parts[0].strip()
	      if aux!="":
	      	  token_list.append(aux)
	      aux = parts[1].strip()
	      if aux!="":
	      	  token_list.append(aux)
	      command = parts[2].strip()
	      if command=="":
	      	  break
	if token_list[0]=="exec":
	      token_list.remove("exec")
	      run_command = ""
	      for token in token_list:
	      	  run_command = run_command + " " + token
	      run_command = run_command.strip()
	      self.push_line("Executing engine call: " + run_command)
	      exec(run_command)
	elif token_list[0]=="help":
	      self.push_line("Available commands:")
	      self.push_line("exec <python command> - execute code right in the engine")
	      self.push_line("help - display this help")
	      self.push_line("extend - double the barrels, double the fun")
	      self.push_line("[reg] <python function> <params> - call registered function")
	elif token_list[0]=="extend":
	      self.extended = True
	      self.extend_lines()
	elif token_list[0]=="add":
	      if len(token_list)==1:
	      	  self.push_line("Error - no arguments given")
	      	  return
	      if len(token_list)>3:
	      	  self.push_line("Error - too many arguments (tuples must not contain spaces)")
	          return
	      if len(token_list)==2:
	      	  self.mem_var.append(token_list[1])
	      elif token_list[1]=="-s":
	      	  self.mem_var.append(token_list[2])
	      elif token_list[1]=="-f":
	      	  self.mem_var.append(float(token_list[2]))
	      elif token_list[1]=="-t":
	          self.mem_var.append(tuple(token_list[2]))
	      elif token_list[1]=="-o":
	      	  exec("self.mem_var.append("+token_list[2]+")")
	      self.push_line("Variable added at position "+str(len(self.mem_var)-1))
	      
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
	shift[key.SLASH] = key.QUESTION
	self.shift_chars = shift

