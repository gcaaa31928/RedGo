from .sgf_parser import sgf
from enum import Enum
import numpy as np


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
        if pos in self.stones:
            return
        self.stones.append(pos)

    def add_liberty(self, pos):
        if pos in self.liberties:
            return
        self.liberties.append(pos)

    def num_liberties(self):
        return len(self.liberties)

    def can_not_breath(self):
        return len(self.liberties) == 0

    def remove_liberty(self, pos):
        if pos in self.liberties:
            self.liberties.remove(pos)

    def merge_chain(self, chain, joint_pos):
        self.stones += list(set(chain.stones) - set(self.stones))
        self.liberties += list(set(chain.liberties) - set(self.liberties))
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
        chain = Chain(color, self.size)
        row, col = pos
        chain.add_stone(pos)
        for liberty_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            self.add_liberty(chain, liberty_pos)
        self.chains[pos] = chain
        self.board[pos] = color
        return chain

    def remove_enemy_liberty(self, color, pos):
        row, col = pos
        for enemy_chain_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if self.over_bound(enemy_chain_pos) or enemy_chain_pos not in self.board:
                continue
            # is enemy
            if self.board[enemy_chain_pos] != color:
                enemy_chain = self.chains[enemy_chain_pos]
                enemy_chain.remove_liberty(pos)
                if enemy_chain.can_not_breath():
                    self.chains_can_not_breath(enemy_chain)

    def chains_can_not_breath(self, chain):
        captured_stones = 0
        for stone_pos in chain.stones:
            row, col = stone_pos
            del self.board[stone_pos]
            del self.chains[stone_pos]
            captured_stones += 1
            for move_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                if self.over_bound(move_pos) or move_pos not in self.chains:
                    continue
                enemy_chain = self.chains[move_pos]
                if enemy_chain.color != chain.color:
                    self.add_liberty(enemy_chain, stone_pos)
        self.last_move_captured = captured_stones

    def merge_adjacent_chain(self, chain, pos):
        row, col = pos
        for adjacent_pos in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if self.over_bound(adjacent_pos) or adjacent_pos not in self.chains:
                continue
            adjacent_chain = self.chains[adjacent_pos]
            if adjacent_chain.color == chain.color:
                chain.merge_chain(adjacent_chain, pos)
                for stone_pos in adjacent_chain.stones:
                    self.chains[stone_pos] = chain
                self.chains[adjacent_pos] = chain
        return chain

    def move(self, color, pos):
        if self.over_bound(pos):
            assert True, "position should not over bound when apply move"
            return
        chain = self.create_chain(color, pos)
        self.merge_adjacent_chain(chain, pos)
        self.remove_enemy_liberty(color, pos)

    def get_features(self, color, move):
        sol = None
        if move:
            row, col = move
            sol = row * self.size + col
        probs = np.zeros((self.size, self.size, 7))
        for row in range(0, self.size):
            for col in range(0, self.size):
                pos = (row, col)
                stone_color = self.board.get(pos)
                if stone_color is None:
                    continue
                probs[row, col, 0] = 1 if stone_color == color else 2
                chain = self.chains.get(pos)
                if stone_color == color:
                    if chain.num_liberties() <= 1:
                        probs[row, col, 1] = 1
                    elif chain.num_liberties() <= 2:
                        probs[row, col, 2] = 1
                    elif chain.num_liberties() >= 3:
                        probs[row, col, 3] = 1
                else:
                    if chain.num_liberties() <= 1:
                        probs[row, col, 4] = 1
                    elif chain.num_liberties() <= 2:
                        probs[row, col, 5] = 1
                    elif chain.num_liberties() >= 3:
                        probs[row, col, 6] = 1
                probs[row, col, 7] = 1
        return probs, sol

    def show_liberty_info(self):
        res = ''
        for i in range(self.size - 1, -1, -1):
            line = ''
            for j in range(0, self.size):
                chain = self.chains.get((i, j))
                if chain is None:
                    line += '.'
                else:
                    line += str(chain.num_liberties())
            res += line + '\n'
        return res

    def decode_move(self, encode_move):
        encode_move = int(encode_move)
        size = int(self.size)
        row = encode_move // size
        col = encode_move % size
        return row, col

    def __str__(self):
        res = ' ' + '-' * (self.size * 2 + 1) + '\n'
        print(res)
        for i in range(self.size - 1, -1, -1):
            line = '|'
            for j in range(0, self.size):
                stone = self.board.get((i, j))
                if stone is None:
                    line += ' .'
                elif stone == Color.black:
                    line += ' X'
                elif stone == Color.white:
                    line += ' O'
            res += line + ' |\n'
        res += ' ' + '-' * (self.size * 2 + 1) + '\n'
        return res

    @staticmethod
    def get_from_string(board_str):
        rows = [line.strip() for line in board_str.strip().split('\n')]
        rows.reverse()
        board = Board(len(rows))
        for i, row in enumerate(rows):
            for j, color in enumerate(row):
                if color == 'w':
                    board.move(Color.white, (i, j))
                elif color == 'b':
                    board.move(Color.black, (i, j))
        return board
