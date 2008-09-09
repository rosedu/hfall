"""
Mathematic auxiliary functions
"""

import pyglet
from pyglet.gl import *
import math

#matrix identity
def identity(n):
        if n == 4: return __identity4()
        elif n==3: return __identity3()

def __identity4():
        return (GLfloat * 16)(*[1, 0, 0, 0,
                                0, 1, 0, 0,
                                0, 0, 1, 0,
                                0, 0, 0, 1])
def __identity3():
        return (GLfloat * 9)(*[1, 0, 0,
                                0, 1, 0,
                                0, 0, 1])

#matrix multiplication
def matrixmult(m1, m2):
        size = m1.__len__()
        if size == 16: return __matrixmult4(m1, m2)
        elif size == 9: return __matrixmult3(m1, m2)

def __matrixmult4(m1, m2):
	m = (GLfloat * 16)(*(16 * [0]))

	m[0] = m1[0] * m2[0] + m1[4] * m2[1] + m1[8] * m2[2] + m1[12] * m2[3]
	m[1] = m1[1] * m2[0] + m1[5] * m2[1] + m1[9] * m2[2] + m1[13] * m2[3]
	m[2] = m1[2] * m2[0] + m1[6] * m2[1] + m1[10] * m2[2] + m1[14] * m2[3]
	m[3] = m1[3] * m2[0] + m1[7] * m2[1] + m1[11] * m2[2] + m1[15] * m2[3]

	m[4] = m1[0] * m2[4] + m1[4] * m2[5] + m1[8] * m2[6] + m1[12] * m2[7]
	m[5] = m1[1] * m2[4] + m1[5] * m2[5] + m1[9] * m2[6] + m1[13] * m2[7]
	m[6] = m1[2] * m2[4] + m1[6] * m2[5] + m1[10] * m2[6] + m1[14] * m2[7]
	m[7] = m1[3] * m2[4] + m1[7] * m2[5] + m1[11] * m2[6] + m1[15] * m2[7]

	m[8] = m1[0] * m2[8] + m1[4] * m2[9] + m1[8] * m2[10] + m1[12] * m2[11]
	m[9] = m1[1] * m2[8] + m1[5] * m2[9] + m1[9] * m2[10] + m1[13] * m2[11]
	m[10] = m1[2] * m2[8] + m1[6] * m2[9] + m1[10] * m2[10] + m1[14] * m2[11]
	m[11] = m1[3] * m2[8] + m1[7] * m2[9] + m1[11] * m2[10] + m1[15] * m2[11]

	m[12] = m1[0] * m2[12] + m1[4] * m2[13] + m1[8] * m2[14] + m1[12] * m2[15]
	m[13] = m1[1] * m2[12] + m1[5] * m2[13] + m1[9] * m2[14] + m1[13] * m2[15]
	m[14] = m1[2] * m2[12] + m1[6] * m2[13] + m1[10] * m2[14] + m1[14] * m2[15]
	m[15] = m1[3] * m2[12] + m1[7] * m2[13] + m1[11] * m2[14] + m1[15] * m2[15]

	return m

def __matrixmult3(m1, m2):
	m = (GLfloat * 9)(*(9 * [0]))

	m[0] = m1[0] * m2[0] + m1[3] * m2[1] + m1[6] * m2[2]
	m[1] = m1[1] * m2[0] + m1[4] * m2[1] + m1[7] * m2[2]
	m[2] = m1[2] * m2[0] + m1[5] * m2[1] + m1[8] * m2[2]
	
	m[3] = m1[0] * m2[3] + m1[3] * m2[4] + m1[6] * m2[5]
	m[4] = m1[1] * m2[3] + m1[4] * m2[4] + m1[7] * m2[5]
	m[5] = m1[2] * m2[3] + m1[5] * m2[4] + m1[8] * m2[5]
	
	m[6] = m1[0] * m2[6] + m1[3] * m2[7] + m1[6] * m2[8]
	m[7] = m1[1] * m2[6] + m1[4] * m2[7] + m1[7] * m2[8]
	m[8] = m1[2] * m2[6] + m1[5] * m2[7] + m1[8] * m2[8]
	
	return m

#matrix determinant
def det(m):
        size = m.__len__()
        if size == 16: return __det4(m)
        elif size == 9: return __det3(m)

