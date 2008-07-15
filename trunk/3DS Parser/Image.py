import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../UI")
from Bitmap import Bitmap
from switch import switch

class Image:

    class Format:
        JPEG   = 1
        BMP    = 2
        TGA    = 3
        

    def __init__(self, filename, channels = 3, format = Format.BMP):
        self.file = filename
        self.channels = channels
        self.format = format
        self.load()

    def load(self):
        for case in switch(self.format):
            if case(Image.Format.BMP):
                bitmap = Bitmap(self.file)
                self.width = bitmap.width
                self.height = bitmap.height
                self.data = bitmap.data.tolist()
