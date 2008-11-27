import sys
sys.path.insert(0, "..")
from ctypes import *
from pyglet.gl import *
from switch import switch
from Vector import *

class Variable:

    def __init__(self, _type, loc, val):
        self.type = _type
        self.location = None
        self.value = val

class Shader:
    glInfo = None
    
    def __init__(self, source, _type):
        if not self.__class__.glInfo:
            self.__class__.glInfo = gl_info.GLInfo()
            self.__class__.glInfo.set_active_context()
        self.shader = (GLuint)(*[])
        self.type = _type
        self.status = supports(_type)
        if self.status == GL_FALSE or source == None:
            return
        source = cast(pointer(pointer(create_string_buffer(source))), POINTER(POINTER(GLchar)))
        self.status = (GLint)(*[])
        self.shader = glCreateShader(_type)
        glShaderSource(self.shader, 1, source, None)
        glCompileShader(self.shader)
        glGetShaderif(self.shader, GL_COMPILE_STATUS, self.status)
        self.status = self.status.value

    def loadShader(self, filename):
        f = open(filename);
        source = f.read();
        if self.status == GL_FALSE or len(source) == 0:
            return
        self.status = (GLint)(*[])
        source = cast(pointer(pointer(create_string_buffer(source))), POINTER(POINTER(GLchar)))
        self.shader = glCreateShader(self.type)
        glShaderSource(self.shader, 1, source, None)
        glCompileShader(self.shader)
        glGetShaderiv(self.shader, GL_COMPILE_STATUS, self.status)
        self.status = self.status.value

    def getInfoLog(self):
        if self.status == GL_FALSE and not supports(self.type):
            return "Unsupported shader"
        logLength = (GLint)(*[])
        writen = (GLint)(*[])
        glGetShaderiv(self.shader, GL_INFO_LOG_LENGTH, logLength)
        log = c_buffer(logLength.value)
        if logLength > 0:
            glGetShaderInfoLog(self.shader, logLength, writen, log)
        return log.value

    
