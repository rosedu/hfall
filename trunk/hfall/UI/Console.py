"""
Hammerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.1'
__author__ = 'Alex Eftimie (alexeftimie@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine")
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
		
    def __init__(self,width,height,c_back,c_line,c_text):
        """
        About constructor.
        
        """
	self.enabled = True
	
	self.bottom_left_y = UI.global_render.w.height - height
	self.bottom_left_x = 0 
	self.background = Sprite(self.bottom_left_x,self.bottom_left_y,\
	   UI.global_render.w.width,height,None,c_back) 
	UI.global_UI.load_2DUI(self.background)

    def enable(self):
        self.enabled = True 

    def disable(self):
        self.enabled = False
