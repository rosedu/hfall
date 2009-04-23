"""
Hammerfall Console class. This class will be used to implement a real time
debugging console.

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet

import base
import GUI
import Listener

CPH = 25

class Console(base.Task):
    """
    The Console will be implemented as another task to be inserted in the
    kernel's core.

    """
    def __init__(self, kernel, render, listener, activationKey):
        self.render = render
        self.listener = listener
        self.listener.CAK = activationKey
        self.active = False
        self.percent = 0.5
        self.text = "Hammerfall Graphics Engine \n"
        self.w = render.w.width
        self.h = int(render.w.height * self.percent)
        self.top = render.w.height
        self.batch = pyglet.graphics.Batch()
        self.consolePanel = GUI.HPanel(self.batch, 0, self.top - self.h,
                                       self.w, self.h)
        self.consolePanel.addMemo(0, 0, self.w, self.h - CPH,
                                  bcolor = (150, 150, 150, 255),
                                  text = "Welcome to Hammerfall engine!\n")
        self.tf = self.consolePanel.addTextField(0, self.h - CPH, self.w, CPH,
                                       text = '> ', startPos = 2,
                                       multiline = True)
        
        def consoleActivationChange(symbol, modifier):
            self.active = not self.active
            if self.active:
                self.listener.addWidget(self.tf)
                self.listener.clearWidget(self.tf)
            else:
                self.listener.removeWidget(self.tf)
            return pyglet.event.EVENT_HANDLED
        listener.staticBind(kernel, activationKey, consoleActivationChange)

        def consoleRender():
            if self.active:
                self.batch.draw()
        self.render.addOrthoRenderingFunction(kernel, consoleRender)

    def start(self, kernel):
        kernel.log.msg("Console up and listening to commands")

    def stop(self, kernel):
        kernel.log.msg("Console down")

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        pass

    def name(self):
        return "Console"
