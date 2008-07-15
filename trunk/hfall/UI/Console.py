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
		
    def __init__(self,c_back,c_line,c_text):
        """
        About constructor.
        
        """
	self.enabled = False
	self.background = Sprite(0,UI.global_render.w.height-100,\
	   UI.global_render.w.width,100,None,c_back) 
	UI.global_UI.load_2DUI(self.background)

	#init background
        pass

    def enable(self):
        self.enabled = True 

    def disable(self):
        self.enabled = False
