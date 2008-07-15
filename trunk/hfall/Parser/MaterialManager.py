class MaterialManager:

    def __init__(self):
        self.materials = {}

    def add(self, material):
        self.materials[material.name] = material

    def get(self, name):
        if not self.materials[name]:
            return None
        return self.materials[name]

    def size(self):
        return len(self.materials)
        
