"""
Hammerfall user interface elements. This file containts the implementation for
the following GUI elements:
    - HPanel: Hammerfall Panel class

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet

import base
import Listener

class HComponent:
    """
    The HComponent class will hold the implementation details for the
    Hammerfall GUI Component.
    
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
            
    def setVertices(self, x, y, w, h):
        """
        This function will set new coordinates for a HComponent.
        """
        self.vertex_list.vertices = [x, y, x + w, y, x + w, y + h, x, y + h];

class HPanel(HComponent):
    """
    The HPanel class will hold the implementation details for the Hammerfall
    Panel.
    """
    def __init__(self, batch, x, y, w, h, color = (200, 200, 200, 255)):
        HComponent.__init__(self, batch, x, y, w, h, color)
        self.componentlist = []
        
    def redraw(self, x, y, w, h):
        self.setVertices(x, y, w, h);
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def add(self, string, x, y, w, h, bcolor = (200, 200, 200, 255), 
            fcolor = (0, 0, 0, 255), text = '', border = 0, multiline = False, 
            startPos = 0):
            
        if string == 'Memo':
            x = self.x + x
            y = self.y + self.h - y -h
            memo = HMemo(self.batch, x, y, w, h,
                                bcolor, fcolor, border, text)
            self.componentlist.append(memo)
            return memo
        
        if string == 'Label':
            x = self.x + x
            y = self.y + self.h - y - h
            self.componentlist.append(HMemo(self.batch, x, y, w, h, bcolor,
                                            fcolor, text, multiline))
                                            
        if string == 'TextField':
            x = self.x + x
            y = self.y + self.h - y - h
            tf = HTextField(self.batch, x, y, w, h, bcolor,
                        fcolor, border, text, multiline, startPos)
            self.componentlist.append(tf)
            return tf            

class HLabel(HComponent):
    """
    The HLabel class will hold the implementation details for the Hammerfall
    Label.
    
    """
    def __init__(self, batch, x, y, w, h, bcolor = (200, 200, 200, 255),
                 fcolor = (0, 0, 0, 255), text = 'HLabel', multiline = False):
        HComponent.__init__(self, batch, x, y, w, h, bcolor)
        self._text = text
        self._label = pyglet.text.Label(text, x = x, y = y,\
                                        color = fcolor, batch = batch,\
                                        multiline = multiline, width = w,\
                                        height = h)
        self._set_text_position()
        
    def redraw(self, x, y, w, h):
        #Note: This is not fully tested.
        self.setVertices(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def _set_text_position(self):
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

class HTextField(HComponent):
    """
    The HPanel class will hold the implementation details for the Hammerfall
    TextField.

    """
    def __init__(self, batch, x, y, w, h, bcolor = (200, 200, 200, 255),
                 fcolor = (0, 0, 0, 255), border = 1, text = 'HTextField',
                 multiline = False, startPos = 0):
        HComponent.__init__(self, batch, x, y, w, h, bcolor)
        self.actions = {}
        self._border = border
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                 dict(color = fcolor))
        self._layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                w, h, multiline = multiline, batch = batch)
        self.caret = pyglet.text.caret.Caret(self._layout)
        self._layout.x = x + border
        self._layout.y = y - border # - because the alignment is top
        self.specialStartPosition = startPos
        
    def redraw(self, x, y, w, h):
        """
        Redraws a HTextField object.
        """
        #Note: This is not fully tested.
        self.setVertices(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._layout.begin_update()
        self._layout.x = x + self._border
        self._layout.y = y - self._border
        self._layout.height = self.h
        self._layout.end_update()

    def hit_test(self, x, y):
        return (0 < x - self._layout.x < self._layout.width) and\
               (0 < y - self._layout.y < self._layout.height)

    def addActionChar(self, char, action):
        self.actions[char] = action

    def parseforAction(self, char):
        if char in self.actions.keys():
            self.actions[char]()
            return Listener.HANDLED
        return None
    
    def setText(self, text):
        self._text = text
        self._layout.begin_update()
        self._layout.document.text = self._text
        self._layout.end_update()
        self._layout.view_y = self._layout.height - self._layout.content_height

class HMemo(HComponent):
    """
    This class will hold the implementation for a textbox in which the text will
    scroll from bottom to top.

    """
    def __init__(self, batch, x, y, w, h, bcolor = (200, 200, 200, 255),
                 fcolor = (0, 0, 0, 255), border = 0, text = 'HTextField'):
        HComponent.__init__(self, batch, x, y, w, h, bcolor)
        self._text = text
        self._border = border
        self._document = pyglet.text.document.UnformattedDocument(text)
        self._document.set_style(0, len(self._document.text),
                                 dict(color = fcolor))
        self._layout = pyglet.text.layout.IncrementalTextLayout(self._document,
                                w, h, multiline = True, batch = batch)
        self._layout.content_valign = 'bottom'
        self._layout.x = x + border
        self._layout.y = y + border #+ because the alignment is bottom
        self._layout.view_y = self._layout.height - self._layout.content_height
        
    def redraw(self, x, y, w, h):
        """
        Redraws a HMemo object.
        """
        #Note: This is not fully tested.
        self.setVertices(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._layout.begin_update()
        self._layout.x = x + self._border
        self._layout.y = y + self._border
        self._layout.height = self.h - self._border
        self._layout.end_update()

    def addLine(self, line):
        self._text = self._text + "\n" + line
        self._layout.begin_update()
        self._layout.document.text = self._text
        self._layout.end_update()
        self._layout.view_y = self._layout.height - self._layout.content_height

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text
        self._layout.begin_update()
        self._layout.document.text = self._text
        self._layout.end_update()
        self._layout.view_y = self._layout.height - self._layout.content_height

    def clearText(self):
        self.setText("")
        
    def hit_test(self, x, y):
        return (0 < x - self._layout.x < self._layout.width) and\
               (0 < y - self._layout.y < self._layout.height)
               
    def scroll (self, dx, dy):
        font = self._layout.document.get_font()
        lt_h = font.ascent - font.descent
        self._layout.begin_update()
        self._layout.view_y = self._layout.view_y + dy * lt_h
        self._layout.end_update()
