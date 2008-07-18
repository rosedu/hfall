import sys
sys.path.insert(0, "../Engine")
import ModelLoader
import MaterialManager
import ModelManager
import TextureManager
import Render
import pyglet
from pyglet.gl import *

global Loader
global modelmng
def init(render):
    materialmng = MaterialManager.MaterialManager()
    global modelmng
    modelmng = ModelManager.ModelManager()
    texturemng = TextureManager.TextureManager()
    global Loader
    global g_render
    g_render = render
    Loader = ModelLoader.ModelLoader(modelmng, materialmng,\
                                         texturemng)
def add_model(model_name, position):
    Loader.loadModel(model_name)
    model = Loader.getModel()
    model.matrix4[12:] = position
    model.matrix4 = (GLfloat * 16)(* model.matrix4)
    g_render.add3D(model)
    
def scale_model(model, scaling):
    model.matrix4[0] = scaling[0]
    model.matrix4[5] = scaling[1]
    model.matrix4[10] = scaling[2]
