import chess
import math
import copy


def static_eval(chess_board, maximizing_color):
    # Types:
    """{chess.PAWN, chess.KNIGHT, chess.BISHOP,
             chess.ROOK, chess.QUEEN, chess.KING}"""
    piece_values = [1, 3, 3, 5, 9, 100]
    value = 0
    for i, piece_value in enumerate(piece_values):
        value += len(chess_board.pieces(i+1, maximizing_color))*piece_value
        value -= len(chess_board.pieces(i+1,
                                        not maximizing_color))*piece_value
    if not maximizing_color == chess_board.turn and chess_board.is_check():
        value += 5
    return value


def minimax(chess_board, depth, alpha, beta, maximizing_player, minimizing_color, moves, verbose=False):
    chess_board = copy.deepcopy(chess_board)
    if chess_board.result() == "1-0":
        return ((math.inf, moves) if maximizing_player else (-math.inf, moves))
    elif chess_board.result() == "0-1":
        return ((math.inf), moves if not maximizing_player else (-math.inf, moves))
    elif chess_board.result() == "1/2-1/2" or chess_board.is_stalemate():
        return 0, moves

    if depth == 0:
        return (static_eval(chess_board, minimizing_color), moves)

    if maximizing_player:
        max_val = -math.inf
        max_move = None
        for move in chess_board.legal_moves:
            chess_board.push(move)
            value, _ = minimax(chess_board,
                               depth - 1, alpha, beta, not maximizing_player, minimizing_color, moves + [move], verbose)
            if verbose:
                print("maximizing_player:", maximizing_player)
                print("move,value", move, value)
                print(chess_board)

            chess_board.pop()
            max_val = max(max_val, value)
            if max_val == value:
                max_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        assert chess_board.legal_moves  # should not be here if its a stalemate
        assert not max_move == None
        return max_val, moves + [max_move]
    else:
        min_val = +math.inf
        min_move = None
        for move in chess_board.legal_moves:
            chess_board.push(move)
            value, _ = minimax(chess_board, depth - 1, alpha,
                               beta, not maximizing_player, not minimizing_color, moves + [move], verbose)
            if verbose:
                print("maximizing_player:", maximizing_player)
                print("move,value", move, value)
                print(chess_board)
            chess_board.pop()
            min_val = min(min_val, value)
            if min_val == value:
                min_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        assert chess_board.legal_moves  # should not be here if its a stalemate
        assert not min_move == None
        return min_val, moves + [min_move]


def minimax_for_color(board, color, depth, verbose=False):
    return minimax(copy.deepcopy(board), depth, -math.inf, +math.inf, True, not color, [], verbose)
