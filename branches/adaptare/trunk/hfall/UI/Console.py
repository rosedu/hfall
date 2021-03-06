"""
Hammerfall Console and Command class. This class will be used to implement a 
real time debugging console. 
Version 0.8 has a working command logging system (in logs/console.log) and 4 
commands already implemented (quit, set, clear and help). 
"""

__version__ = '0.8'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

import pyglet

import base
import GUI
import Listener

CPH = 22

class Console(base.Task):
    """
    The Console will be implemented as another task to be inserted in the
    kernel's core.

    """
    def __init__(self, kernel, render, listener, activationKey):
        try:
            self.hFile = open("./logs/console.log", 'r')
        except IOError:
            self.hFile = None
        self.history = [""]
        self.readHistory()
        try:
            self.hFile = open("./logs/console.log", 'w')
        except IOError:
            self.hFile = None
        self.render = render
        self.window = self.render.w
        self.kernel = kernel
        self.listener = listener
        #self.listener.CAK = activationKey
        self.active = False
        self.counter = -1
        self.percent = 0.5
        self.text = "Hammerfall Graphics Engine \n"
        self.w = render.w.width
        self.h = int(render.w.height * self.percent)
        self.top = render.w.height
        self.batch = pyglet.graphics.Batch()
        self.consolePanel = GUI.HPanel(self.batch, 0, self.top - self.h,
                                       self.w, self.h)
        
        self.memo = self.consolePanel.add('Memo', 0, 0, self.w, self.h - CPH, 
                                        bcolor = (150, 150, 150, 225),
                                        text = "Welcome to Hammerfall engine!\n")
        self.tf = self.consolePanel.add('TextField', 0, self.h - CPH + 5, 
                                        self.w, CPH, text = '> ', startPos = 2,
                                        multiline = True)

        """
        A dictionary representing the Hammerfall commands. help, clear, quit
        and set are in by default. Use addCommand to add new Commands.
        """
        self.commands = {"help": Command("help", "<help command> for\
information about the command""", self.help),
                         "clear": Command("clear", "<clear> to clear the\
text on the Console.", self.clear), 
                         "quit": Command("quit", "<quit> to quit Hammerfall",\
                             self.quit),\
                         "set": Command("set", "<set parameter_name\
parameter_value> to set a parameter with a given value. This command is not\
implemented yet.", None)} #the function SHOULD BE ADDED LATER

        def consoleActivationChange(symbol, modifier):
            self.active = not self.active
            if self.active:
                self.listener.addWidget(self.tf)
                self.listener.addScrollableWidget(self.memo)
                self.listener.clearWidget(self.tf)
            else:
                self.listener.removeWidget(self.tf)
                self.listener.removeScrollableWidget(self.memo)
                self.listener.focus = None
            return pyglet.event.EVENT_HANDLED
        listener.staticBind(kernel, activationKey, consoleActivationChange)

        def consoleRender():
            if self.active:
                self.batch.draw()
        self.render.addOrthoRenderingFunction(kernel, consoleRender)

        def consoleGetMsg():
            #print "msg got", self.tf.document.text
            self.parseMessage()
            self.listener.clearWidget(self.tf)
        self.tf.addActionChar(pyglet.window.key.ENTER, consoleGetMsg)
        
        def consoleDeactivation():
            if self.active:
                self.counter = -1
                consoleActivationChange(None, None)
        self.tf.addActionChar(activationKey, consoleDeactivation)

        def browseHistory(symbol):
            if self.active:
                if symbol == pyglet.window.key.UP:
                    if self.counter is not (len(self.history)-1):
                        self.counter += 1 
                        self.tf.setText("> " + self.history[self.counter])
                elif symbol == pyglet.window.key.DOWN:
                    if self.counter > 0:                       
                        self.counter = self.counter - 1    
                        self.tf.setText("> " + self.history[self.counter])
                    else:
                        if self.counter is 0:
                            self.tf.setText("> ")
                            self.counter -= 1
        
        def browseHistoryUp():
            if self.active:
                browseHistory(pyglet.window.key.UP)
        self.tf.addActionChar(pyglet.window.key.UP, browseHistoryUp)

        def browseHistoryDown():
            if self.active:
                browseHistory(pyglet.window.key.DOWN)
        self.tf.addActionChar(pyglet.window.key.DOWN, browseHistoryDown)        
        
        @self.window.event
        def on_resize(width, height):
            """
            When the window is resized the console coordinates and dimension 
            are updated. This means updating the HPanel, HMemo and HTextField 
            components of the console.
            """
            self.w = self.window.width
            self.h = int(self.window.height * self.percent)
            self.top = self.window.height
            self.consolePanel.redraw(0, self.top - self.h, self.w, self.h)
            self.memo.redraw(0, self.top - self.h + CPH, self.w, self.h - CPH)
            self.tf.redraw(0, self.top - self.h - 5, self.w, CPH)

    def start(self, kernel):
        kernel.log.msg("Console up and listening to commands")

    def stop(self, kernel):
        self.writeHistory(10)
        kernel.log.msg("Console down")

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        pass

    def name(self):
        return "Console"
        
    def addLine(self, line):
        if line != None:
            self.memo.addLine(line)
    def getLine(self):
        line=self.memo.getText()
        return line
    def parseMessage(self):
        if self.tf.document.text:
            self.counter = -1
            text = self.tf.document.text[1:]
            text = text.lstrip()
            textTuple = text.partition(" ")
            command = textTuple[0]
            args = textTuple[2]
            commandFound = 0
            currentCommand = command + " " + args
            if self.history[0] != currentCommand:
                self.history[1:] = self.history[0:]
                self.history[0] = command + " " + args
            for commandNameIter in self.commands:
                if commandNameIter == command:
                    commandFound = 1
                    break
            if commandFound == 1:
                self.addLine("> " + command + " " + args)
                if args:
                    self.launchCommand(command, args)
                else:
                    self.launchCommand(command)
            else:
                self.addLine("> " + command + " " + args)
                self.help(command)
    
    def writeHistory(self,hSize):
        #log last n console commands
        self.history[0:]=self.history[:hSize]
        if self.hFile is not None:
            for message in self.history:
                self.hFile.write(message + '\n')

    def readHistory(self):
        if self.hFile is not None:
            self.history = self.hFile.readlines()
            self.hFile.close()
        for i in range(len(self.history)):
            self.history[i] = self.history[i][:-1]
        if (len(self.history) == 0):
            self.history = [""]

    def addCommand(self, commandName, commandHelp, commandFunction):
        self.commands[commandName] = Command(commandName, commandHelp, 
                                            commandFunction)
                                            
    def deleteCommand(self, commandName):
        del self.commands[commandName]
        
    def launchCommand(self, *parameters):
        """
        parameters[0] represents the actual command.
        """
        for commandNameIter in self.commands:
            if commandNameIter == parameters[0]:
                if self.commands[parameters[0]].function():
                    self.commands[parameters[0]].function()(*parameters)
            
        
    def help(self, *command):
        """
        Hammerfall default help command.
        Prints out the help for a given command. If no command is given then
        the help command help message is printed.
        """
        if len(command) == 1 and command[0] == "help":
            self.addLine(self.commands["help"].help())
            return True
        elif len(command) > 1:
            for commandNameIter in self.commands:
                if commandNameIter == command[1]:
                    self.addLine(self.commands[commandNameIter].help())
                    return True
        self.addLine("Command not found. Use help to find information about a \
specific command.\n" + self.commands["help"].help())
        return False
    
    def clear(self, *command):
        """
        Hammerfall default clear function.
        Clears the text on the screen.
        """
        self.memo.clearText()
        self.addLine("Welcome to Hammerfall engine!\n")
        
    def quit(self, *command):
        """
        Hammerfall default quit function.
        """
        print 'ESC-ing'
        self.kernel.log.msg('Application ending')
        self.kernel.shutdown()
        

class Command():

    def __init__(self, commandName, commandHelp, commandFunction):
        """
        The Command class implements the commands of the Hammerfal Console.
        """
        self._name = commandName
        self._help = commandHelp
        self._function = commandFunction
        
    def name(self):
        return self._name
        
    def help(self):
        return self._name + " command details:\n" + self._help
        
    def function(self):
        return self._function
        
