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

class Console():
    """
    The Console class. It represents one of the most important tasks in
    the game.

    """
    #Public variables
    enabled = False 
    bottom_left_y = 0
    bottom_left_x = 0
    size = 13
    lines = []
    texts = []
		
    def __init__(self,width,height,c_back,c_line,c_text):
        """
        About constructor.
        
        """
	self.enabled = True
	self.con_font = font.load('Helvetica',self.size)
	self.c_back = c_back
	self.c_line = c_line
	self.c_text = c_text
	
	self.bottom_left_y = UI.global_render.w.height - height
	self.bottom_left_x = 0 
	self.background = Sprite(self.bottom_left_x,self.bottom_left_y,\
	   UI.global_render.w.width,height,None,c_back) 
	self.lineground = Sprite(self.bottom_left_x,self.bottom_left_y,\
	    UI.global_render.w.width,self.size+3,None,c_line)
	UI.global_UI.load_2DUI(self.background)
  	UI.global_UI.load_2DUI(self.lineground)

  	self.add_line("blablalblablabl")
	self.add_line("gibberish")
	self.add_line("bla bla")
	self.render_lines()

    def enable(self):
        self.enabled = True 

    def disable(self):
        self.enabled = False

    def add_line(self,str):
        str = ">"+str
        self.lines.append(str)

    def render_lines(self):
        iter = 1
	texts = []
      	for str in self.lines:
	 	texts.append(font.Text(self.con_font,str,self.bottom_left_x+4,\
		      self.bottom_left_y+(self.size+3)*iter,halign=font.Text.LEFT,\
		      valign = font.Text.BOTTOM,color = self.c_text))
		iter = iter+1
	for txt in texts:
	       UI.global_UI.load_2Dtext(txt)
	

		      
