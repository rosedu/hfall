"""
Hamerfall Debug Console class. All user commands and logging output should be done using
this class.

"""

__version__ = '0.1'
__author__ = 'Alex Eftimie (alexeftimie@gmail.com)'

import base

class Console(base.Task):
    """
    The Console class. It represents one of the most important task in
    the game.

    """
		
    def __init__(self):
        """
        About constructor.
        
        """
        'Lines list'
        self.lines = []
        
        pass

    def start(self):
        """
        bla

        """
        pass

    def stop(self):
        """
        bla

        """
        pass

    def pause(self):
        """
        bla

        """
        pass

    def resume(self):
        """
        bla

        """		
	
    def name(self):
        return 'Console'
       
    def run(self):
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
