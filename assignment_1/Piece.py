# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:25:03 2023

@author: 20192020
"""
import numpy as np

class Piece:
    '''
    Class that defines valid moves for pieces, with each piece having their own
    method. These methods return an (X, 5) array, with X the number of valid 
    moves found and the columns being old x, old y, new x, new y, piece number.
    
    Some helper functions are also included, with helper_qbr defining possible 
    movements for bishop, rook and queen (queen's moveset is bishop + rook) and
    next to the validate function doing general validation checks, there are 
    additional validation methods (leap_validate, column_validate, 
                                   king_check_validate, pawn_capt_validate)
    These return an (X,2) array named validated with first column being x and 
    second being y coordinates. 
    
    pawn_promotion is a function to determine if a pawn has been promoted. 
    
    '''

    def __init__(self, board, player, col_switch):
        '''

        Parameters
        ----------
        board : array
            Numpy array that describes current state of the board
        player : integer
            If it's white's turn, player = 1
            If it's black's turn, player = 2
        col_switch : array
            Array containing 0 and 1 to indicate if column switching is allowed
            First row = white, second row = black
            Columns refer to the pieces (first six according to the order 
             defined, from seven onwards are promoted pawns)

        '''
        self.board = board 
        self.size = len(self.board) #size of board 
        self.player = player 
        self.col_switch = col_switch
        
        # numbers for pieces per player 
        # on order of King, Knight, Rook, Bischop, Queen, Pawn
        if self.player == 1:
            self.self_codes = [1, 2, 3, 4, 5, 6]
            self.opp_codes = [7, 8, 9, 10, 11, 12]
        else: #player 2, black
            self.self_codes = [7, 8, 9, 10, 11, 12]
            self.opp_codes = [1, 2, 3, 4, 5, 6]
            
    def king(self, check = True):
        '''
        Returns valid moves for the king

        Parameters
        ----------
        check : Boolean, optional
            Whether to look at opponents moveset to see what moves are valid
            for the king. Option is given as otherwise an endless recursion
            will follow. The default is True.

        '''
        # get location of the king
        king_code = self.self_codes[0]
        old_loc = np.transpose(np.where(self.board == king_code))
        
        # no check whether there's a king at all because the king cannot leave  
            # the board or it's gameover 
            
        # initialize array for all possible moves (5)
        king_moves = np.ones([5, 5])*-1
        king_moves[:, 0:2] = np.repeat(old_loc, 5, axis=0)
        king_moves[:, -1] = [king_code]*len(king_moves)
        
        # get coordinates of possible moves 
        x = old_loc[0][0]
        y = old_loc[0][1]
        if self.player == 1: #white 
            new_x = [x]*2 + [x-1]*3
        else: # black 
            new_x = [x]*2 + [x+1]*3
        new_y = [y-1, y+1, y-1, y, y+1]
        
        # validate moves 
        unvalidated = np.transpose(np.array([new_x, new_y]))
        validated = self.validate(unvalidated, king_code, old_loc = old_loc[0])
        if check:
            validated = self.king_check_validate(validated)
        king_moves[:, 2:4] = validated
        
        # remove invalid moves 
        ind = np.prod(king_moves >= 0, axis = 1).astype(bool)
        king_moves = king_moves[ind, :]
              
        return king_moves

    
    def knight(self):
        '''
        Returns valid moves for the knight 
        '''
        # get location of the knight
        knight_code = self.self_codes[1]
        old_loc = np.transpose(np.where(self.board == knight_code))
        
        # check if there's a knight in the first place
        if len(old_loc) == 0:
            return np.empty((0, 5))
        
        # initialize array for all possible moves (4)
        knight_moves = np.ones([4, 5])*-1
        knight_moves[:, 0:2] = np.repeat(old_loc, 4, axis=0)
        knight_moves[:, -1] = [knight_code]*len(knight_moves)
        
        # get coordinates of possible moves 
        x = old_loc[0][0]
        y = old_loc[0][1]
        if self.player == 1: #white
            new_x = [x-2, x-2, x-1, x-1]
        else: #black 
            new_x = [x+2, x+2, x+1, x+1]
        new_y = [y-1, y+1, y-2, y+2]
        
        # validate moves 
        unvalidated = np.transpose(np.array([new_x, new_y])) 
        validated = self.validate(unvalidated, knight_code, old_loc = old_loc[0])
        knight_moves[:, 2:4] = validated
        
        # remove invalid moves
        ind = np.prod(knight_moves >= 0, axis = 1).astype(bool)
        knight_moves = knight_moves[ind, :]
        
        return knight_moves
    
    def rook(self):
        '''
        Returns valid moves for the rook 
        '''
        # get location of the rook
        rook_code = self.self_codes[2]
        old_loc = np.transpose(np.where(self.board == rook_code))
        
        # check if there's a rook present
        if len(old_loc) == 0:
            return np.empty((0, 5))
        
        # initialize array for all possible moves (12)
        rook_moves = np.ones([12, 5])*-1
        rook_moves[:, 0:2] = np.repeat(old_loc, 12, axis=0)
        rook_moves[:, -1] = [rook_code]*len(rook_moves)

        # get coordinates of possible moves 
        x = old_loc[0][0]
        y = old_loc[0][1]
        new_x, new_y = self.helper_qbr(x, y, rook_code)
           
        # validate moves
        unvalidated = np.transpose(np.array([new_x, new_y]))   
        validated = self.validate(unvalidated, rook_code, False, old_loc = old_loc[0])
        rook_moves[:, 2:4] = validated
        
        # remove invalid moves
        ind = np.prod(rook_moves >= 0, axis = 1).astype(bool)
        rook_moves = rook_moves[ind, :]
                        
        return rook_moves
        
    def bishop(self):
        '''
        Returns valid moves for the bishop 
        '''
        # get location of the bishop
        bishop_code = self.self_codes[3]
        old_loc = np.transpose(np.where(self.board == bishop_code))
        
        # check if bishop is present 
        if len(old_loc) == 0:
            return np.empty((0, 5))
        
        # intialize array for all possible moves (8)
        bishop_moves = np.ones([8, 5])*-1
        bishop_moves[:, 0:2] = np.repeat(old_loc, 8, axis=0)
        bishop_moves[:, -1] = [bishop_code]*len(bishop_moves)
        
        # get coordinates of possible moves 
        x = old_loc[0][0]
        y = old_loc[0][1]
        new_x, new_y = self.helper_qbr(x, y, bishop_code)
            
        # validate moves 
        unvalidated = np.transpose(np.array([new_x, new_y])) 
        validated = self.validate(unvalidated, bishop_code, False, old_loc = old_loc[0])
        bishop_moves[:, 2:4] = validated 
        
        # remove invalid moves 
        ind = np.prod(bishop_moves >= 0, axis = 1).astype(bool)
        bishop_moves = bishop_moves[ind, :]
        
        return bishop_moves
    
    def queen(self):
        '''
        Returns valid moves for the queen 
        '''
        # get location of queen(s)
        queen_code = self.self_codes[4]
        old_loc = np.transpose(np.where(self.board == queen_code))
        
        # check if a queen is present 
        if len(old_loc) == 0:
            return np.empty((0, 5))
        
        # multiple queens can be present after promotion 
        # so initialize array based on nr of queens * possible moves (20)
        queen_moves = np.ones([20*len(old_loc), 5])*-1
        queen_moves[:, 0:2] = np.repeat(old_loc, 20*len(old_loc), axis=0)
        queen_moves[:, -1] = [queen_code]*len(queen_moves)
        
        # go through every queen 
        j = 0
        # i == 0 is 'original' queen, if i > 0, it's a promoted pawn 
        for i in range(len(old_loc)):
            x = old_loc[i][0]
            y = old_loc[i][1]
            
            # get coordinates of possible moves 
            new_x, new_y = self.helper_qbr(x, y, queen_code)
            
            # validate moves 
            unvalidated = np.transpose(np.array([new_x, new_y]))
            validated = self.validate(unvalidated, queen_code, False, 
                                      old_loc = old_loc[i], col_int = i)
            queen_moves[j:j+20, 2:4] = validated
            
            j += 20
        
        # remove invalid moves 
        ind = np.prod(queen_moves >= 0, axis = 1).astype(bool)
        queen_moves = queen_moves[ind, :]
        
        return queen_moves
    
    def pawn(self):
        '''
        Returns valid moves for the pawns 
        '''
        # get location of all pawns 
        pawn_code = self.self_codes[-1]
        old_loc = np.transpose(np.where(self.board == pawn_code))
        
        # check if at least one pawn is present 
        if len(old_loc) == 0:
            return np.empty((0, 5))
        
        # length of old_loc = nr of pawns left
        # initialize array for all possible moves 
        pawn_moves = np.ones([len(old_loc)*3, 5])*-1
        
        # get overview of regular (non-capture) moves 
        if self.player == 1: #white 
            reg_moves = np.add(np.ones(np.shape(old_loc)[0])*-1, old_loc[:, 0])
        else: #black 
            reg_moves = np.add(np.ones(np.shape(old_loc)[0]), old_loc[:, 0])
         
        # validate regular moves 
        not_validated = np.transpose(np.stack([reg_moves, old_loc[:, 1]]))
        validated = self.validate(not_validated, pawn_code) 
        pawn_moves[0:len(validated), 0:2] = old_loc
        pawn_moves[0:len(validated), 2:4] = validated
        pawn_moves[0:len(validated), -1] = self.pawn_promotion(validated)
        
        # get diagonal (capture) moves  
        counter = len(validated) #from what index you should add to the new_loc 
        cap_moves = np.zeros([len(old_loc)*2, 2])
        i = 0 # keep track of amount of moves added
        for x, y in old_loc:
            if self.player == 1: #white
                new_x = x-1
            else: #black 
                new_x = x+1
            
            cap_moves[i, :] = [new_x, y-1]
            cap_moves[i+1, :] = [new_x, y+1]
            
            i += 2
        
        # validated capture moves 
        # a zero is given in validation below as the capture move has different
            # validation than regular move 
        partial_validated = self.validate(cap_moves, 0)
        validated = self.pawn_capt_validate(partial_validated)
        pawn_moves[counter:counter+len(validated), 0:2] = np.repeat(old_loc, 2, axis=0)
        pawn_moves[counter:counter+len(validated), 2:4] = validated
        pawn_moves[counter:counter+len(validated), -1] = self.pawn_promotion(validated)

        # remove invalid moves
        ind = np.prod(pawn_moves >= 0, axis = 1).astype(bool)
        pawn_moves = pawn_moves[ind, :]
        
        return pawn_moves
        
    def helper_qbr(self, x, y, piece):
        '''
        Function to get all possible moves for queen, bishop or rook
        
        Parameters
        ----------
        x, y : list
            Coordinates of original location
        piece : integer  / float
            Number referring to what type of piece the moveset is needed

        Returns
        -------
        Two lists: x and y coordinates of possible moves 

        '''
        
        # the new y are not dependent on whether black or white is playing
        new_y1 = [y-i for i in range(1,5)] + [y+i for i in range(1,5)]
        new_y2 = [y-i for i in range(1, 5)] + [y+i for i in range(1, 5)] + [y]*4
        
        
        if self.player == 1: #white
            # bishop or queen 
            if piece == self.self_codes[3] or piece == self.self_codes[4]:
                new_x1 = [x-1, x-2, x-3, x-4]*2
                if piece == self.self_codes[3]:
                    return new_x1, new_y1
                
            # rook or queen
            if piece == self.self_codes[2] or piece == self.self_codes[4]: 
                new_x2 = [x]*8 + [x-1, x-2, x-3, x-4]
                if piece == self.self_codes[2]:
                    return new_x2, new_y2
            
            
        else: #black
            # bishop or queen
            if piece == self.self_codes[3] or piece == self.self_codes[4]:
                new_x1 = [x+1, x+2, x+3, x+4]*2
                if piece == self.self_codes[3]:
                    return new_x1, new_y1
               
            # rook or queen 
            if piece == self.self_codes[2] or piece == self.self_codes[4]:
                new_x2 = [x]*8 + [x+1, x+2, x+3, x+4]
                if piece == self.self_codes[2]:
                    return new_x2, new_y2
                
          
        return new_x1+new_x2, new_y1+new_y2
            
    
    def validate(self, moves, piece, leap = True, old_loc = None, col_int = 0):
        '''
        Spatial check (if move is still within board), leap check, additional 
        pawn checks, if the move is to an occupied (by own piece) space and 
        column switching checks. 

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves
        piece : integer / float
            Number referring to what type of piece the moveset is needed
        leap : Boolean, optional
            Whether leaping is allowed or not. The default is True.
        old_loc : array, optional
            (1,2) array with x and y coordinate of original location. 
            The default is None.
        col_int : integer, optional
            Index number to define whether a 'regular' piece is currently given
            or a promoted pawn to queen. The default is 0 ('regular' piece). 
            A value above 0 means it concerns a promoted pawn.

        '''
        validated = moves.copy()
        
        # loop over every row to validate move 
        for i in range(moves.shape[0]):
            x = moves[i, 0]
            y = moves[i, 1]
            
            # check if move goes outside field, remove from list (so change to -1)
            if x >= self.size or x < 0 or y >= self.size or y < 0:
                validated[i, :] = -1
                continue # no need to check the extra check for the pawn below
            
            # check if an own piece is occupying the space 
            # if leap is False, you want to keep the moves going to a field with 
            # an own piece for now to check for leaps 
            elif self.board[int(x), int(y)] in self.self_codes and leap:
                validated[i, :] = -1
                continue
               
            # special check for pawn (regular straight forward move cannot 
                #capture piece)
            elif piece == self.self_codes[-1]:
                if self.board[int(x), int(y)] in self.opp_codes:
                    validated[i, :] = -1
                    
        # check if a leap has been made over another piece 
        if not leap:
            validated = self.leap_validate(validated) 
            
        # check whether a piece has switched columns five times already 
        # get location of column for piece 
        if piece%6 == 0:
            col_int = -1 # using this as condiion to not go into the if-loop below
            code= 1
        elif piece >= 7:
            code = piece%6-1
        else:
            code = piece-1

        if col_int == 0 and self.col_switch[self.player-1, code] == 0:
            validated = self.column_validate(validated, old_loc)
        # check whether a 'promoted' queen has switched columns already 5 times
        elif col_int>0 and len(self.col_switch[self.player-1, :]) > 6:
            if self.col_switch[self.player-1, i+5] == 0:
                validated = self.column_validate(validated, old_loc)

        return validated
    
    def leap_validate(self, moves):
        '''
        Checks if an invalid leap move was included

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves

        '''
        validated = moves.copy()
        i = -1
        
        for j in range(int(len(moves)/4)):
            piece_enc = False # keep track whether piece was encountered or not
            counter = 4 # counter to keep track how many moves need to be invalidated

            while not piece_enc and counter >= 0:
                i += 1
                x = moves[i, 0]
                y = moves[i, 1]
                
                # first check if move has not been determined as invalid
                if x != -1 and y != -1:
                    board_piece = self.board[int(x), int(y)]
                    
                    # check if there is a piece present 
                    if board_piece != 0:
                        piece_enc = True
                        
                        if board_piece in self.self_codes:
                            # if an own piece is present
                            # also remove the move going to the field with this piece
                            validated[i:i+counter, :] = -1
                            i += counter-1
                        else:
                            # if a piece of the opponent is present
                            # the move going to that field doesn't need to be removed
                            validated[i+1:i+counter, :] = -1
                            i += counter-1
                else:
                    # if -1 is found, it means it's outside of the field 
                    # so the other moves afterwards also don' need additional 
                    # validation
                    piece_enc = True
                    i += counter-1
                
                counter -= 1
    
        return validated
            
    def column_validate(self, moves, old_loc):
        '''
        Validating whether column switching is still allowed

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves
        old_loc : array
            (1,2) array of x and y coordinates of original location

        '''
        validated = moves.copy()
        for j in range(len(moves)):
            y = old_loc[1]
            new_y = moves[j, 1]
            
            # check for column switching
            if y != new_y:
                validated[j, :] = -1
                
        return validated
    
    def king_check_validate(self, moves):
        '''
        Look at all possible moves of opponent to determine whether a king's 
        move goes to a field that is attacked by the opponent 

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves

        '''
        validated = moves.copy()
        
        # first get all moves of the opponent 
        opponent = Piece(self.board.copy(), 3-self.player, self.col_switch)
        
        # pawn is special case : need to check whether it's a capture move or not
        # if capture move, the y coordinate should change 
        pm = opponent.pawn()
        pm = pm[pm[:,1] != pm[:,3], :] 
        
        bm = opponent.bishop()
        km = opponent.knight()
        rm = opponent.rook()
        qm = opponent.queen()
        kingm = opponent.king(False)
        
        all_moves = np.concatenate((pm, bm, km, rm, qm, kingm), axis=0)
        
        # remove invalid king moves
        for i in range(moves.shape[0]):
            x = moves[i, 0]
            y = moves[i, 1]

            if [x, y] in all_moves[:, 2:4].tolist():
                validated[i, :] = -1
        
        return validated
        
    
    def pawn_capt_validate(self, moves):
        '''
        Checks whether the pawn captures an opponent piece at new location. 
        Assumption is that spatial validation has already been done. 

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves

        '''
        validated = moves.copy()
            
        for i in range(moves.shape[0]):
            x = moves[i, 0]
            y = moves[i, 1]
            
            if self.board[int(x), int(y)] not in self.opp_codes:
                validated[i, :] = -1
                
        return validated
    
    def pawn_promotion(self, moves):
        '''
        Checks whether the number referring to this piece should change to that 
        of a queen after promotion

        Parameters
        ----------
        moves : array
            (X,2) array of x and y coordinates of possible moves

        Returns
        -------
        code_lst : list
            A list with a value for each pawn (either stays a pawn or changed
                                               to queen)

        '''
        code_lst = np.zeros(len(moves))
        for i in range(len(moves)):
            if moves[i, 0] == 0 or moves[i, 0] == self.size-1:
                code_lst[i] = self.self_codes[4] # Queen code 
            else:
                code_lst[i] = self.self_codes[-1] # Pawn code 
                
        return code_lst
        



        
        
        
        
        
        
        
        
        
        