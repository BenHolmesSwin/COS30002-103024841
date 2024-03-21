'''Tic-Tac-Toe AI

This is the Tic-Tac_Toe Ai file, it has the two seperate AI's that i created stored hear.

'''

from random import randrange

board = [' '] * 9

def get_ai_move():
    '''Get the Ai's next move'''
    #An Ai that attempts to win by taking the centre tile and performing multi traps in order to win, resets to random if it cant
    if board[4] == ' ':
        return 4
    elif board[4] == 'o':
        if board[8] == ' ':
            return 8
        elif board[6] == ' ':
            return 6
        elif board[8] == 'x' and board[0] == ' ':
            return 0
        elif board[6] == 'x' and board[2] == ' ':
            return 2
        elif board[8] == 'o' and board[6] == 'o':
            if board[0] == ' ':
                return 0
            if board[2] == ' ':
                return 2
            if board[7] == ' ':
                return 7
        elif board[0] == 'o' and board[6] == 'o':
            if board[2] == ' ':
                return 2
            if board[3] == ' ':
                return 3
        elif board[0] == 'o' and board[2] == 'o':
            if board[1] == ' ':
                return 1
    return randrange(9)


def get_ai_move1():
    '''Get the Ai's next move'''
    #A simple AI that attempt to win on the right side, and falls back on random moves if it cant.
    if board[2] == ' ':
        return 2
    elif board[5] == ' ':
        return 5
    elif board[8] == ' ':
        return 8
    else:
        return randrange(9)