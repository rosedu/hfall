"""
View Matrix Manager
Version 0.1

Matrix types:
        Modelview
        Projection
        
Projection Matrices:
        Perspective
        Ortho
      
"""

from pyglet.gl import *
from math import *
from glcalls import *


""" 
HOW TO USE THIS CLASS

notes: 
        - only PROJECTION debugging is done
        - all functions should be used as "static"


DEBUGGING THE PROJECTION STACK
note: absolutely nothing is changed in the stack when debugging functions are called
-how the function name is built:
[TargetStack][PartOfTarget]Name
Names:
        MatrixType 
        MatrixData (values that are encoded in the matrix)
        MatrixRaw  (the matrix)
PartOfTarget:
        C       - output is built based on the matrix that is top of the stack
        S       - full stack info is dumped
        (blank) - parameter info is obtained (requires matrix to be sent)
TargetStack:
        P       - projection
        M       - modelview
        T       - texture
        C       - color
        X       - default (stack that is currently active)
        
Examples:
        PCMatrixType    - matrix type of the matrix on top of the projection stack
        PSMatrixRaw     - all the raw data in the projection stack
        PMatrixType(someMatrix) - type of the projection matrix someMatrix is obtained
        
"""
class MatrixManager:

        def __init__(self):
                self.ErrorLogs = ""
                self.precision = 6
                
                self.PROJ_PERSPECTIVE = "TYPE=PERSPECTIVE\n"
                self.PROJ_ORTHOGRAPHIC = "TYPE=ORTHOGRAPHIC\n"
                pass
                
#----------------------------------------------------------
#       GENERIC MATRIX SEGMENT                            |
#----------------------------------------------------------
                
        def MatrixRaw(self,matrix):
                """
        Raw Matrix function, doesn't do any type check, just prints the contents
                """
                PacketMatrixData = "|" + self.Mod(matrix[0][0]) + "\t" + self.Mod(matrix[0][1]) + \
                        "\t" + self.Mod(matrix[0][2]) + "\t" + self.Mod(matrix[0][3]) +"\t|\n" + \
                        "|" + self.Mod(matrix[1][0]) + "\t" + self.Mod(matrix[1][1]) + "\t" + \
                        self.Mod(matrix[1][2]) + "\t" + self.Mod(matrix[1][3]) + "\t|\n" + "|" + \
                        self.Mod(matrix[2][0]) + "\t" + self.Mod(matrix[2][1]) + "\t" + \
                        self.Mod(matrix[2][2]) + "\t" + self.Mod(matrix[2][3]) + "\t|\n" + "|" + \
                        self.Mod(matrix[3][0]) + "\t" + self.Mod(matrix[3][1]) + "\t" + \
                        self.Mod(matrix[3][2]) + "\t" + self.Mod(matrix[3][3]) + "\t|\n"
                return PacketMatrixData
        
        
