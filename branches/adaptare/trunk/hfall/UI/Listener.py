"""
Hammerfall Listener class. This class will be used to listen all events that
the application has to handle. All keyboard and mouse events (at least) must
be handled via this class. Consult each method documentation for more info.

"""

__version__ = '0.7'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet
from pyglet import window
from pyglet.window import *

import base

HANDLED = pyglet.event.EVENT_HANDLED
MOUSE_PRESS = 142
MOUSE_DRAG = 143
MOUSE_MOTION = 144

class Listener(base.Task):
    """
    The Listener class is another important class of the engine, being part
    of it's core.
    
    """
    def __init__(self, render):
        self._staticBindings = {} #key bindings to different functions (only
                                  # the press event will be listened
        self._dinamicBindings = [] #key bindings for transient actions (as
                                   # long as the key is pressed
        self._mousePressBindings = []
        self._mouseDragBindings = []
        self._mouseMotionBindings = [] # mouse events
        self.render = render #used for passing commands to the render
        self.widgets = [] #list of 2D widgets - only for focus setup
        self.scrollableWidgets = [] 
        self.text_cursor = self.render.w.get_system_mouse_cursor("text")
        self.focus = None
        self.enabled = False

        def on_text(text):
            self.on_text(text)
        render.w.push_handlers(on_text)

        def on_text_motion(motion):
            self.on_text_motion(motion)
        render.w.push_handlers(on_text_motion)

        def on_text_motion_select(motion):
            self.on_text_motion_select(motion)
        render.w.push_handlers(on_text_motion_select)

        def on_mouse_press(X, Y, button, modifiers):
            self.on_mouse_press(X, Y, button, modifiers)
        render.w.push_handlers(on_mouse_press)

        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        render.w.push_handlers(on_mouse_drag)

        def on_mouse_motion(x, y, dx, dy):
            self.on_mouse_motion(x, y, dx, dy)
        render.w.push_handlers(on_mouse_motion)
        
        def on_mouse_enter(x, y):
            pass
            
        def on_mouse_leave(x, y):
            pass
            
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            self.on_mouse_scroll(x, y, scroll_x, scroll_y)
        render.w.push_handlers(on_mouse_scroll)
            
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)
        render.w.push_handlers(on_key_press)

        self.keyboard = key.KeyStateHandler()
        render.w.push_handlers(self.keyboard)

    def start(self, kernel):
        kernel.log.msg("Listening to all events...")
        self.enabled = True

    def stop(self, kernel):
        kernel.log.msg("Not listening anymore.")
        self.enabled = False

    def pause(self, kernel):
        kernel.log.msg("Listeners taking a break")
        self.enabled = False

    def resume(self, kernel):
        kernel.log.msg("Listeners returning from break.")
        self.enabled = True

    def run(self, kernel):
        self.check_keyboard(self.keyboard)

    def name(self):
        return "Listener"

    def staticBind(self, kernel, key, action):
        if key in self._staticBindings:
            self._staticBindings[key].insert(0, action)
        else:
            self._staticBindings[key] = [action]
        kernel.log.msg("New static binding for key " + str(key) + " as " + \
                       action.func_name + " (" + \
                       str(len(self._staticBindings[key])) + ")")

    def staticUnbind(self, kernel, key):
        if key in self._staticBindings:
            oldaction = self._staticBindings[key][0]
            self._staticBindings[key] = self._staticBindings[key][1:]
            kernel.log.msg("Static binding for key " + str(key) + " as " + \
                           oldaction.func_name + " was removed (" + \
                           str(len(self._staticBindings[key])) + ")")
            return oldaction
        return None

    def dinamicBind(self, kernel, action):
        self._dinamicBindings.insert(0, action)
        kernel.log.msg("New dinamic binding for " + action.func_name + " (" + \
                       str(len(self._dinamicBindings)) + ")")

    def dinamicUnbind(self, kernel, action):
        if action in self._dinamicBindings:
            self._dinamicBindings.remove(action)
            kernel.log.msg("Dinamic binding for " + \
                           action.func_name + " was removed (" + \
                           str(len(self._dinamicBindings)) + ")")

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if len(self.widgets) != 0:             
                if modifiers & pyglet.window.key.MOD_SHIFT:
                    dir = -1
                else:
                    dir = 1

                if self.focus in self.widgets:
                    i = self.widgets.index(self.focus)
                else:
                    i = 0
                    dir = 0
                    
                self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        if self.focus:
            if self.focus.parseforAction(symbol): return
        if self.enabled and not self.focus:
            if symbol in self._staticBindings:
                action_list = self._staticBindings[symbol]
                for action in action_list:
                    if action(symbol, modifiers) == HANDLED:
                        break
        return pyglet.event.EVENT_HANDLED

    def mouseBind(self, kernel, action, bindingType):
        if bindingType == MOUSE_PRESS:
            self._mousePressBindings.insert(0, action)
            kernel.log.msg("New mouse press binding: " + action.func_name + \
                           " (" + str(len(self._mousePressBindings)) + ")")
        elif bindingType == MOUSE_DRAG:
            self._mouseDragBindings.insert(0, action)
            kernel.log.msg("New mouse drag binding: " + action.func_name + \
                           " (" + str(len(self._mouseDragBindings)) + ")")
        elif bindingType == MOUSE_MOTION:
            self._mouseMotionBindings.insert(0, action)
            kernel.log.msg("New mouse motion binding: " + action.func_name + \
                           " (" + str(len(self._mouseMotionBindings)) + ")")

    def mouseUnbind(self, kernel, action, bindingType):
        if bindingType == MOUSE_PRESS:
            if action in self._mousePressBindings:
                self._mousePressBindings.remove(action)
                kernel.log.msg("Mouse press binding for " + action.func_name + \
                           " removed (" + str(len(self._mousePressBindings)) +\
                            ")")
        elif bindingType == MOUSE_DRAG:
            if action in self._mousePressBindings:
                self._mouseDragBindings.remove(action)
                kernel.log.msg("Mouse drag binding for " + action.func_name + \
                            " removed (" + str(len(self._mouseDragBindings)) +\
                            ")")
        elif bindingType == MOUSE_MOTION:
            if action in self._mousePressBindings:
                self._mouseMotionBindings.remove(action)
                kernel.log.msg("Mouse motion binding for " + action.func_name +\
                            " removed (" + str(len(self._mouseMotionBindings)) +\
                            ")")

    def on_mouse_press(self, X, Y, buttons, modifiers):
        for widget in self.widgets:
            if widget.hit_test(X, Y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(X, Y, buttons, modifiers)

        if self.enabled and not self.focus:
            for action in self._mousePressBindings:
                if action(X, Y, buttons, modifiers) == HANDLED:
                    break;
        return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

        if self.enabled and not self.focus:
            for action in self._mouseDragBindings:
                if action(x, y, dx, dy, buttons, modifiers) == HANDLED:
                    break;
        return pyglet.event.EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.render.w.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.render.w.set_mouse_cursor(None)

        if self.enabled and not self.focus:
            for action in self._mouseMotionBindings:
                if action(x, y, dx, dy) == HANDLED:
                    break;
        return pyglet.event.EVENT_HANDLED
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for widget in self.scrollableWidgets:
            if widget.hit_test(x, y):
                widget.scroll(scroll_x, scroll_y)
            

    def check_keyboard(self, keyboard):
        if self.enabled and not self.focus:
            for action in self._dinamicBindings:
                if action(keyboard) == HANDLED:
                    break;
        return pyglet.event.EVENT_HANDLED

    def setDefaultBindings(self, kernel):
        """
        This function will set default bindings for different useful keys. For
        example, the keys needed to move the camera or to hide/show different
        visual clues of the engine (the console, the axes, etc)

        """
        #camera bindings:
        def cameraKeyMovement(keyboard):
            if keyboard[key.W]:
                self.render.camera.translate(0, 0, 1)
            elif keyboard[key.S]:
                self.render.camera.translate(0, 0, -1)
            elif keyboard[key.A]:
                self.render.camera.translate(-1, 0, 0)
            elif keyboard[key.D]:
                self.render.camera.translate(1, 0, 0)
            elif keyboard[key.Q]:
                self.render.camera.translate(0, 1, 0)
            elif keyboard[key.E]:
                self.render.camera.translate(0, -1, 0)
        self.dinamicBind(kernel, cameraKeyMovement)

        def cameraDrag(x, y, dx, dy, buttons, modifiers):
            factor = 0.005
            if buttons == mouse.RIGHT:
		self.render.camera.rotate(0,0,dx,factor)
		pass
            if buttons == window.mouse.LEFT:
		self.render.camera.rotate(dy,dx,0,factor)
	self.mouseBind(kernel, cameraDrag, MOUSE_DRAG)

        #axes bindings:
        def changeAxesState(symbol, modifiers):
            if symbol == key.X:
                self.render.enableAxes = not self.render.enableAxes
			    
		self.staticBind(kernel, key.X, changeAxesState)

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.set_focus(widget)

    def removeWidget(self, widget):
        self.widgets.remove(widget)
        self.set_focus(None)
        
    def addScrollableWidget(self, widget):
        self.scrollableWidgets.append(widget)

    def removeScrollableWidget(self, widget):
        self.scrollableWidgets.remove(widget)

    def clearWidget(self, widget):
        t = widget.document.text
        widget.caret.position = widget.specialStartPosition - 1
        tt = ""
        for i in range(0, widget.specialStartPosition):
            tt += t[i]
        widget.document.text = tt

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = self.focus.specialStartPosition
            self.focus.caret.position = len(self.focus.document.text)

    def on_text(self, text):
        if self.focus:
            if self.focus.parseforAction(text): return
            if self.focus.caret.position < self.focus.specialStartPosition:
                self.focus.caret.position = self.focus.specialStartPosition
                self.focus.caret.mark = self.focus.specialStartPosition + 1
                return
            self.focus.caret.on_text(text)
            self.focus.caret.position = max(self.focus.caret.position,\
                                            self.focus.specialStartPosition)

    def on_text_motion(self, motion):
        if self.focus:
            #print self.focus
            #if motion in self.focus.forbidden_motions:
            #    self.focus.replacement(motion)
            if motion == pyglet.window.key.MOTION_BACKSPACE and\
               self.focus.caret.position == self.focus.specialStartPosition:
                if self.focus.caret.mark is None:
                    return
            self.focus.caret.on_text_motion(motion)
            self.focus.caret.position = max(self.focus.caret.position,\
                                            self.focus.specialStartPosition)
      
    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)
            self.focus.caret.position = max(self.focus.caret.position,\
                                            self.focus.specialStartPosition)
