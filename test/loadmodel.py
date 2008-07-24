import sys
import pyglet
from pyglet.gl import *
sys.path.insert(0, "../trunk/hfall")
sys.path.insert(0, "../trunk/hfall/UI")
sys.path.insert(0, "../trunk/hfall/Engine")
sys.path.insert(0, "../trunk/hfall/Parser")
import ctypes
import array
import base
import OGLbase
from UI import * 
import Render
import AddModel
import Mesh
import Model
import ModelLoader
import MaterialManager
import ModelManager
import TextureManager
import Bitmap
import Light
from base import kernel as hfk

class drawer(base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe = 100
        self._vertexes = []
        self._faces = []
        # self.mesh = []
        # self.materialmng = None
        # self.modelmng = None
        # self.texturemng = None
        # self.model = None
        # self.Loader = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        AddModel.init(render)
        light1 = Light.Light( GL_LIGHT1, \
                    rLightAmbient = [1.0, 1.0, 1.0, 1.0],\
                    rLightDiffuse = [1.0, 1.0, 1.0, 1.0],\
                    rLightPosition = [0.0, -1.5, -50.0, 1.0])
        render.addLight(light1)
        
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

render = Render.Render(800, 600, posx = 0, posy = -1.5, posz = -100)
hfk.insert(drawer())
hfk.insert(render)
hfk.insert(UI(render))
hfk.run()
