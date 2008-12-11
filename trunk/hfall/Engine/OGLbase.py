"""
Hamerfall OpenGL class. This class initializes the OpenGL interface and
then draws vertices and lines to the screen, after changing properly the
state of the OpenGL finite-state machine.

"""

__version__ = '0.2'
__author__ = 'Maruseac Mihai (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)'

import sys
sys.path.insert(0, "..")

from TextureFormat import TextureFormat
from base import kernel as hfk
from Texture import Texture
from pyglet.gl import *
from glcalls import *
from Vector import *
from Matrix import *
from Camera import *

class GLInfo:
    def __init__(self):
        self.info = gl_info.GLInfo()
        self.info.set_active_context()
        self.numTextureUnits = (GLint)(*[])
        self.maxTextures = (GLint)(*[])
        self.maxTextureSize = (GLint)(*[])
        self.maxLights = (GLint)(*[])
        # get video card info
        self.vendor = cast(glGetString(GL_VENDOR), c_char_p).value
        self.renderer = cast(glGetString(GL_RENDERER), c_char_p).value
        self.version = cast(glGetString(GL_VERSION), c_char_p).value
        self.supportedExtensions = cast(glGetString(GL_EXTENSIONS), c_char_p).value
        # get textures and lights info
        if self.info.have_extension("GL_ARB_multitexture"):
            glGetIntegerv(GL_MAX_TEXTURE_UNITS_ARB, self.numTextureUnits)
            self.numTextureUnits = self.numTextureUnits.value
        else: self.numTextureUnits = 1
        if self.info.have_extension("GL_NV_fragment_program"):
            glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS_NV, self.maxTextures)
            self.maxTextures = self.maxTextures.value
        else: self.maxTextures = self.numTextureUnits
        glGetIntegerv(GL_MAX_TEXTURE_SIZE, self.maxTextureSize)
        self.maxTextureSize = self.maxTextureSize.value
        glGetIntegerv(GL_MAX_LIGHTS, self.maxLights)
        self.maxLights = self.maxLights.value        

    def __str__(self):
        return "Vendor: " + self.vendor + "\n" + \
               "Renderer: " + self.renderer + "\n" + \
               "OpenGL version: " + self.version + "\n\n" + \
               "Max. Lights: " + str(self.maxLights) + "\n" + \
               "Max. Textures: " + str(self.maxTextures) + "\n" + \
               "Texture units: " + str(self.numTextureUnits) + "\n" + \
               "Max. Texture size: " + str(self.maxTextureSize) + "\n"
               
               

