'''Tic-Tac-Toe

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Notes:
* Formatted with 4-space indentation
* This simple function based implementation does not use an OO design.
* Each function has a description string -- read to know more.
* Overall game flow follows a standard game loop trinity:
    - process_input() # from the current player (human/AI)
    - update_mode()   # check the players input, then update the game world
    - render_board()  # draw the current game board
* Global variable (oh no!) are used to store and share game related data.
* You need to be able to interact with this code when it runs. Either run
  from a terminal or make sure your tool allows you to enter input as the
  script runs.

If you want to create your own AI it is suggested that you:
* Copy the get_ai_move function and rename it.
* Write your own new fancy AI thinking code
* Update the "process_input" function to call your new "get_ai_move" code.

Want OO? There's another version of this code. Same functions, with nice
classes.

Updates:
2019-03-12: python 2 to 3 (mainly print() changes, and raw_input to input())

'''

from random import randrange

# static game data - doesn't change (hence immutable tuple data type)
WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
)

# global variables for game data
board = [' '] * 9
current_player = ''  # 'x' or 'o' for first and second player

players = {
    'x': 'Human',
    'o': 'Super AI',  # final comma is optional, but doesn't hurt
}

winner = None
move = None

# "horizontal rule", printed as a separator ...
HR = '-' * 40


#==============================================================================
# Game model functions

def check_move():
    '''This function will return True if ``move`` is valid (in the board range
    and free cell), or print an error message and return False if not valid.
    ``move`` is an int board position [0..8].
    '''
    global move
    try:
        move = int(move)
        if board[move] == ' ':
            return True
        else:
            print('>> Sorry - that position is already taken!')
            return False
    except:  # a "bare" except is bad practice, but simple and works still
        print('>> %s is not a valid position! Must be int between 0 and 8.' % move)
        return False


def check_for_result():
    '''Checks the current board to see if there is a winner, tie or not.
    Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
    simply False if the game is still going.
    '''
    for row in WIN_SET:
        if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
            return board[row[0]]  # return an 'x' or 'o' to indicate winner

    if ' ' not in board:
        return 'tie'

    return None


#==============================================================================
# agent (human or AI) functions


def get_human_move():
    '''Get a human players raw input. Returns None if a number is not entered.'''
    return input('[0-8] >> ')

def get_ai_move():
    '''Get the Ai's next move'''
    # old random method atm
    return randrange(9)

#==============================================================================
# Task 4 ai and board stuff

def get_ai_move_spike():
    board_move = ai_find_next_move_for_win()
    if board_move == None:
        return randrange(9)
    else:
        return board_move

def ai_find_next_move_for_win(root_board):
    i = 0
    while i < 9:
        if root_board[i] == ' ':
            root_board[i] = current_player
            for row in WIN_SET:
                if root_board[row[0]] == root_board[row[1]] == root_board[row[2]] != ' ':
                    return i
            i += 1
        else:
            i += 1
            continue
    return None

def generate_possible_path_stupid():
    # deliverable 2
    board_state = get_current_board_state()
    board_state_list = [board_state]
    win = False
    while win == False:
        move = False
        while move == False:
            try_move = randrange(9)
            move = board_state.do_move(try_move)
            if board_state.move_count == 9: # incase of draw
                move = True
                win = True
        board_state_list.append(board_state)
        for row in WIN_SET:
            if board_state.board[row[0]] == board_state.board[row[1]] == board_state.board[row[2]] != ' ':
                win = True
    return board_state_list

def get_current_board_state():
    #deliverable 1
    return Board_State(current_player,board,move)

class Board_State(object):
    '''A Board State'''
    #delivarable 1
    def __init__(self, current_player = 'x', board = [' ']*9, previous_move = 9):
        # move's default set at 9 is so that if it does somehow get set as the default, it wont affect anything as 9 is an invalid move
        self.current_player = current_player
        self.board = board
        self.move_count = 0
        self.previous_move = previous_move
        #cycling through current board to check how many moves have occured
        i = 0
        while i < 9:
            if self.board[i] != ' ':
                self.move_count += 1
            i += 1

    def do_move(self,move:int):
        if self.board[move] == ' ' & self.move_count < 9:
            self.board[move] = self.current_player
            self.move_count +=1
            self.previous_move = move
            if self.current_player == 'x':
                self.current_player = 'o'
            else:
                self.current_player = 'x'
            return True
        else:
            return False


            
#==============================================================================
# Standard trinity of game loop methods (functions)

def process_input():
    '''Get the current players next move.'''
    # save the next move into a global variable
    global move
    if current_player == 'x':
        move = get_human_move()
    else:
        move = get_ai_move()


def update_model():
    '''If the current players input is a valid move, update the board and check
    the game model for a winning player. If the game is still going, change the
    current player and continue. If the input was not valid, let the player
    have another go.
    '''
    global winner, current_player

    if check_move():
        # do the new move (which is stored in the global 'move' variable)
        board[move] = current_player
        # check board for winner (now that it's been updated)
        winner = check_for_result()
        # change the current player (regardless of the outcome)
        if current_player == 'x':
            current_player = 'o'
        else:
            current_player = 'x'
    else:
        print('Try again')


def render_board():
    '''Display the current game board to screen.'''

    print('    %s | %s | %s' % tuple(board[:3]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(board[3:6]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(board[6:]))

    # pretty print the current player name
    if winner is None:
        print('The current player is: %s' % players[current_player])


#==============================================================================


def show_human_help():
    '''Show the player help/instructions. '''
    tmp = '''
To make a move enter a number between 0 - 8 and press enter.
The number corresponds to a board position as illustrated:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    '''
    print(tmp)
    print(HR)


#==============================================================================
# Separate the running of the game using a __name__ test. Allows the use of this
# file as an imported module
#==============================================================================


if __name__ == '__main__':
    # Welcome ...
    print('Welcome to the amazing+awesome tic-tac-toe!')
    show_human_help()

    # by default the human player starts. This could be random or a choice.
    current_player = 'x'

    # show the initial board and the current player's move
    render_board()

    # Standard game loop structure
    while winner is None:
        process_input()
        update_model()
        render_board()

    # Some pretty messages for the result
    print(HR)
    if winner == 'tie':
        print('TIE!')
    elif winner in players:
        print('%s is the WINNER!!!' % players[winner])
    print(HR)
    print('Game over. Goodbye')