def __det4(m):
        return m[0] * m[5] * m[10] * m[15] +\
               m[0] * m[7] * m[9] * m[14] +\
               m[0] * m[6] * m[11] * m[13] -\
               m[0] * m[7] * m[10] * m[13] -\
               m[0] * m[5] * m[11] * m[14] -\
               m[0] * m[6] * m[9] * m[15] -\
               \
               m[4] * m[1] * m[10] * m[15] -\
               m[4] * m[3] * m[9] * m[14] -\
               m[4] * m[2] * m[11] * m[13] +\
               m[4] * m[3] * m[10] * m[13] +\
               m[4] * m[1] * m[11] * m[14] +\
               m[4] * m[2] * m[9] * m[15] -\
               \
               m[8] * m[5] * m[2] * m[15] -\
               m[8] * m[7] * m[1] * m[14] -\
               m[8] * m[6] * m[3] * m[13] +\
               m[8] * m[7] * m[2] * m[13] +\
               m[8] * m[5] * m[3] * m[14] +\
               m[8] * m[6] * m[1] * m[15] -\
               \
               m[12] * m[5] * m[10] * m[3] -\
               m[12] * m[7] * m[9] * m[2] -\
               m[12] * m[6] * m[11] * m[1] +\
               m[12] * m[7] * m[10] * m[1] +\
               m[12] * m[5] * m[11] * m[2] +\
               m[12] * m[6] * m[9] * m[3]
               

def __det3(m):
        return m[0] * m[4] * m[8] +\
               m[3] * m[7] * m[2] +\
               m[1] * m[5] * m[6] -\
               m[2] * m[4] * m[6] -\
               m[0] * m[5] * m[7] -\
               m[1] * m[3] * m[8] 

#matrix inverse
def invmatrix(m):
        size = m.__len__()
        if size == 16: return __invmatrix4(m)
        elif size == 9: return __invmatrix3(m)

