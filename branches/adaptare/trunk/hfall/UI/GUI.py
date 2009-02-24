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
    def __init__(self, batch, x, y, w, h, bcolor = (200, 200, 200, 255),\
                 fcolor = (0, 0, 0, 255), text = 'HLabel', pad = 5, \
                 multiline = False):
        HPanel.__init__(self, batch, x, y, w, h, bcolor)
        self.text = text
        self.label = pyglet.text.Label(text, x = x + 2 * pad, y = y + 2 * pad,\
                                       color = fcolor, batch = batch, \
                                       multiline = multiline, anchor_y='bottom')
        
