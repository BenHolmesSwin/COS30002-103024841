'''Goal Oriented Behaviour

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Works with Python 3+

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''

import copy

VERBOSE = True

# Global move depth you wish to path
move_depth = 3

# Global the amount of moves that the path actually generated ( incase it hits 0,0,0 before hitting depth 3)
move_amount = 3

# Global move counter to loop through path once paths are generated
move_counter = 0

# Global move number
move_number = 1

# Global path chosen
path_chosen = []

# Global goals with initial values
goals = {
    'Energy': 10,
    'Hunger': 10,
    'Fitness': 20,
}

# Global (read-only) actions and effects
actions = {
    'cook and eat food': {  'Energy': 2 ,'Hunger': -3 , 'Fitness': 0},
    'get snack': {  'Energy': 1 , 'Hunger': -2 , 'Fitness': 2 },
    'go to sleep': { 'Energy': -3 , 'Hunger': 1 , 'Fitness': 0 },
    'have a nap': { 'Energy': -1, 'Hunger': 0 , 'Fitness': 0  },
    'go for a walk': { 'Energy': 1, 'Hunger': 0 , 'Fitness': -2 },
    'go to the gym': { 'Energy': 2, 'Hunger': 1 , 'Fitness': -4 },
}

class Path(object):
    '''a single path for GOAP'''

    def __init__(self, moves, goals):
        self.moves = moves
        self.goals = goals

def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in actions[action].items():
        goals[goal] = max(goals[goal] + change, 0)


def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".

    For example::
        action_utility('get raw food', 'Eat')

    returns a number representing the effect that getting raw food has on our
    'Eat' goal. Larger (more positive) numbers mean the action is more
    beneficial.
    '''
    ### Simple version - the utility is the change to the specified goal

    if goal in actions[action]:
        # Is the goal affected by the specified action?
        return -actions[action][goal]
    else:
        # It isn't, so utility is zero.
        return 0

def choose_action():
    '''Return the best action to respond to the current most insistent goal.
    '''
    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'

    # Find the most insistent goal - the 'Pythonic' way...
    best_goal, best_goal_value = max(goals.items(), key=lambda item: item[1])

    # ...or the non-Pythonic way. (This code is identical to the line above.)
    #best_goal = None
    #for key, value in goals.items():
    #    if best_goal is None or value > goals[best_goal]:
    #        best_goal = key

    if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])

    # Find the best (highest utility) action to take.
    # (Not the Pythonic way... but you can change it if you like / want to learn)
    best_action = None
    best_utility = None
    for key, value in actions.items():
        # Note, at this point:
        #  - "key" is the action as a string,
        #  - "value" is a dict of goal changes (see line 35)

        # Does this action change the "best goal" we need to change?
        if best_goal in value:

            # Do we currently have a "best action" to try? If not, use this one
            if best_action is None:
                best_action = key
                best_utility = action_utility(best_action,best_goal)

            # Is this new action better than the current action?
            else:
                utility = action_utility(key,best_goal)
                if(utility > best_utility):
                    best_action = key
                    best_utility = utility

    # Return the "best action"
    return best_action

def choose_action_path():
    '''chose an action path and return current action on that path'''

    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'
    global move_counter
    global path_chosen

    if move_counter == 0:
        paths = action_paths(goals,move_depth,0,[])
        path_number = 0
        goals_check = paths[0].goals.copy()
        i = 0
        for path in paths:
            if path_check(goals_check,path):
                path_number = i
                goals_check = path.goals.copy()
            i += 1

        path_chosen = paths[path_number]
        
    print('PATH MOVES:',path_chosen.moves)
    print('PATH GOALS:',path_chosen.goals)
    move_amount = len(path_chosen.moves) - 1

    apply_action(path_chosen.moves[move_counter])
    if move_counter == move_amount:
        move_counter = 0
    else:
        move_counter += 1

    pass

def path_check(goal_check,path):
    if (goal_check.get('Energy') >= path.goals.get('Energy') and goal_check.get('Hunger') >= path.goals.get('Hunger') and goal_check.get('Fitness') >= path.goals.get('Fitness')):
        return True
    else:
        return False

def action_paths(path_goals, max_move, counter, path_moves):
    counter += 1
    result_paths = []
    for key, value in actions.items():
        path_goals_temp = path_goals.copy()
        path_moves_temp = path_moves[:]
        path_moves_temp.append(key)
        path_apply_action(key,path_goals_temp)
        if counter < max_move and any(value != 0 for goal, value in path_goals_temp.items()):
            temp_paths = action_paths(path_goals_temp,max_move,counter,path_moves_temp)
            for path in temp_paths:
                result_paths.append(path)
        else:
            path = Path(path_moves_temp,path_goals_temp)
            result_paths.append(path)
        
    return result_paths         
            

def path_apply_action(action,path_goals):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in actions[action].items():
        path_goals[goal] = max(path_goals[goal] + change, 0)

#==============================================================================

def print_actions():
    print('ACTIONS:')
    # for name, effects in list(actions.items()):
    #     print(" * [%s]: %s" % (name, str(effects)))
    for name, effects in actions.items():
        print(" * [%s]: %s" % (name, str(effects)))


def run_until_all_goals_zero():
    global move_number
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    while running:
        print('MOVE NUMBER:', move_number)
        print('GOALS:', goals)
        # What is the best action
        action = choose_action_path()
        print('PATH MOVE NUMBER:', move_counter + 1)
        print('BEST ACTION:', action)
        # Apply the best action
        #apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in goals.items()):
            running = False
        print(HR)
        move_number += 1
    # finished
    print('>> Done! <<')


if __name__ == '__main__':
    # print(actions)
    # print(actions.items())
    # for k, v in actions.items():
    #     print(k,v)
    # print_actions()

    run_until_all_goals_zero()
