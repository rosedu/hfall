"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

from base import Task
from pyglet import window
from Console import Console
from pyglet import font 

class Model2D:
    """
    A basic class for any 2D object.

    """
    
    def __init__(self,  x, y, w=2.0, h=2.0, color=(0.0, 0.0, 0.0, 0.0)):
        """
        Model2D class initialization.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        self.x = x
        self.y = y
        self.xx = x + w
        self.yy = y + h
        self.color = color
	

class UI(Task):
  	""" 
	  Contains UI elements including console interaction
	"""

	"""
		Global variable list:
		 - surface (Render)
  		 - console_bck (Model2D object)
  		 - console (Console)
  	"""
	def x_topt(self,x):
		return x*self._width_pt/self.surface.width - self._width_pt/2	

	def y_topt(self,y):
  		return -1.0*y*self._height_pt/self.surface.height + 1.0*self._height_pt/2

	def px_topt(self,px):
  		return 1.0*px/86

	def __init__(self,render):
	  	self.surface = render
		self._height_pt = 7 
		self._width_pt = 9.2 

		self.console_bck = Model2D(self.x_topt(50),self.y_topt(50),\
		    self.px_topt(25), self.px_topt(25),(0.8,0.8,0.8))
		self.surface.add2D(self.console_bck)
	
  		self.console = Console()
  		self.console.enable()
  		ft = font.load('Arial',36)
	  	self.some_gibberish = font.Text(ft,"Hello, Console!",0,0,(240,0,0))

	def start(self,kernel):
	  	pass

	def stop(self,kernel):
	  	pass

	def pause(self,kernel):
	  	pass

	def resume(self,kernel):
	  	pass

	def run(self,kernel):
	  	#Render text
		self.some_gibberish.draw()
	  	pass
	
	def name(self):
	  	return "" 
