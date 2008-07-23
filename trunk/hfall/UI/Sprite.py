"""
	2D Bitmap control & display class
"""

__version__ = "0.1"
__author__ = "Sergiu Costea (sergiu.costea@gmail.com)"

import sys
sys.path.insert(0, "..")
from pyglet.gl import *
from ctypes import *
from Bitmap import *
import array
from UI import *
from base import *

class Sprite:
  	x = 0
	y = 0
	xx = 0
	yy = 0
	pixel_height = 0
        pixel_width = 0
   	data = None
   	color = (0.0,0.0,0.0,0.0)
	height = 0
	width = 0
	is_textured = False
	
	#TEMP
	texture_ids = None 

	def __init__(self, x=0, y=0, width = 2, height = 2,texture = None,\
	    color=(0.0,0.0,0.0,0.0)):
	  	
	  	self.x = x
		self.y = y
		self.xx = x + width
		self.yy = y + height
	  	if texture==None:
			self.width = width
			self.height = height
			self.color = color
			self.is_textured = False
		else:
			self.is_textured = True
			TEX_NO = 4
			texture_ids = array.array('L',range(TEX_NO))
			self.texture_ids = (GLuint * TEX_NO)(*texture_ids)
			glGenTextures(TEX_NO,self.texture_ids)
  			glBindTexture(GL_TEXTURE_2D,self.texture_ids[0])

  			bitmap = Bitmap(texture,BMP_RGB)
  			if bitmap == None:
                                kernel.log.error("Bitmap " + texture + " could \
                                        not be opened")
                                return
                        else:
                                kernel.log.msg("Bitmap " + texture + " loaded\
                                        successfully")
			data_list = bitmap.data.tolist()
			self.data = (GLubyte * len(data_list))(*data_list)

	  		self.pixelheight = bitmap.height
			self.pixelwidth = bitmap.width
			
	def refresh(self, x, y, width, height):
		self.x = x
		self.y = y
		self.xx = width + x
		self.yy = height + y
