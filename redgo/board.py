from .sgf_parser import sgf
from enum import Enum


class Color(Enum):
    black = 0
    white = 1


class Chain:
    def __init__(self, color, size=19):
        self.board_size = size
        self.color = color
        self.stones = []
        self.liberties = []

    def add_stone(self, pos):
        self.stones.append(pos)

    def add_liberty(self, pos):
        self.liberties.append(pos)

    def num_liberties(self):
        return len(self.liberties)

    def can_not_breath(self):
        return len(self.liberties) == 0

    def remove_liberty(self, pos):
        self.liberties.remove(pos)

    def merge_chain(self, chain, joint_pos):
        self.stones.extend(chain.stones)
        self.liberties.extend(chain.liberties)
        self.remove_liberty(joint_pos)
        return self


class Board:
    def __init__(self, size):
        self.board = {}
        self.size = size
        self.chains = {}
        self.last_move_captured = 0

    def over_bound(self, pos):
        row, col = pos
        if row >= self.size or row < 0 or col >= self.size or col < 0:
            return True
        return False

    def add_liberty(self, chain, pos):
        if pos in self.board:
            return
        if not self.over_bound(pos):
            chain.add_liberty(pos)

    def create_chain(self, color, pos):
        chain = Chain(color)
        row, col = pos
        chain.add_stone(pos)
        for liberty_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            self.add_liberty(chain, liberty_pos)
        self.chains[pos] = chain
        self.board[pos] = color
        return chain

    def remove_enemy_liberty(self, color, pos):
        row, col = pos
        for liberty_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            # is enemy
            if self.board[liberty_pos] != color:
                enemy_chain = self.chains[liberty_pos]
                enemy_chain.remove_liberty(pos)
                if enemy_chain.can_not_breath():
                    self.chains_can_not_breath(enemy_chain)

    def chains_can_not_breath(self, chain):
        color = chain.color
        captured_stones = 0
        for stone_pos in chain.stones:
            row, col = stone_pos
            del self.board[stone_pos]
            del self.chains[stone_pos]
            captured_stones += 1
            for move_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                enemy_chain = self.chains[move_pos]
                self.add_liberty(enemy_chain, move_pos)
        self.last_move_captured = captured_stones

    def merge_adjacent_chain(self, chain, pos):
        row, col = pos
        for adjacent_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            adjacent_chain = self.chains[adjacent_pos]
            if adjacent_chain.color == chain.color:
                chain.merge_chain(adjacent_chain, pos)
                del self.chains[adjacent_pos]
        return chain

    def move(self, color, pos):
        if self.over_bound(pos):
            assert True, "position should not over bound when apply move"
            return
        chain = self.create_chain(color, pos)
        self.merge_adjacent_chain(chain, pos)

    def get_features(self, color, move):
        pass
