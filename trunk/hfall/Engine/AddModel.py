import sys
sys.path.insert(0, "../Engine")
import ModelLoader
import MaterialManager
import ModelManager
import TextureManager
import Render
import pyglet
import numpy
import array
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

def rem_model(model_nr):
    g_render.rem3D(model_nr)

    
def scale_model(model, scaling):
    scale_matrix = [scaling[0], 0, 0, 0,\
                    0, scaling[1], 0, 0,\
                    0, 0, scaling[2], 0,\
                    0, 0, 0, 1]
    glMultMatrix
    matrixmultiply()
