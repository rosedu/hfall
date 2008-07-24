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
import os.path
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
    __calls = []
    __calls_enabled = False
    __calls_file = "calls.con"
    rev_file = "rev.txt"
    __speed_ratio = 0.1

    #Constants
    MAX_CHARS = 80 
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
	self.init_clock()
      
    	self.input_line = UI.LightInputBox(0,UI.global_render.w.height - height - self.size - 2,\
                                       UI.global_render.w.width, self.size + 2,\
				       'Verdana',self.size,(0.8,1.0,0.8,1.0))
	self.input_line.default(self.prompt)
	self.input_line.set_clock(60)
	
    	self.text_box = UI.LightTextBox(0,UI.global_render.w.height - height, \
                                    UI.global_render.w.width, height,'Verdana',\
				    self.size,(0.8,0.8,1.0,1.0))
	self.text_box.force_line_after("Type <rev> to find out the latest changes")
	self.enable_calls(self.__calls_file)
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

    def read_hold(self, keyboard):
    	if self.__input_time==0:
    		if keyboard[key.LEFT]:
    			self.input_line.input(key.LEFT, 0)
    		elif keyboard[key.RIGHT]:
    			self.input_line.input(key.RIGHT, 0)
    		elif keyboard[key.BACKSPACE]:
    			self.input_line.input(key.BACKSPACE, 0)
        pass
        
    def input_clock(self):
    	if self.__input_time==0:	
    		self.init_clock()
    	else:
    		self.__input_time -= 1
    	return self.__input_time
    
    def init_clock(self,factor = 1):
    	self.__input_time = int(int(UI.global_render.fps) * self.__speed_ratio * factor)
            def read(self,symbol,modifiers):
      	if self.enabled == False:
		return
	self.init_clock(3) #prevent double keypress
	if symbol == key.ENTER and len(self.input_line._text.text)>len(self.input_line.base_text):
	  	self.command = self.input_line.text()
	  	self.text_box.force_line_after(self.command)
  		self.input_line.input(symbol,modifiers)
		self.parse_command()
  	if symbol == key.UP and len(self.command_history)>0:
  		if self.command_index - 1 < 0:
  		    pass
  		else:
  		    self.command_index -= 1
                self.input_line.set_text(self.command_history[self.command_index])
        elif symbol == key.DOWN and len(self.command_history)>0:
        	if self.command_index + 1 > len(self.command_history)-1:
        	    pass
        	else:
        	    self.command_index += 1
        	self.input_line.set_text(self.command_history[self.command_index])
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
	      	  break	if token_list[0]=="axes":
		self.warning_argc(token_list, 1)
              	UI.global_render.enableaxis = not UI.global_render.enableaxis
        elif token_list[0]=="lines":
        	self.warning_argc(token_list, 1)
              	self.text_box.force_line_after("Usage of lines: " + \
                          str(self.text_box.get_line_count()) + " out of " + 
                          str(self.text_box.get_max_lines()))
        elif token_list[0]=="history":
       		self.warning_argc(token_list, 1)
              	self.text_box.force_line_after("Command history:")
              	for command in self.command_history:
               	    	self.text_box.force_line_after(command)
	elif token_list[0]=="help":
		self.warning_argc(token_list, 1)
	     	self.text_box.force_line_after("Available commands:")
	      	self.text_box.force_line_after("rev - display changes")
	      	self.text_box.force_line_after("history - display latest commands")
	      	self.text_box.force_line_after("help - display this help")
	      	self.text_box.force_line_after("axes - enable axes")
	      	self.text_box.force_line_after("calls - show calls")
	      	self.text_box.force_line_after("call <index> - call an existing function")
	      	self.text_box.force_line_after("purge - clear the call list")
	elif token_list[0]=="rev":
		#get the changes from a file
		if os.path.exists(self.rev_file) == False:
			self.text_box.force_line_after("Error - file is missing")
		else:
			f = open(self.rev_file,"r")
			for line in f:
				if line.find("<OLD>")>=0:
					break
				self.text_box.force_line_after(line)
			f.close()
	elif token_list[0]=="calls":
		self.warning_argc(token_list, 1)
		self.print_calls()
	elif token_list[0]=="call":
		self.warning_argc(token_list, 2)
		index = int(token_list[1])
		self.make_call(token_list[1])
	elif token_list[0]=="purge":
		self.purge_calls(self.__calls_file)
        else:
              run_command = ""
              for token in token_list:
                  run_command = run_command + " " + token
              run_command = run_command.strip()
              self.text_box.force_line_after("Executing engine call: " + run_command)
              exec(run_command)
              self.add_call(run_command)
        self.add_command(aux_command)
        
    def warning_argc(self, token_list, max_count):
    	if len(token_list)>max_count:
    		self.text_box.force_line_afte("Warning - arguments dropped (" + \
    					str(len(token_list)-max_count) + ")")
    	
    def enable_calls(self,file_name):
    	if os.path.exists(file_name) == False:
    		self.text_box.force_line_after("Warning - call file doesn't exist - creating it")
    		f = open(file_name,"w")
    		f.close()
    	if os.path.exists(file_name) == False:
    		self.text_box.force_line_after("Error - couldn't create file")
    	else:
    		self.__calls_enabled = True
    		f = open(file_name,"r")
    		self.__calls = f.readlines()
    		for index in range(len(self.__calls)):
    			newline_pos = self.__calls[index].find("\n")
    			self.__calls[index] = self.__calls[index][:newline_pos]
    		f.close()
    		
    def save_calls(self,file_name):
    	if os.path.exists(file_name) == False:
    		self.text_box.force_line_after("Error - call file doesn't exist")
    	else:
    		self.__calls_enabled = False
    		f = open(file_name,"w")
    		for line in self.__calls:
    			f.write(line+"\n")
    		#f.writelines(self.__calls)
	          def print_calls(self):
    	if self.__calls_enabled == False:
    		self.text_box.force_line_after("Error - calls have not been initialized")
    	else:
    		counter = 0
    		for line in self.__calls:
    			self.text_box.force_line_after(str(counter) + ") " + line)
    			counter += 1
    
    def purge_calls(self,file_name):
    	if self.__calls_enabled == False:
    		self.text_box.force_line_after("Error - calls have not been initialized")
    	else:
    		self.__calls = []
    
    def add_call(self,call):
    	if self.__calls_enabled == False:
    		print "Dropped call"
    		pass
    	else:
    		self.__calls.append(call)
    
    def make_call(self,index):
    	exec(self.__calls[int(index)])
    			
    def shutdown(self):
    	self.save_calls(self.__calls_file)
    			
