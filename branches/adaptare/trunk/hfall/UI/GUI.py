"""
Hammerfall user interface elements. This file containts the implementation for
the following GUI elements:
    - HPanel: Hammerfall Panel class

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet

class HPanel:
    """
    The HPanel class will hold the implementation details for the Hammerfall
    Panel.
    
    """
    def __init__(self, batch, x, y, w, h, color = (200, 200, 200, 255)):
        self.batch = batch
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x, y, x + w, y, x + w, y + h, x, y + h]),
            ('c4B', color * 4)
        )


class HLabel(HPanel):
    """
    The HLabel class will hold the implementation details for the Hammerfall
    Label.
    
    """
    def __init__(self, batch, x, y, w, h, bcolor = (200, 200, 200, 255),
                 fcolor = (0, 0, 0, 255), text = 'HLabel', multiline = False):
        HPanel.__init__(self, batch, x, y, w, h, bcolor)
        self._text = text
        self._label = pyglet.text.Label(text, x = x, y = y,\
                                        color = fcolor, batch = batch,\
                                        multiline = multiline, width = w,\
                                        height = h)
        self._set_position()

    def _set_position(self):
        c_w = self._label.content_width #content width
        font = self._label.document.get_font()
        lt_h = font.ascent - font.descent #line of text height
        c_h = self._label.content_height #content height
        n_l = c_h / lt_h #number of lines
        self._label.x = self.x + (self.w - c_w) / 2
        self._label.y = self.y + (self.h + c_h) / 2 - font.ascent

    def setText(self, text):
        self._label.begin_update()
        self._label.text = text
        self._set_position()
        self._label.end_update()
