import hfall.base
import hfall.OGLbase
import hfall.UI
import hfall.Render
from hfall.base import kernel as hfk

class drawer(hfall.base.Task):
    """
    Desenez cateva chenare si apoi ies
    
    """
    def __init__(self):
        self._maxframe=100
        self._model=hfall.UI.Model2D(-1,-1, 2,2, color=(0.0,0.5,1.0));
        pass

    def start(self, kernel):
        kernel.log.msg("Drawer started");
        render.add2D(self._model)

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
hfk.run()
