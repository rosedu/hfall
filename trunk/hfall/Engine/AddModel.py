import sys
sys.path.insert(0, "../Parser/")
##sys.path.insert(0, "..")

from Vector import Vector3
import ModelLoader
import MaterialManager
import ModelManager
import TextureManager
import Render
import pyglet
import math
import MathBase
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
def add_model(model_name, position = [1,1,1]):
    Loader.loadModel(model_name)
    model = Loader.getModel()
    model.translate(position[0], position[1], position[2])
    g_render.add3D(model)
    #this line should be removed, only for testing purposes
    return model

def rem_model(model_nr):
    g_render.rem3D(model_nr)
