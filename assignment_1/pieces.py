from abc import ABC, abstractmethod
import numpy as np

import assignment_1.constants as c


class Piece(ABC):
    """A base class to represent a piece on a chess board

    :param player: The player who owns the piece.
    """

    # def __init__(
    #     self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    # ):
    def __init__(self, player: c.Players, init_pos: np.ndarray):
        self.player = player  # The player who owns the piece.
        self.name = "Piece"  # Placeholder name for debug, should not be used.
        self.position: np.ndarray = init_pos  # Position on the board.
        self.n_moves: int = 0  # The number of moves the piece can at max make.
        self.column_switch: bool = (
            True  # Whether the piece can switch columns
        )
        self.column_switch_count: int = 0  # Times the piece switched columns
        self.jump: bool = False  # Whether the piece can jump over other pieces
        self.symbol: str = "*"  # Symbol used to represent the piece.

    def __str__(self):
        return f"{self.name} owned by player {self.player}"

    def get_player(self) -> c.Players:
        """
        Returns the player who owns the piece.

        :return: The player who owns the piece.
        """
        return self.player

    def get_name(self) -> str:
        """
        Returns the name of the piece.

        :return: The name of the piece.
        """
        return self.name

    def get_position(self) -> np.ndarray:
        """
        Returns the position of the piece on the board.

        :return: Position encoded as a [x, y] numpy array.
        """
        return self.position

    def set_position(self, position: np.ndarray, ignore_pos_check=False):
        """
        Sets the position of the piece on the board.

        :param position: Position encoded as a [x, y] numpy array.
        :param ignore_pos_check: Ignore check if piece is already on this pos.
        """
        for i in position:
            if i < 0 or i > c.BOARD_SIZE - 1:
                raise ValueError("Position is not on the board.")
        if (position == self.position).all() and not ignore_pos_check:
            raise ValueError("Piece is already on this position.")
        self.position = position

    def _init_move_cand(self, n_moves: int):
        move_cand = np.ones((n_moves, 4), dtype=int) * -1

        # write old position of this piece to move candidates
        old_loc = [self.position]
        move_cand[:, 0:2] = np.repeat(old_loc, n_moves, axis=0)

        # get coordinates of start position for new moves
        x_old = old_loc[0][0]
        y_old = old_loc[0][1]

        return x_old, y_old, move_cand

    def _get_diagonal_moves(
        self, n_moves_d: int = c.BOARD_SIZE - 1
    ) -> np.ndarray:
        """
        Returns a list of diagonal moves for the piece.

        :param n_moves_dir: Nr. of moves in one direction.
        :return: A list of diagonal moves for the piece.
        """
        x_old, y_old, move_cand = self._init_move_cand(2 * n_moves_d)

        # y_new (columns) does not depend on whether it is white or black
        y_new = np.arange(y_old - n_moves_d, y_old + n_moves_d + 1)
        y_new = np.delete(y_new, n_moves_d)  # del old position (center of arr)

        vert = np.arange(1, n_moves_d + 1)
        vert = np.concatenate((vert[::-1], vert))
        assert len(vert) == len(y_new) == 2 * n_moves_d

        # white only moves up, never moves down
        if self.player == c.Players.WHITE:
            x_new = x_old - vert

        # black only moves down, never moves up
        else:
            x_new = x_old + vert

        # x_new = np.tile(x_new, 2)

        move_cand[:, 2] = x_new
        move_cand[:, 3] = y_new

        return move_cand

    def _get_straight_moves(
        self,
        n_moves_d: int = c.BOARD_SIZE - 1,
        hor: bool = True,
        ver: bool = True,
    ) -> np.ndarray:
        """
        Returns a list of vertical moves for the piece.

        :param n_moves_dir: Nr. of moves in one direction.
        :param hor: Generate moves in horizontal direction.
        :param ver: Generate moves in vertical direction.
        :return: A list of vertical moves for the piece.
        """

        n_moves = 0
        if hor:
            n_moves += 2 * n_moves_d
        if ver:
            n_moves += n_moves_d
        if n_moves == 0:
            raise ValueError("At least one direction must be True.")

        x_old, y_old, move_cand = self._init_move_cand(n_moves)

        # generate horizontal moves, does not depend on player
        if hor:
            y_new = np.arange(y_old - n_moves_d, y_old + n_moves_d + 1)
            y_new = np.delete(y_new, n_moves_d)
            x_new = np.repeat(x_old, 2 * n_moves_d)
            move_cand[0 : len(x_new), 2] = x_new
            move_cand[0 : len(x_new), 3] = y_new

        # generate vertical moves
        if ver:
            vert = np.arange(1, n_moves_d + 1)
            if self.player == c.Players.WHITE:
                x_new = x_old - vert
            else:
                x_new = x_old + vert
            start_idx = 0

            if hor:
                start_idx = 2 * n_moves_d
            move_cand[start_idx : start_idx + len(x_new), 2] = x_new
            move_cand[start_idx : start_idx + len(x_new), 3] = y_old

        return move_cand

    @abstractmethod
    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        """
        Returns a list of valid moves for the piece.

        :param board: The current board state.
        :return: A list of valid moves for the piece.
        """
        pass

    def draw_valid_moves(self, board: np.ndarray, moves: np.ndarray):
        """
        Print a string representation of the board with valid moves marked by x

        :param board: The current board state.
        """

        # set all move locations of array moves with 1
        for move in moves:
            x = move[2]
            y = move[3]
            board[x][y] = 1

        s = ""
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if board[i][j] is None:
                    s += " ."
                elif board[i][j] == self:
                    symbol = f" {self.symbol}"
                    symbol = c.bcolors.OKBLUE + symbol + c.bcolors.ENDC
                    s += symbol
                elif board[i][j] == 1:
                    s += " x"

            s += "\n"
        return "\n" + s

    def validate_moves(
        self, moves: np.ndarray, board: np.ndarray
    ) -> np.ndarray:
        """
        Validates the moves gives moves for the piece.

        :param moves: The moves to validate.
        :param board: The current board state.
        :return: A list of valid moves for the piece.
        """
        valid_moves = moves.copy()

        for i, move in enumerate(moves):
            x = move[2]  # row nr. of target position
            y = move[3]  # col nr. of target position

            # check if move goes outside field, remove from list
            if x > c.BOARD_SIZE - 1 or x < 0 or y > c.BOARD_SIZE - 1 or y < 0:
                valid_moves[i, :] = -1
                continue

            # check if we can switch columns
            if not self.column_switch and move[1] != move[3]:
                valid_moves[i, :] = -1
                continue

            # TODO: if king is in check we only allow moves that get him out
            # TODO: if move puts our king in check, it's not valid
            # TODO: check if we can jump over pieces

        # delete all moves with -1
        valid_moves = valid_moves[valid_moves[:, 0] != -1]

        return valid_moves


