import sys
sys.path.insert(0, "../trunk")

import hfall.base
import hfall.OGLbase
import hfall.UI
from hfall.Sprite import Sprite
import hfall.Render
from hfall.UI import UI
from hfall.Console import Console
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe=100
        #self._model=Sprite(-1,-1, 2, 2, None,color=(0.0,0.5,1.0));
        #self._model2=Sprite(1.3,-1,2, 2, None,color=(1,1,0.4));
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");
        #render.add2D(self._model)
        #render.add2D(self._model2)

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
hfk.insert(UI(render))
hfk.insert(drawer())
hfk.insert(render)
#hfk.insert(Console(render))
hfk.run()
