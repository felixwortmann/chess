import chess
import math
import copy


def static_eval(chess_board, maximizing_player):
    # Types:
    """{chess.PAWN, chess.KNIGHT, chess.BISHOP,
             chess.ROOK, chess.QUEEN, chess.KING}"""

    if chess_board.is_variant_end():
        if chess.Board.is_variant_draw():
            return 0
        elif chess_board.is_variant_loss():
            return -math.inf
        elif chess_board.is_variant_win():
            return math.inf
        else:
            assert False  # Should not happen
    piece_values = [1, 3, 3, 5, 9, 100]
    value = 0
    for i, piece_value in enumerate(piece_values):
        value += len(chess_board.pieces(i+1, maximizing_player))*piece_value
        value -= len(chess_board.pieces(i+1,
                                        not maximizing_player))*piece_value
    return value


def minimax(chess_board, depth, alpha, beta, maximizing_player, moves):
    chess_board = copy.deepcopy(chess_board)
    
    if depth == 0:
        return (static_eval(chess_board, maximizing_player), moves)

    if maximizing_player:
        max_val = -math.inf
        max_move = None
        for move in chess_board.legal_moves:
            chess_board.push(move)
            value, _ = minimax(chess_board,
                               depth - 1, alpha, beta, False, moves + [move])
            chess_board.pop()
            max_val = max(max_val, value)
            if max_val == value:
                max_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_val, moves + [max_move]
    else:
        min_val = +math.inf
        min_move = None
        for move in chess_board.legal_moves:
            chess_board.push(move)
            value, _ = minimax(chess_board, depth - 1, alpha,
                               beta, True, moves + [move])
            chess_board.pop()
            min_val = min(min_val, value)
            if min_val == value:
                min_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_val, moves + [min_move]
