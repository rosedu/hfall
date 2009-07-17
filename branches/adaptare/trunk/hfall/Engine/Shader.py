"""
Hammerfall Shader classes. Loading and using shaders.

Basic steps required for loading and running a shader:

1. Import all the classes in this file.

2. Set up the manager. Example:
    myShaderManager = Shader.ShaderManager()

3. Create the shader instances. Example:
    vertexShader1 = myShaderManager.addVertexShader('vshaderfile.vsh')
    fragmentShader1 = myShaderManager.addFragmentShader('fshaderfile.fsh')
    vertexShader2 = myShaderManager.addVertexShader('vshaderfile.vsh')
    Note: On this example de vshaderfile.vsh will only be loaded once.

4. Create the shader program. Example:
    shader = ShaderProgram(vertexShader1, fragmentShader1, vertexShader2)

5. Run the shader program. Example:
    shader.use()
    Note: This will do all the necessary compilation and linking steps.
"""

__version__ = '0.7'
__authors__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)\
               Dragos Dena (dragos.dena@gmail.com)'

import sys
sys.path.insert(0, "...")
from ctypes import (
    byref, c_char, c_char_p, c_int, cast, create_string_buffer, pointer,
    POINTER
)
from pyglet.gl import *

import base
import Manager


class ShaderError(Exception): pass
class CompileError(ShaderError): pass
class LinkError(ShaderError): pass


shaderErrors = {
    GL_INVALID_VALUE: 'GL_INVALID_VALUE (bad 1st arg)',
    GL_INVALID_OPERATION: 'GL_INVALID_OPERATION '
        '(bad id or immediate mode drawing in progress)',
    GL_INVALID_ENUM: 'GL_INVALID_ENUM (bad 2nd arg)',
}

class ShaderManager(Manager.Manager):
    """
    Shader resource manager. We are not defining the addInstance method,\
    because we need two methods for adding two different types of instances:
    * VertexShader
    * FragmentShader
    """
    
    def addVertexShader(self, resourceFileName):
        if resourceFileName in self.resourceList:
            resource = self.resourceList[resourceFileName]
            instance = VertexShader(resource)
            resource.incrementAppearences()
        else:
            resource = ShaderResource(resourceFileName, self)
            self.resourceList[resourceFileName] = resource
            instance = VertexShader(resource)
        return instance
    
    def addFragmentShader(self, resourceFileName):
        if resourceFileName in self.resourceList:
            resource = self.resourceList[resourceFileName]
            instance = FragmentShader(resource)
            resource.incrementAppearences()
        else:
            resource = ShaderResource(resourceFileName, self)
            self.resourceList[resourceFileName] = resource
            instance = FragmentShader(resource)
        return instance


class ShaderResource(Manager.Resource):
    """
    Hammerfall Shader Resource Class. Check Manager.py for details about the
    Resource class.
    Initialisation:
    __init__(self, filename, manager)
    filename -> the name of the shader file.
    manager -> the Hammerfall manager 
    """
    
    def __del__(self):
        """
        Delets the shader resource.
        """
        if self.loaded == False:
            pass
        else:
            del self.fileContent
            
    def loadResource(self):
        """
        Loads the shader to fileContent.
        """
        f = open(self.filename)
        try:
            self.fileContent = f.read()
        finally:
            f.close()
        return self.fileContent


