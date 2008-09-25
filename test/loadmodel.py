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
import Terrain
import math
from base import kernel as hfk

class drawer(base.Task):
    def __init__(self):
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
        # creature = AddModel.add_model("models/creature.3ds", [0, 0, -20, 1])
        # AddModel.scale_model(creature, [18.0, 18.0, 18.0])

        #atrium = AddModel.add_model("models/atrium.3ds")
        #AddModel.scale_model(atrium, [0.1, 0.1, 0.1])

        light1 = Light.Light( GL_LIGHT1, \
                    rLightAmbient = [1.9, 1.9, 1.9, 1.9],\
                    rLightDiffuse = [1.0, 1.0, 1.0, 1.0],\
                    rLightPosition = [0.0, -1.5, -50.0, 30.0])
        render.addLight(light1)
        """This is an example of terrain rendering
        terrain = Terrain.Terrain()
        patch = Terrain.TerrainPatch(x_origin = -64)
        patch.preparebuffers()
        patch.makeVisible()
        terrain.addPatch(patch)
        hf = Terrain.HeightField()
        for x in range(65):
            for y in range(65):
                hf.setHeight(x, y, math.sin(x+y))
        patch = Terrain.TerrainPatch(hfield = hf)
        patch.preparebuffers()
        patch.makeVisible()
        terrain.addPatch(patch)
        terrain.Enable()
        render.terrain = terrain
        """
        
    def stop(self, kernel):
        pass

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        pass

    def name(self):
        return "drawer"

render = Render.Render(800, 600, posx = 0, posy = -1.5, posz = -100, far = 10000)
hfk.insert(drawer())
hfk.insert(render)
hfk.insert(UI(render))
hfk.run()