def __invmatrix4(m):
        d = __det4(m)
        if d == 0:
                return __identity4()
        nm = (GLfloat * 16)(*(16 * [0]))
        nm[0] = (m[5] * m[10] * m[15] +\
                m[6] * m[11] * m[13] +\
                m[7] * m[9] * m[14] -\
                m[7] * m[10] * m[13] -\
                m[6] * m[9] * m[15] -\
                m[5] * m[11] * m[14]) / (d)
        nm[1] = (m[1] * m[10] * m[15] +\
                m[2] * m[11] * m[13] +\
                m[3] * m[9] * m[14] -\
                m[3] * m[10] * m[13] -\
                m[2] * m[9] * m[15] -\
                m[1] * m[11] * m[14]) / (-d)
        nm[2] = (m[1] * m[6] * m[15] +\
                m[2] * m[7] * m[13] +\
                m[3] * m[5] * m[14] -\
                m[3] * m[6] * m[13] -\
                m[2] * m[5] * m[15] -\
                m[1] * m[7] * m[14]) / (d)
        nm[3] = (m[1] * m[6] * m[11] +\
                m[2] * m[7] * m[9] +\
                m[3] * m[5] * m[10] -\
                m[3] * m[6] * m[9] -\
                m[2] * m[5] * m[11] -\
                m[1] * m[7] * m[10]) / (-d)
        
        nm[4] = (m[4] * m[10] * m[15] +\
                m[6] * m[11] * m[12] +\
                m[7] * m[8] * m[14] -\
                m[7] * m[10] * m[12] -\
                m[6] * m[8] * m[15] -\
                m[4] * m[11] * m[14]) / (-d)
        nm[5] = (m[0] * m[10] * m[15] +\
                m[2] * m[11] * m[12] +\
                m[3] * m[8] * m[14] -\
                m[3] * m[10] * m[12] -\
                m[2] * m[8] * m[15] -\
                m[0] * m[11] * m[14]) / (d)
        nm[6] = (m[0] * m[6] * m[15] +\
                m[2] * m[7] * m[12] +\
                m[3] * m[4] * m[14] -\
                m[3] * m[6] * m[12] -\
                m[2] * m[4] * m[15] -\
                m[0] * m[7] * m[14]) / (-d)
        nm[7] = (m[0] * m[6] * m[11] +\
                m[2] * m[7] * m[8] +\
                m[3] * m[4] * m[10] -\
                m[3] * m[6] * m[8] -\
                m[2] * m[4] * m[11] -\
                m[0] * m[7] * m[10]) / (d)
        
        nm[8] = (m[4] * m[9] * m[15] +\
                m[5] * m[11] * m[12] +\
                m[7] * m[8] * m[13] -\
                m[7] * m[9] * m[12] -\
                m[5] * m[8] * m[15] -\
                m[4] * m[11] * m[13]) / (d)
        nm[9] = (m[0] * m[9] * m[15] +\
                m[1] * m[11] * m[12] +\
                m[3] * m[8] * m[13] -\
                m[3] * m[9] * m[12] -\
                m[1] * m[8] * m[15] -\
                m[0] * m[11] * m[13]) / (-d)
        nm[10] = (m[0] * m[5] * m[15] +\
                m[1] * m[7] * m[12] +\
                m[3] * m[4] * m[13] -\
                m[3] * m[5] * m[12] -\
                m[1] * m[4] * m[15] -\
                m[0] * m[7] * m[13]) / (d)
        nm[11] = (m[0] * m[5] * m[11] +\
                m[1] * m[7] * m[8] +\
                m[3] * m[4] * m[9] -\
                m[3] * m[5] * m[8] -\
                m[1] * m[4] * m[11] -\
                m[0] * m[7] * m[9]) / (-d)
        
        nm[12] = (m[4] * m[9] * m[14] +\
                m[5] * m[10] * m[12] +\
                m[6] * m[8] * m[13] -\
                m[6] * m[9] * m[12] -\
                m[5] * m[8] * m[14] -\
                m[4] * m[10] * m[13]) / (-d)
        nm[13] = (m[0] * m[9] * m[14] +\
                m[1] * m[10] * m[12] +\
                m[2] * m[8] * m[13] -\
                m[2] * m[9] * m[12] -\
                m[1] * m[8] * m[14] -\
                m[0] * m[10] * m[13]) / (d)
        nm[14] = (m[0] * m[5] * m[14] +\
                m[1] * m[6] * m[12] +\
                m[2] * m[4] * m[13] -\
                m[2] * m[5] * m[12] -\
                m[1] * m[4] * m[14] -\
                m[0] * m[6] * m[13]) / (-d)
        nm[15] = (m[0] * m[5] * m[10] +\
                m[1] * m[6] * m[8] +\
                m[2] * m[4] * m[9] -\
                m[2] * m[5] * m[8] -\
                m[1] * m[4] * m[10] -\
                m[0] * m[6] * m[9]) / (d)
        return nm

def __invmatrix3(m):
        d = __det3(m)
        if d == 0:
                return __identity4()
        nm = (GLfloat * 9)(*(9 * [0]))
        nm[0] = (m[4] * m[8] -\
                m[5] * m[7]) / (d)
        nm[1] = (m[1] * m[8] -\
                m[2] * m[7]) / (-d)
        nm[2] = (m[1] * m[5] -\
                m[2] * m[4]) / (d)
        nm[3] = (m[3] * m[8] -\
                m[5] * m[6]) / (-d)
        nm[4] = (m[0] * m[8] -\
                m[2] * m[6]) / (d)
        nm[5] = (m[0] * m[5] -\
                m[2] * m[3]) / (-d)
        nm[6] = (m[3] * m[7] -\
                m[4] * m[6]) / (d)
        nm[7] = (m[0] * m[7] -\
                m[1] * m[6]) / (-d)
        nm[8] = (m[0] * m[4] -\
                m[1] * m[3]) / (d)
        return nm

#matrix transpose
def transpmatrix(m):
        size = m.__len__()
        if size == 16: return __transpmatrix4(m)
        elif size == 9: return __transpmatrix3(m)

