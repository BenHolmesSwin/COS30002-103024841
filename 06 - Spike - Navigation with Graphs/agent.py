from graphics import COLOUR_NAMES, window
import pyglet
from point2d import Point2D
from graph import SparseGraph, Node, Edge
from searches import SEARCHES

class agent(object):
    '''An agent for BoxWorld'''

    def __init__(self,start,target,box_types,max,x_boxes, y_boxes, boxes, agent_number, path_color,agent_color):
        self.start = start
        self.target = target
        self.box_types = box_types
        self.max = max
        self.x_boxes = x_boxes
        self.y_boxes = y_boxes
        self.boxes = boxes
        self.agent_number = agent_number
        self.path_color = path_color
        self.agent_color = agent_color
        self.x = 0
        self.y = 0

        self.search = 3
        self.limit = 0
        self.counter = 1
        self.move = 0

        self.path = None
        self.graph = None

        #lists used to store the primitives that render out our various pathfinding data
        self.render_path = []
        self.render_tree = []
        self.render_open_nodes = []
        self.render_graph = []
        self.render_agents = None

    def _add_edge(self, from_idx, to_idx, distance=1.0):
        b = self.boxes
        if "cost" in self.box_types[b[from_idx].type] and b[to_idx].type in self.box_types[b[from_idx].type]["cost"]:
            cost = self.box_types[b[from_idx].type]["cost"][b[to_idx].type]
            self.graph.add_edge(Edge(from_idx, to_idx, cost*distance))

    def reset_navgraph(self):
        ''' Create and store a new nav graph for this box world configuration.
        The graph is build by adding NavNode to the graph for each of the
        boxes in box world. Then edges are created (4-sided).
        '''
        self.path = None # invalid so remove if present
        self.graph = SparseGraph()
        self.graph.cost_h = self.max

        nx, ny = self.x_boxes, self.y_boxes
		# add all the nodes required
        for i, box in enumerate(self.boxes):
            box.pos = (i % nx, i // nx) #tuple position
            box.node = self.graph.add_node(Node(idx=i))
		# build all the edges required for this world
        for i, box in enumerate(self.boxes):
			# four sided N-S-E-W connections
            if "cost" not in self.box_types[box.type]:
                continue
			# UP (i + nx)
            if (i+nx) < len(self.boxes):
                self._add_edge(i, i+nx)
			# DOWN (i - nx)
            if (i-nx) >= 0:
                self._add_edge(i, i-nx)
			# RIGHT (i + 1)
            if (i%nx + 1) < nx:
                self._add_edge(i, i+1)
			# LEFT (i - 1)
            if (i%nx - 1) >= 0:
                self._add_edge(i, i-1)
			# Diagonal connections
			# UP LEFT(i + nx - 1)
            j = i + nx
            if (j-1) < len(self.boxes) and (j%nx - 1) >= 0:
                self._add_edge(i, j-1, 1.4142) # sqrt(1+1)
            # UP RIGHT (i + nx + 1)
            j = i + nx
            if (j+1) < len(self.boxes) and (j%nx + 1) < nx:
                self._add_edge(i, j+1, 1.4142)
            # DOWN LEFT(i - nx - 1)
            j = i - nx
            if (j-1) >= 0 and (j%nx - 1) >= 0:
                print(i, j, j%nx)
                self._add_edge(i, j-1, 1.4142)
            # DOWN RIGHT (i - nx + 1)
            j = i - nx
            if (j+1) >= 0 and (j%nx +1) < nx:
                self._add_edge(i, j+1, 1.4142)

    def plan_path(self):
        '''Conduct a nav-graph search from the current world start node to the
        current target node, using a search method that matches the string
        specified in `search`.
        '''
        cls = SEARCHES[self.search]
        self.path = cls(self.graph, self.start.index, self.target.index, self.limit)
        # print the path details
        print(self.path.report())
        #then add them to the renderer
        #render the final path
        for line in self.render_path:
            try:
                line.delete() #pyglets Line.delete method is slightly broken
            except:
                pass
        p = self.path.path # alias to save us some typing
        if(len(p) > 1):
            for idx in range(len(p)-1):
                self.render_path.append(
                    pyglet.shapes.Line(
                        self.boxes[p[idx]].center().x, 
                        self.boxes[p[idx]].center().y,
                        self.boxes[p[idx+1]].center().x,
                        self.boxes[p[idx+1]].center().y,
                        width=3, 
                        color=self.path_color,
                        batch=window.get_batch("path")
                    )
                )
        for line in self.render_tree:
            try:
                line.delete() #pyglets Line.delete method is slightly broken
            except:
                pass
        #render the search tree
        t = self.path.route # alias to save us some typing
        if(len(t) > 1):
            for start, end in t.items():
                self.render_tree.append(
                    pyglet.shapes.Line(
                        self.boxes[start].center().x, 
                        self.boxes[start].center().y,
                        self.boxes[end].center().x,
                        self.boxes[end].center().y,
                        width=2, 
                        color=COLOUR_NAMES['PINK'],
                        batch=window.get_batch("tree")
                    )
                )
        for circle in self.render_open_nodes:
            try:
                circle.delete() #pyglets Line.delete method is slightly broken
            except:
                pass
        #render the nodes that were still on the search stack when the search ended
        o = self.path.open # alias to save us some typing
        if(len(o) > 0):
            for idx in o:
                self.render_open_nodes.append(
                    pyglet.shapes.Circle(
                        self.boxes[idx].center().x, 
                        self.boxes[idx].center().y,
                        5, 
                        color=COLOUR_NAMES['ORANGE'],
                        batch=window.get_batch("tree")
                    )
                )

    def set_start(self, idx):
        '''Set the start box based on its index idx value. '''
        # remove any existing start node, set new start node
        if self.target == self.boxes[idx]:
            print("Can't have the same start and end boxes!")
            return
        self.start = self.boxes[idx]

    def set_target(self, idx):
        '''Set the target box based on its index idx value. '''
        # remove any existing target node, set new target node
        if self.start == self.boxes[idx]:
            print("Can't have the same start and end boxes!")
            return
        self.target = self.boxes[idx]
    
    def update(self):
        if self.path == None:
            return   
        if self.counter == 60:# the value of 60 means it travels across an entire move over 60 frames
            self.counter = 1
            self.move += 1
        if self.move == self.path.path.__len__() - 1:
            return
        move_start = self.boxes[self.path.path[self.move]]
        move_end = self.boxes[self.path.path[self.move + 1]]
        x_change = move_end.center().x - move_start.center().x
        y_change = move_end.center().y - move_start.center().y
        x = x_change * (self.counter/60) + move_start.center().x
        y = y_change * (self.counter/60) + move_start.center().y
        self.counter += 1
        self.render_agents = pyglet.shapes.Circle(
                        x, 
                        y,
                        5, 
                        color=self.agent_color,
                        batch=window.get_batch("agents")
                    )
        
    def reset(self):
        self.counter = 1
        self.move = 0

        

