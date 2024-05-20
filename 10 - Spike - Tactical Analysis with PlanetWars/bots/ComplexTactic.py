''' Simple "Blank" PlanetWars controller bot.

The Bot does nothing, but shows the minimum a bot needs to have. 

See the `update` method which is where your code goes. 

The `PlanetWars` `Player` object (see players.py), will contain your bot 
controller instance. The Player will provide a current `GameInfo` instance 
to your bot `update` method each time it is called. 

The `gameinfo` instance is a facade of the state of the game for the `Player`, 
and includes all planets and fleets that currently exist. Note that the 
details are limited by "fog of war" vision and only match what you can see. If
you want to know more you'll need to scout!

A gameinfo instance has various (possibly useful) dict's for you to use:

	# all planet and fleets (that you own or can see)
	planets
	fleets

	# dict's of just your planets/fleets
	my_planets
	my_fleets

	# dict's of both neutral and enemy planets/fleets 
	not_my_planets
	not_my_fleets

	# dict's of just the enemy planet/fleets (fog limited)
	enemy_planets
	enemy_fleets

You issue orders from your bot using the methods of the gameinfo instance. 

	gameinfo.planet_order(src, dest, ships)
	gameinfo.fleet_order(src, dest, ships) 

For example, to send 10 ships from planet src to planet dest, you would
say `gameinfo.planet_order(src, dest, 10)`.

There is also a player specific log if you want to leave a message

	gameinfo.log("Here's a message from the bot")

'''

from entities import NEUTRAL_ID 

class ComplexTactic(object):
	def update(self, gameinfo):
		# check if we should attack
		if gameinfo._my_planets() and gameinfo._not_my_planets():
			# select largest source and smallest destination own planets
			dest = min(gameinfo._my_planets().values(), key=lambda p: p.ships)
			src = max(gameinfo._my_planets().values(), key=lambda p: p.ships)
			# check if dest planet has less than half src planets ships and lauches a quarter of src planets ships
			if src.ships * 0.5 > dest.ships:
				gameinfo.planet_order(src, dest, int(src.ships * 0.25) )
			else:
				# hitting lowest enemy planet if enemy planet has less than half src planets ships
				if any(planet.owner != NEUTRAL_ID for planet in gameinfo._not_my_planets().values()):# checking enemy planets exsist
					enemies = []
					for planet in gameinfo._not_my_planets().values():
						if planet.owner != NEUTRAL_ID:
							enemies.append(planet)
					if enemies: # checking enemies is not empty
						dest = min(enemies, key=lambda p: p.ships)
						if src.ships * 0.5 > dest.ships: # check has less that half sources ships
							gameinfo.planet_order(src, dest, int(src.ships * 0.75) )
						else:
							# grab neutral planet with lowest ships
							if any(planet.owner == NEUTRAL_ID for planet in gameinfo._not_my_planets().values()):# checking neutral planets exsist
								neutrals = []
								for planet in gameinfo._not_my_planets().values():
									if planet.owner == NEUTRAL_ID:
										neutrals.append(planet)
								if neutrals: # checking neutrals is not empty
									dest = min(neutrals, key=lambda p: p.ships)
									if src.ships * 0.9 > dest.ships:# checks dest has at most 90% of src planets ships then send 10% src
										gameinfo.planet_order(src, dest, int(src.ships * 0.1) )