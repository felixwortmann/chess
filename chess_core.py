#!/usr/bin/env python
# coding: utf-8

# In[1]:


import chess
import chess.polyglot
import math
import random


# In[2]:


# Define Styles
#from IPython.core.display import HTML
#with open('style.css','r') as file:
#    css = file.read()
#HTML(css)


# # Evaluation of the given state
# https://www.chessprogramming.org/Simplified_Evaluation_Function

# ## Hash function (zobrist hash)

# In[3]:


# Maximum number of moves is 5898 (due to the 50 Moves Rule - that makes this number big enough)
WIN_VALUE = 2147483647
CACHED_VALUES = None
CACHED_VALUES_ACCESS_COUNT = 0
OVERALL_ACCESS_COUNT = 0
TABLE = [[random.randint(0, 2**64 - 1) for piece_value in range(1,13)] for square in range(1,65)]

def piece_key(piece):
    return (piece.piece_type + (6 if piece.color else 0)) - 1

def zobrist_hash(board):
    return chess.polyglot.zobrist_hash(board)


# ## Evaluation function

# ### Piece-Square Tables
# Source: https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece-Square_Tables

# In[26]:


black_pawn_values   =   [0,  0,  0,  0,  0,  0,  0,  0,
                        50, 50, 50, 50, 50, 50, 50, 50,
                        10, 10, 20, 30, 30, 20, 10, 10,
                         5,  5, 10, 25, 25, 10,  5,  5,
                         0,  0,  0, 20, 20,  0,  0,  0,
                         5, -5,-10,  0,  0,-10, -5,  5,
                         5, 10, 10,-20,-20, 10, 10,  5,
                         0,  0,  0,  0,  0,  0,  0,  0]

black_knight_values = [-50,-40,-30,-30,-30,-30,-40,-50,
                       -40,-20,  0,  0,  0,  0,-20,-40,
                       -30,  0, 10, 15, 15, 10,  0,-30,
                       -30,  5, 15, 20, 20, 15,  5,-30,
                       -30,  0, 15, 20, 20, 15,  0,-30,
                       -30,  5, 10, 15, 15, 10,  5,-30,
                       -40,-20,  0,  5,  5,  0,-20,-40,
                       -50,-40,-30,-30,-30,-30,-40,-50]

black_bishop_values = [-20,-10,-10,-10,-10,-10,-10,-20,
                       -10,  0,  0,  0,  0,  0,  0,-10,
                       -10,  0,  5, 10, 10,  5,  0,-10,
                       -10,  5,  5, 10, 10,  5,  5,-10,
                       -10,  0, 10, 10, 10, 10,  0,-10,
                       -10, 10, 10, 10, 10, 10, 10,-10,
                       -10,  5,  0,  0,  0,  0,  5,-10,
                       -20,-10,-10,-10,-10,-10,-10,-20]

black_rook_values = [0,  0,  0,  0,  0,  0,  0,  0,
                     5, 10, 10, 10, 10, 10, 10,  5,
                    -5,  0,  0,  0,  0,  0,  0, -5,
                    -5,  0,  0,  0,  0,  0,  0, -5,
                    -5,  0,  0,  0,  0,  0,  0, -5,
                    -5,  0,  0,  0,  0,  0,  0, -5,
                    -5,  0,  0,  0,  0,  0,  0, -5,
                     0,  0,  0,  5,  5,  0,  0,  0]

black_queen_values = [-20,-10,-10, -5, -5,-10,-10,-20,
                      -10,  0,  0,  0,  0,  0,  0,-10,
                      -10,  0,  5,  5,  5,  5,  0,-10,
                       -5,  0,  5,  5,  5,  5,  0, -5,
                        0,  0,  5,  5,  5,  5,  0, -5,
                      -10,  5,  5,  5,  5,  5,  0,-10,
                      -10,  0,  5,  0,  0,  0,  0,-10,
                      -20,-10,-10, -5, -5,-10,-10,-20]

# TBD: King


# In[29]:


def raw_eval(board):
    
    # Check if game is over
    if (board.result() == "1-0" and board.turn) or (board.result() == "0-1" and not board.turn):
        result = WIN_VALUE - board.fullmove_number
        return result
    elif (board.result() == "0-1" and board.turn) or (board.result() == "1-0" and not board.turn):
        result = -WIN_VALUE + board.fullmove_number
        return result
    elif board.result() == "1/2-1/2" or board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        result = 0
        return result
    
    value = 0
    
    # Piece values, numbers represent centipawns; Pawn, Knight, Bishop, Rook, Queen
    # Source: https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece_Values
    piece_values = [100, 320, 330, 500, 900]
    
    for piece_type, piece_value in enumerate(piece_values):
        piece_type += 1
        
        player_pieces = board.pieces(piece_type, board.turn)
        enemy_pieces = board.pieces(piece_type, not board.turn)
        
        value += len(player_pieces)*piece_value
        value -= len(enemy_pieces)*piece_value
        
        if piece_type == chess.PAWN:
            value = piece_square_tables(black_pawn_values, player_pieces, enemy_pieces, board, value)
            
        if piece_type == chess.KNIGHT:
            value = piece_square_tables(black_knight_values, player_pieces, enemy_pieces, board, value)
            
        if piece_type == chess.BISHOP:
            value = piece_square_tables(black_bishop_values, player_pieces, enemy_pieces, board, value)
            
        if piece_type == chess.ROOK:
            value = piece_square_tables(black_rook_values, player_pieces, enemy_pieces, board, value)
            
        if piece_type == chess.QUEEN:
            value = piece_square_tables(black_queen_values, player_pieces, enemy_pieces, board, value)
        
    return value

def static_eval(board):
    global CACHED_VALUES
    global CACHED_VALUES_ACCESS_COUNT
    global OVERALL_ACCESS_COUNT
    
    OVERALL_ACCESS_COUNT += 1
    cache_key = zobrist_hash(board)
    if cache_key in CACHED_VALUES:
        CACHED_VALUES_ACCESS_COUNT += 1
        return CACHED_VALUES[cache_key]
    value = raw_eval(board)
    CACHED_VALUES[cache_key] = value
    return value


# ### Function for the Piece-Square Tables

# In[30]:


def piece_square_tables(black_piece_values, player_pieces, enemy_pieces, board, value):
    white_piece_values = black_piece_values[::-1]
    
    for piece in player_pieces:
        if board.turn:
            value += white_piece_values[piece]
        else:
            value += black_piece_values[piece]
            
    for piece in enemy_pieces:
        if board.turn:
            value -= black_piece_values[piece]
        else:
            value -= white_piece_values[piece]
            
    return value


# ## Main minimax function

# In[6]:


ANALYZING_DEPTH = None
def minimax(board, depth, alpha, beta):
    global BEST_MOVE
    if (depth == 0 or not board.legal_moves):
        return static_eval(board)
    max_value = alpha
    for move in board.legal_moves:
        board.push(move)
        value = -minimax(board, depth - 1, -beta, -max_value)
        board.pop()
        if (value > max_value):
            max_value = value
            if (depth == ANALYZING_DEPTH):
                BEST_MOVE = move;
            if (max_value >= beta):
                break
    return max_value


# In[7]:


BEST_MOVE = None
def minimax_input(board, depth):
    global CACHED_VALUES
    global ANALYZING_DEPTH
    ANALYZING_DEPTH = depth
    CACHED_VALUES = dict()
    value, polyglot_move = get_polyglot_move(board)
    if polyglot_move != "":
        return value, polyglot_move
    return minimax(board, depth, -math.inf, math.inf), BEST_MOVE


# In[8]:


def get_polyglot_move(board):
    with chess.polyglot.open_reader("data/polyglot/performance.bin") as reader:
        maximum = 0
        move = ""
        for entry in reader.find_all(board):
            print(entry.move, entry.weight, entry.learn)
            if entry.learn > maximum:
                maximum = entry.learn
                move = entry.move
        return maximum, move