class ShaderProgram:

    def __init__(self, shaders):
        self.program = (GLuint)(*[])
        self.uniforms = {}
        self.attributes = {}
        self.status = supports(GL_PROGRAM_OBJECT_ARB)
        self.hasGeometryShader = False
        if self.status == GL_FALSE: return
        self.status = (GLint)(*[])
        self.program = glCreateProgram()
        for i in range(len(shaders)):
            if shaders[i].status == GL_TRUE:
                glAttachShader(self.program, shaders[i].shader)
                #if shaders[i].type == GL_GEOMETRY_SHADER_EXT:
                #    self.hasGeometryShader = True
        glLinkProgram(self.program)
        glGetProgramiv(self.program, GL_LINK_STATUS, self.status)
        self.status = self.status.value
        if self.status == GL_FALSE: return
        if self.hasGeometryShader:
            maxVertices = 0
            glGetIntegerv(GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT, maxVertices)
            glProgramParameteriEXT(self.program, GL_GEOMETRY_VERTICES_OUT_EXT, maxVertices)
        self.getUniformsAndAttributes()

    def validateProgram(self):
        if not self.program:
            return GL_FALSE
        logLength = (GLint)(*[])
        writen = (GLint)(*[])
        valid = (GLint)(*[])
        glValidateProgram(self.program)
        glGetProgramiv(self.program, GL_VALIDATE_STATUS, valid)
        return valid.value

    def getInfoLog(self):
        if not self.program:
            return "Shading language is unsupported"
        logLength = (GLint)(*[])
        writen = (GLint)(*[])
        glGetProgramiv(self.program, GL_INFO_LOG_LENGTH, logLength)
        log = c_buffer(logLength.value)
        if logLength > 0:
            glGetProgramInfoLog(self.program, logLength, writen, log)
        return log.value

    def setGeometryInputType(self, _type):
	if self.hasGeometryShader:
		glProgramParameteriEXT(self.program, GL_GEOMETRY_INPUT_TYPE_EXT, _type)

    def setGeometryOutputType(self, _type):
	if self.hasGeometryShader:
		glProgramParameteriEXT(self.program, GL_GEOMETRY_OUTPUT_TYPE_EXT, _type)

    def enable(self):
	if self.status == GL_TRUE:
		glUseProgram(self.program)

    def disable(self):
	glUseProgram(0)

    def setUniform(self, name, value):
        if not self.program: return
        if not name in self.uniforms: return
        u = self.uniforms[name]
        u.value = value
        if isinstance(value, float) or isinstance(value, int):
            if u.type == GL_FLOAT:
                glUniform1f(u.location, value)
            elif u.type == GL_INT:
                glUniform1i(u.location, value)
        elif isinstance(value, Vector2):
            if u.type == GL_INT_VEC2 or u.type == GL_BOOL_VEC2:
                glUniform2i(u.location, 1, value[0], value[1])
            elif u.type == GL_FLOAT_VEC2:
                glUniform2f(u.location, 1, value[0], value[1])
        elif isinstance(value, Vector3):
            if u.type == GL_INT_VEC3 or u.type == GL_BOOL_VEC3:
                glUniform3i(u.location, value[0], value[1], value[2])
            elif u.type == GL_FLOAT_VEC3:
                glUniform3f(u.location, value[0], value[1], value[2])
        elif isinstance(value, Vector4):
            if u.type == GL_INT_VEC4 or u.type == GL_BOOL_VEC4:
                glUniform4i(u.location, value[0], value[1], value[2], value[3])
            elif u.type == GL_FLOAT_VEC4:
                glUniform4f(u.location, value[0], value[1], value[2], value[3])
        elif isinstance(value, Matrix3):
            l = []
            if u.type == GL_FLOAT_MAT3:
                for i in range(3): l += value[i]
                glUniformMatrix3fv(u.location, 1, GL_FALSE, (GLfloat * 9)(*l))
        elif isinstance(value, Matrix4):
            l = []
            if u.type == GL_FLOAT_MAT4:
                for i in range(4): l += value[i]
                glUniformMatrix4fv(u.location, 1, GL_FALSE, (GLfloat * 4)(*l))

    def setAttribute(self, name, value):
        if not self.program: return
        if not name in self.attributes: return
        a = self.attributes[name]
        a.value = value
        if isinstance(value, float):
            if a.type == GL_FLOAT:
                glVertexAttrib1f(a.location, value)
            elif a.type == GL_INT:
                glVertexAttrib1i(a.location, value)
        elif isinstance(value, Vector2):
            if a.type == GL_INT_VEC2 or a.type == GL_BOOL_VEC2:
                glVertexAttrib2i(a.location, value[0], value[1])
            elif a.type == GL_FLOAT_VEC2:
                glVertexAttrib2f(a.location, value[0], value[1])
        elif isinstance(value, Vector3):
            if a.type == GL_INT_VEC3 or a.type == GL_BOOL_VEC3:
                glVertexAttrib3i(a.location, value[0], value[1], value[2])
            elif a.type == GL_FLOAT_VEC3:
                glVertexAttrib3f(a.location, value[0], value[1], value[2])
        elif isinstance(value, Vector4):
            if a.type == GL_INT_VEC4 or a.type == GL_BOOL_VEC4:
                glVertexAttrib4i(a.location, value[0], value[1], value[2], value[3])
            elif a.type == GL_FLOAT_VEC4:
                glVertexAttrib4f(a.location, value[0], value[1], value[2], value[3])

    def getUniformsAndAttributes(self):
        nameLength = (GLint)(*[])
        numVariables = (GLint)(*[])
        writeLength = (GLint)(*[])
        size = (c_int * 1)()
        _type = (GLuint)(*[])
	current = (c_int * 1)()
	glGetIntegerv(GL_CURRENT_PROGRAM, current)
	glUseProgram(self.program)
	
	glGetProgramiv(self.program, GL_ACTIVE_ATTRIBUTE_MAX_LENGTH, nameLength)
	glGetProgramiv(self.program, GL_ACTIVE_ATTRIBUTES, numVariables)
	for i in range(numVariables.value):
            attr = Variable(None, None, None)
            attr.type = (GLuint)(*[])
            name = c_buffer(nameLength.value)
            glGetActiveAttrib(self.program, i, nameLength.value, writeLength, size, _type, name)
            name = name.value
            attr.type = _type.value
	    if len(name) > 3 and name.find("gl_") != -1:
		continue
            attr.location = glGetAttribLocation(self.program, name)
	    self.attributes[name] = attr
	
	glGetProgramiv(self.program, GL_ACTIVE_UNIFORM_MAX_LENGTH, nameLength)
	glGetProgramiv(self.program, GL_ACTIVE_UNIFORMS, numVariables)
	for i in range(numVariables.value):
            unif = Variable(None, None, None)
            unif.type = (GLuint)(*[])
            name = c_buffer(nameLength.value)
            glGetActiveUniform(self.program, i, nameLength.value, writeLength, size, _type, name)
            name = name.value
            unif.type = _type.value
	    if len(name) > 3 and name.find("gl_") != -1:
		continue
	    unif.location = glGetUniformLocation(self.program, name)
	    self.uniforms[name] = unif
	
	glUseProgram(current[0])

def supports(_type):
    shader = Shader.glInfo.have_extension("GL_ARB_shader_objects")
    vertex = Shader.glInfo.have_extension("GL_ARB_vertex_shader")
    fragment = Shader.glInfo.have_extension("GL_ARB_fragment_shader")
    geometry = Shader.glInfo.have_extension("GL_EXT_geometry_shader4")

    if not shader:
        return False
    for case in switch(_type):
        if case(GL_VERTEX_SHADER): return vertex
        if case(GL_FRAGMENT_SHADER): return fragment
        if case(GL_PROGRAM_OBJECT_ARB): return shader
        #if case(GL_GEOMETRY_SHADER_EXT): return geometry
        if case(): return False

