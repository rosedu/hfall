import struct

class BinaryFile(file):
    def readShort(self):
        return struct.unpack('h', self.read(2))[0]

    def readInt(self):
        return struct.unpack('i', self.read(4))[0]

    def readFloat(self):
        return struct.unpack('f', self.read(4))[0]
