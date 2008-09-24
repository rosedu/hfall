"""
Auxiliary package
Hammerfall line class (straight)

"""

__version__ = '0.1'
__authors__ = 'Sergiu Costea (sergiu.costea@gmail.com)'

import math
from pyglet.gl import *

LINE_DEF_COLOR = (1,1,1)

class Line:
    
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
	self.y1 = y1
	self.z1 = z1
	self.x2 = x2
	self.y2 = y2
	self.z2 = z2
	self.color = LINE_DEF_COLOR

    def set_color(self,red, green, blue, alpha = 1):
        if alpha == 1:
	    self.color = (red, green, blue)
	else:
	    self.color = (red, green, blue, alpha)

    def draw(self):
        glBegin(GL_LINES)
	glColor3f(self.color[0],self.color[1],self.color[2])
	glVertex3f(self.x1, self.y1, self.z1)
	glVertex3f(self.x2, self.y2, self.z2)
	glEnd()
        
class LineManager:
    def __init__(self):
        self.lines = {}
	self.default_key = 0

    def add(self, line, key=-1):
        if key < -1:
	     print "Erroneous key in LineManager"
	     return -1
	elif key == -1:
	     while self.default_key in self.lines:
	         self.default_key += 1
	     self.lines[self.default_key] = line
	     return self.default_key
	elif key in self.lines:
	     print "Double key in LineManager"
	     return -1
	else:
	     self.lines[key] = line
	     return key

    def remove(self,key):
         if key in self.lines:
	      del self.lines[key]
	 else:
	      print "Error - attempt to remove invalid key entry"

    def clear(self):
         self.lines.clear()

    def run_diag(self):
         print "running diag..."
         for k,v in self.lines.iteritems():
	     print "self.lines[",k,"]=((",v.x1,",",v.y1,",",v.z1,")(",v.x2,",",v.y2,",",v.z2,"))"

    def draw(self):
         for k,v in self.lines.iteritems():
	     v.draw()
