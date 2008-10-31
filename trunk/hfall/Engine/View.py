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
        - only debugging is (partly) done
        - only the functions concerning PROJECTION should be used (for the moment)
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
                PackedMatrixData = "|" + self.Mod(matrix[0][0]) + "\t" + self.Mod(matrix[0][1]) + \
                        "\t" + self.Mod(matrix[0][2]) + "\t" + self.Mod(matrix[0][3]) +"\t|\n" + \
                        "|" + self.Mod(matrix[1][0]) + "\t" + self.Mod(matrix[1][1]) + "\t" + \
                        self.Mod(matrix[1][2]) + "\t" + self.Mod(matrix[1][3]) + "\t|\n" + "|" + \
                        self.Mod(matrix[2][0]) + "\t" + self.Mod(matrix[2][1]) + "\t" + \
                        self.Mod(matrix[2][2]) + "\t" + self.Mod(matrix[2][3]) + "\t|\n" + "|" + \
                        self.Mod(matrix[3][0]) + "\t" + self.Mod(matrix[3][1]) + "\t" + \
                        self.Mod(matrix[3][2]) + "\t" + self.Mod(matrix[3][3]) + "\t|\n"
                return PackedMatrixData
        
        
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
                        PackedMatrixData = "Orthographic Matrix:\n"
                        PackedMatrixData += "bottom\t" + self.Mod(bottom) + "\n" + \
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
                        PackedMatrixData = "Perspective Matrix:\n"
                        PackedMatrixData += "zFar\t" + self.Mod(zFar) + "\n" + \
                                "zNear\t" + self.Mod(zNear) + "\n" + \
                                "f\t" + self.Mod(f) + "\n" + \
                                "aspect\t" + self.Mod(aspect) + "\n" + \
                                "fovy\t" + self.Mod(fovy) + "\n"
                else:
                        PackedMatrixData = "Weird data\n"
                return PackedMatrixData
        
                                
        def PMatrixRaw(self,matrix):    
                if self.PMatrixType(matrix)==self.PROJ_ORTHOGRAPHIC:
                        PackedMatrixData = "Orthographic matrix:\n"
                elif self.PMatrixType(matrix)==self.PROJ_PERSPECTIVE:
                        PackedMatrixData = "Perspective matrix:\n"
                else:
                        PackedMatrixData = "Unknown projection matrix:\n"
                PackedMatrixData += self.MatrixRaw(matrix)
                return PackedMatrixData
                
        def PCMatrixType(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack matrix type:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixType,msg)
                return PackedMatrixData
                
        def PCMatrixData(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack matrix data:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixData,msg)
                return PackedMatrixData
                
        def PCMatrixRaw(self, header = "default"):
                if header=="default":
                        msg = "\tTop projection stack raw matrix:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_PROJECTION_MATRIX,self.PMatrixRaw,msg)
                return PackedMatrixData
                
        def PSMatrixType(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixType)
                
        def PSMatrixData(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixData)
                
        def PSMatrixRaw(self):
                return self.IterateThroughStack(GL_PROJECTION,self.PMatrixRaw)
                
#----------------------------------------------------------
#       MODELVIEW MATRIX SEGMENT                          |
#----------------------------------------------------------
        def MMatrixType(self,pMatrix):
                if pMatrix[0][0]==1 and pMatrix[1][1]==1 and pMatrix[2][2]==1 and \
                        pMatrix[3][3]==1:
                        return "TYPE=IDENTITY"
                else:
                        return "TYPE=NONE"
                pass
                
        def MMatrixData(self,pMatrix):
                pass
                
        def MMatrixRaw(self,pMatrix):
                return self.MatrixRaw(pMatrix)
                pass
                        
        def MCMatrixType(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Modelview stack matrix type:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_MODELVIEW_MATRIX,self.MMatrixRaw,msg)
                return PackedMatrixData
                
        def MCMatrixData(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Modelview stack matrix data:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_MODELVIEW_MATRIX,self.MMatrixRaw,msg)
                return PackedMatrixData
                
        def MCMatrixRaw(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Modelview stack raw matrix:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_MODELVIEW_MATRIX,self.MMatrixRaw,msg)
                return PackedMatrixData
                
        def MSMatrixType(self):
                return self.IterateThroughStack(GL_MODELVIEW,self.MMatrixType)
                
        def MSMatrixData(self):
                return self.IterateThroughStack(GL_MODELVIEW,self.MMatrixData)
                
        def MSMatrixRaw(self):
                return self.IterateThroughStack(GL_MODELVIEW,self.MMatrixRaw)
                 
