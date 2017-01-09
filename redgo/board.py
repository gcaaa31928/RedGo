from .sgf_parser import sgf
from enum import Enum


class Color(Enum):
    black = 0
    white = 1


class Chain:
    def __init__(self, color):
        self.color = color
        self.stones = []
        self.liberties = []

    def add_stone(self, pos):
        self.stones.append(pos)

    def add_liberty(self, pos):
        self.liberties.append(pos)


class Board:
    def __init__(self, size):
        self.board = {}
        self.size = size
        self.chains = {}
        pass

    def create_chain(self, color, pos):
        chain = Chain(color)

    def merge_adjacent_chain(self, chain):
        pass

    def move(self, color, pos):
        pass

    def get_features(self, color, move):
        pass
