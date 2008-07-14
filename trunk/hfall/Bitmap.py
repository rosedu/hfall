"""
	Simple bitmap loader
"""

__version__ = "0.1"
__author__ = "Sergiu Costea (sergiu.costea@gmail.com)"

from struct import *
from array import *

BMP_RGBA = 1
BMP_RGB = 2

class Bitmap:
  	"""
	  	Bitmap loader class
		
		Supported input : RGBA(32bit), RGB(24bit)
		
		Variables:
			width - pixel table width
			height - pixel table height
			data - pixel table (array)
  			size - pixel table size
			bytesize - pixel table size in bytes
  	"""
  	
  	def __init__(self,file_path,format=BMP_RGB,default_alpha=255):
	  	bmp_file = open(file_path,"r")
		if (bmp_file==None):
	  		return None 

		#Load bitmap headers
		bmp_file_contents = bmp_file.read()
      		bmp_file_header = unpack_from("=BBIHHI",bmp_file_contents)
     		offset = 14
     		bmp_info_header = unpack_from("=IiiHHIIiiII",bmp_file_contents,offset)
     		offset = 54

		#Check bitmap headers
     		if bmp_file_header[0]==66 and bmp_file_header[1]==77:
			print "Bitmap file type ok!"
		else:
			print "Not a bitmap"
			return None 

		#Set instance variables
		self.width = bmp_info_header[1]
		self.height = bmp_info_header[2]
		self.size = self.width * self.height
		self.bytesize = self.size * 4
		self.data = array('B',self.bytesize*[0])

		#Build pixel table according to format
		index = 0
		if format==BMP_RGB:
			while index < self.bytesize:
		  		pixel = unpack_from("=BBB",bmp_file_contents,offset)
				offset+=3
				self.data[index+2] = pixel[0]
				self.data[index+1] = pixel[1]
				self.data[index] = pixel[2]
				self.data[index+3] = default_alpha
				index+=4
		if format==BMP_RGBA:
			tmp_string = bmp_file_contents[54:]
			self.data.fromstring(tmp_string)
