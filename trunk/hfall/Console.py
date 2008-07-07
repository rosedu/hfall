"""
Hamerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.1'
__author__ = 'Alex Eftimie (alexeftimie@gmail.com)'

import base
import Render
import UI

class Console(base.Task):
    """
    The Console class. It represents one of the most important task in
    the game.

    """
		
    def __init__(self,surface):
        """
        About constructor.
        
        """
        'Lines list'
        self.lines = []
	self.background = UI.Model2D(-3,2,7,4,(0.33,0.33,0.33))
	surface.add2D(self.background)
	
        
        pass

    def start(self,kernel):
        """
        bla

        """
        pass

    def stop(self,kernel):
        """
        bla

        """
        pass

    def pause(self,kernel):
        """
        bla

        """
        pass

    def resume(self,kernel):
        """
        bla

        """		
	
    def name(self):
        return 'Console'
       
    def run(self,kernel):
	map(Console.show_line, self.lines)
	
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
