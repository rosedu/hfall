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
        if format == self.format:
            return
        colors = []
        for c in format:
            index = self.format.find(c)
            colors.append(self.colors[index])
        self.colors = colors
        self.format = format

    def get_data(self):
        data = []
        for i in range(self.size):
            for j in range(len(self.format)):
                data.append(self.colors[j][i])
        return data
        