#----------------------------------------------------------
#       COLOR STACK SEGMENT                               |
#----------------------------------------------------------
        def CMatrixType(self,pMatrix):
                if pMatrix[0][0]==1 and pMatrix[1][1]==1 and pMatrix[2][2]==1 and \
                        pMatrix[3][3]==1:
                        return "TYPE=IDENTITY"
                else:
                        return "TYPE=NONE"
                pass
                
        def CMatrixData(self,pMatrix):
                pass
                
        def CMatrixRaw(self,pMatrix):
                return self.MatrixRaw(pMatrix)
                pass
                        
        def CCMatrixType(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Color stack matrix type:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_COLOR_MATRIX,self.CMatrixRaw,msg)
                return PackedMatrixData
                
        def CCMatrixData(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Color stack matrix data:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_COLOR_MATRIX,self.CMatrixRaw,msg)
                return PackedMatrixData
                
        def CCMatrixRaw(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Color stack raw matrix:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_COLOR_MATRIX,self.CMatrixRaw,msg)
                return PackedMatrixData
                
        def CSMatrixType(self):
                return self.IterateThroughStack(GL_COLOR,self.CMatrixType)
                
        def CSMatrixData(self):
                return self.IterateThroughStack(GL_COLOR,self.CMatrixData)
                
        def CSMatrixRaw(self):
                return self.IterateThroughStack(GL_COLOR,self.CMatrixRaw)
                
#----------------------------------------------------------
#       TEXTURE STACK SEGMENT                             |
#----------------------------------------------------------
        def TMatrixType(self,pMatrix):
                if pMatrix[0][0]==1 and pMatrix[1][1]==1 and pMatrix[2][2]==1 and \
                        pMatrix[3][3]==1:
                        return "TYPE=IDENTITY"
                else:
                        return "TYPE=NONE"
                pass
                
        def TMatrixData(self,pMatrix):
                pass
                
        def TMatrixRaw(self,pMatrix):
                return self.MatrixRaw(pMatrix)
                pass
                        
        def TCMatrixType(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Texture stack matrix type:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_TEXTURE_MATRIX,self.TMatrixRaw,msg)
                return PackedMatrixData
                
        def TCMatrixData(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Texture stack matrix data:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_TEXTURE_MATRIX,self.TMatrixRaw,msg)
                return PackedMatrixData
                
        def TCMatrixRaw(self,pMatrix,header="default"):
                if header=="default":
                        msg = "\tTop Texture stack raw matrix:\n"
                else:
                        msg = header
                PackedMatrixData = self.GetTopOfStack(GL_TEXTURE_MATRIX,self.TMatrixRaw,msg)
                return PackedMatrixData
                
        def TSMatrixType(self):
                return self.IterateThroughStack(GL_TEXTURE,self.TMatrixType)
                
        def TSMatrixData(self):
                return self.IterateThroughStack(GL_TEXTURE,self.TMatrixData)
                
        def TSMatrixRaw(self):
                return self.IterateThroughStack(GL_TEXTURE,self.TMatrixRaw)
                
