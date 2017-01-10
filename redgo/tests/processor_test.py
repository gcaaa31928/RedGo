import unittest
from redgo.definitions import *
from redgo.processor import *
import os

np.set_printoptions(threshold=np.nan)


class ProcessorTest(unittest.TestCase):
    def test_board_derive_sgf(self):
        processor = Processor()
        f = open(os.path.join(ROOT_DIR, './kgs/test.sgf'))
        sgf_string = f.read()
        sgf_string = bytes(sgf_string, encoding='utf8')
        pros, sols = processor.derive_sgf_content(sgf_string)
        print(np.array(pros).shape)

    def test_board_get_features(self):
        processor = Processor()
        f = open(os.path.join(ROOT_DIR, './kgs/test.sgf'))
        sgf_string = f.read()
        sgf_string = bytes(sgf_string, encoding='utf8')
        board = processor.simulate_sgf_content(sgf_string)
        features = board.get_features(Color.white, (0, 0))[0]
        # print(features[:, :, 0])

    def test_simulate_sgf_board(self):
        processor = Processor()
        f = open(os.path.join(ROOT_DIR, './kgs/test.sgf'))
        sgf_string = f.read()
        sgf_string = bytes(sgf_string, encoding='utf8')
        board = processor.simulate_sgf_content(sgf_string)
        self.assertEqual(str(board).strip(), '''
 ---------------------------------------
| . . . . O O O O O X . O O . O X X . . |
| O O . . O . O X X X X X O . O O X X . |
| X O O . O O X X X O X O . O . . O X X |
| X X O O X O O X O O O . O X X O . X O |
| . X X O X O X X X O . O O X X O X . O |
| . . X X X X X O O O . O O O X X X O O |
| . . . . . X O O O . O O O X . X O . . |
| . . . O X X X X O O X O X X . X O O X |
| . . . X O O X X X X X O O X . X O . . |
| . . X X X O O O O X . O X X X X O O O |
| . . X O O O O X O X . O O X . X X X . |
| . O X O . O X X X X O O X X X . O X X |
| . X O O O . O O X X X O X O X . O O X |
| . X X O . O . X O X O X X O . X X O O |
| . . X O . X . X O X O O O O X X O X . |
| . . X O . . O O O X O . O O . X O O . |
| . X O O . O O . O X X O . O X X X O . |
| . X X X O . X O X X . X O O X . X O . |
| . . . X O . . O O X X X O . X X O O . |
 ---------------------------------------
'''.strip())
        print(board.show_liberty_info())
