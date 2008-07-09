import sys
sys.path.insert(0, "../trunk")

import hfall.base
import hfall.OGLbase
import hfall.UI
import hfall.Render
import hfall.Vertex
from hfall.Console import Console
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe=100
        self._vertexes = []
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");
        self._vertexes.append(hfall.Vertex.Vertex([0, 1, 0], [1, 0, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([-1, -1, 1], [0, 1, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([1, -1, 1], [0, 0, 1]))

        self._vertexes.append(hfall.Vertex.Vertex([0, 1, 0], [1, 0, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([1, -1, 1], [0, 0, 1]))
        self._vertexes.append(hfall.Vertex.Vertex([1, -1, -1], [0, 1, 0]))

        self._vertexes.append(hfall.Vertex.Vertex([0, 1, 0], [1, 0, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([1, -1, -1], [0, 1, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([-1, -1, -1], [0, 0, 1]))

        self._vertexes.append(hfall.Vertex.Vertex([0, 1, 0], [1, 0, 0]))
        self._vertexes.append(hfall.Vertex.Vertex([-1, -1, -1], [0, 0, 1]))
        self._vertexes.append(hfall.Vertex.Vertex([-1, -1, 1], [0, 1, 0]))

        render.add3D(self._vertexes)

    def stop(self, kernel):
        pass

    def pause(self, kernel):
        pass

    def resume(self, kernel):
        pass

    def run(self, kernel):
        #self._maxframe-=1
        #print "Frame: ",self._maxframe
        if (self._maxframe<0):
            kernel.shutdown()

    def name(self):
        return "drawer"

render = hfall.Render.Render(800, 600)
hfk.insert(drawer())
hfk.insert(render)
hfk.insert(Console(render))
hfk.run()
