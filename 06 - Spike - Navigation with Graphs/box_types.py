box_types = {
	"GRASS":{"symbol":'.', "cost":{"GRASS":2, "MUD":5,"WATER":7,"HILL":4,"ROAD":2}, "colour":"WHITE"},
	"MUD":{"symbol":'m', "cost":{"GRASS":2, "MUD":7,"WATER":9,"HILL":4,"ROAD":3}, "colour":"BROWN"},
	"WATER":{"symbol":'~', "cost":{"GRASS":2, "MUD":9,"WATER":10,"HILL":4,"ROAD":4}, "colour":"AQUA"},
	"HILL":{"symbol":'-', "cost":{"GRASS":2, "MUD":6,"WATER":10,"HILL":4,"ROAD":3}, "colour":"DARK_GREEN"},
	"ROAD":{"symbol":'=', "cost":{"GRASS":2, "MUD":4,"WATER":10,"HILL":4,"ROAD":1}, "colour":"YELLOW"},
	"WALL":{"symbol":'X', "colour":"GREY"},
}

#the box_type values used by agent 1 (this one is better on hills)
box_types_agent1 = {
	"GRASS":{"symbol":'.', "cost":{"GRASS":2, "MUD":5,"WATER":7,"HILL":2,"ROAD":2}, "colour":"WHITE"},
	"MUD":{"symbol":'m', "cost":{"GRASS":2, "MUD":7,"WATER":9,"HILL":4,"ROAD":3}, "colour":"BROWN"},
	"WATER":{"symbol":'~', "cost":{"GRASS":2, "MUD":9,"WATER":10,"HILL":4,"ROAD":4}, "colour":"AQUA"},
	"HILL":{"symbol":'-', "cost":{"GRASS":2, "MUD":4,"WATER":10,"HILL":1,"ROAD":3}, "colour":"DARK_GREEN"},
	"ROAD":{"symbol":'=', "cost":{"GRASS":2, "MUD":4,"WATER":10,"HILL":1,"ROAD":1}, "colour":"YELLOW"},
	"WALL":{"symbol":'X', "colour":"GREY"},
}

#the box_type values used by agent 2 (this one passes through walls)
box_types_agent2 = {
	"GRASS":{"symbol":'.', "cost":{"GRASS":2, "MUD":5,"WATER":7,"HILL":4,"ROAD":2,"WALL":1}, "colour":"WHITE"},
	"MUD":{"symbol":'m', "cost":{"GRASS":2, "MUD":7,"WATER":9,"HILL":4,"ROAD":3,"WALL":1}, "colour":"BROWN"},
	"WATER":{"symbol":'~', "cost":{"GRASS":2, "MUD":9,"WATER":10,"HILL":4,"ROAD":4,"WALL":1}, "colour":"AQUA"},
	"HILL":{"symbol":'-', "cost":{"GRASS":2, "MUD":6,"WATER":10,"HILL":4,"ROAD":3,"WALL":1}, "colour":"DARK_GREEN"},
	"ROAD":{"symbol":'=', "cost":{"GRASS":2, "MUD":4,"WATER":10,"HILL":4,"ROAD":1,"WALL":1}, "colour":"YELLOW"},
	"WALL":{"symbol":'X', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1,"WALL":1}, "colour":"GREY"},
}

#the box_type values used by agent 3 (this one ignores terrain values but cant pass through walls)
box_types_agent3 = {
	"GRASS":{"symbol":'.', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1}, "colour":"WHITE"},
	"MUD":{"symbol":'m', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1}, "colour":"BROWN"},
	"WATER":{"symbol":'-', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1}, "colour":"AQUA"},
	"HILL":{"symbol":'=', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1}, "colour":"DARK_GREEN"},
	"ROAD":{"symbol":'~', "cost":{"GRASS":1, "MUD":1,"WATER":1,"HILL":1,"ROAD":1}, "colour":"YELLOW"},
	"WALL":{"symbol":'X', "colour":"GREY"},
}