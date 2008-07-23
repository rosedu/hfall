"""
Hammerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.3'
__author__ = 'Sergiu Costea (sergiu.costea@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
from pyglet import font
import base
import UI
import AddModel
from AddModel import *
from pyglet.gl import *
from Sprite import Sprite
from pyglet.window import key

# global modelmng
  
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
    size = 11
    lines = []
    extended_lines = []
    extended = False
    texts = []
    command = ""
    command_history = []
    prompt = ">>>"
    command_index = 0

    #Constants
    MAX_CHARS = 80 
    MAX_LINES = 0 	#changed from init
    CON_STAY = 0
    CON_PUSH = 1
    CON_MAX_COMMAND_HISTORY = 10
		
    def __init__(self,width,height,c_back,c_line,c_text,c_comm):
        """
        About constructor.
        
        """
	self.enabled = True
	self.c_back = c_back
	self.c_line = c_line
	self.c_text = c_text
	self.c_comm = c_comm

	self.MAX_LINES = height/(self.size+4)
      
    	self.input_line = UI.LightInputBox(0,UI.global_render.w.height - height - self.size - 2,\
                                       UI.global_render.w.width, self.size + 2,\
				       'Verdana',self.size,(0.8,1.0,0.8,1.0))
	self.input_line.default(self.prompt)
    	self.text_box = UI.LightTextBox(0,UI.global_render.w.height - height, \
                                    UI.global_render.w.width, height,'Verdana',\
				    self.size,(0.8,0.8,1.0,1.0))
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
	self.input_line.unload(UI.global_UI.unload_2Dtext,UI.global_UI.unload_2DUI)
    	self.text_box.unload(UI.global_UI.unload_2Dtext,UI.global_UI.unload_2DUI)
  	self.disable()

    def show(self):
      	if self.hidden == False:
		    return
        self.hidden = False
	self.input_line.load(UI.global_UI.load_2Dtext,UI.global_UI.load_2DUI)
    	self.text_box.load(UI.global_UI.load_2Dtext,UI.global_UI.load_2DUI)
	self.enable()
    def read(self,symbol,modifiers):
      	if self.enabled == False:
		return
	if symbol == key.ENTER and len(self.input_line._text.text)>len(self.input_line.base_text):
	  	self.command = self.input_line._text.text
	  	self.text_box.force_line_after(self.input_line._text.text)
  		self.input_line.input(symbol,modifiers)
		self.parse_command()
  	if symbol == key.UP and len(self.command_history)>0:
  		if self.command_index - 1 < 0:
  		    pass
  		else:
  		    self.command_index -= 1
                self.input_line.text(self.command_history[self.command_index])
        elif symbol == key.DOWN and len(self.command_history)>0:
        	if self.command_index + 1 > len(self.command_history)-1:
        	    pass
        	else:
        	    self.command_index += 1
        	self.input_line.text(self.command_history[self.command_index])
        else:
        	self.command_index = len(self.command_history)
        	
	self.input_line.input(symbol,modifiers)
	
    def add_command(self,command):
    	if len(self.command_history)==self.CON_MAX_COMMAND_HISTORY:
    	    self.command_history.pop(0)
    	self.command_history.append(command)

    def parse_command(self):
      	command = self.command[len(self.prompt):]
	command = command.strip()
	aux_command = command
	token_list = []
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
	      if len(token_list) > 1:
	      	  self.text_box.force_line_after("Error - too many arguments")
	      else:
	          if token_list[0]=="axes":
                      UI.global_render.enableaxis = not UI.global_render.enableaxis
                  elif token_list[0]=="lines":
                      self.text_box.force_line_after("Usage of lines: " + \
                          str(self.text_box.get_line_count()) + " out of " + 
                          str(self.text_box.get_max_lines()))
                  elif token_list[0]=="history":
                      self.text_box.force_line_after("Command history:")
                      for command in self.command_history:
                          self.text_box.force_line_after(command)
	elif token_list[0]=="help":
	      self.text_box.force_line_after("Available commands:")
	      self.text_box.force_line_after("exec <python command> - execute code right in the engine")
	      self.text_box.force_line_after("help - display this help")
	      self.text_box.force_line_after("axes - enable axes")
        else:
              run_command = ""
              for token in token_list:
                  run_command = run_command + " " + token
              run_command = run_command.strip()
              self.text_box.force_line_after("Executing engine call: " + run_command)
              exec(run_command)
        self.add_command(aux_command)
                  
	      