class Shader(Manager.Instance):
    """
    Hammerfall Shader Class. It inherents the instance class. 
    Vertex Shaders And Fragment Shaders inherent this class.
    Initialisation of a Shader object:
    __init__(self, shaderResource)
    shaderResource is an object of the type ShaderResource (described above).
    type reffers to Vertex Shader or Fragment Shader. The type is defined for
    the two classes which inherent the Shader Class.
    """
    
    def __init__(self, shaderResource):
        Manager.Instance.__init__(self, shaderResource)
        self.shaderId = None
        self.type = None
        
    def get(self, paramId):
        """
        Returns the requested object parameter depending on the paramId.
        The supported paramId's are:
        GL_SHADER_TYPE,
	    GL_DELETE_STATUS,
		GL_COMPILE_STATUS,
		GL_INFO_LOG_LENGTH,
		GL_SHADER_SOURCE_LENGTH
		If the shader wasn't compiled (shaderId is set to None) the function
		will return False.
        """
        if self.shaderId == None:
            return False
        outvalue = c_int(0)
        glGetShaderiv(self.shaderId, paramId, byref(outvalue))
        value = outvalue.value
        if value in shaderErrors.keys():
            msg = '%s from glGetShader(%s, %s, &value)'
            raise ValueError(msg % (shaderErrors[value], self.id, paramId))
        return value
        
    def getCompileStatus(self):
        """
        Returns the status of the compilation.
        """
        return bool(self.get(GL_COMPILE_STATUS))

    def getInfoLogLength(self):
        """
        Returns the length of the shader info log.
        """
        return self.get(GL_INFO_LOG_LENGTH)

    def getInfoLog(self):
        """
        Returns the actual shader info log.
        """
        length = self.getInfoLogLength()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        glGetShaderInfoLog(self.shaderId, length, None, buffer)
        return buffer.value
        
    def compile(self):
        """
        Compiles the shader.
        The type of the shader is specified in their respective class (which\
        inherents this one).
        """
        if self.type == None:
            return
        self.shaderId = glCreateShader(self.type)
        self.resource.loadResource()
        shaderContent = (c_char_p)(self.resource.fileContent)
        shaderContentP = cast(pointer(shaderContent), POINTER(POINTER(c_char)))
        glShaderSource(self.shaderId, 1, shaderContentP, None)
        glCompileShader(self.shaderId)
        if not self.getCompileStatus():
            raise CompileError(self.getInfoLog())
            
            
class VertexShader(Shader):
    """
    The Hammerfall Vertex Shader Class. Inherents the Shader class above.
    """
    def __init__(self, shaderResource):
        Shader.__init__(self, shaderResource)
        self.type = GL_VERTEX_SHADER
    

class FragmentShader(Shader):
    """
    The Hammerfall Fragment Shader Class. Inherents the Shader class above.
    """
    def __init__(self, shaderResource):
        Shader.__init__(self, shaderResource)
        self.type = GL_FRAGMENT_SHADER
        
        
class ShaderProgram():

    def __init__(self, *shaders):
        """
        The initialisation takes as argument a list of shaders.
        """
        self.shaders = list(shaders)
        self.programId = None
        
    def get(self, paramId):
        """
        Returns the requested object parameter based on the paramId given.
        paramId can take one of the following values:
        GL_DELETE_STATUS,
		GL_LINK_STATUS,
		GL_VALIDATE_STATUS,
		GL_INFO_LOG_LENGTH,
	    GL_ATTACHED_SHADERS,
		GL_ACTIVE_ATTRIBUTES,
		GL_ACTIVE_ATTRIBUTE_MAX_LENGTH,
		GL_ACTIVE_UNIFORMS,
		GL_ACTIVE_UNIFORM_MAX_LENGTH
		If the program wasn't created the function will return False.
        """
        if self.programId == None:
            return False
        outvalue = c_int(0)
        glGetProgramiv(self.programId, paramId, byref(outvalue))
        value = outvalue.value
        if value in shaderErrors.keys():
            msg = '%s from glGetProgram(%s, %s, &value)'
            raise ValueError(msg % (shaderErrors[value], self.programId,\
                                                                    paramId))
        return value
        
    def getLinkStatus(self):
        return bool(self.get(GL_LINK_STATUS))

    def getInfoLogLength(self):
        """
        Returns the length of the info log.
        """
        return self.get(GL_INFO_LOG_LENGTH)

    def getInfoLog(self):
        """
        Returns the actual info log.
        """
        length = self.getInfoLogLength()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        glGetProgramInfoLog(self.programId, length, None, buffer)
        return buffer.value
        
    def getMessage(self):
        messages = []
        for shader in self.shaders:
            log = shader.getInfoLog()
            if log:
                messages.append(log)
        log = self.getInfoLog()
        if log:
            messages.append(log)
        return '\n'.join(messages)

    def use(self):
        self.programId = glCreateProgram()
        for shader in self.shaders:
            shader.compile()
            glAttachShader(self.programId, shader.shaderId)
        glLinkProgram(self.programId)
        message = self.getMessage()
        if not self.getLinkStatus():
            raise LinkError(message)
        glUseProgram(self.programId)
        return message

