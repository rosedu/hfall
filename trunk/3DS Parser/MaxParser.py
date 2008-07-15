import Chunks
import os
from BinaryFile import BinaryFile
from switch import switch
import _3DS

class MaxParser:

    def __init__(self, filename = None):
        self.keyframe = None
        self.object = Chunks.ObjectChunk()
        self.filename = filename
        
    def readChunkHeader(self, header):
        header.start_position = self.file.tell()
        header.chunk_id = self.file.readShort()
        header.chunk_length = self.file.readInt()
       # print "------------\n%d" %(header.start_position)
       # print "%X" %(header.chunk_id)
       # print "%d\n---------------" %(header.chunk_length)

    def parseFile(self, filename):
        self.filename = filename
        return self.parse()

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
                    self.object.materials = []
                    self.object.meshes = []
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
                    print "  Master scale: %.2f" %(self.object.masterScale)
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
        material.textures = []
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.MATERIAL_NAME):
                    material.name = self.readName()
                    print "   Name: %s" %(material.name)
                    break
                if case(_3DS.AMBIENT_COLOR):
                    os.write(1,"   Ambient color: ")
                    material.ambientColor = self.readColor()
                    break
                if case(_3DS.DIFFUSE_COLOR):
                    os.write(1, "   Diffuse color: ")
                    material.diffuseColor = self.readColor()
                    break
                if case(_3DS.SPECULAR_COLOR):
                    os.write(1, "   Specular color: ")
                    material.specularColor = self.readColor()
                    break
                if case(_3DS.SHININESS_PERCENT):
                    os.write(1, "   Shininess percent: ")
                    material.shininess = self.readPercent()
                    break
                if case(_3DS.SHIN2PCT_PERCENT):
                    os.write(1, "   Shininess sterngth: ")
                    material.shininessSterngth = self.readPercent()
                    break
                if case(_3DS.SHIN3PCT_PERCENT):
                    os.write(1, "   Shininess secoind sterngth: ")
                    material.secondShininessSterength = self.readPercent()
                    break
                if case(_3DS.TRANSPARENCY_PERCENT):
                    os.write(1, "   Transparency percent: ")
                    material.transparency = self.readPercent()
                    break
                if case(_3DS.TRANSP_FALLOF_PERCENT):
                    os.write(1, "   Transparency fallof percent: ")
                    material.transparencyFallof = self.readPercent()
                    break
                if case(_3DS.REFLECTION_BLUR_PERCENT):
                    os.write(1, "   Reflection Blur percent: ")
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
                    print "   Wire size: %.2f" %(material.wireSize)
                    break
                if case(_3DS.SHADING):
                    material.shadingType = self.file.readShort()
                    print "   Shading: %d" %(material.shadingType)
                    break
                if case(_3DS.TEXTURE_MAP_1):
                    print "   Texture Map 1"
                    os.write(1, "    Percentage: ")
                    material.textureMap1 = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.textureMap1)
                    break
                if case(_3DS.TEXTURE_MAP_2):
                    print "   Texture Map 2"
                    os.write(1, "    Percentage: ")
                    material.textureMap2 = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.textureMap2)
                    break
                if case(_3DS.BUMP_MAP):
                    print "   Bump Map"
                    os.write(1, "    Percentage: ")
                    material.bumpMap = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.bumpMap)
                    break
                if case(_3DS.SPECULAR_MAP):
                    print "   Specular Map"
                    os.write(1, "    Percentage: ")
                    material.specularMap = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.specularMap)
                    break
                if case(_3DS.REFLECTION_MAP):
                    print "   Reflection Map"
                    os.write(1, "    Percentage: ")
                    material.reflectionMap = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.reflectionMap)
                    break
                if case(_3DS.OPACITY_MAP):
                    print "   Opacity Map"
                    os.write(1, "    Percentage: ")
                    material.opacityMap = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.opacityMap)
                    break
                if case(_3DS.SHININESS_MAP):
                    print "   Shininess Map"
                    os.write(1, "    Percentage: ")
                    material.shininessMap = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.shininessMap)
                    break
                if case(_3DS.TEXTURE_1_MASK):
                    print "   Texture 1 mask"
                    material.textureMask1 = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.textureMask1)
                    break
                if case(_3DS.TEXTURE_2_MASK):
                    print "   Texture 2 mask"
                    material.textureMask2 = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.textureMask2)
                    break
                if case(_3DS.OPACITY_MASK):
                    print "   Opacity mask"
                    material.opacityMask = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.opacityMask)
                    break
                if case(_3DS.BUMP_MASK):
                    print "   Bump mask"
                    material.bumpMask = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.bumpMask)
                    break
                if case(_3DS.SHININESS_MASK):
                    print "   Shininess mask"
                    material.shininessMask = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.shininessMask)
                    break
                if case(_3DS.SPECULAR_MASK):
                    print "   Specular mask"
                    material.specularMask = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.specularMask)
                    break
                if case(_3DS.REFLECTION_MASK):
                    print "   Reflection mask"
                    material.reflectionMask = self.readTextureChunk(header.chunk_length - 6)
                    material.textures.append(material.reflectionMask)
                    break
                if case():
                    print "   Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        self.object.materials.append(material)

    def readMeshChunk(self, bytes):
        mesh = Chunks.MeshChunk()
        mesh.name = self.readName()
        print "   Name: %s" %(mesh.name)
        bytes = bytes - (len(mesh.name) - 1)
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.MESH_DATA):
                    mesh.type = 1
                    print "   Mesh data"
                    mesh.data = self.readMeshData(header.chunk_length - 6)
                    break
                if case(_3DS.LIGHT):
                    mesh.type = 2
                    print "   Light"
                    mesh.light = self.readLightChunk(header.chunk_length - 6)
                    break
                if case(_3DS.CAMERA):
                    mesh.type = 3
                    print "   Camera"
                    mesh.camera = self.readCameraChunk(header.chunk_length - 6)
                    break
                if case():
                    print "   Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        self.object.meshes.append(mesh)

    def readTextureChunk(self, bytes):
        texture = Chunks.TextureChunk()
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.INT_PERCENTAGE):
                    texture.percentage = self.file.readShort()
                    print texture.percentage
                    break
                if case(_3DS.MAPPING_FILENAME):
                    texture.name = self.readName()
                    print "    Filename: %s" %(texture.name)
                    break
                if case(_3DS.MAP_TEXBLUR):
                    texture.blur = self.file.readFloat()
                    print "    Texture blur: %.2f" %(texture.blur)
                    break
                if case(_3DS.MAP_TILING):
                    texture.tiling = self.file.readShort()
                    print "    Texture tiling: %d" %(texture.tiling)
                    break
                if case(_3DS.MAP_ANGLE):
                    texture.rotationAngle = self.file.readFloat()
                    print "    Rotation angle: %.2f" %(texture.rotationAngle)
                    break
                if case(_3DS.MAP_U_SCALE):
                    texture.uScale = self.file.readFloat()
                    print "    U Scale: %.2f" %(texture.uScale)
                    break
                if case(_3DS.MAP_V_SCALE):
                    texture.vScale = self.file.readFloat()
                    print "    V Scale: %.2f" %(texture.vScale)
                    break
                if case(_3DS.MAP_U_OFFSET):
                    texture.uOffset = self.file.readFloat()
                    print "    U Offset: %.2f" %(texture.uOffest)
                    break
                if case(_3DS.MAP_V_OFFSET):
                    texture.vOffset = self.file.readFloat()
                    print "    V Offset: %.2f" %(texture.vOffset)
                    break
                if case(_3DS.MAP_COL1):
                    os.write(1, "    Color 1: ")
                    texture.firstBlendColor = self.readColor()
                    break
                if case(_3DS.MAP_COL2):
                    os.write(1, "    Color 2: ")
                    texture.secondBlendColor = self.readColor()
                    break
                if case(_3DS.MAP_R_COL):
                    os.write(1, "    R_Color: ")
                    texture.redBlendColor = self.readColor()
                    break
                if case(_3DS.MAP_G_COL):
                    os.write(1, "    G_Color: ")
                    texture.greenBlendColor = self.readColor()
                    break
                if case(_3DS.MAP_B_COL):
                    os.write(1, "    B_Color: ")
                    texture.blueBlendColor = self.readColor()
                    break
                if case(_3DS.MAT_BUMP_PERCENT):
                    texture.bumpPercentage = self.file.readShort()
                    print "    Bump percent: %d" %(texture.bumpPercentage)
                    break
                if case():
                    print "   Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        return texture

    def readMeshData(self, bytes):
        data = Chunks.MeshData()
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.VERTICES_LIST):
                    data.vertices = []
                    data.nrOfVertices = self.file.readShort()
                    for i in range(0, data.nrOfVertices):
                        data.vertices.append(self.file.readArray(3, 'f'))
                    print "    Number of vertices: %d" %(data.nrOfVertices)
                    break
                if case(_3DS.MAPPING_COORDINATES_LIST):
                    data.nrOfCoordinates = self.file.readShort()
                    data.coordinates = []
                    for i in range(0, data.nrOfCoordinates):
                        data.coordinates.append(self.file.readArray(2, 'f'))
                    print "    Number of map coordinates: %d" %(data.nrOfCoordinates)
                    break
                if case(_3DS.FACES_DESCRIPTION):
                    data.faces = self.readFacesChunk(header.chunk_length - 6)
                    break
                if case(_3DS.LOCAL_COORDINATES_SYSTEM):
                    print "    Mesh Matrix: "
                    data.matrix = self.file.readArray(12, 'f')
                    for i in range(0, 4):
                        print "     %.2f %.2f %.2f" %(data.matrix[i*3], data.matrix[i*3+1], data.matrix[i*3+2])
                    break
                if case(_3DS.MESH_COLOR):
                    data.color = self.file.readByte()
                    print "    Mesh color: %d" %(data.color)
                    break
                if case(_3DS.MESH_TEXTURE_INFO):
                    data.textureInfo = Chunks.TextureInfoChunk()
                    data.textureInfo.mapType = self.file.readShort()
                    data.textureInfo.tiling = self.file.readFloat()
                    data.textureInfo.icon = self.file.readFloat()
                    data.textureInfo.matrix = self.file.readArray(12, 'f')
                    data.textureInfo.planIconW = self.file.readFloat()
                    data.textureInfo.planIconH = self.file.readFloat()
                    data.textureInfo.cylIconH = self.file.readFloat()
                    print "    Mesh Texture info"
                    break
                if case(_3DS.BOX_MAP):
                    print "    Box Map"
                    data.mapMaterials = []
                    for i in range(0, 6):
                        data.mapMaterials.append(self.readName())
                        print "     %s" %(data.mapMaterials[i])
                    break
                if case():
                    print "    Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        return data

    def readFacesChunk(self, bytes):
        faces = Chunks.FacesChunk()
        faces.nrOfFaces = self.file.readShort()
        faces.flags = []
        faces.faces = []
        faces.materialGroups = []
        for i in range(0, faces.nrOfFaces):
            faces.faces.append(self.file.readArray(3, 'H'))
            faces.flags.append(self.file.readShort())
        print "    Number of faces: %d" %(faces.nrOfFaces)
        bytes = bytes - faces.nrOfFaces*8 + 2
        header = Chunks.ChunkHeader()
        while bytes > 0:
            self.readChunkHeader(header)
            for case in switch(header.chunk_id):
                if case(_3DS.MESH_MATERIAL_GROUP):
                    group = Chunks.MaterialGroupChunk()
                    group.materialName = self.readName()
                    group.nrOfFaces = self.file.readShort()
                    group.faces = self.file.readArray(group.nrOfFaces, 'H')
                    print "    Mesh Group"
                    print "     Material name: %s" %(group.materialName)
                    print "     Number of faces: %d" %(group.nrOfFaces)
                    faces.materialGroups.append(group)
                    break
                if case(_3DS.SMOOTHING_GROUP_LIST):
                    faces.smoothingList = self.file.readArray(faces.nrOfFaces, 'l')
                    print "    Face Smoothing Group"
                    break
                if case():
                    print "    Skip unknown %X subchunk" %(header.chunk_id)
            self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
            bytes = self.updateBytesToRead(bytes, header.chunk_length)
        return faces

    def readLightChunk(self, bytes):
        pass

    def readCameraChunk(self, bytes):
        pass

    def readKeyFrameChunk(self, bytes):
        pass

    def readName(self):
        name = ""
        while True:
            c = self.file.readChar()
            name = name + c
            if c == '\0':
                break
        return name

    def readColor(self):
        color = self.file.readArray(3, 'B')
        print color
        return color

    def readFloatColor(self):
        header = Chunks.ChunkHeader()
        self.readChunkHeader(header)
        for case in switch(header.chunk_id):
            if case(_3DS.LIN_COLOR_F) or case(_3DS.COLOR_F):
                color = self.file.readArray(3, 'f')
                print color
                break
            if case():
                print "    Skip unknown %X subchunk" %(header.chunk_id)
        self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
        return color

    def readPercent(self):
        percent = 0
        header = Chunks.ChunkHeader()
        self.readChunkHeader(header)
        for case in switch(header.chunk_id):
            if case(_3DS.INT_PERCENTAGE):
                percent = self.file.readShort()
                print percent
                break
            if case():
                print "    Skip unknown %X subchunk" %(header.chunk_id)
        self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
        return percent
         
    def readFloatColor(self):
        percent = 0
        header = Chunks.ChunkHeader()
        self.readChunkHeader(header)
        for case in switch(header.chunk_id):
            if case(_3DS.FLOAT_PERCENTAGE):
                percent = self.file.readFloat()
                print percent
                break
            if case():
                print "    Skip unknown %X subchunk" %(header.chunk_id)
        self.file.seek(header.start_position + header.chunk_length, os.SEEK_SET)
        return percent

    def updateBytesToRead(self, bytes, length):
        if length == 0:
            return 0
        bytes = bytes - length
        if bytes < 0:
            self.file.seek(bytes, os.SEEK_CUR)
            return 0
        return bytes
                
                
                
        
            
        
        
