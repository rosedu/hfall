"""
	Simple bitmap loader
"""

__version__ = "0.1"
__author__ = "Sergiu Costea (sergiu.costea@gmail.com)"

from struct import *
from array import *
from pyglet import image

BMP_RGBA = 1
BMP_RGB = 2
_DEFAULT_RED = 255
_DEFAULT_GREEN = 0
_DEFAULT_BLUE = 255 	

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
		Private constants:
                        _DEFAULT_RED  - used for transparency 
                        _DEFAULT_GREEN- used for transparency
                        _DEFAULT_BLUE - duh
  	"""
  	
  	def __init__(self,file_path,format=BMP_RGB,default_alpha=255):
                pic = image.load(file_path)
                print "loaded"
                self.width = pic.width
                self.height = pic.height
                self.size = self.width * self.height
                self.bytesize = self.size * 4
                #self.data = array('B',self.bytesize*[0])
                rawimage = pic.image_data
                print "raw data"
                self.format = rawimage.format
                l = []
                datastr = rawimage.data
                print "data loaded"
                index = 0
                length = len(datastr)
                i = 0
                if rawimage.format == 'BGR':
                        for i in range(length):
                                l.insert(index, unpack('B', datastr[i])[0])
                                if i % 3 == 2:
                                        l.append(default_alpha)
                                        index += 4
                        for i in range(length/4-1):
                                pixel = l[i*4:4*i+4]
                                if pixel[0] == _DEFAULT_RED and pixel[1] == _DEFAULT_GREEN and pixel[2] == _DEFAULT_BLUE:
                                        l[4*i+4] = 0
                elif rawimage.format == 'BGRA':
                        for i in range(length):
                                if i%4 == 3:
                                        l.append(unpack('B', datastr[i])[0])
                                        index += 4
                                else:
                                        l.insert(index, unpack('B', datastr[i])[0])
                elif rawimage.format == 'RGB':
                        for i in range(length):
                                l.append(unpack('B', datastr[i])[0])
                                if i % 3 == 2:
                                        l.append(default_alpha)
                        for i in range(length/4-1):
                                pixel = l[i*4:4*i+4]
                                if pixel[0] == _DEFAULT_RED and pixel[1] == _DEFAULT_GREEN and pixel[2] == _DEFAULT_BLUE:
                                        l[4*i+4] = 0
                elif rawimage.format == 'RGBA':
                        for i in range(length):
                                l.append(unpack('B', datastr[i])[0])
                else:
                        print "Unknown  or unsuported format ", rawimage.format
                        # TODO: log this message
                length = len(l)
                w = self.width * 4
                max_range = (length / w - 1) / 2 + 1
                for i in range(max_range):
                        l[i*w:(i+1)*w], l[length-(i+1)*w:length-i*w]=l[length-(i+1)*w:length-i*w], l[i*w:(i+1)*w]
                self.data = l
