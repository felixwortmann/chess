import chess
def print_board_state(board):
    print(board)
    print("-----------------------------------")
    print("white_turn:              ", board.turn)
    print("is_game_over:            ", board.is_game_over())
    print("is_variant_end:          ", board.is_variant_end())
    print("is_stalemate::           ", board.is_stalemate())
    print("is_variant_win:          ", board.is_variant_win())
    print("is_variant_loss:         ", board.is_variant_loss())
    print("is_variant_draw:         ", board.is_variant_draw())
    print("is_seventyfive_moves:    ", board.is_seventyfive_moves())
    print("result:                  ", board.result())


def board_is_in_end_state(board):
    return (not board.result() == "*")


def return_result(board, print_state=True):
    if print_state:
        print_board_state(board)
    if board.result() == "1-0":
        return 1
    elif board.result() == "0-1":
        return -1
    elif board.is_stalemate():
        return 0
    elif board.result() == "*":
        assert False  # Should not be called if this is the case
    else:
        return 0