"""
Hammerfall user interface module. Usefull for rendering menus, buttons,
panels and status windows.

"""

__version__ = '0.2'
__author__ = 'Mihai Maruseac (mihai.maruseac@gmail.com)'

class Model2D:
    """
    A basic class for any 2D object.

    """
    
    def __init__(self,  x, y, w=32.0, h=32.0, color=(0.0, 0.0, 0.0, 0.0)):
        """
        Model2D class initialization.
            x - the x position of the 2D rendered element
            y - the y position of the 2D rendered element
            w - the width of the 2D rendered element
            h - the height of the 2D rendered element
            color - the color of the rendered element. It is possible to
                    use alpha blending.

        """
        self.x = x
        self.y = y
        self.xx = x + w
        self.yy = y + h
        self.color = color
        
