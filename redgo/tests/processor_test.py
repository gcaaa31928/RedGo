import unittest
from redgo.definitions import *
from redgo.processor import *
import os


class ProcessorTest(unittest.TestCase):
    def test_simulate_sgf_board(self):
        processor = Processor()
        with open(os.path.join(ROOT_DIR, './kgs/test.sgf'):
            
        sgf_string =
        sgf_string = bytes(sgf_string, encoding='utf8')
        processor.derive_sgf_content(sgf_string)
