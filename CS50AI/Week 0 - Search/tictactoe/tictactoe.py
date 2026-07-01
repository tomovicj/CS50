"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = {X: 0, O: 0}

    for row in board:
        for col in row:
            if col == X:
                count[X] += 1
            elif col == O:
                count[O] += 1

    if count[X] > count[O]:
        return O
    
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available = set()

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                available.add((i, j))
    
    return available


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in [0, 1, 2] or action[1] not in [0, 1, 2]:
        raise AttributeError
    
    if board[action[0]][action[1]] != EMPTY:
        raise AttributeError
    
    b = copy.deepcopy(board)
    player_turn = player(b)

    b[action[0]][action[1]] = player_turn
    
    return b


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = board

    # Rows
    if b[0][0] is not EMPTY and (b[0][0] == b[0][1] == b[0][2]): return b[0][0]
    if b[1][0] is not EMPTY and (b[1][0] == b[1][1] == b[1][2]): return b[1][0]
    if b[2][0] is not EMPTY and (b[2][0] == b[2][1] == b[2][2]): return b[2][0]

    # Columns 
    if b[0][0] is not EMPTY and (b[0][0] == b[1][0] == b[2][0]): return b[0][0]
    if b[0][1] is not EMPTY and (b[0][1] == b[1][1] == b[2][1]): return b[0][1]
    if b[0][2] is not EMPTY and (b[0][2] == b[1][2] == b[2][2]): return b[0][2]

    # Diagonally
    if b[0][0] is not EMPTY and (b[0][0] == b[1][1] == b[2][2]): return b[0][0]
    if b[2][0] is not EMPTY and (b[2][0] == b[1][1] == b[0][2]): return b[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for row in board:
        for col in row:
            if col == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)

    if winner_player == X:
        return 1
    
    if winner_player == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)

    if current_player == X:
        return max_value(board)[1]
    
    return min_value(board)[1]


def max_value(board):
    v = (-10, None)

    if terminal(board):
        return (utility(board), None)

    for action in actions(board):
        new_min = min_value(result(board, action))
        if new_min[0] > v[0]:
            v = (new_min[0], action)
        if v[0] == 1:
            return v
    return v


def min_value(board):
    v = (10, None)

    if terminal(board):
        return (utility(board), None)
    
    for action in actions(board):
        new_min = max_value(result(board, action))
        if new_min[0] < v[0]:
            v = (new_min[0], action)
        if v[0] == -1:
            return v
    return v
