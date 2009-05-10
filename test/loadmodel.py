import sys
import traceback
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

##        light1 = Light.Spotlight( GL_LIGHT1, \
##                    rLightSpecular = [1.0, 1.0, 1.0, 1.0],\
##                    rLightAmbient = [.9, .9, .9, 1.0],\
##                    rLightDiffuse = [1.0, 0.0, 0.0, 1.0],\
##                    rLightPosition = [0.0, 38, -10.0, 1.0],\
##                                  ca = 1.0, la = 0.01, qa = 0.0)
##        light1.enableAttenuation()
##        render.addLight(light1)
##        
##        light2 = Light.Light( GL_LIGHT2, \
##                    rLightSpecular = [1.0, 1.0, 1.0, 1.0],\
##                    rLightAmbient = [1.9, 1.9, 1.9, 1.9],\
##                    rLightDiffuse = [0.0, 0.0, 1.0, 1.0],\
##                    rLightPosition = [0.0, 30, -10.0, 1.0])
##        light2.enableAttenuation()
##        render.addLight(light2)
        #'''
        #This is an example of terrain rendering
        AddModel.add_model("models/machinegun/3dm-q3machinegun.3ds", [0, 10, 10])
        terrain = Terrain.Terrain()
        patch = Terrain.TerrainPatch(x_origin = -64)
        patch.opreparebuffers()
        patch.makeVisible()
        terrain.addPatch(patch)
        hf = Terrain.HeightField()
        for x in range(65):
            for y in range(65):
                hf.setHeight(x, y, 10* (math.exp(math.sin(x/13.0))))
        patch = Terrain.TerrainPatch(hfield = hf)
        patch.opreparebuffers()
        patch.makeVisible()
        terrain.addPatch(patch)#
        terrain.Enable()
        render.terrain = terrain
        #model = Test.TTest()
        #render.testmodel = model
        
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

render = Render.Render(800, 600, posx = 0, posy = 0, posz = -100, far = 10000)
hfk.insert(drawer())
hfk.insert(render)
hfk.insert(UI(render))
hfk.run()
