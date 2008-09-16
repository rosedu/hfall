from TextureFormat import TextureFormat
from switch import switch
from pyglet import image
from math import sqrt
from struct import *
import os

class Callable:
    def __init__(self, method):
        self.__call__ = method

class Image:

    def __init__(self, filename, format = None):
        self.data = None
        if not os.path.exists(filename):
            print "Could not find ", filename
            return
        img = image.load(filename)
        self.width = img.width
        self.height = img.height
        self.size = self.width * self.height
        self.format = img.image_data.format
        self.textureFormat = format
        data = img.image_data.data
        length = len(data)
        self.colors = []
        for i in range(len(self.format)):
            self.colors.append([])
        for i in range(self.size-1, -1, -1):
            for j in range(len(self.format)):
                self.colors[j].append(unpack('B', data[i*len(self.format)+j])[0])
        if not format:
            self.textureFormat = self.supportedFormat(self.format)
        self.convert(self.textureFormat)

        print filename, "loaded", "(", self.format, ")"

    def convert(self, textureFormat, alpha = 255):
        format = textureFormat.toString()
        if len(format) > len(self.format):
            self.colors.append(len(self.colors[0])*[alpha])
            self.format += 'A'
        if format == self.format:
            self.__getData(textureFormat.dataType())
            return
        colors = []
        for c in format:
            index = self.format.find(c)
            if index != -1:
                colors.append(self.colors[index])
        self.colors = colors
        self.format = format
        self.__getData(textureFormat.dataType())

    def __getData(self, dataType):
        self.data = []
        for i in range(self.size):
            for j in range(len(self.format)):
                self.data.append(self.colors[j][i])
        self.data = (dataType*len(self.data))(*self.data)

    def supportedFormat(format):
        if len(format) == 1:
            return TextureFormat.fromString(format)
        if len(format) == 2 and format.find("L") != -1 and format.find("A") != -1:
            return TextureFormat.fromString("LA")
        if len(format) == 3:
            return TextureFormat.fromString("RGB")
        return TextureFormat.fromString("RGBA")

    def computeNormalMap(self, whiteHeightInPixels = -1.0, lowPassBump = False, scaleHeightByNz = False):
        if whiteHeightInPixels == -1.0:
            whiteHeightInPixels = max(self.width, self.height)
        w = self.width
        h = self.height
        self.convert(TextureFormat.fromString("RGB"))
        stride = len(self.format)
        
        bump = self.data
        normal = [w*h*[0], w*h*[0], w*h*[0], w*h*[0]]
        for y in range(h):
            for x in range(w):
                i = x + y*w
                j = stride*i

                def height(dx, dy):
                    return bump[(((dx + x + w) % w) + ((dy + y + h) % h) * w) * stride]

                deltay = -(height(-1, -1) *  1 + height( 0, -1) *  2 + height( 1, -1) *  1 + \
                           height(-1,  1) * -1 + height( 0,  1) * -2 + height( 1,  1) * -1)
                deltax = -(height(-1, -1) * -1 + height( 1, -1) * 1 + \
                           height(-1,  0) * -2 + height( 1,  0) * 2 + \
                           height(-1,  1) * -1 + height( 1,  1) * 1)
                deltaz = 4 * 2 * (whiteHeightInPixels / 255.0)
                r = 1/sqrt(deltax*deltax + deltay*deltay + deltaz*deltaz)
                deltax *= r
                deltay *= r
                deltaz *= r

                H = bump[j] / 255.0
                if lowPassBump:
                    H = (height(-1, -1) + height( 0, -1) + height(1, -1) + \
                         height(-1,  0) + height( 0,  0) + height(1,  0) + \
                         height(-1,  1) + height( 0,  1) + height(1,  1)) / (255.0 * 9.0)
                if scaleHeightByNz:
                    H *= deltaz

                def clamp(val, low, high):
                    if val > high: return high
                    elif val < low: return low
                    else: return val
                
                normal[3][i] = int(H * 255.0)
                normal[0][i] = clamp(int(deltax*127.5 + 127.5),0, 255)
                normal[1][i] = clamp(int(deltay*127.5 + 127.5),0, 255)
                normal[2][i] = clamp(int(deltaz*127.5 + 127.5),0, 255)
                
        self.colors = normal
        self.format = "RGBA"
        self.convert(self.textureFormat)

    supportedFormat = Callable(supportedFormat)
                
        
        
