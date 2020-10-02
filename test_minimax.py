import chess
import random
import math
import copy
import time
from chess_core import minimax


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


def return_result(board, print_state=True):
    if print_state:
        print_board_state(board)
    if board.result() == "1-0":
        return 1
    elif board.result() == "0-1":
        return -1
    elif board.result() == "*":
        assert False  # Should not be called if this is the case
    else:
        return 0


def minimax_for_color(board, color, depth):
    # start = time.time()
    val = minimax(copy.deepcopy(board), depth, -math.inf, +math.inf, True, [])
    # print("Seconds for move:", time.time()-start)
    return val


def play_one_game_vs_self_test(board, depth_white, depth_black):
    counter = 0
    while True:
        counter += 1
        # White
        value, white_moves = minimax_for_color(board, True, depth_white)
        # print("nr:", counter, "white turn:",
        #       board.turn, white_moves, "value:", value)
        # print(white_moves)
        # print("----------------------------")
        board.push(white_moves[0])
        # print(board)
        if not board.result() == "*":
            return return_result(board)
        # Black
        value, black_moves = minimax_for_color(board, False, depth_black)
        # print("nr:", counter, "white turn:",
        #       board.turn, black_moves, "value:", value)
        board.push(black_moves[0])
        # print("----------------------------------------------------------------")
        # print(board)
        if not board.result() == "*":
            return return_result(board)


def play_one_game_vs_random_test(board, ki_color, ki_depth):
    # Does not work - white always wins
    counter = 0
    while True:
        counter += 1
        if not (counter == 1 and ki_color):  # skip if ki is white
            # Random
            mov = list(board.legal_moves)
            # print("white turn:", board.turn, "random:", mov[0])
            random.shuffle(mov)
            board.push(mov[0])
            # print(board)
            # print("----------------------------------------------------------------")
            if not board.result() == "*":
                return return_result(board)
        # KI
        value, moves = minimax_for_color(board, ki_color, ki_depth)
        # print("nr:", counter, "white turn:",
        #       board.turn, moves, "value:", value)
        # print(board)
        # print("----------------------------")
        board.push(moves[0])
        if not board.result() == "*":
            return return_result(board)


# Play test games
iteration_start = time.time()
white_wins = 0
black_wins = 0
draw_games = 0
average_time_for_game = 0
for i in range(0, 10):
    game_start = time.time()
    board = chess.Board()
    board.root()
    # result = play_one_game_vs_self_test(board, 1, 3)
    result = play_one_game_vs_random_test(board, True, 2)
    if result > 0:
        white_wins += 1
    elif result < 0:
        black_wins += 1
    else:
        draw_games += 1
    print("Result:", result)
    print("Game:", i+1, "finished----------------------------------------------------------------------------------")
    this_game_time = time.time() - game_start
    print(this_game_time, "seconds")
    average_time_for_game = (average_time_for_game *
                             i + this_game_time) / (i+1)

print("Finished in", time.time() - iteration_start, "seconds",
      " |  Average Seconds:", average_time_for_game)
print("White Wins:", white_wins)
print("Black Wins:", black_wins)
print("Draws:", draw_games)
