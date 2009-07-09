"""
Hammerfall example and testing application. This should be used for testing
purposes and for learning how to use the Hammerfall Graphics Engine.

Quick tips:
    - the engine is structured around a kernel which must be passed as argument
        to all functions needing to communicate with other tasks
    - your app will need a Render task for rendering to the screen
    - by calling render.end(kernel) the application will end (in the current
        frame)
    - by calling only kernel.remove(self.name()) you are only stopping the
        current task and removing access to it. The rendering task will still
        be available and holding all the data that was pased to it for rendering
        (consult the Render documentation for more info)
        
"""

__version__ = "0.7"
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import sys
import os
if sys.argv[0].rfind('/') > 0:
    os.chdir(os.path.dirname(sys.argv[0]))
sys.path.insert(0, "../trunk/hfall")
sys.path.insert(0, "../trunk/hfall/Engine")
sys.path.insert(0, "../trunk/hfall/UI")
import math

import pyglet

import base
from base import kernel as hfk
import Render
import Listener
import Console
import Terrain
import GUI
from pyglet.gl import *

class Hammer(base.Task):
    def __init__(self, render, listener, console):
        self.render = render #to be used when passing parameters and options to
                             # the renderer
        self.listener = listener #used for handling keyboard and mouse events
        self.console = console #different commands
        self.tp = 0 #just for demo purposes
        pass

    def start(self, kernel):
        kernel.log.msg("Hammer is falling down...")
            
        def f1(symbol, modifier):
            print "T was pressed."
            print self.tp
            if self.tp > 100:
                self.listener.dinamicUnbind(kernel, f3)
            self.tp = 1000
        self.listener.staticBind(kernel, pyglet.window.key.T, f1)

        def f2(symbol, modifier):
            print "T was pressed second function (just deleting self)"
            print self.listener.staticUnbind(kernel, pyglet.window.key.T)
            return Listener.HANDLED # use this if you want exclusivity
        self.listener.staticBind(kernel, pyglet.window.key.T, f2)

        def f3(keyboard):
            if keyboard[pyglet.window.key.P] and keyboard[pyglet.window.key.T]:
                self.tp += 1 #just counting the number of Ts with Ps
        self.listener.dinamicBind(kernel, f3) #this would be called as long
                                              # as keys are pressed

        self.listener.setDefaultBindings(kernel) # camera, axes,...

        def f4(X, Y, buttons, modifiers):
            if modifiers & pyglet.window.key.LSHIFT:
                self.render.camera.rotate(1, 0, 0, math.pi)
        self.listener.mouseBind(kernel, f4, Listener.MOUSE_PRESS)
        
        def drawCube():
            glPushMatrix()
            glTranslatef(30.0, 30.0, 30.0)
            pyglet.graphics.draw_indexed(12, GL_TRIANGLES, range(12), 
                                        ('v3f', (0.0, 30.0, 0.0,\
                                  -30.0, -30.0, 30.0,\
                                30.0, -30.0, 30.0,\
                                  0.0, 30.0, 0.0,\
                                  30.0, -30.0, 30.0,\
                                  30.0, -30.0, 30.0,\
                                  0.0, 30.0, 0.0,\
                                  30.0, -30.0, -30.0,\
                                  -30.0, -30.0, -30.0,\
                                  0.0, 30.0, 0.0,\
                                  -30.0, -30.0, -30.0,\
                                  -30.0, -30.0, 30.0)),\
                        ('c3B', (255, 0, 0,\
                                 255, 0, 0,\
                                 0, 255, 255,\
                                 0, 255, 255,\
                                 0, 255, 0,\
                                 0, 255, 0,\
                                 255, 0, 255,\
                                 255, 0, 255,\
                                 0, 0, 255,\
                                 0, 0, 255,\
                                 255, 255, 0,\
                                 255, 255, 0)))
            glPopMatrix()
        self.render.addRenderingFunction(kernel, drawCube)
        terrain = Terrain.Terrain(self.render)
        patch = Terrain.TerrainPatch()
        terrain.addPatch(kernel, patch)
        hf = Terrain.HeightField(size=64)
        for i in range(65):
            for j in range(65):
                hf.setHeight(i, j, (1-math.exp(math.sin((i+j/2.1)/42.0))))
        patch = Terrain.TerrainPatch(x_origin = -100, hfield = hf)
        terrain.addPatch(kernel, patch)
        kernel.insert(terrain) # we can insert other modules anywhere we want
                               # after we entered the run or start phase of
                               # another one

##        panel1 = GUI.HPanel(self.render.batch, 25, 25, 500, 500)
##        self.label1 = GUI.HLabel(self.render.batch, 50, 50, 142, 120,\
##                            text = "A\nb\nc", multiline = True)
##        self.tf1 = GUI.HTextField(self.render.batch, 25, 25, 150, 20,
##                                  text = "> ", startPos = 2)
##        self.listener.addWidget(self.tf1) # to have mouse interaction with it
##        self.tf2 = GUI.HTextField(self.render.batch, 125, 125, 150, 20,
##                                  text = ">> ", startPos = 3)
##        self.listener.addWidget(self.tf2) # to have mouse interaction with it

##        self.memo = GUI.HMemo(self.render.batch, 50, 50, 142, 120,\
##                            text = "")
        self.frame = 0
        
    def stop(self, kernel):
        kernel.log.msg("Hammer stopped falling")
        
    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
##        self.frame += 1
##        if self.frame % 100 == 0:
##            self.memo.addLine(str(self.frame))
##            print "adding", self.frame
##            if self.frame > 1000:
##                print self.memo.getText()
##                self.memo.clearText()
##                self.frame = 0
        pass

    def name(self):
        return "Hammer"

    
render = Render.Render(800, 600, posx = -10, posy = 30, posz = -30,\
                         near = 0.0001, far = 10000)
listener = Listener.Listener(render)
console = Console.Console(hfk, render, listener,\
                          activationKey = pyglet.window.key.QUOTELEFT)
hfk.insert(listener)#don't forget to insert this if you wish mouse and keyboard
                    #for best results insert the listener first
hfk.insert(console) #also, insert a console, just after the listener
hfk.insert(Hammer(render, listener, console))
hfk.insert(render) #this should be ALWAYS the LAST task inserted at the start
hfk.run()
