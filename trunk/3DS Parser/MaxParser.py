import Chunks
import os
from BinaryFile import BinaryFile
from switch import switch
import _3DS

class MaxParser:
    def __init__(self):
        self.keyframe = None
        self.object = Chunks.ObjectChunk()
        self.filename = None
    
    def __init__(self, filename):
        self.keyframe = None
        self.object = Chunks.ObjectChunk()
        self.filename = filename
        
    def readChunkHeader(self, header):
        header.start_position = self.file.tell()
        header.chunk_id = self.file.readShort()
        header.chunk_length = self.file.readInt()

    def parse(self, obj = True, anim = False):
        if self.filename == None:
            print "No file\n"
            return False
        if ".3ds" not in self.filename:
            print "Invalid source file extension\nExtension must be .3ds\n"
            return False
        if anim == True:
            self.keyframe = Chunks.KeyframeChunk()
        if obj == False:
            self.object = None
        self.file = BinaryFile(self.filename, "rb")
        header = Chunks.ChunkHeader()
        self.readChunkHeader(header)
        if header.chunk_id != _3DS.MAIN_CHUNK:
            print "Invalid 3DS file\n"
            self.file.close()
            return False
        print "Main Chunk"
        self.readMainChunk(header.chunk_length - 6)
        end_position = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        eof = self.file.tell()
        self.file.close()
        if eof != end_position:
            return False
        return True

    def readMainChunk(self, bytes):
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.M3D_VERSION):
                    self.version = self.file.readInt()
                    print 'Version: %d' %(self.version)
                    break
                if case(_3DS.EDITOR_CHUNK):
                    if self.object == None:
                        break
                    print " Editor Chunk"
                    self.readObjectChunk(header.chunk_length - 6)
                    break
                if case(_3DS.KEYFRAME_CHUNK):
                    if self.keyframe == None:
                        break
                    print " Key Frame"
                    self.readKeyframeChunk(header.chunk_length - 6)
                    break
                if case():
                    print ' Skip unknown %X subchunk' %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)

    def readObjectChunk(self, bytes):
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.MESH_VERSION):
                    self.object.version = self.file.readInt()
                    print "  Mesh Version: %d" %(self.object.version)
                    break
                if case(_3DS.MATERIAL_BLOCK):
                    print "  Material"
                    self.readMaterialChunk(header.chunk_length - 6)
                    break
                if case(_3DS.MASTER_SCALE):
                    self.object.masterScale = self.file.readFloat()
                    print "  Master scale: %f" %(self.object.masterScale)
                    break
                if case(_3DS.AMBIENT_LIGHT):
                    print "  Ambient light: "
                    self.object.ambientLight = self.readFloatColor()
                    break;
                if case(_3DS.MESH):
                    print "  Mesh"
                    self.readMeshChunk(header.chunk_length - 6)
                    break
                if case():
                    print "  Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)


    def readMaterialChunk(self, bytes):
        pass

    def readMeshChunk(self, bytes):
        pass

    def readKeyFrameChunk(self, bytes):
        pass


    def readFloatColor(self):
        pass

    def updateBytesToRead(self, bytes, length):
        if length == 0:
            return 0
        bytes = bytes - length
        if bytes < 0:
            self.file.seek(bytes, os.SEEK_CUR)
            return 0
        return bytes
                
                
                
        
            
        
        
