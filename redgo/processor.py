from redgo.board import Board
from .definitions import *


class Processor:

    @staticmethod
    def read_sgf_file(file_path):
        with open(file_path, 'r') as content_file:
            content = bytes(content_file.read(), encoding='utf8')
