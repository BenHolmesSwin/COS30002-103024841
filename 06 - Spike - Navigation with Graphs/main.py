'''  BoxWorldWindow to test/demo graph (path) search.

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>, James Bonner <jbonner@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

See readme.txt for details.

'''

import sys
from pyglet import app
from pyglet import clock
#importing graphics for side-effects - it creates the egi and window module objects. 
#This is the closest python has to a global variable and it's completely gross
import graphics
#game has to take another approach to exporting a global variable
#the game object is importable, but only contains the game object if it's being imported after the game object has been created below
import game

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "map.txt"

	game.game = game.Game(filename)
	#clock.schedule_interval(graphics.window.on_update(), 1/60)
	app.run()