def __transpmatrix3(m):
        return (GLfloat *9)(*[m[0], m[3], m[6],\
                              m[1], m[4], m[7],\
                              m[2], m[5], m[8])

def __transpmatrix4(m):
        return (GLfloat *16)(*[m[0], m[4], m[8],  m[12],\
                               m[1], m[5], m[9],  m[13],\
                               m[2], m[6], m[10], m[14],\
                               m[3], m[7], m[11], m[15]])

"""----------------------------------------------------------------------"""

#vector cross product
def cross_product(v1, v2):
	v = 3 * [0]

	v[0] = v1[1]*v2[2] - v1[2]*v2[1]
	v[1] = v1[2]*v2[0] - v1[0]*v2[2]
	v[2] = v1[0]*v2[1] - v1[1]*v2[0]
	
	return v

#vector dot product
def dot_product(v1, v2):
        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

#vector length
def length(v):
        return math.sqrt(dot_product(v1,v1))

#vector normalize
def normalize(v1):
        v = 3 * [0]
        
        l = length(v1)

        if l == 0:
                return v1

        v[0] = v1[0] / l
        v[1] = v1[1] / l
        v[2] = v1[2] / l

        return v

def _sum(v1, v2):
        return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

"""------------------------------------------------------------------"""

def computeTangentSpace(vertices, texels, faces):
        nr_connections = len(vertices)*[0]
        normals = 3*len(vertices)*[0]
        tangents = 3*len(vertices)*[0]
        binormals = 3*len(vertices)*[0]
        for i in range(len(faces)):
            v1 = vertices[faces[i][0]]
            v2 = vertices[faces[i][1]]
            v3 = vertices[faces[i][2]]
            p21 = [v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]]
            p31 = [v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]]
            normal = normalize(cross_product(p21, p31))
                            
            if texels:
                    t1 = texels[faces[i][0]]
                    t2 = texels[faces[i][1]]
                    t3 = texels[faces[i][2]]
                    uv21 = [t2[0]-t1[0], t2[1]-t1[1]]
                    uv31 = [t3[0]-t1[0], t3[1]-t1[1]]
                    tangent = [p21[0]*uv31[1]-p31[0]*uv21[1], p21[1]*uv31[1]-p31[1]*uv21[1], p21[2]*uv31[1]-p31[2]*uv21[1]]
                    tangent = normalize(tangent)
                    binormal = [p31[0]*uv21[0]-p21[0]*uv31[0], p31[1]*uv21[0]-p21[1]*uv31[0], p31[2]*uv21[0]-p21[2]*uv31[0]]
                    binormal = normalize(binormal)
                    dot = dot_product(normal, tangent)
                    tangent = [tangent[0] - normal[0]*dot, tangent[1] - normal[1]*dot, tangent[2] - normal[2]*dot]
                    tangent = normalize(tangent)
                    rightHanded = dot_product(cross_product(tangent, binormal), normal) >= 0
                    binormal = cross_product(normal, tangent)
                    if not rightHanded:
                            binormal = [-binormal[0], -binormal[1], -binormal[2]]

            nr_connections[faces[i][0]] += 1
            nr_connections[faces[i][1]] += 1
            nr_connections[faces[i][2]] += 1

            normals[faces[i][0]] = _sum(normals[faces[i][0]], normal)
            normals[faces[i][1]] = _sum(normals[faces[i][1]], normal)
            normals[faces[i][2]] = _sum(normals[faces[i][2]], normal)
                
            if texels:
                    tangents[faces[i][0]] = _sum(tangents[faces[i][0]], tangent)
                    tangents[faces[i][1]] = _sum(tangents[faces[i][1]], tangent)
                    tangents[faces[i][2]] = _sum(tangents[faces[i][2]], tangent)

                    binormals[faces[i][0]] = _sum(binormals[faces[i][0]], binormal)
                    binormals[faces[i][1]] = _sum(binormals[faces[i][1]], binormal)
                    binormals[faces[i][2]] = _sum(binormals[faces[i][2]], binormal)
                        
        for i in range(len(vertices)):
                if nr_connections[i] > 0:
                        normals[3*i] /=nr_connections[i]
                        normals[3*i+1] /=nr_connections[i]
                        normals[3*i+2] /=nr_connections[i]
                        if texels:
                                tangents[3*i] /=nr_connections[i]
                                tangents[3*i+1] /=nr_connections[i]
                                tangents[3*i+2] /=nr_connections[i]

                                binormals[3*i] /=nr_connections[i]
                                binormals[3*i+1] /=nr_connections[i]
                                binormals[3*i+2] /=nr_connections[i]

        if texels:
                return [tangents, binormals, normals]
        else: return [None, None, normals]
