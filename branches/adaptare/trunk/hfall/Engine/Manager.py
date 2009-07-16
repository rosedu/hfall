"""
Hammerfall Resource Manager class. 
Note: The classes in this file are NOT tested yet.
"""

__version__ = '0.1'
__authors__ = 'Dragos Dena (dragos.dena@gmail.com)'

import pyglet

import base
import Listener

class Manager(base.Task):
    
    def __init__(self, kernel, listener):
        """
        resourceList - a dictionary. resource name => resource object
        """
        print 1/0
        self.kernel = kernel
        self.listener = listener
        self.resourceList = {}
        
    def addInstance(self, resourceFileName):
        """
        Adding an instance requires the file name from which the instance gets\
        it's resources.
        """
        if resourceFileName in self.resourceList:
            resource = self.resourceList[resourceFileName]
            instance = Instance(resource)
            resource.incrementAppearences()
        else:
            resource = Resource(resourceFileName, self)
            self.resourceList[resourceFileName] = resource
            instance = Instance(resource)
        return instance
            
    def deleteInstance(self, instance):
        """
        Delets an instance object.
        If the resource used by the instance isn't used by any other instance\
        then the resource object is also deleted by the instance destructor.
        """
        resource = instance.getResource()
        del instance
            
    def deleteResource(self, resource):
        """
        Delets a resource object.
        Gets the filename for the resource. Looks up in the Resource List the\
        current resource. Deletes it from the Resource it and finnaly it\
        deletes the object.
        """
        resourceName = resource.resourceFileName()
        del self.resourceList[resourceName]
        del resource
        
        
class Resource():
    
    def __init__(self, filename, manager):
        self.filename = filename
        self.count = 1
        self.manager = manager
    
    def __del__(self):
        """
        Depends on the type of resource.
        """
        pass
    
    def resourceFileName(self):
        return self.filename
        
    def incrementAppearences(self):
        self.count = self.count + 1
        
    def decrementAppearences(self):
        self.count = self.count - 1
        
    def loadResource(self):
        """
        Depends on the type of resource.
        """
        pass
        
        
class Instance():
    
    def __init__(self, resource):
        self.resource = resource
        self.manager = self.resource.manager
        
    def __del__(self):
        """
        Specific deletion operations for instances should be inherented.
        """
        self.resource.decrementAppearences()
        if self.resource.count == 0:
            self.manager.deleteResource(self.resource)
    
    def getResource(self):
        return self.resource
