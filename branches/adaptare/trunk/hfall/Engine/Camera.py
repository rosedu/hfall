"""
Hamerfall Camera class. This class represents a camera.

"""

__version__ = '0.7'
__authors__ = 'Maruseac Mihai (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)'

import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../Engine/")
from math import *

from pyglet.gl import *

from Object import *
from Matrix import *
import OGLbase
from GeometricObject import Plane

class Camera(Object):
    """
    For Camera control.
    
    """
    def __init__(self, posx = 0, posy = 0, posz = 0):
        self.modelView = Matrix4()
        self.position = Vector3(posx, posy, posz)
        self.modelView[0][3] = -posx
        self.modelView[1][3] = -posy
        self.modelView[2][3] = posz
        self.modelView[0][0] = 1
        self.modelView[1][1] = 1
        self.modelView[2][2] = -1
        self.modelView[3][3] = 1
        self.enabled = False
        self.pitch = self.yaw = self.roll = 0;
        
    def enable(self):
        self.enabled = True
        OGLbase.OGL.setModelViewMatrix(self.modelView)

    def disable(self):
        self.enabled = False

    def translate(self, tranx, trany, tranz):
        """
        Used for differential translation.
        
        """
       	self.modelView[0][3] -= tranx
       	self.modelView[1][3] -= trany
       	self.modelView[2][3] += tranz
	self.position.x = -self.modelView[0][0]*self.modelView[0][3] - \
                          self.modelView[1][0]*self.modelView[1][3] - \
                          self.modelView[2][0]*self.modelView[2][3]
	self.position.y = -self.modelView[0][1]*self.modelView[0][3] - \
                          self.modelView[1][1]*self.modelView[1][3] - \
                          self.modelView[2][1]*self.modelView[2][3]
	self.position.z = -self.modelView[0][2]*self.modelView[0][3] - \
                          self.modelView[1][2]*self.modelView[1][3] - \
                          self.modelView[2][2]*self.modelView[2][3]

        if (self.enabled):
            OGLbase.OGL.setModelViewMatrix(self.modelView)

    def rotate(self, vx, vy, vz, angle):
        """
        Used for differential rotation.
        
        """
        self.yaw += vy*angle
        self.roll += vz*angle
        self.pitch += vx*angle

        c1 = cos(self.pitch)
        s1 = sin(self.pitch)
        c2 = cos(-self.yaw)
        s2 = sin(-self.yaw)
        c3 = cos(self.roll)
        s3 = sin(self.roll)
                           
        #self.modelView = X*Y*Z*I;
        self.modelView = Matrix4([c2 * c3, c2 * s3, s2, 0,\
                                  s1 * s2 * c3 - c1 * s3, s1 * s2 * s3 +\
                                  c1 * c3, -s1 * c2, 0,\
                                  c1 * s2 * c3 + s1 * s3, c1 * s2 * s3 -\
                                  s1 * c3, -c1 * c2, 0,\
                                  0, 0, 0, 1])

        self.modelView[0][3] = -self.position.x*self.modelView[0][0] - \
                               self.position.y*self.modelView[0][1] - \
                               self.position.z*self.modelView[0][2];
        self.modelView[1][3] = -self.position.x*self.modelView[1][0] - \
                               self.position.y*self.modelView[1][1] - \
                               self.position.z*self.modelView[1][2];
        self.modelView[2][3] = -self.position.x*self.modelView[2][0] - \
                               self.position.y*self.modelView[2][1] - \
                               self.position.z*self.modelView[2][2];
        if (self.enabled):
            OGLbase.OGL.setModelViewMatrix(self.modelView)

    def lookAt(self, vx, vy, vz):
        f = Vector3(vx,vy,vz) - self.position
        f.normalize()
        self.pitch = self.yaw = 0
        self.rotate(asin(f.y), atan2(f.x, f.z), 0, 1)
        if (self.enabled):
            OGLbase.OGL.setModelViewMatrix(self.modelView)

    def setPosition(self, px, py, pz):
    	self.position.x = px
	self.position.y = py
	self.position.z = pz
	self.modelView[0][3] = -px*self.modelView[0][0] - \
                               py*self.modelView[0][1] - \
                               pz*self.modelView[0][2]
	self.modelView[1][3] = -px*self.modelView[1][0] - \
                               py*self.modelView[1][1] - \
                               pz*self.modelView[1][2]
	self.modelView[2][3] = -px*self.modelView[2][0] - \
                               py*self.modelView[2][1] - \
                               pz*self.modelView[2][2]
        if (self.enabled):
            OGLbase.OGL.setModelViewMatrix(self.modelView)

    #y
    def upVector(self):
	    return Vector3(self.modelView[0][1], self.modelView[1][1],\
                       self.modelView[2][1])
	
	#z
    def viewVector(self):
	    return Vector3(-self.modelView[0][2], -self.modelView[1][2],\
                       -self.modelView[2][2])
    #x
    def rightVector(self):
	    return Vector3(self.modelView[0][0], self.modelView[1][0],\
                       self.modelView[2][0])
    
    def perspectivePlane(self, string):
        cameraPosition = self.position
        
        fov = OGLbase.OGL.fov 
        aspect = OGLbase.OGL.aspect
        near = OGLbase.OGL.near
        far = OGLbase.OGL.far
        
        auxPoint = CameraPosition + far * self.viewVector()
        axPoint = CameraPosition + near * self.viewVector()
        
        auxH = math.tan(math.radians(fov / 2)) * far
        auxW = auxH / aspect
        
        auxABPoint = auxPoint + auxH * self.upVector()
        auxCDPoint = auxPoint - auxH * self.upVector()
        
        APoint = auxABPoint + auxW * self.rightVector()
        BPoint = auxABPoint - auxW * self.rightVector()
        CPoint = auxCDPoint - auxW * self.rightVector()
        DPoint = auxCDPoint + auxW * self.rightVector()
        
        VA = APoint - cameraPosition
        VB = BPoint - cameraPosition
        VC = CPoint - cameraPosition
        VD = DPoint - cameraPosition
        
        if string == 'left':
            normal = VA.crossProduct(VD)
            normal.normalize()
            return Plane(cameraPosition, normal)
        
        if string == 'right':
            normal = VB.crossProduct(VC)
            normal.normalize()
            return Plane(cameraPosition, normal)
        
        if string == 'top':
            normal = VA.crossProduct(VB)
            normal.normalize()
            return Plane(cameraPosition, normal)
        
        if string == 'bottom':
            normal == VC.crossProduct(VD)
            normal.normalize()
            return Plane(cameraPosition, normal)
        
        if string == 'near':
            return Plane(axPoint, self.viewVector())
        
        if string == 'far':
            return Plane(auxPoint, -self.viewVector())
