'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by 
	Clinton Woodward <cwoodward@swin.edu.au>
	James Bonner <jbonner@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''
import pyglet
from vector2d import Vector2D
from vector2d import Point2D
from graphics import COLOUR_NAMES, window, ArrowLine
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from HideClasses import HidePoint
from bullet import Bullet, BULLET_SPEEDS

CHANGE_MODES = {
	pyglet.window.key.S: 'Speed',
	pyglet.window.key.F: 'Force',
}

AGENT_TYPES = {
	pyglet.window.key.H: 'Hunter',
	pyglet.window.key.A: 'Agent'
}

AGENT_MODES = {
	pyglet.window.key._1: 'seek',
	pyglet.window.key._2: 'arrive_slow',
	pyglet.window.key._3: 'arrive_normal',
	pyglet.window.key._4: 'arrive_fast',
	pyglet.window.key._5: 'flee',
	pyglet.window.key._6: 'pursuit',
	pyglet.window.key._7: 'follow_path',
	pyglet.window.key._8: 'wander',
	pyglet.window.key._9: 'hide',
	pyglet.window.key._0: 'patrol',
	# dont press, here to be part of the list, button functionality not implemented
	pyglet.window.key.NUM_0: 'hold', 
	pyglet.window.key.NUM_ENTER: 'shoot',
}

