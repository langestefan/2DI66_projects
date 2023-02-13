import numpy as np
import copy

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.pieces import King


class GameState:
    """
    This class is used to represent the state of the game.

    It contains the round number, the players, who owns which chess pieces,
    the history of moves and decides if the game is over. (docs in reST style)

    In baby chess there are
     - Two players
     - Each player has 10 pieces:
       (1x king, 1x queen, 1x rooks, 1x bishops, 1x knights, 5x pawns)
     - The board has 5x5
     - Players are represented by integers 0 and 1
     - The game is over when one player has no pieces left or when the
       king is captured.

    Attributes:
        round_number (int): The round number of the game.
        current_player (Players): The player who is currently playing.
        game_state (GameStates): The game state. Ongoing, draw or won.
        chess_board (ChessBoard): The chess board. NxN ndarray.
    """

    def __init__(self):
        self.round_number: int = -1  # Call start_new_round() to increment to 0
        self.current_player: c.Players = c.Players.WHITE  # White starts
        self.game_state: c.GameStates = c.GameStates.ONGOING
        self.white_in_check: bool = False
        self.black_in_check: bool = False
        self.chess_board: ChessBoard = ChessBoard(init_pieces=True)

    def __str__(self) -> str:
        return f"Round number: {self.round_number}"

    def get_round_number(self) -> int:
        """
        Returns the round number of the game.

        :return: The round number of the game.
        """
        return self.round_number

    def get_current_player(self) -> c.Players:
        """
        Returns the player who is currently playing.

        :return: The player who is currently playing.
        """
        return self.current_player

    def increment_round_number(self) -> None:
        """
        Increments the round number.
        """
        # start new round, increment round number and set current player
        self.round_number += 1
        self.current_player = c.Players(self.round_number % 2)

    def start_new_round(self, move: np.ndarray) -> None:
        """
        Starts a new round.

        :param move: Move to be made.
        """
        if move.shape == (1, 4):
            move = move.squeeze()
        if move.shape != (4,):
            raise ValueError("Move must be a 4 element array.")

        # make move
        old_pos = move[0:2]
        new_pos = move[2:4]
        self.chess_board.move_piece(old_pos, new_pos, self.current_player)

    def get_game_state(self) -> c.GameStates:
        """
        Returns the game state.

        :return: The game state.
        """
        return self.game_state

    def set_game_state(self, game_state: c.GameStates) -> None:
        """
        Sets the game state.

        :param game_state: The game state.
        """
        self.game_state = game_state

    def get_board(self) -> ChessBoard:
        """
        Returns the chess board.

        :return: The chess board.
        """
        return self.chess_board

    def get_valid_moves(self, player) -> np.ndarray:
        """Checks which moves are valid for the player.

        :param player: The player whose moves are to be checked.
        :return: A list of valid moves for the player.
        """
        board_arr = self.get_board().get_board_arr()

        # collect valid moves here
        valid_moves = np.ones((200, 4), dtype=int) * -1

        # our king is in check, so we can only do moves that get us out of check
        if (
            player == c.Players.WHITE
            and self.white_in_check is True  # noqa: W503
            or player == c.Players.BLACK  # noqa: W503
            and self.black_in_check is True  # noqa: W503
        ):
            king_obj = self.get_board().get_king_obj(player)
            king_moves = king_obj.get_valid_moves(board_arr)
            print(f"king moves: {king_moves}")

        # our king is not in check, so we can do all moves
        else:
            valid_moves = self.__get_all_moves(player)

        # filter out invalid moves
        valid_moves = valid_moves[valid_moves[:, 0] != -1]

        return valid_moves
    
    # TODO: filter pawn moves that are not diagonal attacks so they dont put the king in check
    # TODO: implement check counter by attacking piece that is attacking the king
    # TODO: implement check counter by moving piece to block the attack

    def __set_check(self, player, check):
        if player == c.Players.WHITE:
            self.white_in_check = check
        else:
            self.black_in_check = check

    def king_is_in_check(self, player) -> bool:
        """Checks if the king of the player is in check.

        :param player: The player whose king is to be checked.
        :return: True if the king is in check, False otherwise.
        """
        # get king position
        king_obj = self.get_board().get_king_obj(player)
        king_pos = king_obj.get_position()

        # get opponent pieces
        opponent_pieces = self.get_board().get_all_pieces(
            c.Players(1 - player.value)
        )

        # check if opponent pieces can attack king
        for piece in opponent_pieces:
            moves = piece.get_valid_moves(self.get_board().get_board_arr())

            # check if king pos is in moves
            for move in moves:
                if np.array_equal(move[2:4], king_pos):
                    self.__set_check(player, True)
                    return True

        # our king is not in check
        self.__set_check(player, False)
        return False

    def __get_all_moves(self, player) -> np.ndarray:
        """Returns all possible moves for the player's pieces.

        :param player: The player whose moves are to be checked.
        :return: A list of all possible moves for the player.
        """
        # collect all moves here
        all_moves = np.ones((200, 4), dtype=int) * -1

        # get all pieces of player
        pieces = self.get_board().get_all_pieces(player)

        # get all moves for each piece
        move_idx = 0
        for piece in pieces:
            moves = piece.get_valid_moves(self.get_board().get_board_arr())
            moves_len = len(moves)
            all_moves[move_idx : move_idx + moves_len] = moves
            move_idx += moves_len

        # filter out invalid moves
        all_moves = all_moves[all_moves[:, 0] != -1]

        return all_moves

    # def get_valid_moves(self, player) -> np.ndarray:
    #     """Checks which moves are valid for the player.

    #     :param player: The player whose moves are to be checked.
    #     :return: A list of valid moves for the player.
    #     """
    #     board_arr = self.get_board().get_board_arr()

    #     # we will initialize the array with -1, so we can filter valid moves
    #     # format: [from_x, from_y, to_x, to_y]
    #     valid_moves = np.ones((100, 4), dtype=int) * -1

    #     # our king is not in check, so we can check all moves
    #     if self.check_state == c.CheckStates.NONE:
    #         move_index: int = 0
    #         for i in range(c.BOARD_SIZE):
    #             for j in range(c.BOARD_SIZE):
    #                 piece = board_arr[i, j]  # type: ignore

    #                 # only check pieces of the current player
    #                 if piece is not None and piece.get_player() == player:
    #                     pos_piece = piece.get_position()
    #                     pos_array = np.array([i, j])
    #                     if not (pos_piece == pos_array).all():
    #                         raise ValueError(
    #                             "Piece position does not match board position."
    #                         )

    #                     moves = piece.get_valid_moves(board_arr)

    #                     # we check if any of the moves puts the king in check
    #                     if isinstance(piece, King):
    #                         for idx, move in enumerate(moves):
    #                             print(
    #                                 f"Checking move: {move} for player:"
    #                                 f" {player}."
    #                             )
    #                             # copy the game state (myself)
    #                             gs_cpy = copy.deepcopy(self)
    #                             gs_cpy.current_player = player

    #                             # make the move
    #                             gs_cpy.chess_board.move_piece(
    #                                 move[0:2],
    #                                 move[2:4],
    #                                 player,
    #                                 print_info=False,
    #                             )

    #                             # check if the king is in check
    #                             if gs_cpy.king_is_in_check(player, [move]):
    #                                 # remove the move from the valid moves
    #                                 moves[idx] = -1
    #                                 print("Puts king in check.")

    #                             # delete the copy
    #                             del gs_cpy

    #                     # add the moves to the valid moves array
    #                     valid_moves[move_index : move_index + len(moves)] = (
    #                         moves
    #                     )
    #                     move_index += len(moves)

    #     # our king is in check, so we need to check if we can get out of check
    #     elif (
    #         self.check_state == c.CheckStates.WHITE_IN_CHECK
    #         and player == c.Players.WHITE
    #         or self.check_state == c.CheckStates.BLACK_IN_CHECK
    #         and player == c.Players.BLACK
    #     ):
    #         # first we need to get the king position
    #         king_pos = self.chess_board.get_piece_loc_by_type(
    #             piece_type=King, player=player
    #         )
    #         if king_pos is None:
    #             raise ValueError("King not found by type.")

    #         king = self.chess_board.get_piece(king_pos)
    #         if king is None:
    #             raise ValueError("King not found by position.")

    #         # get all valid moves for the king
    #         king_moves = king.get_valid_moves(board_arr)
    #         print(f"King moves: {king_moves}")
    #         valid_moves = king_moves

    #     else:
    #         # the king is in check, but it is not the current player's turn
    #         raise ValueError("It is not the current player's turn.")

    #     # filter out invalid moves
    #     valid_moves = valid_moves[valid_moves[:, 0] != -1]

    #     return valid_moves

    # def king_is_in_check(self, player, valid_moves) -> bool:
    #     """
    #     Checks if the king of the current player is in check.

    #     :param player: The player whose king is to be checked.
    #     :return: True if the king is in check, False otherwise.
    #     """
    #     if player != self.current_player:
    #         raise ValueError("Player must be the current player.")

    #     in_check = False

    #     # get king position of current player
    #     board_arr = self.get_board()
    #     king_pos = board_arr.get_piece_loc_by_type(
    #         piece_type=King, player=player
    #     )

    #     # check if any of the opponent's valid moves is to the king
    #     for move in valid_moves:
    #         if (move[2:4] == king_pos).all():
    #             in_check = True
    #             break

    #     # a player's king is now in check
    #     if in_check:
    #         if player == c.Players.WHITE:
    #             self.check_state = c.CheckStates.WHITE_IN_CHECK
    #         else:
    #             self.check_state = c.CheckStates.BLACK_IN_CHECK

    #     # a player's king is no longer in check
    #     else:
    #         self.check_state = c.CheckStates.NONE

    #     return in_check
