import sys
sys.path.insert(0, "..")
from struct import *
from pyglet import image


class Image:

    def __init__(self, filename):
        
        img = image.load(filename)
        self.width = img.width
        self.height = img.height
        self.size = self.width * self.height
        self.format = img.image_data.format
        self.channels = len(self.format)
        data = img.image_data.data
        length = len(data)
        self.colors = []
        for i in range(self.channels):
            self.colors.append([])
        for i in range(self.size-1, -1, -1):
            for j in range(self.channels):
                self.colors[j].append(unpack('B', data[i*self.channels+j])[0])

        print filename, "loaded", "(", self.format, ")"

    def convert(self, format, alpha = 255):
        if len(format) > len(self.format):
            self.colors.append(len(self.colors[0])*[alpha])
            self.format += 'A'
            self.channels = len(self.format)
        if format == self.format:
            return
        colors = []
        for c in format:
            index = self.format.find(c)
            colors.append(self.colors[index])
        self.colors = colors
        self.format = format
        self.channels = len(self.format)

    def get_data(self):
        data = []
        for i in range(self.size):
            for j in range(len(self.format)):
                data.append(self.colors[j][i])
        return data

    def computeNormalMap(self, whiteHeightInPixels = -1.0, lowPassBump = False, scaleHeightByNz = False):
        if whiteHeightInPixels == -1.0:
            whiteHeightInPixels = max(self.width, self.height)
        w = self.width
        h = self.height
        self.convert("RGB")
        stride = self.channels
        
        bump = self.get_data()
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
                r = deltax*deltax + deltay*deltay + deltaz*deltaz
                deltax /= r
                deltay /= r
                deltaz /= r

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
        self.channels = 4
                
        
        
