"""
Hammerfall Console class. This class will be used to implement a real time
debugging console.

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet

import base

class Console(base.Task):
    """
    The Console will be implemented as another task to be inserted in the
    kernel's core.

    """
    def __init__(self, kernel, render, listener, activationKey):
        self.render = render
        self.active = False
        self.percent = 0.5
        
        def consoleActivationChange(symbol, modifier):
            self.active = not self.active
        listener.staticBind(kernel, activationKey, consoleActivationChange)

        def consoleRender():
            if self.active:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,\
                    ('v2f', [0, 0, render.w.width, 0,\
                             render.w.width, render.w.height * self.percent,\
                             0, render.w.height * self.percent]),\
                    ('c4B', [200, 200, 220, 255] * 4))
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
