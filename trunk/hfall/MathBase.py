"""
Mathematic auxiliary functions
"""

import pyglet
from pyglet.gl import *
import math

def identity():
        return (GLfloat * 16)(*[1, 0, 0, 0,
                                0, 1, 0, 0,
                                0, 0, 1, 0,
                                0, 0, 0, 1])

def matrixmult(m1, m2):
	m = (GLfloat * 16)(*(16 * []))

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

def invmatrix(matrix):
        s = 6*[0]
        s[0] = matrix[0]*matrix[5] - matrix[1]*matrix[4]
	s[1] = matrix[0]*matrix[6] - matrix[2]*matrix[4]
	s[2] = matrix[0]*matrix[7] - matrix[3]*matrix[4]
	s[3] = matrix[1]*matrix[6] - matrix[2]*matrix[5]
	s[4] = matrix[1]*matrix[7] - matrix[3]*matrix[5]
	s[5] = matrix[2]*matrix[7] - matrix[3]*matrix[6]
	c = 6*[0]
	c[0] = matrix[10]*matrix[15] - matrix[11]*matrix[14]
	c[1] = matrix[9]*matrix[15] - matrix[11]*matrix[13]
	c[2] = matrix[9]*matrix[14] - matrix[10]*matrix[13]
	c[3] = matrix[8]*matrix[15] - matrix[11]*matrix[12]
	c[4] = matrix[8]*matrix[14] - matrix[10]*matrix[12]
	c[5] = matrix[8]*matrix[13] - matrix[9]*matrix[12]
	det = (s[0]*c[0] - s[1]*c[1] + s[2]*c[2] + s[3]*c[3] - s[4]*c[4] + s[5]*c[5])
	if det == 0: return identity()
	invDet = 1/det
	return (GLfloat * 16)(*[(matrix[5]*c[0] - matrix[6]*c[1] + matrix[7]*c[2])      *invDet,
                                (- matrix[1]*c[0] + matrix[2]*c[1] - matrix[3]*c[2])    *invDet,
                                (matrix[13]*s[5] - matrix[14]*s[4] + matrix[15]*s[3])   *invDet,
                                (- matrix[9]*s[5] + matrix[10]*s[4] - matrix[11]*s[3])  *invDet,
                                (- matrix[4]*c[0] + matrix[6]*c[3] - matrix[7]*c[4])    *invDet,
                                (matrix[0]*c[0] - matrix[2]*c[3] + matrix[3]*c[4])      *invDet,
                                (- matrix[12]*s[5] + matrix[14]*s[2] - matrix[15]*s[1]) *invDet,
                                (matrix[8]*s[5] - matrix[10]*s[2] + matrix[11]*s[1])    *invDet,
                                (matrix[4]*c[1] - matrix[5]*c[3] + matrix[7]*c[5])      *invDet,
                                (- matrix[0]*c[1] + matrix[1]*c[3] - matrix[3]*c[5])    *invDet,
                                (matrix[12]*s[4] - matrix[13]*s[2] + matrix[15]*s[0])   *invDet,
                                (- matrix[8]*s[4] + matrix[9]*s[2] - matrix[11]*s[0])   *invDet,
                                (- matrix[4]*c[2] + matrix[5]*c[4] - matrix[6]*c[5])    *invDet,
                                (matrix[0]*c[2] - matrix[1]*c[4] + matrix[2]*c[5])      *invDet,
                                (- matrix[12]*s[3] + matrix[13]*s[1] - matrix[14]*s[0]) *invDet,
                                (matrix[8]*s[3] - matrix[9]*s[1] + matrix[10]*s[0])     *invDet])

def transpmatrix(m):
        return (GLfloat *16)(*[m[0], m[4], m[8],  m[12],
                               m[1], m[5], m[9],  m[13],
                               m[2], m[6], m[10], m[14],
                               m[3], m[7], m[11], m[15]])

def cross_product(v1, v2):
	v = 3 * [0]

	v[0] = v1[1]*v2[2] - v1[2]*v2[1]
	v[1] = v1[2]*v2[0] - v1[0]*v2[2]
	v[2] = v1[0]*v2[1] - v1[1]*v2[0]
	
	return v

def dot_product(v1, v2):
        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def length(v):
        a = v[1] * v[1] + v[2] * v[2] + v[0] * v[0]
        return a

def normalize(v1):
        v = 3 * [0]
        
        l = math.sqrt(v1[0]*v1[0] + v1[1]*v1[1] + v1[2]*v1[2])

        if l == 0:
                return v1

        v[0] = v1[0] / l
        v[1] = v1[1] / l
        v[2] = v1[2] / l

        return v

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
            for j in range(3):
                    normals[3*faces[i][0]+j] += normal[j]
                    normals[3*faces[i][1]+j] += normal[j]
                    normals[3*faces[i][2]+j] += normal[j]
                    if texels:
                            tangents[3*faces[i][0]+j] += tangent[j]
                            tangents[3*faces[i][1]+j] += tangent[j]
                            tangents[3*faces[i][2]+j] += tangent[j]

                            binormals[3*faces[i][0]+j] += binormal[j]
                            binormals[3*faces[i][1]+j] += binormal[j]
                            binormals[3*faces[i][2]+j] += binormal[j]
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