class Agent(object):

	# NOTE: Class Object (not *instance*) variables!
	DECELERATION_SPEEDS = {
		'slow': 0.9,
		'normal': 0.5,
        'fast': 0.1,
	}

	def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek', color = 'ORANGE'):
		# keep a reference to the world object
		self.world = world
		self.mode = mode
		# where am i and where am i going? random start pos
		dir = radians(random()*360)
		self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
		self.vel = Vector2D()
		self.heading = Vector2D(sin(dir), cos(dir))
		self.side = self.heading.perp()
		self.scale = Vector2D(scale, scale)  # easy scaling of agent size
		self.force = Vector2D()  # current steering force
		self.accel = Vector2D() # current acceleration due to force
		self.mass = mass

		# data for drawing this agent
		self.color = color
		self.vehicle_shape = [
			Point2D(-10,  6),
			Point2D( 10,  0),
			Point2D(-10, -6)
		]
		self.vehicle = pyglet.shapes.Triangle(
			self.pos.x+self.vehicle_shape[1].x, self.pos.y+self.vehicle_shape[1].y,
			self.pos.x+self.vehicle_shape[0].x, self.pos.y+self.vehicle_shape[0].y,
			self.pos.x+self.vehicle_shape[2].x, self.pos.y+self.vehicle_shape[2].y,
			color= COLOUR_NAMES[self.color],
			batch=window.get_batch("main")
		)

		# wander info render objects
		self.info_wander_circle = pyglet.shapes.Circle(0, 0, 0, color=COLOUR_NAMES['WHITE'], batch=window.get_batch("info"))
		self.info_wander_target = pyglet.shapes.Circle(0, 0, 0, color=COLOUR_NAMES['GREEN'], batch=window.get_batch("info"))
		# add some handy debug drawing info lines - force and velocity
		self.info_force_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['BLUE'], batch=window.get_batch("info"))
		self.info_vel_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['AQUA'], batch=window.get_batch("info"))
		self.info_net_vectors = [
			ArrowLine(
				Vector2D(0,0), 
				Vector2D(0,0), 
				colour=COLOUR_NAMES['GREY'], 
				batch=window.get_batch("info")
			),
			ArrowLine(
				Vector2D(0,0), 
				Vector2D(0,0), 
				colour=COLOUR_NAMES['GREY'], 
				batch=window.get_batch("info")
			),
		]

		### path to follow?
		self.path = Path()
		self.randomise_path()
		self.waypoint_threshold = 70.0

		### wander details
		self.wander_target = Vector2D(1, 0)
		self.wander_dist = 1.0 * scale
		self.wander_radius = 1.0 * scale
		self.wander_jitter = 10.0 * scale
		self.bRadius = scale

		# limits?
		self.max_speed = 5.0 * scale
		self.max_force = 1000

		# debug draw info?
		self.show_info = False

		# hide 
		self.hide_points = []

		#shoot
		self.been_hit = False
		self.hit_timer = 0
		self.hit_lifetime = 60

		#patrol
		self.patrol_couter = 0

	def calculate(self,delta):
		# calculate the current steering force
		mode = self.mode
		target_pos = Vector2D(self.world.target.x, self.world.target.y)
		if mode == 'seek':
			force = self.seek(target_pos)
		elif mode == 'arrive_slow':
			force = self.arrive(target_pos, 'slow')
		elif mode == 'arrive_normal':
			force = self.arrive(target_pos, 'normal')
		elif mode == 'arrive_fast':
			force = self.arrive(target_pos, 'fast')
		elif mode == 'flee':
			force = self.flee(target_pos)
		elif mode == 'pursuit':
			force = self.pursuit(self.world.hunter)
		elif mode == 'wander':
			force = self.wander(delta)
		elif mode == 'follow_path':
			force = self.follow_path()
		elif mode == 'hide':
			force = self.hide(self.world.hunter)
		elif mode == 'patrol':
			force = self.patrol()
		elif mode == 'hold':
			force = Vector2D()
		elif mode == 'shoot':
			force = self.shoot(self.world.target_agent,self.world.bullet_mode)
		else:
			force = Vector2D()
		self.force = force
		return force

	def update(self, delta):
		''' update vehicle position and orientation '''
		# calculate and set self.force to be applied
		## force = self.calculate()
		force = self.calculate(delta)  # <-- delta needed for wander
		force.truncate(self.max_force)
		# determin the new acceleration
		self.accel = force / self.mass  # not needed if mass = 1.0
		# new velocity
		self.vel += self.accel * delta
		# check for limits of new velocity
		self.vel.truncate(self.max_speed)
		# update position
		self.pos += self.vel * delta
		# update heading is non-zero velocity (moving)
		if self.vel.lengthSq() > 0.00000001:
			self.heading = self.vel.get_normalised()
			self.side = self.heading.perp()
		# treat world as continuous space - wrap new position if needed
		self.world.wrap_around(self.pos)
		# update the vehicle render position
		self.vehicle.x = self.pos.x+self.vehicle_shape[0].x
		self.vehicle.y = self.pos.y+self.vehicle_shape[0].y
		self.vehicle.rotation = -self.heading.angle_degrees()

		s = 0.5 # <-- scaling factor
		# force
		self.info_force_vector.position = self.pos
		self.info_force_vector.end_pos = self.pos + self.force * s
		# velocity
		self.info_vel_vector.position = self.pos
		self.info_vel_vector.end_pos = self.pos + self.vel * s
		# net (desired) change
		self.info_net_vectors[0].position = self.pos+self.vel * s
		self.info_net_vectors[0].end_pos = self.pos + (self.force+self.vel) * s
		self.info_net_vectors[1].position = self.pos
		self.info_net_vectors[1].end_pos = self.pos + (self.force+self.vel) * s
		if self.been_hit:
			self.hit()

	def speed(self):
		return self.vel.length()

	#--------------------------------------------------------------------------

	def seek(self, target_pos):
		''' move towards target position '''
		desired_vel = (target_pos - self.pos).normalise() * self.max_speed
		return (desired_vel - self.vel)

	def flee(self, hunter_pos):
		''' move away from hunter position '''
		if self.pos.distance(hunter_pos) < 500:
			desired_vel = (hunter_pos - self.pos).normalise() * self.max_speed
			return (desired_vel - self.vel).get_reverse()
		return Vector2D()

	def arrive(self, target_pos, speed):
		''' this behaviour is similar to seek() but it attempts to arrive at
			the target position with a zero velocity'''
		decel_rate = self.DECELERATION_SPEEDS[speed]
		to_target = target_pos - self.pos
		dist = to_target.length()
		if dist > 0:
			# calculate the speed required to reach the target given the
			# desired deceleration rate
			speed = dist / decel_rate
			# make sure the velocity does not exceed the max
			speed = min(speed, self.max_speed)
			# from here proceed just like Seek except we don't need to
			# normalize the to_target vector because we have already gone to the
			# trouble of calculating its length for dist.
			desired_vel = to_target * (speed / dist)
			return (desired_vel - self.vel)
		return Vector2D(0, 0)

	def pursuit(self, evader):
		''' this behaviour predicts where an agent will be in time T and seeks
			towards that point to intercept it. '''
		## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
		return Vector2D()

	def wander(self, delta):
		''' Random wandering using a projected jitter circle. '''
		wander_target = self.wander_target
		# this behaviour is dependent on the update rate, so this line must
		# be included when using time independent framerate.
		jitter = self.wander_jitter * delta # this time slice
		# first, add a small random vector to the target's position
		wander_target += Vector2D(uniform(-1,1) * jitter, uniform(-1,1) * jitter)
		# re-project this new vector back on to a unit circle
		wander_target.normalise()
		# increase the length of the vector to the same as the radius
		# of the wander circle
		wander_target *= self.wander_radius
		# move the target into a position wander_dist in front of the agent
		wander_dist_vector = Vector2D(self.wander_dist, 0) #also used for rendering
		target = wander_target + Vector2D(self.wander_dist, 0)
		# set the position of the Agent’s debug circle to match the vectors we’ve created
		circle_pos = self.world.transform_point(wander_dist_vector, self.pos, self.heading, self.side,)
		self.info_wander_circle.x = circle_pos.x
		self.info_wander_circle.y = circle_pos.y
		self.info_wander_circle.radius = self.wander_radius
		# project the target into world space
		world_target = self.world.transform_point(target, self.pos, self.heading, self.side)
		#set the target debug circle position
		self.info_wander_target.x = world_target.x
		self.info_wander_target.y = world_target.y
		# and steer towards it
		return self.seek(world_target)
	
	def randomise_path(self):
		cx = self.world.cx
		cy = self.world.cy
		margin = min(cx, cy) * (1/6)
		self.path.create_random_path( 5, margin, margin, cx - margin, cy - margin)

	def follow_path(self):
		if self.path.is_finished():
			return self.arrive(self.path.current_pt(),'fast')
		else:
			if self.pos.distance(self.path.current_pt()) < self.waypoint_threshold:
				self.path.inc_current_pt()
			return self.seek(self.path.current_pt())
	
	def change_max_force(self,change):
		self.max_force += change
	
	def change_max_force(self,change):
		self.max_force += change

	def change_max_speed(self,change):
		self.max_speed += change

	def hide(self, hunter_pos):
		distance = 1000
		id = 0
		counter = 0
		self.hide_points = []
		for circle in self.world.circles:
			hide_pos = ((hunter_pos.pos - circle.pos).normalise() * self.max_speed).get_reverse()
			pos = hide_pos.copy()
			pos.truncate(self.world.circle_radius* 2)
			pos.__iadd__(circle.pos)
			self.hide_points.append(
				HidePoint(
					pos,
					pyglet.shapes.Star(
						pos.x,pos.y,
						20, 1, 8, 
						color=COLOUR_NAMES['BLUE'], 
						batch=window.get_batch("main")
					)
				)
			)
			if self.pos.distance(pos) < distance:
				id = counter
				distance = self.pos.distance(pos)
			counter += 1
			
		hide_point = self.hide_points[id].pos
		self.hide_points[id].circle.color = COLOUR_NAMES['PINK']
		return self.arrive(hide_point,'fast')
	
	def shoot(self,target,bullet_mode):
		to_target = self.pos.distance(target.pos)
		bullet_speed = BULLET_SPEEDS['fast']
		if bullet_mode == 3 or bullet_mode == 4:
			bullet_speed = BULLET_SPEEDS['slow']
		look_ahead_time = to_target/(bullet_speed + target.speed())
		predicted_pos = target.pos + target.vel * look_ahead_time
		bullet_start_pos = self.pos.copy()
		self.world.bullets.append(Bullet(self.world,bullet_start_pos,predicted_pos,bullet_mode))
		self.mode = 'hold'
		return Vector2D()

	def patrol(self):
		target = self.world.patrol[self.patrol_couter]
		target_vel = self.seek(target)
		if self.pos.distance(target) < 10:
			self.patrol_couter += 1
			if self.patrol_couter >= len(self.world.patrol):
				self.patrol_couter = 0
		return target_vel
	
	def hit(self):
		self.vehicle.color = COLOUR_NAMES['BLUE']
		self.hit_timer +=1
		if self.hit_timer > self.hit_lifetime:
			self.been_hit = False
			self.vehicle.color = COLOUR_NAMES['ORANGE']
			self.hit_timer = 0