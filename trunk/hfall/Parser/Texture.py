from TextureFormat import TextureFormat
from switch import switch
from Image import Image
from pyglet.gl import *

class Callable:
    def __init__(self, method):
        self.__call__ = method


class Texture:

    #texture target (dimension)
    TEXTURE_1D		= 0x0DE0
    TEXTURE_2D		= 0x0DE1
    TEXTURE_3D		= 0x806F
    TEXTURE_CUBE_MAP	= 0x8513
    TEXTURE_RECTANGLE	= 0x84F5

    #texture wrap mode
    CLAMP  = 2
    TILE   = 1
    ZERO   = 0

    #texture interpolate mode
    TRILINEAR_MIPMAP 	= 1 
    BILINEAR_MIPMAP 	= 2
    NEAREST_MIPMAP 	= 3
    BILINEAR_NO_MIPMAP 	= 4
    NEAREST_NO_MIPMAP 	= 5

    #texture depth read mode
    DEPTH_NORMAL	= 0x0000
    DEPTH_LEQUAL	= 0x0203
    DEPTH_GEQUAL	= 0x0206

    info = None

    class Parameters:
        def __init__(self):
            self.wrapMode = 1          # TILE
            self.maxLOD = 1000
            self.minLOD = -1000
            self.maxAnisotropy = 1
            self.depthReadMode = 0     # DEPTH_NORMAL
            self.interpolateMode = 1   # TRILINEAR_MIPMAP
            self.autoGenerateMipMaps = False

        def defaults():
            return Texture.Parameters()

        def video():
            param = Texture.Parameters()
            param.interpolateMode = Texture.BILINEAR_NO_MIPMAP
            param.wrapMode = Texture.CLAMP
            param.depthReadMode = Texture.DEPTH_NORMAL
            param.maxAnisotropy = 1.0
            param.autoGenerateMipMaps = True
            return param

        def shadow():
            param = Texture.Parameters()
            param.interpolateMode = Texture.BILINEAR_NO_MIPMAP
            param.wrapMode = Texture.CLAMP
            param.depthReadMode = Texture.DEPTH_LEQUAL
            param.maxAnisotropy = 1.0
            param.autoGenerateMipMaps = False
            return param

        defaults = Callable(defaults)
        shadow = Callable(shadow)
        video = Callable(video)

    class Settings:
        def __init__(self):
            self.scaleFactor = 1

        def defaults():
            return Settings()

        defaults = Callable(defaults)


    def __init__(self, name, glID, target, format, parameters):
        if not self.__class__.info:
            self.__class__.info = gl_info.GLInfo()
            self.__class__.info.set_active_context()
        self.name = name
        self.glID = glID
        self.width = (GLint)(*[])
        self.height = (GLint)(*[])
        self.format = format
        self.target = target
        self.parameters = parameters
        glBindTexture(target, glID)
	glGetTexLevelParameteriv(target, 0, GL_TEXTURE_WIDTH, self.width)
	glGetTexLevelParameteriv(target, 0, GL_TEXTURE_HEIGHT, self.height)
	self.setTexParameters(target, parameters)

    def create(name, bytes, width, height, target, format, param, settings):
        glID = (GLuint)(*[])
        glGenTextures(1, glID)
        glBindTexture(target, glID)
	
	hasMipMaps = param.interpolateMode != Texture.BILINEAR_NO_MIPMAP and \
                     param.interpolateMode != Texture.NEAREST_NO_MIPMAP
	if hasMipMaps and param.autoGenerateMipMaps:
            glTexParameteri(target, GL_GENERATE_MIPMAP_SGIS, GL_TRUE)

        for case in switch(target):
            if case(Texture.TEXTURE_1D):
		break
	    if case(Texture.TEXTURE_2D):
		if hasMipMaps and not param.autoGenerateMipMaps:
		    gluBuild2DMipmaps(target, format.internalFormat, width, height, format.format, format.dataFormat, bytes)
		else:
                    glTexImage2D(target, 0, format.internalFormat, width, height, 0, format.format, format.dataFormat, bytes)
		break
	    if case(Texture.TEXTURE_3D):
		glTexImage3DEXT(target, 0, format.internalFormat, width, height, depth, 0, format.format, format.dataFormat, bytes)
		break
	    if case(Texture.TEXTURE_CUBE_MAP):
		break
	    if case(Texture.TEXTURE_RECTANGLE):
		break
        return Texture(name, glID, target, format, param)

    def setTexParameters(target, param):
        color = (GLfloat * 4)(*[0, 0, 0, 0])
        mode = GL_NONE
        for case in switch(param.wrapMode):
            if case(Texture.TILE):
                mode = GL_REPEAT
                break
            if case(Texture.CLAMP):
                if Texture.info.have_extension("GL_EXT_texture_edge_clamp"):
                    mode = GL_CLAMP_TO_EDGE
                else: mode = GL_CLAMP
                break
            if case(Texture.ZERO):
                if Texture.info.have_extension("GL_ARB_texture_border_clamp"):
                    mode = GL_CLAMP_TO_BORDER_ARB
                else: mode = GL_CLAMP
                glTexParameterfv(target, GL_TEXTURE_BORDER_COLOR, color)
                break
        glTexParameteri(target, GL_TEXTURE_WRAP_S, mode)
        glTexParameteri(target, GL_TEXTURE_WRAP_T, mode)
        if Texture.info.have_extension("GL_EXT_texture3D"):
            glTexParameteri(target, GL_TEXTURE_WRAP_R, mode)

        hasMipMaps = (target != Texture.TEXTURE_RECTANGLE) and \
    		     (param.interpolateMode != Texture.BILINEAR_NO_MIPMAP) and \
    		     (param.interpolateMode != Texture.NEAREST_NO_MIPMAP)

    	if hasMipMaps and (Texture.info.have_extension("GL_EXT_texture_lod") or \
                           Texture.info.have_extension("GL_SGIS_texture_lod")):
            glTexParameteri(target, GL_TEXTURE_MAX_LOD_SGIS, param.maxLOD)
            glTexParameteri(target, GL_TEXTURE_MIN_LOD_SGIS, param.minLOD)

        supports_generate_mipmaps = Texture.info.have_extension("GL_SGIS_generate_mipmap")

        for case in switch(param.interpolateMode):
            if case(Texture.TRILINEAR_MIPMAP):
                glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
	        if supports_generate_mipmaps:
	            glTexParameteri(target, GL_GENERATE_MIPMAP_SGIS, GL_TRUE)
	        break
            if case(Texture.BILINEAR_MIPMAP):
	        glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
	        if param.autoGenerateMipMaps and supports_generate_mipmaps:
	            glTexParameteri(target, GL_GENERATE_MIPMAP_SGIS, GL_TRUE)
	        break
	
	    if case(Texture.NEAREST_MIPMAP):
	        glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
	        if param.autoGenerateMipMaps and supports_generate_mipmaps:
	            glTexParameteri(target, GL_GENERATE_MIPMAP_SGIS, GL_TRUE)
	        break
	
	    if case(Texture.BILINEAR_NO_MIPMAP):
	        glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	        break
	
	    if case(Texture.NEAREST_NO_MIPMAP):
	        glTexParameteri(target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	        break

        if Texture.info.have_extension("GL_EXT_texture_filter_anisotropic"):
            glTexParameterf(target, GL_TEXTURE_MAX_ANISOTROPY_EXT, param.maxAnisotropy)

        if Texture.info.have_extension("GL_ARB_shadow"):
            if param.depthReadMode == Texture.DEPTH_NORMAL:
                glTexParameteri(target, GL_TEXTURE_COMPARE_MODE_ARB, GL_NONE)
            else:
                glTexParameteri(target, GL_TEXTURE_COMPARE_MODE_ARB, GL_COMPARE_R_TO_TEXTURE_ARB)
                glTexParameteri(target, GL_TEXTURE_COMPARE_FUNC_ARB, param.depthReadMode)


    def delete(self):
        glDeleteTextures(1, self.glID)
        self.glID = None

    create = Callable(create)
    setTexParameters = Callable(setTexParameters)
    
