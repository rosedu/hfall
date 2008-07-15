import struct
import array

class BinaryFile(file):
    def readShort(self):
        return struct.unpack('H', self.read(2))[0]

    def readInt(self):
        return struct.unpack('i', self.read(4))[0]

    def readLong(self):
        return struct.unpack('l', self.read(4))[0]

    def readFloat(self):
        return struct.unpack('f', self.read(4))[0]

    def readByte(self):
        return struct.unpack('B', self.read(1))[0]

    def readChar(self):
        return struct.unpack('c', self.read(1))[0]

    def readArray(self, length, _type):
        a = array.array(_type)
        a.read(self, length)
        return a.tolist()
