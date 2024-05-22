import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import COLOUR_NAMES, window, ArrowLine

class Obstacle(object):
    '''A Green Circlular obstacle for the world'''

    def __init__(self,pos,circle):
        self.pos = pos
        self.circle = circle

class HidePoint(object):
    '''A Green Circlular obstacle for the world'''

    def __init__(self,pos,circle):
        self.pos = pos
        self.circle = circle