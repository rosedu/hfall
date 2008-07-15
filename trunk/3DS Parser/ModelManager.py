#from ModelLoader import ModelLoader

class ModelManager:

    def __init__(self):
        self.models = {}
    """
    def loadModel(self, name):
        loader = ModelLoader(self, materialManager, textureManger)
        return loader.loadModel(name)
    """
    def add(self, model):
        self.models[model.name] = model
        
    def size(self):
        return len(self.models)
