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
        header = Chunks.ChunkHeader()
        material = Chunks.MaterialChunk()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.MATERIAL_NAME):
                    material.name = self.readName()
                    print "   Name: %s" %(material.name)
                    break
                if case(_3DS.AMBIENT_COLOR):
                    print "   Ambient color: "
                    material.ambientColor = self.readColor()
                    break
                if case(_3DS.DIFFUSE_COLOR):
                    print "   Diffuse color: "
                    material.diffuseColor = self.readColor()
                    break
                if case(_3DS.SPECULAR_COLOR):
                    print "   Specular color: "
                    material.specularColor = self.readColor()
                    break
                if case(_3DS.SHININESS_PERCENT):
                    print "   Shininess percent: "
                    material.shininess = self.readPercent()
                    break
                if case(_3DS.SHIN2PCT_PERCENT):
                    print "   Shininess sterngth: "
                    material.shininessSterngth = self.readPercent()
                    break
                if case(_3DS.SHIN3PCT_PERCENT):
                    print "   Shininess secoind sterngth: "
                    material.secondShininessSterength = self.readPercent()
                    break
                if case(_3DS.TRANSPARENCY_PERCENT):
                    print "   Transparency percent: "
                    material.transparency = self.readPercent()
                    break
                if case(_3DS.TRANSP_FALLOF_PERCENT):
                    print "   Transparency fallof percent: "
                    material.transparencyFallof = self.readPercent()
                    break
                if case(_3DS.REFLECTION_BLUR_PERCENT):
                    print "   Reflection Blur percent: "
                    material.reflectionBlur = self.readPercent()
                    break
                if case(_3DS.SELF_ILLUM):
                    print "   Self illuminted"
                    material.isSelfIlluminated = True
                    break
                if case(_3DS.TWO_SIDE):
                    print "   Two-sided lighting"
                    material.twoSided = True
                    break
                if case(_3DS.ADDITIVE):
                    print "   Additive blend"
                    material.aditive = True
                    break
                if case(_3DS.WIREFRAME):
                    print "   Wireframe"
                    material.wireframe = True
                    break
                if case(_3DS.WIRESIZE):
                    material.wireSize = self.file.readFloat()
                    print "   Wire size: %f" %(material.wireSize)
                    break
                if case(_3DS.SHADING):
                    material.shadingType = self.file.readShort()
                    print "   Shading: %d" %(material.shadingType)
                    break
                if case(_3DS.TEXTURE_MAP_1):
                    print "   Texture Map 1\n    Percentage: "
                    self.readTextureChunk(material.textureMap1, header.chunk_length - 6)
                    break
                if case(_3DS.TEXTURE_MAP_2):
                    print "   Texture Map 2\n    Percentage: "
                    self.readTextureChunk(material.textureMap2, header.chunk_length - 6)
                    break
                if case(_3DS.BUMP_MAP):
                    print "   Bump Map\n    Percentage: "
                    self.readTextureChunk(material.bumpMap, header.chunk_length - 6)
                    break
                if case(_3DS.SPECULAR_MAP):
                    print "   Specular Map\n    Percentage: "
                    self.readTextureChunk(material.specularMap, header.chunk_length - 6)
                    break
                if case(_3DS.REFLECTION_MAP):
                    print "   Reflection Map\n    Percentage: "
                    self.readTextureChunk(material.reflectionMap, header.chunk_length - 6)
                    break
                if case(_3DS.OPACITY_MAP):
                    print "   Opacity Map\n    Percentage: "
                    self.readTextureChunk(material.opacityMap, header.chunk_length - 6)
                    break
                if case(_3DS.SHININESS_MAP):
                    print "   Shininess Map\n    Percentage: "
                    self.readTextureChunk(material.shininessMap, header.chunk_length - 6)
                    break
                if case(_3DS.TEXTURE_1_MASK):
                    print "   Texture 1 mask"
                    self.readTextureChunk(material.textureMask1, header.chunk_length - 6)
                    break
                if case(_3DS.TEXTURE_2_MASK):
                    print "   Texture 2 mask"
                    self.readTextureChunk(material.textureMask2, header.chunk_length - 6)
                    break
                if case(_3DS.OPACITY_MASK):
                    print "   Opacity mask"
                    self.readTextureChunk(material.opacityMask, header.chunk_length - 6)
                    break
                if case(_3DS.BUMP_MASK):
                    print "   Bump mask"
                    self.readTextureChunk(material.bumpMask, header.chunk_length - 6)
                    break
                if case(_3DS.SHININESS_MASK):
                    print "   Shininess mask"
                    self.readTextureChunk(material.shininessMask, header.chunk_length - 6)
                    break
                if case(_3DS.SPECULAR_MASK):
                    print "   Specular mask"
                    self.readTextureChunk(material.specularMask, header.chunk_length - 6)
                    break
                if case(_3DS.REFLECTION_MASK):
                    print "   Reflection mask"
                    self.readTextureChunk(material.reflectionMask, header.chunk_length - 6)
                    break
                if case():
                    print "  Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        self.object

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
                
                
                
        
            
        
        
