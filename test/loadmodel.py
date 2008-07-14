import sys
import pyglet
from pyglet.gl import *
sys.path.insert(0, "../trunk")
import ctypes
import array
import hfall.base
import hfall.OGLbase
# import hfall.UI
import hfall.Render
import hfall.Vertex
import hfall.Mesh
import hfall.Model
import hfall.ModelLoader
import hfall.Bitmap
# from hfall.Console import Console
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe = 100
        self._vertexes = []
        self._faces = []
        # self.mesh = []
        self.model = None
        self.Loader = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        
        # ppoints = (GLfloat * len(points))(*points)
        # pcolors = (GLfloat * len(colors))(*colors)
        # self._vertexes = ppoints
        # pfaces = (GLuint * len(faces))(*faces)
        # self._faces = pfaces
        # self.mesh.append(hfall.Mesh.Mesh(self._faces, self._vertexes, None, None, None, GL_TRIANGLES))

        Loader = hfall.ModelLoader.ModelLoader()
        Loader.loadModel("test.3ds")
        self.model = Loader.getModel()
        #print self.model.meshes[0].vertices
        #print self.model.meshes[0].faces
        TEX_NO = 16
	texture_ids = array.array('L',range(TEX_NO))
	ptexture_ids = (GLuint * TEX_NO)(*texture_ids)
	glGenTextures(TEX_NO,ptexture_ids)

  	bitmap = hfall.Bitmap.Bitmap("test.bmp")
        data_list = bitmap.data.tolist()
	pdata = (GLubyte * len(data_list))(*data_list)
	    
	glBindTexture(GL_TEXTURE_2D,ptexture_ids[0])
  	glTexImage2D(GL_TEXTURE_2D,0,4,bitmap.width,\
		    bitmap.height,0,GL_RGBA,GL_UNSIGNED_BYTE,pdata)
 	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
 	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
 	          
        for i in range(0,len(self.model.meshes)):
            self.model.meshes[i].vertices = (GLfloat * len(self.model.meshes[i].vertices))(*self.model.meshes[i].vertices)
            self.model.meshes[i].faces = (GLuint * len(self.model.meshes[i].faces))(*self.model.meshes[i].faces)
            self.model.meshes[i].texels = (GLfloat * len(self.model.meshes[i].texels))(*self.model.meshes[i].texels)
            self.model.meshes[i].texture = ptexture_ids[i]
            print self.model.meshes[i].materials

        # self.model = hfall.Model.Model(self.mesh, None)
        render.add3D(self.model)

    def stop(self, kernel):
        pass

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        #self._maxframe-=1
        #print "Frame: ",self._maxframe
        if (self._maxframe<0):
            kernel.shutdown()

    def name(self):
        return "drawer"

render = hfall.Render.Render(800, 600, posx = 0, posy = 0, posz = -70)
hfk.insert(drawer())
hfk.insert(render)
# hfk.insert(Console(render))
hfk.run()