#----------------------------------------------------------
#       DEFAULT STACK SEGMENT                             |
#----------------------------------------------------------

        def XMatrixType(self,pMatrix):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PMatrixType(pMatrix)
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MMatrixType(pMatrix)
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CMatrixType(pMatrix)
                else:
                        PackedMatrixData = self.TMatrixType(pMatrix)
                return PackedMatrixData
                
        def XMatrixData(self,pMatrix):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PMatrixData(pMatrix)
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MMatrixData(pMatrix)
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CMatrixData(pMatrix)
                else:
                        PackedMatrixData = self.TMatrixData(pMatrix)
                return PackedMatrixData
                
        def XMatrixRaw(self,pMatrix):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PMatrixRaw(pMatrix)
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MMatrixRaw(pMatrix)
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CMatrixRaw(pMatrix)
                else:
                        PackedMatrixData = self.TMatrixRaw(pMatrix)
                return PackedMatrixData 
                
        def XCMatrixType(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PCMatrixType()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MCMatrixType()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CCMatrixType()
                else:
                        PackedMatrixData = self.TCMatrixType()
                return PackedMatrixData
                
        def XCMatrixData(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PCMatrixData()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MCMatrixData()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CCMatrixData()
                else:
                        PackedMatrixData = self.TCMatrixData()
                return PackedMatrixData
                
        def XCMatrixRaw(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PCMatrixRaw()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MCMatrixRaw()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CCMatrixRaw()
                else:
                        PackedMatrixData = self.TCMatrixRaw()
                return PackedMatrixData
                
        def XSMatrixType(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PSMatrixType()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MSMatrixType()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CSMatrixType()
                else:
                        PackedMatrixData = self.TSMatrixType()
                return PackedMatrixData
                
        def XSMatrixData(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PSMatrixData()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MSMatrixData()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CSMatrixData()
                else:
                        PackedMatrixData = self.TSMatrixData()
                return PackedMatrixData
                
        def XSMatrixRaw(self):
                mode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,mode)
                mode = mode[0]
                
                if mode==GL_PROJECTION:
                        PackedMatrixData = self.PSMatrixRaw()
                elif mode==GL_MODELVIEW:
                        PackedMatrixData = self.MSMatrixRaw()
                elif mode==GL_COLOR:
                        PackedMatrixData = self.CSMatrixRaw()
                else:
                        PackedMatrixData = self.TSMatrixRaw()
                return PackedMatrixData
        
#----------------------------------------------------------
#       INTERNAL FUNCTIONS                                |
#----------------------------------------------------------

        def Log(self,msg):
                self.ErrorLogs = self.ErrorLogs + msg + "\n"
                
        def Mod(self,x):
                return str(x).rjust(self.precision)[:self.precision]
                
        def GetTopOfStack(self,MATRIX,function,header=""):
                pMatrix = glGetMatrix(MATRIX)
                PackedMatrixData = header
                PackedMatrixData += function(pMatrix)
                return PackedMatrixData
                
        def IterateThroughStack(self,STACK,function):
                #Fill the constants
                if STACK==GL_PROJECTION:
                        DEPTH = GL_PROJECTION_STACK_DEPTH
                        MATRIX = GL_PROJECTION_MATRIX
                        header = "Projection stack (Top first):\n"
                elif STACK==GL_MODELVIEW:
                        DEPTH = GL_MODELVIEW_STACK_DEPTH
                        MATRIX = GL_MODELVIEW_MATRIX
                        header = "Modelview stack (Top first):\n"
                elif STACK==GL_COLOR:
                        DEPTH = GL_COLOR_MATRIX_STACK_DEPTH
                        MATRIX = GL_COLOR_MATRIX
                        header = "Color stack (Top first):\n"
                elif STACK==GL_TEXTURE:
                        DEPTH = GL_TEXTURE_STACK_DEPTH
                        MATRIX = GL_TEXTURE_MATRIX
                        header = "Texture stack (Top first):\n"
                        
                stackDepth = (GLint * 1)()
                glGetIntegerv(DEPTH,stackDepth)
                stackDepth = stackDepth[0]
                
                savedMode = (GLint * 1)()
                glGetIntegerv(GL_MATRIX_MODE,savedMode)
                savedMode = savedMode[0]
                
                glMatrixMode(STACK)
                PackedMatrixData = "*"*40 + "\n"
                PackedMatrixData += header
                PackedMatrixData += "Total stack depth =\t" + str(stackDepth) + "\n"
                matrixList = []
                for i in range(stackDepth-1):
                        tempMatrix = glGetMatrix(MATRIX)
                        PackedMatrixData += "\nMatrix " + str(i) + ":\n"
                        PackedMatrixData += function(tempMatrix)
                        matrixList.append(tempMatrix)
                        glPopMatrix()
                tempMatrix = glGetMatrix(MATRIX)
                PackedMatrixData += "\nMatrix " + str(stackDepth-1) + ":\n"
                PackedMatrixData += function(tempMatrix)
                
                #Rebuild the stack
                for m in matrixList:
                        glPushMatrix()
                        glLoadMatrix(m)
                                
                glMatrixMode(savedMode)
                PackedMatrixData += "*"*40 + "\n"
                return PackedMatrixData
