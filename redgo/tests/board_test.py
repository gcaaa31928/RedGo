import unittest

from redgo.board import Board, Color


class BoardTest(unittest.TestCase):
    def test_board_captured(self):
        board = Board(5)
        for move in [(3, 0), (3, 1)]:
            board.move(Color.black, move)
        board.move(Color.white, (4, 0))
        board_string = board.show_liberty_info()
        lines = board_string.split('\n')
        print(board_string)
        self.assertEqual([
            '1....',
            '44...',
            '.....',
            '.....',
            '.....',
            ''
        ], lines)

        board.move(Color.black, (4, 1))
        board_string = board.show_liberty_info()
        # lines = board_string.split('\n')
        lines = board_string.split('\n')
        print(board_string)
        self.assertEqual([
            '.5...',
            '55...',
            '.....',
            '.....',
            '.....',
            ''
        ], lines)

    def test_board_liberties(self):
        board = Board(5)
        for move in [(3, 0), (4, 1), (3, 1)]:
            board.move(Color.black, move)
        for move in [(0, 2), (1, 2), (1, 3), (1, 4)]:
            board.move(Color.white, move)

        board_string = board.show_liberty_info()
        lines = board_string.split('\n')
        print(board_string)
        self.assertEqual([
            '.6...',
            '66...',
            '.....',
            '..888',
            '..8..',
            ''
        ], lines)

    def test_board_str(self):
        board = Board(5)
        for move in [(3, 0), (3, 1), (4, 1)]:
            board.move(Color.black, move)
        for move in [(0, 2), (1, 2), (1, 3), (1, 4)]:
            board.move(Color.white, move)

        board_string = str(board)
        lines = board_string.split('\n')
        print(board_string)
        self.assertEqual([
            '.*...',
            '**...',
            '.....',
            '..000',
            '..0..',
            ''
        ], lines)
