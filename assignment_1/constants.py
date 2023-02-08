# Game states: 0 = ongoing, 1 = player 1 won, 2 = player 2 won, 3 = draw
game_states = {"ongoing": 0, "player_1_won": 1, "player_2_won": 2, "draw": 3}


n_players = 2
n_pieces = 10
PLAYER_WHITE = 0
PLAYER_BLACK = 1

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

chess_pieces = {0: "K", 1: "Q", 2: "R", 3: "B", 4: "N", 5: "P"}
