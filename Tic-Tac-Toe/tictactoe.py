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
    Returns starting state of the board
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    number_of_x = 0
    number_of_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                number_of_x += 1
            elif board[i][j] == "O":
                number_of_O += 1
    return "X" if number_of_x == number_of_O else "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_moves = {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}
    return set_of_moves if set_of_moves != set() else None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    try:
        x, y = action
    except:
        raise Exception("Invalid action")
    else:
        if x not in range(3) or y not in range(3) or not isinstance(action, tuple) or action not in actions(board):
            raise Exception("Invalid action")
        new_board[x][y] = player(new_board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
        elif board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X" or winner(board) == "O" or actions(board) is None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "O":
        return -1
    return 1 if winner(board) == "X" else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    else:
        for action in actions(board):
            if utility(result(board, action)) != 0:
                return action

        positive_inf = math.inf
        negative_inf = -math.inf

        def max_value(board):
            v = negative_inf
            if terminal(board):
                return utility(board)
            for action in actions(board):
                v = max(v, min_value(result(board, action)))
            return v

        def min_value(board):
            v = positive_inf
            if terminal(board):
                return utility(board)
            for action in actions(board):
                v = min(v, max_value(result(board, action)))
            return v

        if player(board) == "X":
            maxi = max_value(board)
            for action in actions(board):
                if maxi == min_value(result(board, action)):
                    return action

        else:
            mini = min_value(board)
            for action in actions(board):
                if mini == max_value(result(board, action)):
                    return action
