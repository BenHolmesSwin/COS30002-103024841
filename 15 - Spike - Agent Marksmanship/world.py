'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from matrix33 import Matrix33
import pyglet
from graphics import COLOUR_NAMES, window
from agent import Agent, AGENT_MODES, CHANGE_MODES, AGENT_TYPES  # Agent with seek, arrive, flee and pursuit
from random import random, randrange, uniform
from HideClasses import Obstacle
from bullet import BULLET_MODES, BULLET_MODES_SET

class World(object):

	def __init__(self, cx, cy):
		self.cx = cx
		self.cy = cy
		self.target = Vector2D(cx / 2, cy / 2)
		self.hunter = None
		self.agents = []
		self.paused = True
		self.show_info = True
		self.target = pyglet.shapes.Star(
			30,30,#cx / 2, cy / 2, 
			30, 1, 4, 
			color=COLOUR_NAMES['RED'], 
			batch=window.get_batch("main")
		)
		self.change_mode = 'Speed'
		self.agent_type = 'Agent'
		self.circles = []
		
		self.circle_radius = 20
		#i = 0
		#margin = min(self.cx, self.cy) * (1/4)
		#while i < 5:
		#	pos = Vector2D(randrange(int(margin), int(self.cx - margin)), randrange(int(margin), int(self.cy - margin)))
		#	self.circles.append(
		#		Obstacle(
		#			pos,
		#			pyglet.shapes.Circle(
		#				pos.x,pos.y,
		#				self.circle_radius,
		#				color=COLOUR_NAMES['GREEN'], 
		#				batch=window.get_batch("main")
		#			)
		#		)
		#	)
		#	i += 1
		
		
		self.bullets = []
		self.bullet_mode = BULLET_MODES['rifle']
		self.hunter = Agent(self,mode='hold',color='PURPLE')
		self.hunter.pos = Vector2D(cx / 2, cy / 2)
		self.hunter.vel = Vector2D()

		self.patrol = []
		self.patrol.append(Vector2D(100,700))
		self.patrol.append(Vector2D(700,700))
		self.target_agent = Agent(self,mode='patrol',color='ORANGE')

	def update(self, delta):
		if not self.paused:
			self.hunter.update(delta)
			for agent in self.agents:
				agent.update(delta)
			self.target_agent.update(delta)
			active_bullets = [] # this is to replace list of current bullets after list is checked
			for bullet in self.bullets:
				bullet.update(delta)
				if bullet.check_hit():
					self.target_agent.been_hit = True
					self.target_agent.hit_timer = 0
				elif bullet.check_lifetime():
					active_bullets.append(bullet)
			self.bullets = active_bullets

	def wrap_around(self, pos):
		''' Treat world as a toroidal space. Updates parameter object pos '''
		max_x, max_y = self.cx, self.cy
		if pos.x > max_x:
			pos.x = pos.x - max_x
		elif pos.x < 0:
			pos.x = max_x - pos.x
		if pos.y > max_y:
			pos.y = pos.y - max_y
		elif pos.y < 0:
			pos.y = max_y - pos.y

	def transform_points(self, points, pos, forward, side, scale):
		''' Transform the given list of points, using the provided position,
			direction and scale, to object world space. '''
		# make a copy of original points (so we don't trash them)
		wld_pts = [pt.copy() for pt in points]
		# create a transformation matrix to perform the operations
		mat = Matrix33()
		# scale,
		mat.scale_update(scale.x, scale.y)
		# rotate
		mat.rotate_by_vectors_update(forward, side)
		# and translate
		mat.translate_update(pos.x, pos.y)
		# now transform all the points (vertices)
		mat.transform_vector2d_list(wld_pts)
		# done
		return wld_pts

	def input_mouse(self, x, y, button, modifiers):
		if button == 1:  # left
			self.target.x = x
			self.target.y = y
	
	def input_keyboard(self, symbol, modifiers):
		if symbol == pyglet.window.key.P:
			self.paused = not self.paused
		elif symbol in AGENT_MODES:
			if self.agent_type == 'Agent':
				for agent in self.agents:
					agent.mode = AGENT_MODES[symbol]
			else:
				self.hunter.mode = AGENT_MODES[symbol]
		elif symbol in BULLET_MODES_SET:
			self.bullet_mode = BULLET_MODES[BULLET_MODES_SET[symbol]]
		elif symbol in AGENT_TYPES:
			self.agent_type = AGENT_TYPES[symbol]
		elif symbol == pyglet.window.key.SPACE:
			self.agents.append(Agent(self))
		elif symbol == pyglet.window.key.R:
			for agent in self.agents:
				agent.randomise_path()
			self.hunter.randomise_path()
		elif symbol in CHANGE_MODES:
			self.change_mode = CHANGE_MODES[symbol]
		elif symbol == pyglet.window.key.UP:
			if self.agent_type == 'Agent':
				for agent in self.agents:
					if self.change_mode == 'Force':
						agent.change_max_force(100)
					if self.change_mode == 'Speed':
						agent.change_max_speed(100.0)
			else:
				if self.change_mode == 'Force':
					self.hunter.change_max_force(100)
				if self.change_mode == 'Speed':
					self.hunter.change_max_speed(100.0)		
		elif symbol == pyglet.window.key.DOWN:
			if self.agent_type == 'Agent':
				for agent in self.agents:
					if self.change_mode == 'Force':
						agent.change_max_force(-100)
					if self.change_mode == 'Speed':
						agent.change_max_speed(-100.0)
			else:
				if self.change_mode == 'Force':
					self.hunter.change_max_force(-100)
				if self.change_mode == 'Speed':
					self.hunter.change_max_speed(-100.0)
		elif symbol == pyglet.window.key.NUM_SUBTRACT:
			self.hunter.mode = 'shoot'	
	
	def transform_point(self, point, pos, forward, side):
		''' Transform the given single point, using the provided position,
		and direction (forward and side unit vectors), to object world space. '''
		# make a copy of the original point (so we don't trash it)
		world_pt = point.copy()
		# create a transformation matrix to perform the operations
		mat = Matrix33()
		# rotate
		mat.rotate_by_vectors_update(forward, side)
		# and translate
		mat.translate_update(pos.x, pos.y)
		# now transform the point (in place)
		mat.transform_vector2d(world_pt)
		# done
		return world_pt
