import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import COLOUR_NAMES, window, ArrowLine
from math import sin, cos, radians
from random import random, randrange, uniform

BULLET_SPEEDS = {
        'slow': 200,
        'fast': 400,
    }

BULLET_MODES = {
        'rifle': 1,
        'rocket': 2,
        'pistol': 3,
        'grenade':4,
    }

BULLET_MODES_SET = {
        pyglet.window.key.NUM_1: 'rifle',
        pyglet.window.key.NUM_2: 'rocket',
        pyglet.window.key.NUM_3: 'pistol',
        pyglet.window.key.NUM_4: 'grenade',
    }

class Bullet(object):

    def __init__(self, world, source_pos, target_pos, mode=1):
        self.world = world
        self.target = target_pos
        self.pos = source_pos
        self.inaccuracy = False
        self.color = 'RED'
        self.speed = BULLET_SPEEDS['fast']
        self.mode = BULLET_MODES['rifle']
        if mode == 2:
            self.mode = BULLET_MODES['rocket']
            self.inaccuracy = True
        elif mode == 3:
            self.speed = BULLET_SPEEDS['slow']
            self.mode = BULLET_MODES['pistol']
        elif mode == 4:
            self.speed = BULLET_SPEEDS['slow']
            self.mode = BULLET_MODES['grenade']
            self.inaccuracy = True
        
        self.vel = (target_pos - self.pos).normalise() * self.speed
        self.heading = self.vel.get_normalised()

        if self.inaccuracy:
            inaccuracy_amount = randrange(1,10)/100 # makes the inacuracy be between 1% and 10% of the perp of current vel
            inaccuracy_sign = 1 # makes inaccuracy either positive or negative randomly
            if randrange(1,10) > 5:
                inaccuracy_sign = -1
            self.vel = self.vel + self.vel.perp() * inaccuracy_amount * inaccuracy_sign

        self.predicted = pyglet.shapes.Star(
			self.target.x,self.target.y,
			30, 1, 4, 
			color=COLOUR_NAMES['GREEN'], 
			batch=window.get_batch("main")
		)
        self.vehicle_shape = [
			Point2D( 0,  6),
			Point2D( 10,  0),
			Point2D( 0, -6)
		]

        self.vehicle = pyglet.shapes.Triangle(
			self.pos.x+self.vehicle_shape[1].x, self.pos.y+self.vehicle_shape[1].y,
			self.pos.x+self.vehicle_shape[0].x, self.pos.y+self.vehicle_shape[0].y,
			self.pos.x+self.vehicle_shape[2].x, self.pos.y+self.vehicle_shape[2].y,
			color= COLOUR_NAMES[self.color],
			batch=window.get_batch("main")
		)

        self.lifetime = 0
        self.max_lifetime = (200/self.speed)* 200

    def update(self,delta):
        self.pos += self.vel * delta
        self.world.wrap_around(self.pos)
        self.vehicle.x = self.pos.x+self.vehicle_shape[0].x
        self.vehicle.y = self.pos.y+self.vehicle_shape[0].y
        self.vehicle.rotation = -self.heading.angle_degrees()
        self.lifetime += 1

    def check_hit(self):
        '''checks if it has hit the target could be changed to provide a specific target to check against rather than the single targe_agent'''
        if self.pos.distance(self.world.target_agent.pos) < 10:
            return True
        return False

    def check_lifetime(self):
        '''checks if the lifetime is up and returns false if so, else returns true'''
        if self.lifetime >= self.max_lifetime:
            return False
        return True
