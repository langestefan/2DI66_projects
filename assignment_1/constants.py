from enum import Enum
import numpy as np


# Game states: 0 = ongoing, 1 = player 1 won, 2 = player 2 won, 3 = draw
# game_states = {"ongoing": 0, "player_1_won": 1, "player_2_won": 2, "draw": 3}
class GameStates(Enum):
    ONGOING = 0
    WHITE_WON = 1
    BLACK_WON = 2
    DRAW = 3


n_players = 2
n_pieces = 10
BOARD_SIZE = 5


# Player definitions:
class Players(Enum):
    WHITE = 0
    BLACK = 1


# chesspiece types
class ChessPieceTypes(Enum):
    KING = 0
    KNIGHT = 1
    ROOK = 2
    BISHOP = 3
    QUEEN = 4
    PAWN = 5


# We will use algebraic chess notation to represent the pieces.
# The first letter is the piece type, the second letter is the player.
# The first player is always white, the second player is always black.
# The piece types are:
# K = king, Q = queen, R = rook, B = bishop, N = knight, P = pawn
# The players are:
# 1 = player 1, 2 = player 2
# The board is 5x5, so the columns are a-e and the rows are 1-5.
# The first row is the bottom row, the last row is the top row.
# The first column is the left column, the last column is the right column.


# Chess piece definitions:
PIECES = {
    Players.WHITE: {
        "KW": {
            "name": "WhiteKing",  # name of the piece
            "value": 0,  # value of the piece
            "type": ChessPieceTypes.KING,  # type of the piece
            "player": Players.WHITE,  # player owning the piece
            "pos": np.array([4, 4]),  # initial position of the piece
        },
        "NW": {
            "name": "WhiteKnight",
            "value": 3,
            "type": ChessPieceTypes.KNIGHT,
            "player": Players.WHITE,
            "pos": np.array([4, 1]),
        },
        "RW": {
            "name": "WhiteRook",
            "value": 5,
            "type": ChessPieceTypes.ROOK,
            "player": Players.WHITE,
            "pos": np.array([4, 0]),
        },
        "BW": {
            "name": "WhiteBishop",
            "value": 3,
            "type": ChessPieceTypes.BISHOP,
            "player": Players.WHITE,
            "pos": np.array([4, 2]),
        },
        "QW": {
            "name": "WhiteQueen",
            "value": 9,
            "type": ChessPieceTypes.QUEEN,
            "player": Players.WHITE,
            "pos": np.array([4, 3]),
        },
        "PW0": {
            "name": "WhitePawn0",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.WHITE,
            "pos": np.array([3, 0]),
        },
        "PW1": {
            "name": "WhitePawn1",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.WHITE,
            "pos": np.array([3, 1]),
        },
        "PW2": {
            "name": "WhitePawn2",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.WHITE,
            "pos": np.array([3, 2]),
        },
        "PW3": {
            "name": "WhitePawn3",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.WHITE,
            "pos": np.array([3, 3]),
        },
        "PW4": {
            "name": "WhitePawn4",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.WHITE,
            "pos": np.array([3, 4]),
        },
    },
    Players.BLACK: {
        "KB": {
            "name": "King",
            "value": 0,
            "type": ChessPieceTypes.KING,
            "player": Players.BLACK,
            "pos": np.array([0, 0]),
        },
        "NB": {
            "name": "Knight",
            "value": 3,
            "type": ChessPieceTypes.KNIGHT,
            "player": Players.BLACK,
            "pos": np.array([0, 3]),
        },
        "RB": {
            "name": "Rook",
            "value": 5,
            "type": ChessPieceTypes.ROOK,
            "player": Players.BLACK,
            "pos": np.array([0, 4]),
        },
        "BB": {
            "name": "Bishop",
            "value": 3,
            "type": ChessPieceTypes.BISHOP,
            "player": Players.BLACK,
            "pos": np.array([0, 2]),
        },
        "QB": {
            "name": "BlackQueen",
            "value": 9,
            "type": ChessPieceTypes.QUEEN,
            "player": Players.BLACK,
            "pos": np.array([0, 1]),
        },
        "PB0": {
            "name": "BlackPawn0",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.BLACK,
            "pos": np.array([1, 0]),
        },
        "PB1": {
            "name": "BlackPawn1",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.BLACK,
            "pos": np.array([1, 1]),
        },
        "PB2": {
            "name": "BlackPawn2",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.BLACK,
            "pos": np.array([1, 2]),
        },
        "PB3": {
            "name": "BlackPawn3",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.BLACK,
            "pos": np.array([1, 3]),
        },
        "PB4": {
            "name": "BlackPawn4",
            "value": 1,
            "type": ChessPieceTypes.PAWN,
            "player": Players.BLACK,
            "pos": np.array([1, 4]),
        },
    },
}


# for printing coloured text
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
