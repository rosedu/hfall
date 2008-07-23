import sys
sys.path.insert(0, "../Engine")
sys.path.insert(0, "..")
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
def add_model(model_name, position = [0,0,0,1]):
    Loader.loadModel(model_name)
    model = Loader.getModel()
    model.matrix4[12:] = position
    model.matrix4 = (GLfloat * 16)(* model.matrix4)
    g_render.add3D(model)
    #this line should be removed, only for testing purposes
    return model

def rem_model(model_nr):
    g_render.rem3D(model_nr)

    
def scale_model(model, scaling):
    scale_matrix = [scaling[0], 0, 0, 0,\
                    0, scaling[1], 0, 0,\
                    0, 0, scaling[2], 0,\
                    0, 0, 0, 1]
    model.matrix4 = MathBase.matrixmult(model.matrix4, scale_matrix)
    
def rotatex_model(model, theta):
    rot_matrix = [1, 0, 0, 0,\
                    0, math.cos(theta), - math.sin(theta), 0,\
                    0, math.sin(theta), math.cos(theta), 0,\
                    0, 0, 0, 1]
    model.matrix4 = MathBase.matrixmult(model.matrix4, rot_matrix)
def rotatey_model(model, theta):
    rot_matrix = [math.cos(theta), 0, math.sin(theta), 0,\
                    0, 1, 0, 0,\
                    - math.sin(theta), 0, math.cos(theta), 0,\
                    0, 0, 0, 1]
    model.matrix4 = MathBase.matrixmult(model.matrix4, rot_matrix)
def rotatez_model(model, theta):
    rot_matrix = [math.cos(theta), - math.sin(theta), 0, 0,\
                    math.sin(theta), math.cos(theta), 0, 0,\
                    0, 0, 1, 0,\
                    0, 0, 0, 1]
    model.matrix4 = MathBase.matrixmult(model.matrix4, rot_matrix)
