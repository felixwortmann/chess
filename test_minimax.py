import chess
import random
import math
import copy
import time
from chess_core import minimax, minimax_for_color
from chess_utils import board_is_in_end_state, return_result, print_board_state


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
        if board_is_in_end_state(board):
            return return_result(board)
        # Black
        value, black_moves = minimax_for_color(board, False, depth_black)
        # print("nr:", counter, "white turn:",
        #       board.turn, black_moves, "value:", value)
        board.push(black_moves[0])
        # print("----------------------------------------------------------------")
        # print(board)
        if board_is_in_end_state(board):
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
            print_board_state(board)
            if board_is_in_end_state(board):
                return return_result(board)
        # KI
        value, moves = minimax_for_color(board, ki_color, ki_depth)
        # print("nr:", counter, "white turn:",
        #       board.turn, moves, "value:", value)
        # print(board)
        # print("----------------------------")
        print_board_state(board)
        board.push(moves[0])
        if board_is_in_end_state(board):
            return return_result(board)


# Play test games
iteration_start = time.time()
white_wins = 0
black_wins = 0
draw_games = 0
average_time_for_game = 0
for i in range(0, 2):
    game_start = time.time()
    board = chess.Board()
    board.root()
    # result = play_one_game_vs_self_test(board, 1, 1)
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
