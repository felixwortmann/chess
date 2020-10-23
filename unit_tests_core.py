import unittest
import chess_core
import chess


class EvaluationTest(unittest.TestCase):
    def test(self):

        # Setup
        board = chess.Board()
        board.root()

        # Test before move
        self.assertEqual(chess_core.static_eval(board, True), 0)
        self.assertEqual(chess_core.static_eval(board, False), 0)

        # Move
        board.push(chess.Move.from_uci("c2c7"))

        # Test after move
        self.assertEqual(chess_core.static_eval(board, True), 1)
        self.assertEqual(chess_core.static_eval(board, False), -1)


class MinimaxTest(unittest.TestCase):
    def test(self):

        # Setup
        board = chess.Board()
        board.root()

        # Test before move
        self.assertEqual(chess_core.static_eval(board, True), 0)
        self.assertEqual(chess_core.static_eval(board, False), 0)

        # Move
        board.push(chess.Move.from_uci("b2b4"))
        value, ki_moves = chess_core.minimax_for_color(board, False, 3)
        print("value, ki_move", value, ki_moves)
        board.push(ki_moves[0])

        board.push(chess.Move.from_uci("b4a5"))
        value, ki_moves = chess_core.minimax_for_color(board, False, 3)
        print("value, ki_move", value, ki_moves)
        board.push(ki_moves[0])
        print(board)



if __name__ == '__main__':
    unittest.main()
