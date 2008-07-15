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

class Console():
    """
    The Console class. It represents one of the most important task in
    the game.

    """
		
    def __init__(self):
        """
        About constructor.
        
        """
	self.enabled = False
        self.lines = []
        pass

    def name(self):
        return 'Console'

    def enable(self):
        self.enabled = True 

    def disable(self):
        self.enabled = False
       
    def put(self, text):
	"""
	Puts one line at the end of the lines list
		
	"""
		
	self.lines.push(text)
				
    def show_line(self, line):
        """
        Displays one line on the screens. Keep somehow track of displayed lines.

        """
        print line
