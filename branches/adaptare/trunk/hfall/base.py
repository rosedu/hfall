"""
Hamerfall engine core classes

This classes should handle the main loop creation. The core component in
the Hfall engine is the Kernel. The Kernel maintains a list of tasks.
The main loop will keep running while the task list is not empty. At any
given point in time a task can interact with the task list in the kernel

"""

__version__ = '0.2'
__author__ = 'Savu Andrei (savu.andrei@gmail.com)'

import time
import sys
"""import pygame"""

class Task:
    'Basic Task class - no functionality - just the interface'

    def start(self, kernel):
        """
        Task initialization. This function is called when the task is
        added in the kernel task list. This should initialize all the
        subsystems needed for this task.

        """
        pass

    def stop(self, kernel):
        """
        Task destructor. This function is called when the task is
        removed from the kernel task list. This should cleanup all the
        resources used by this task.

        """
        pass

    def pause(self, kernel):
        """
        Pause the current task. The function is called by another task
        inside the kernel task list.

        """
        pass

    def resume(self, kernel):
        """
        Resume the current task operation. The function is called by
        another task from the task list.

        """
        pass

    def run(self, kernel):
        """
        Main task function. This is what the task does. This function
        will be called on each cycle by the kernel as fast as possible.
        The task should do the job and exit as quick as possible.

        """
        pass

    def name(self):
        """
        Get the task name. The name should be unique. The kernel will
        allow in the list only one task for a name. This will keep
        things simple.

        """
        return None


class Log:
    """
    Very basic file logging class. Log major events and errors in very
    simple text files with a predefined log format.

    """

    def __init__(self, sys_log='logs/system.log', error_log='logs/error.log'):
        """Log system initialization"""
        try:
            self.sys = open(sys_log, 'a+')
            self.err = open(error_log, 'a+')
        except IOError:
            self.sys, self.err = None, None

    def msg(self, message):
        """Write a normal log event"""
        if self.sys is not None:
            self.sys.write('[' + time.ctime() + '] ' + message + "\n")

    def error(self, message):
        """Write an error log event"""
        if self.err is not None:
            self.err.write('[' + time.ctime() + '] ' + message + "\n")


class Kernel:
    """
    Engine Kernel class

    The main application loop. A simple task list with some management
    functions. The task order is important.

    """

    def __init__(self):
        'Kernel task list initialization'
        self._task_list = []
        self._task_map = {}
        self.log = Log()
        self.log.msg('Kernel instance created')

    def insert(self, task):
        """
        Insert a new task at the end of the task list. A task is a Task
        class instance.

        """
        if task.name() in self._task_map: return False

        # Add the task in the list
        self._task_map[task.name()] = task
        self._task_list.append(task)
        self.log.msg('Task `' + task.name() + '` added to the end of the task'\
                      + 'list')
        
        task.start(self)
        return True

    def insert_first(self, task):
        """
        Insert a new task at the beginning of the task list. A task is a
        Task class instance.

        """
        if task.name() in self._task_map: return False

        # Add the task in the list
        self._task_map[task.name()] = task
        self._task_list.insert(0, task)
        self.log.msg('Task `' + task.name() + '` added to the beginning of the'\
                      + 'task list')

        task.start(self)
        return True

    def insert_after(self, name, task):
        """
        Insert a new task after the task with the given name.
            name    Task name
            task    Task class instance - the new task

        """
        if name not in self._task_map: return False
        if task.name() in self._task_map: return False

        # Add the task in the list
        id = [x.name() for x in self._task_list].index(name)
        self._task_list.insert(id+1, task)
        self._task_map[task.name()] = task
        self.log.msg('Task `' + task.name() + '` added after the task `' + \
                     name + '`')

        task.start(self)
        return True

    def insert_before(self, name, task):
        """
        Insert a new task before the task with the given name.
            name    Task name
            task    Task class instance - the new task

        """
        if name not in self._task_map: return False
        if task.name() in self._task_map: return False

        # Add the task in the list
        id = [x.name() for x in self._task_list].index(name)
        self._task_list.insert(id, task)
        self._task_map[task.name()] = task
        self.log.msg('Task `' + task.name() + '` added before task `' + name +\
                     '`')

        task.start(self)
        return True

    def remove(self, name):
        """
        Remove a task from the list.
            name    The name of the task

        """
        if name not in self._task_map: return True

        id = [x.name() for x in self._task_list].index(name)
        self._task_list[id].stop(self)
        self.log.msg('Removed task`' + name +'`')
        del self._task_list[id]
        del self._task_map[name]
        return True

    def shutdown(self):
        """
        Stop all the task and empty the task list.

        """
        for x in self._task_list: x.stop(self)
        self._task_list = []
        self._task_map = {}
        self.log.msg('Kernel shutdown\n')
        sys.exit()

    def run(self):
        """
        Main application loop. Run the tasks while the list is not empty.

        """
        while True:
            for task in self._task_list[:]:
                if task.name() in self._task_map:
                    task.run(self)
                if not len(self._task_list):
                    break


#
# Kernel singleton
#
kernel = Kernel()
