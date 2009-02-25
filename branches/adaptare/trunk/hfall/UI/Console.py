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
        self.text = "Hammerfall Graphics Engine \n"
        self.w = render.w.width
        self.h = render.w.height * self.percent
        self.top = render.w.height
        self.batch = pyglet.graphics.Batch()
        self.consoleLayout = self.batch.add(4, pyglet.gl.GL_QUADS, None,\
                    ('v2f', [0, self.h, self.w, self.h,\
                             self.w, self.top, 0, self.top]),\
                    ('c4B', [200, 200, 200, 255] * 4))
##        self.inputBoxText = pyglet.text.document.UnformattedDocument("> ")
##        self.inputBoxText.set_style(0, len(self.inputBoxText.text), \
##                                    dict(color=(0, 0, 0, 255)))
##        font = self.inputBoxText.get_font()
##        fh = font.ascent - font.descent
##        self.h -= fh
##        self.pad = 5
##        self.layout = pyglet.text.layout.IncrementalTextLayout(\
##            self.inputBoxText, self.w, fh, multiline = False, batch=self.batch)
##        self.caret = pyglet.text.caret.Caret(self.layout)
##        self.layout.x = self.pad
##        self.layout.y = self.h
##        self.consoleTextRct = self.batch.add(4, pyglet.gl.GL_QUADS, None,\
##                            ('v2f', [self.pad, self.pad, \
##                                     self.w - self.pad, self.pad,\
##                                     self.w - self.pad, self.h - self.pad,\
##                                     self.pad, self.h - self.pad]),\
##                            ('c4B', [180, 180, 180, 255] * 4))
        
        def consoleActivationChange(symbol, modifier):
            self.active = not self.active
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
