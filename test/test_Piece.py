# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 15:13:29 2023

@author: 20192020
"""
import numpy as np 
from Piece import Piece

opening_board = np.array([[7, 11, 10, 8, 9], [12, 12, 12, 12, 12], [0, 0, 0, 0, 0],
                      [6, 6, 6, 6, 6], [3, 2, 4, 5, 1]]) 

test_board = np.array([[2, 5, 9, 8, 7], [0, 0, 12, 0, 0], [0, 4, 0, 6, 0],
                      [0, 11, 12, 0, 0], [3, 0, 0, 0, 1]]) 
  
col = np.ones([2, 6])
col[1, 4] = 0
test = Piece(opening_board, 2, col)
print('Board \n', test.board)
print('MOVES: old_x old_y new_x new_y piece_code')

pawn_moves = test.pawn()
print('PAWN MOVES \n', pawn_moves)

knight_moves = test.knight()
print('KNIGHT MOVES \n', knight_moves)

rook_moves = test.rook()
print('ROOK MOVES \n', rook_moves)

bishop_moves = test.bishop()
print('BISHOP MOVES \n', bishop_moves)

queen_moves = test.queen()
print('QUEEN MOVES \n', queen_moves)

king_moves = test.king()
print('KING MOVES \n', king_moves)