"""
Hamerfall OpenGL class. This class initializes the OpenGL interface and
then draws vertices and lines to the screen, after changing properly the
state of the OpenGL finite-state machine.

"""

__version__ = '0.2'
__author__ = 'Maruseac Mihai (mihai.maruseac@gmail.com)' ,\
              'Andrei Buhaiu (andreibuhaiu@gmail.com)'

import pyglet
from pyglet.gl import *
from pyglet import window
import ctypes
import Mathbase
import Vertex
import base
from base import kernel as hfk

colors = ((5 // 2) + 1)* [1, 1, 1, 0, 1, 0]
pcolors = (GLfloat * len(colors))(*colors)

class OGL:
    """
    This is the class that encapsulates all OpenGL API calls. All acces
    to the OpenGL interface should be done using this class.

    """

    def __init__(self, w, width, height, near=0.1, far=100.0, \
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
        self.w=w
        @self.w.event
        def on_resize(width, height):
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if height == 0:
                height = 1
            gluPerspective(60.0, width / float(height), .1, 1000.0)
            glMatrixMode(GL_MODELVIEW)
        
        # finalizing the initialization
        glClearColor(clearcolor[0], clearcolor[1], clearcolor[2], \
                     clearcolor[3])
        glShadeModel(GL_SMOOTH)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
  	glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        hfk.log.msg('Open GL started')

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
        glRotatef(angle, direction.x, direction.y, direction.z)
    
    def render(self, mode, vertexes):
        """
        The render function of the OpenGL.
            mode - one of the OpenGL drawing primitives
            vertexes - a list containing all the vertices to be drawn on
                       screen in proper order. All elements in the list
                       should be of Vertex type

        """
        # TODO: a verification for the vertexes list's elements format
        glBegin(mode)
        for vertex in vertexes:
            if vertex.color is not None:
                if len(vertex.color) == 3:
                    glColor3f(vertex.color[0], vertex.color[1], vertex.color[2])
                else:
                    glColor4f(vertex.color[0], vertex.color[1], vertex.color[2],\
                              vertex.color[3])
            if vertex.texture is not None:
                if len(vertex.texture) == 1:
                    glTexCoord1f(vertex.texture[0])
                else:
                    glTexCoord2f(vertex.texture[0], vertex.texture[1])
            if vertex.normal is not None:
                glNormal3f(vertex.normal.x, vertex.normal.y, vertex.normal.z)
            if len(vertex.position) == 2:
                glVertex2f(vertex.position[0], vertex.position[1])
            elif len(vertex.position) == 3:
                glVertex3f(vertex.position[0], vertex.position[1],\
                           vertex.position[2])
            else:
                glVertex4f(vertex.position[0], vertex.position[1],\
                           vertex.position[2], vertex.position[3])
        glEnd()

    def Render2D(self, model):
        """
        This function is used to render any 2D graphic, mainly used for
        rendering the user interface.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        glLoadIdentity()
        glTranslatef(0.0,0.0,-6.0);
  	if model.is_textured==True:
		glBindTexture(GL_TEXTURE_2D,model.texture_ids[0])
  		glTexImage2D(GL_TEXTURE_2D,0,4,model.pixelwidth,\
		    model.pixelheight,0,GL_RGBA,GL_UNSIGNED_BYTE,model.data)
 		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
 		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        	glBegin(GL_QUADS)
  		glTexCoord2f(0.0,0.0)
        	glVertex2f(model.x, model.y)
  		glTexCoord2f(1.0,0.0)
        	glVertex2f(model.xx, model.y)
  		glTexCoord2f(1.0,1.0)
        	glVertex2f(model.xx, model.yy)
  		glTexCoord2f(0.0,1.0)
        	glVertex2f(model.x, model.yy)
  		glEnd()
  	else:
        	if len(model.color) == 3:
            		glColor3f(model.color[0], model.color[1], model.color[2])
        	else:
            		glColor4f(model.color[0], model.color[1], model.color[2], \
              	        	model.color[3])
		glBegin(GL_QUADS)
		glVertex2f(model.x, model.y)
  		glVertex2f(model.xx,model.y)
  		glVertex2f(model.xx, model.yy)
  		glVertex2f(model.x, model.yy)
        	glEnd()      

    def RenderMesh(self, mesh):
        glPushMatrix()
        #glLoadIdentity()
        colors = ((len(mesh.vertices) // 2) + 1)* [1, 1, 1, 0, 1, 0]
        mesh.colors = (GLfloat * len(colors))(*colors) 
        # if (mesh.materials == []):
            # selects the color that will be used if
            # no material was given
        glColorPointer(3, GL_FLOAT, 0, mesh.colors)
        """
        else:
            im = open(mesh.materials)
	    try:
		# get image meta-data (dimensions) and data
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
            except SystemError:
		# has no alpha channel, synthesize one, see the
		# texture module for more realistic handling
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
            # generate a texture ID
            ID = glGenTextures(1)
            # make it current
            glBindTexture(GL_TEXTURE_2D, ID)
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            # copy the texture into the current texture ID
            glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            # re-select our texture, could use other generated textures
            # if we had generated them earlier...
            glBindTexture(GL_TEXTURE_2D, ID)

            glBegin(GL_QUADS);
            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);

            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);

            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);

            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);

            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
            glEnd()
        """
        
        # We send the actual vertices to OpenGL so that it may render them
        glVertexPointer(3, GL_FLOAT, 0, mesh.vertices)
        # We draw that actual faces that form the model
        glDrawElements(GL_TRIANGLES, len(mesh.faces), GL_UNSIGNED_INT, mesh.faces)
        # We extract the perspective matrix that we used
        # so that the new mesh is built on its own matrix
        # print "test"
        glPopMatrix()
        
    def Render3D(self, model):
        """
        This function is used to render any 3D graphic.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        #glLoadIdentity()
        # glMultMatrixf(model.matrix4)
        # We render each mesh in the model
        for mesh in model.meshes:
            self.RenderMesh(mesh)
        
