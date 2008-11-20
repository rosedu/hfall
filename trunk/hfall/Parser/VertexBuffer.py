import pyglet
import ctypes
from pyglet.gl import *

class VertexBuffer:

    # buffer location
    UNKNOWN = 0
    RAM = 1
    VBO = 2

    location = UNKNOWN

    #buffer target
    ARRAY_BUFFER = 0x8892
    ELEMENT_ARRAY_BUFFER = 0x8893

    #buffer usage
    STATIC_DRAW = 0x88E4
    DYNAMIC_DRAW = 0x88E8
    STREAM_DRAW = 0x88E0

    def __init__(self, size, usage = STATIC_DRAW, target = ARRAY_BUFFER):
        self.glID = (GLuint)(*[])
        self.pointer = None
        self.target = target
        self.usage = usage
        self.size = size
        self.usageBytes = 0
        if self.location == self.UNKNOWN:
            info = gl_info.GLInfo()
            info.set_active_context()
            if info.have_extension("GL_ARB_vertex_buffer_object"):
                self.location = self.VBO
                glGenBuffersARB(1, self.glID)
                glBindBufferARB(target, self.glID)
                glBufferDataARB(target, size, None, usage)
            else:
                self.pointer = []
                self.location = self.RAM
        elif self.location == self.RAM:
            self.pointer = []

    def addArray(self, array, size):
        offset = self.usageBytes
        if self.location == self.VBO:
            glBufferSubDataARB(self.target, self.usageBytes, size, array)
            self.usageBytes += size
        else:
            self.pointer.append(array)
            self.usageBytes += 1
        return offset

    def getPointer(self, offset):
        if self.location == self.VBO:
            return offset
        else: return self.pointer[offset]

    def enable(self):
        if self.location == self.VBO:
            glBindBufferARB(self.target, self.glID)

    def disable(self):
        if self.location == self.VBO:
            glBindBufferARB(self.target, 0)


class VBOArray:

    def __init__(self, size, _type, pointer, _buffer):
        self.size = size
        self.type = _type
        self.buffer = _buffer
        pointer = (_type * len(pointer))(*pointer)
        self.offset = _buffer.addArray(pointer, size*sizeof(_type))

    def pointer(self):
        return self.buffer.getPointer(self.offset)

    def size(self):
        return self.size

    def type():
        return self._type
  
