from Coordinate import Coordinate
from pyglet.gl import *
from Matrix import *
from Vector import *

glInfo = None

def glVertex(vector):
    if isinstance(vector, Vector2):
        glVertex2f(vector[0], vector[1])
    elif isinstance(vector, Vector3):
        glVertex3f(vector[0], vector[1], vector[2])
    elif isinstance(vector, Vector4):
        glVertex4f(vector[0], vector[1], vector[2], vector[4])
    elif isinstance(vector, list):
        if len(vector) == 2:
            glVertex2fv((GLfloat*2)(*vector))
        elif len(vector) == 3:
            glVertex3fv((GLfloat*3)(*vector))
        elif len(vector) == 4:
            glVertex4fv((GLfloat*4)(*vector))

def glColor(color):
    if isinstance(color, Vector3):
        glColor3f(color[0], color[1], color[2])
    elif isinstance(color, Vector4):
        glColor4f(color[0], color[1], color[2], color[3])
    elif isinstance(color, list):
        if len(color) == 3:
            glColor3fv((GLfloat*3)(*color))
        elif len(color) == 4:
            glColor4fv((GLfloat*4)(*color))

def glNormal(normal):
    if isinstance(normal, Vector3):
        glNormal3f(normal[0], normal[1], normal[2])
    elif isinstance(normal, list):
        if len(normal) == 3:
           glNormal3fv((GLfloat*3)(*normal))

def glTexCoord(tex):
    if isinstance(tex, Vector2):
        glTexCoord2f(tex[0], tex[1])
    if isinstance(tex, Vector2):
        glTexCoord3f(tex[0], tex[1], tex[2])
    if isinstance(tex, Vector2):
        glTexCoord4f(tex[0], tex[1], tex[2], tex[3])
    elif isinstance(tex, list):
        if len(tex) == 2:
            glTexCoord2fv((GLfloat*2)(*tex))
        if len(tex) == 2:
            glTexCoord3fv((GLfloat*3)(*tex))
        if len(tex) == 2:
            glTexCoord4fv((GLfloat*4)(*tex))

def glMultiTexCoord(unit, tex):
    if isinstance(tex, Vector2):
        glMultiTexCoord2fARB(unit, tex[0], tex[1])
    if isinstance(tex, Vector2):
        glMultiTexCoord3fARB(unit, tex[0], tex[1], tex[2])
    if isinstance(tex, Vector2):
        glMultiTexCoord4fARB(unit, tex[0], tex[1], tex[2], tex[3])
    elif isinstance(tex, list):
        if len(tex) == 2:
            glMultiTexCoord2fvARB(unit, (GLfloat*2)(*tex))
        if len(tex) == 3:
            glMultiTexCoord3fvARB(unit, (GLfloat*3)(*tex))
        if len(tex) == 4:
            glMultiTexCoord4fvARB(unit, (GLfloat*4)(*tex))

def glGetVector2(name):
    v = (GLfloat*4)(*[])
    glGetFloatv(name, v)
    return Vector2(v[0], v[1])

def glGetVector3(name):
    v = (GLfloat*4)(*[])
    glGetFloatv(name, v)
    return Vector3(v[0], v[1], v[2])

def glGetVector4(name):
    v = (GLfloat*4)(*[])
    glGetFloatv(name, v)
    return Vector4(v[0], v[1], v[2], v[3])

def glGetMatrix(name):
    m = (GLfloat*16)(*[])
    glGetFloatv(name, m)
    return Matrix4(m).transpose()

def glLoadMatrix(matrix4):
    m = matrix4
    if isinstance(matrix4, Coordinate):
        m = matrix4.matrix()
    elif isinstance(matrix4, list):
        m = Matrix4(matrix4)
    if isinstance(m, Matrix4):
        transp = (GLfloat * 16)(*[])
        for i in range(4):
            for j in range(4):
                transp[4*i+j] = m[j][i]
        m = transp
    glLoadMatrixf(m)

def glMultMatrix(matrix4):
    m = matrix4
    if isinstance(matrix4, Coordinate):
        m = matrix4.matrix()
    elif isinstance(matrix4, list):
        m = Matrix4(matrix4)
    if isinstance(m, Matrix4):
        transp = (GLfloat * 16)(*[])
        for i in range(4):
            for j in range(4):
                transp[4*i+j] = m[i][j]
        m = transp
    glMultMatrixf(m)

def glLoadInvMatrix(matrix4):
    if isinstance(matrix4, Matrix4):
        inverse = matrix4.inverse()
    if isinstance(matrix4, Coordinate):
        inverse = matrix4.inverseMatrix()
    else: inverse = matrix4
    glLoadMatrix(inverse)

def glMultInvMatrix(matrix4):
    if isinstance(matrix4, Matrix4):
        inverse = matrix4.inverse()
    if isinstance(matrix4, Coordinate):
        inverse = matrix4.invMatrix()
    else: inverse = matrix4
    glMultMatrix(inverse)

def glDisableAllTextures():
    if not glInfo:
        glInfo = gl_info.GLInfo()
        glInfo.set_active_context()
    
    glDisable(GL_TEXTURE_1D)
    glDisable(GL_TEXTURE_2D)
    if glInfo.have_extension("GL_EXT_texture3D"):
        glDisable(GL_TEXTURE_3D)
    if glInfo.have_extension("GL_EXT_texture_cube_map"):
        glDisable(GL_TEXTURE_CUBE_MAP_ARB)
    if glInfo.have_extension("GL_EXT_texture_rectangle"):
        glDisable(GL_TEXTURE_RECTANGLE_ARB)
    
