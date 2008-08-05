"""
Mathematic auxiliary functions
"""

import pyglet
from pyglet.gl import *
import math

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

def cross_product(v1, v2):
	v = 3 * [0]

	v[0] = v1[1]*v2[2] - v1[2]*v2[1]
	v[1] = v1[2]*v2[0] - v1[0]*v2[2]
	v[2] = v1[0]*v2[1] - v1[1]*v2[0]
	
	return v

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

def calculateNormals(vertices, faces):
        nr_connections = len(vertices)*[0]
        normals = 3*len(vertices)*[0]
        for i in range(len(faces)):
            v1 = vertices[faces[i][0]]
            v2 = vertices[faces[i][1]]
            v3 = vertices[faces[i][2]]
            prod = cross_product([v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]], [v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]])
            prod = normalize(prod)
            nr_connections[faces[i][0]] += 1
            nr_connections[faces[i][1]] += 1
            nr_connections[faces[i][2]] += 1
            for j in range(3):
                    normals[3*faces[i][0]+j] += prod[j]
                    normals[3*faces[i][1]+j] += prod[j]
                    normals[3*faces[i][2]+j] += prod[j]
        for i in range(len(vertices)):
                if nr_connections[i] > 0:
                        normals[3*i] /=nr_connections[i]
                        normals[3*i+1] /=nr_connections[i]
                        normals[3*i+2] /=nr_connections[i]
        return normals