#----------------------------------------------------------
#       PROJECTION MATRIX SEGMENT                         |
#----------------------------------------------------------

        def PMatrixType(self,matrix):
                #Returns "P" for Perspective and "O" for Ortho; "X" means 
                #failure to identify
                if matrix[0][1]==0 and matrix[0][2]==0 and matrix[0][3]==0 and \
                        matrix[1][0]==0 and matrix[1][2]==0 and matrix[1][3]==0 \
                        and matrix[2][0]==0 and matrix[2][1]==0 and matrix[3][0]==0 \
                        and matrix[3][1]==0 and matrix[3][2]==-1 and matrix[3][3]==0:
                        return self.PROJ_PERSPECTIVE
                if matrix[0][1]==0 and matrix[0][2]==0 and matrix[1][0]==0 and \
                        matrix[1][2]==0 and matrix[2][0]==0 and matrix[2][1]==0 \
                        and matrix[3][0]==0 and matrix[3][1]==0 and matrix[3][2]==0 \
                        and matrix[3][3]==1:
                        return self.PROJ_ORTHOGRAPHIC
                return "X"
                        
        def PMatrixData(self,matrix):
                if self.PMatrixType(matrix)==self.PROJ_ORTHOGRAPHIC:
                        bottom = 1.0 * (matrix[1][3] + 1) / matrix[1][1]
                        top = -1.0 * (matrix[1][3] + 1) / matrix[1][1]
                        left = -1.0 * (matrix[0][3] + 1) / matrix[0][0]
                        right = 1.0 * (matrix[0][3] + 1) / matrix[0][0]
                        nearVal = (matrix[2][3] + 1) / matrix[2][2]
                        farVal = (matrix[2][3] - 1) / matrix[2][2]
                        PacketMatrixData = "Orthographic Matrix:\n"
                        PacketMatrixData += "bottom\t" + self.Mod(bottom) + "\n" + \
                                "top\t" + self.Mod(top) + "\n" + \
                                "left\t" + self.Mod(left) + "\n" + \
                                "right\t" + self.Mod(right) + "\n" + \
                                "nearVal\t" + self.Mod(nearVal) + "\n" + \
                                "farVal\t" + self.Mod(farVal) + "\n"
                elif self.PMatrixType(matrix)==self.PROJ_PERSPECTIVE:
                        zFar = 1.0 * matrix[2][3] / (matrix[2][2] + 1)
                        zNear = 1.0 * matrix[2][3] / (matrix[2][2] - 1)
                        f = matrix[1][1]
                        aspect = 1.0 * matrix[1][1] / matrix[0][0]
                        fovy = 2*atan(1.0/f)
                        PacketMatrixData = "Perspective Matrix:\n"
                        PacketMatrixData += "zFar\t" + self.Mod(zFar) + "\n" + \
                                "zNear\t" + self.Mod(zNear) + "\n" + \
                                "f\t" + self.Mod(f) + "\n" + \
                                "aspect\t" + self.Mod(aspect) + "\n" + \
                                "fovy\t" + self.Mod(fovy) + "\n"
                else:
                        PacketMatrixData = "Weird data\n"
                return PacketMatrixData
        
                                
        def PMatrixRaw(self,matrix):    
                if self.PMatrixType(matrix)==self.PROJ_ORTHOGRAPHIC:
                        PacketMatrixData = "Orthographic matrix:\n"
                elif self.PMatrixType(matrix)==self.PROJ_PERSPECTIVE:
                        PacketMatrixData = "Perspective matrix:\n"
                else:
                        PacketMatrixData = "Unknown projection matrix:\n"
                PacketMatrixData += self.MatrixRaw(matrix)
                return PacketMatrixData
                
        def PCMatrixType(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack matrix type:\n"
                else:
                        msg = header
                PacketMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixType,msg)
                return PacketMatrixData
                
        def PCMatrixData(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack matrix data:\n"
                else:
                        msg = header
                PacketMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixData,msg)
                return PacketMatrixData
                
        def PCMatrixRaw(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack raw matrix:\n"
                else:
                        msg = header
                PacketMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixRaw,msg)
                return PacketMatrixData
                
        def PSMatrixType(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixType)
                pass
                
        def PSMatrixData(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixData)
                pass
                
        def PSMatrixRaw(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixRaw)
                pass
                
#----------------------------------------------------------
#       INTERNAL FUNCTIONS                                |
#----------------------------------------------------------

        def Log(self,msg):
                self.ErrorLogs = self.ErrorLogs + msg + "\n"
                
        def Mod(self,x):
                return str(x).rjust(self.precision)[:self.precision]
                
        def GetTopOfStack(self,MATRIX,function,header=""):
                pMatrix = glGetMatrix(MATRIX)
                PacketMatrixData = header
                PacketMatrixData += function(pMatrix)
                return PacketMatrixData
                
        def IterateThroughStack(self,STACK,function):
                #Fill the constants
                if STACK==GL_PROJECTION:
                        DEPTH = GL_PROJECTION_STACK_DEPTH
                        MATRIX = GL_PROJECTION_MATRIX
                elif STACK==GL_MODELVIEW:
                        DEPTH = GL_MODELVIEW_STACK_DEPTH
                        MATRIX = GL_MODELVIEW_MATRIX
                elif STACK==GL_COLOR:
                        DEPTH = GL_COLOR_STACK_DEPTH
                        MATRIX = GL_COLOR_MATRIX
                elif STACK==GL_TEXTURE:
                        DEPTH = GL_TEXTURE_STACK_DEPTH
                        MATRIX = GL_TEXTURE_MATRIX
                        
                stackDepth = (GLint * 1)()
                glGetIntegerv(DEPTH,stackDepth)
                stackDepth = stackDepth[0]
                
                savedMode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,savedMode)
                savedMode = savedMode[0]
                
                glMatrixMode(STACK)
                PacketMatrixData = "*"*40 + "\n"
                PacketMatrixData += "Projection stack (Top first):\n"
                PacketMatrixData += "Total stack depth =\t" + str(stackDepth) + "\n"
                matrixList = []
                for i in range(stackDepth-1):
                        tempMatrix = glGetMatrix(MATRIX)
                        PacketMatrixData += "\nMatrix " + str(i) + ":\n"
                        PacketMatrixData += function(tempMatrix)
                        matrixList.append(tempMatrix)
                        glPopMatrix()
                tempMatrix = glGetMatrix(MATRIX)
                PacketMatrixData += "\nMatrix " + str(stackDepth) + ":\n"
                PacketMatrixData += function(tempMatrix)
                
                #Rebuild the stack
                for m in matrixList:
                        glPushMatrix()
                        glLoadMatrix(m)
                                
                glMatrixMode(savedMode)
                PacketMatrixData += "*"*40 + "\n"
                return PacketMatrixData