class Pawn(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "Pawn"
        self.symbol = "P"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1

        # TODO: finish pawn implementation

        return valid_moves


class Rook(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "Rook"
        self.symbol = "R"
        self.n_moves = 3 * (c.BOARD_SIZE - 1)

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        _, _, move_cand = super()._init_move_cand(self.n_moves)

        # get coordinates of all new moves, valid or not
        move_cand = super()._get_straight_moves()

        # check which move candidates are valid and filter them out
        valid_moves = super().validate_moves(move_cand, board)

        return valid_moves


class Knight(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "Knight"
        self.symbol = "N"
        self.jump = True
        self.n_moves = 4

    def __move_l_shape(
        self, x_old: int, y_old: int, move_cand: np.ndarray
    ) -> np.ndarray:
        """
        Returns the coordinates of a knight move in the shape of an L.
        """
        x_new = np.array([x_old + 1, x_old + 2, x_old + 2, x_old + 1])
        y_new = np.array([y_old - 2, y_old - 1, y_old + 1, y_old + 2])

        # if player is black, we need to mirror the row coordinates
        if self.player == c.Players.BLACK:
            x_new = x_new - np.array([2, 4, 4, 2])

        move_cand[0 : len(x_new), 2] = x_new
        move_cand[0 : len(x_new), 3] = y_new

        return move_cand

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        x_old, y_old, move_cand = super()._init_move_cand(self.n_moves)

        # get coordinates of all new moves, valid or not
        move_cand = self.__move_l_shape(x_old, y_old, move_cand)

        # check which move candidates are valid and filter them out
        valid_moves = super().validate_moves(move_cand, board)

        return valid_moves


class Bishop(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "Bishop"
        self.symbol = "B"
        self.n_moves = 2 * (c.BOARD_SIZE - 1)

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        _, _, move_cand = super()._init_move_cand(self.n_moves)

        # get coordinates of all new moves, valid or not
        move_cand = super()._get_diagonal_moves()

        # check which move candidates are valid and filter them out
        valid_moves = super().validate_moves(move_cand, board)

        return valid_moves


class Queen(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "Queen"
        self.symbol = "Q"
        # queen can go in any direction (not down)
        self.n_moves = 5 * (c.BOARD_SIZE - 1)

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        _, _, move_cand = super()._init_move_cand(self.n_moves)

        # get coordinates of all new moves, valid or not
        diag_mov = super()._get_diagonal_moves()
        straight_mov = super()._get_straight_moves()
        move_cand = np.concatenate((diag_mov, straight_mov), axis=0)

        # check which move candidates are valid and filter them out
        valid_moves = super().validate_moves(move_cand, board)

        return valid_moves


class King(Piece):
    def __init__(
        self, player: c.Players, init_pos=np.array([-1, -1], dtype=int)
    ):
        super().__init__(player, init_pos)
        self.name = "King"
        self.symbol = "K"
        # the king can go up, left, right, and diagonally 1 square = 5 moves
        self.n_moves = 5
        self.is_in_check = False

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        _, _, move_cand = super()._init_move_cand(self.n_moves)

        # get coordinates of all new moves, valid or not
        diag_mov = super()._get_diagonal_moves(n_moves_d=1)
        straight_mov = super()._get_straight_moves(n_moves_d=1)
        move_cand = np.concatenate((diag_mov, straight_mov), axis=0)

        # check which move candidates are valid and filter them out
        valid_moves = super().validate_moves(move_cand, board)

        return valid_moves
