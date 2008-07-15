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
import Mesh
import Model
import ModelLoader
import MaterialManager
import ModelManager
import TextureManager
import Bitmap
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
        self.materialmng = None
        self.modelmng = None
        self.texturemng = None
        self.model = None
        self.Loader = None
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");

        print "Model:", sys.argv[1]
        self.materialmng = MaterialManager.MaterialManager()
        self.modelmng = ModelManager.ModelManager()
        self.texturemng = TextureManager.TextureManager()
        Loader = ModelLoader.ModelLoader(self.modelmng, self.materialmng,\
                                         self.texturemng)
        Loader.loadModel(sys.argv[1])
        self.model = Loader.getModel()

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

render = Render.Render(800, 600, posx = 0, posy = -1.5, posz = -100,\
                             raw_LightPosition = [0.0, 1.0, 0.0, 0.0])
hfk.insert(drawer())
hfk.insert(render)
hfk.insert(UI(render))
hfk.run()