class OGL:
    """
    This is the class that encapsulates all OpenGL API calls. All acces
    to the OpenGL interface should be done using this class.

    """

    def __init__(self, w, width, height, near=0.1, far=100.0, fov = 60.0,\
                 clearcolor=(0.0, 0.0, 0.0, 0.0)):
        """
        OpenGL and pyglet initialization.
            w - the window which provides the rendering surface
            width - the width of the game window
            height - the height of the game window
            near - minimum distance. All objects closer to the camera than
                   this distance will not be rendered
            far - maximum distance. All objects further away from the camera than
                  this distance will not be rendered
            clearcolor - the color used for clearing the buffer. Mainly
                         it represents the background color when nothing
                         is drawn over the entire window.
                    
        """
        self.glInfo = GLInfo()
	self.far = far
	self.near = near
	self.fov = fov

        self.shadowMap = Texture.create("shadows", 0, 512, 512, GL_TEXTURE_2D, \
                                        TextureFormat.fromString("DEPTH"), \
                                        Texture.Parameters.shadow(), Texture.Settings())
        
        self.w=w
        @self.w.event
        def on_resize(width, height):
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if height == 0:
                height = 1
            gluPerspective(fov, width / float(height), near, far)
            #glMatrixMode(GL_MODELVIEW)

        # finalizing the initialization
        glClearColor(clearcolor[0], clearcolor[1], clearcolor[2], \
                     clearcolor[3])
        glShadeModel(GL_SMOOTH)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
  	
  	#glDepthFunc(GL_LEQUAL)
  	#glBlendFunc(GL_SRC_ALPHA, GL_ONE)
  	#glEnable(GL_BLEND)
  	#glAlphaFunc(GL_GREATER,0.1)
  	#glEnable(GL_ALPHA_TEST)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        hfk.log.msg('Open GL started')

    # Perspective switches - used for correct 2D/3D rendering
    def activate_perspective(self,width,height):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
	gluPerspective(self.fov, 1.0*width/height, 0.1, 1000.0)

    def activate_ortho(self,left,right,bottom,top,\
	near=-1, far=1):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
	glLoadIdentity()
	glOrtho(left,right,bottom,top,near,far)
	       
    def activate_model(self):
  	glMatrixMode(GL_MODELVIEW)
  	# glLoadIdentity()
  	# self.light1.LPosition()

    # here we should define different functions to change OpenGL state
    # machine status. We should built functions to incrementally change
    # the status (like translate) or that change from the start the
    # status (translate to). Also we will need functions to save a state
    # and revert to it after a given period of time.
    # TODO: those functions, after we done 2 and while working on 3
    
    def translate_to(self, position):
        """
        Translates all points with the position vector, starting from
        the identity position - the position that OpenGL state machine
        starts with.

        """
        glLoadIdentity()
        glTranslatef(position.x, position.y, position.z)

    def translate(self, position):
        """
        Does an incremental translation. Translates the current axes by
        the position vector.

        """
        glTranslatef(position.x, position.y, position.z)

    def rotate(self, angle, direction):
        """
        Does a basic rotation based on a given angle and direction
        """
        # Used if we only want to rotate the model
        glMatrixMode(GL_MODELVIEW)
        glRotatef(angle, direction.x, direction.y, direction.z)
    

    def supports(self, extensionName):
        return self.glInfo.info.have_extension(extensionName)

    def colorPointer(self, color):
        glColorPointer(3, GL_FLOAT, 0, color)

    def vertexPointer(self, vertices):
        glVertexPointer(3, GL_FLOAT, 0, vertices)

    def normalPointer(self, normals):
        glNormalPointer(GL_FLOAT, 0, normals)

    def texCoordPointer(self, texels, units):
        for i in units:    
            glActiveTextureARB(GL_TEXTURE0_ARB + i)
            glClientActiveTextureARB(GL_TEXTURE0_ARB + i)
            glTexCoordPointer(2, GL_FLOAT, 0, texels)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def createShadowMap(self, models, light, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.disable()
        
        lcamera = Camera(light.LightPosition[0], light.LightPosition[1], light.LightPosition[2])
        lcamera.lookAt(light.LightPosition[0] + light.spotDirection[0], light.LightPosition[1] + light.spotDirection[1], light.LightPosition[2] + light.spotDirection[2])
        lcamera.enable()
	lightViewMatrix = glGetMatrix(GL_MODELVIEW_MATRIX)
	lightProjectionMatrix = glGetMatrix(GL_PROJECTION_MATRIX)
	
	glViewport(0, 0, self.shadowMap.width, self.shadowMap.height)
	glEnable(GL_CULL_FACE)
	glCullFace(GL_FRONT)

	glShadeModel(GL_FLAT)
	glColorMask(0, 0, 0, 0)
	
	for model in models:
            model.render(self, False)
	
	glBindTexture(GL_TEXTURE_2D, self.shadowMap.glID)
	glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, self.shadowMap.width, self.shadowMap.height)

        glDisable(GL_CULL_FACE)
	glShadeModel(GL_SMOOTH)
	glColorMask(1, 1, 1, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glViewport(0, 0, self.w.width, self.w.height)

        camera.enable()
	return lightProjectionMatrix*lightViewMatrix

    def enableShadows(self, models, lights, camera):
        lightMVP = self.createShadowMap(models, lights[0], camera)
        self.configureShadowMap(2, lightMVP, self.shadowMap)

    def configureShadowMap(self, unit, lightMVP, shadowMap):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        #glLoadMatrix(cameraToWorldMatrixInverse)
        #glLoadInvMatrix(glGetMatrix(GL_MODELVIEW_MATRIX))

        glActiveTextureARB(GL_TEXTURE0_ARB + unit)
        glBindTexture(shadowMap.target, shadowMap.glID)
        glEnable(shadowMap.target)

        bias = Matrix4([0.5, 0.0, 0.0, 0.5,
                        0.0, 0.5, 0.0, 0.5,
                        0.0, 0.0, 0.5, 0.5 - .000001,
                        0.0, 0.0, 0.0, 1.0])
        
        textureMatrix = glGetMatrix(GL_TEXTURE_MATRIX)
        textureProjectionMatrix = textureMatrix * bias * lightMVP

        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGenfv(GL_S, GL_EYE_PLANE, (GLfloat*4)(*textureProjectionMatrix[0]))
        glEnable(GL_TEXTURE_GEN_S)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGenfv(GL_T, GL_EYE_PLANE, (GLfloat*4)(*textureProjectionMatrix[1]))
        glEnable(GL_TEXTURE_GEN_T)
        glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGenfv(GL_R, GL_EYE_PLANE, (GLfloat*4)(*textureProjectionMatrix[2]))
        glEnable(GL_TEXTURE_GEN_R)
        glTexGeni(GL_Q, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
        glTexGenfv(GL_Q, GL_EYE_PLANE, (GLfloat*4)(*textureProjectionMatrix[3]))
        glEnable(GL_TEXTURE_GEN_Q)

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def configureNormalMap(self, colorUnit, normalUnit, colorTexture, normalTexture):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(normalTexture.target, normalTexture.glID)
        glEnable(normalTexture.target)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE_EXT)
        glTexEnvf(GL_TEXTURE_ENV, GL_COMBINE_RGB_EXT, GL_DOT3_RGB_EXT)
        glTexEnvf(GL_TEXTURE_ENV, GL_SOURCE0_RGB_EXT, GL_TEXTURE)
        glTexEnvf(GL_TEXTURE_ENV, GL_OPERAND0_RGB_EXT, GL_SRC_COLOR)
        glTexEnvf(GL_TEXTURE_ENV, GL_SOURCE1_RGB_EXT, GL_PRIMARY_COLOR_EXT)
        glTexEnvf(GL_TEXTURE_ENV, GL_OPERAND1_RGB_EXT, GL_SRC_COLOR)
        
        if colorTexture:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(colorTexture.target, colorTexture.glID)
            glEnable(colorTexture.target)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE_EXT)
            glTexEnvf(GL_TEXTURE_ENV, GL_COMBINE_RGB_EXT, GL_MODULATE)
            glTexEnvf(GL_TEXTURE_ENV, GL_SOURCE0_RGB_EXT, GL_PREVIOUS_EXT)
            glTexEnvf(GL_TEXTURE_ENV, GL_OPERAND0_RGB_EXT, GL_SRC_COLOR)            
            glTexEnvf(GL_TEXTURE_ENV, GL_SOURCE1_RGB_EXT, GL_TEXTURE)
            glTexEnvf(GL_TEXTURE_ENV, GL_OPERAND1_RGB_EXT, GL_SRC_COLOR)

    def configureMaterial(self, material):
        # Materials initialization and activation
	#glMaterialfv (GL_FRONT_AND_BACK, GL_AMBIENT, material.ambient)
        #glMaterialfv (GL_FRONT_AND_BACK, GL_DIFFUSE, material.diffuse)
        #glMaterialfv (GL_FRONT_AND_BACK, GL_SPECULAR, material.specular)
        #glMaterialfv (GL_FRONT_AND_BACK, GL_SHININESS, material.shininess)
        
        if material.bump:
            self.configureNormalMap(1, 0, material.texture, material.bump)
        elif material.texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(material.texture.target, material.texture.glID)
            glEnable(material.texture.target)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            
        
    def drawRangeElements(self, mode, tri):
        glDrawRangeElements(mode, tri.start, tri.end, tri.size, GL_UNSIGNED_INT, tri.faces.pointer())

        
