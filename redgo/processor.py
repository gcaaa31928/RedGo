import fnmatch

from redgo.board import *
from .definitions import *
import zipfile


def find_files(directory, pattern='*.zip'):
    '''Recursively finds all files matching the pattern.'''
    files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            files.append(os.path.join(root, filename))
    return files


class Processor:
    def __init__(self):
        self.sgf_dir = os.path.join(ROOT_DIR, './kgs/')

    def handicap(self, board, sgf_game):
        if sgf_game.get_handicap():
            for move in sgf_game.get_root().get_setup_stones()[0]:
                board.move(Color.black, move)

    # def read_sgf_file_to_boards(self, file_path):
    #     boards = []
    #     with open(file_path, 'r') as content_file:
    #         content = bytes(content_file.read(), encoding='utf8')

    def simulate_sgf_content(self, sgf_content):
        sgf_game = sgf.Sgf_game.from_string(sgf_content)
        board = Board(19)
        self.handicap(board, sgf_game)
        for node in sgf_game.main_sequence_iter():
            color, move = node.get_move()
            if color is None or move is None:
                continue
            color = Color.black if color == 'b' else Color.white
            board.move(color, move)
        return board

    def derive_sgf_content(self, sgf_content):
        sgf_game = sgf.Sgf_game.from_string(sgf_content)
        board = Board(19)
        board_problems = []
        board_solution = []
        self.handicap(board, sgf_game)
        for node in sgf_game.main_sequence_iter():
            color, move = node.get_move()
            if color is None or move is None:
                continue
            problem, solution = board.get_features(color, move)
            board_problems.append(problem)
            board_solution.append(solution)
            color = Color.black if color == 'b' else Color.white
            board.move(color, move)
        return board_problems, board_solution

    def get_total_samples_in_zip(self, current_zip_file):
        current_zip = zipfile.ZipFile(current_zip_file)
        file_names = current_zip.namelist()
        all_probs = []
        all_sols = []
        for name in file_names:
            if name.endswith('.sgf'):
                sgf_content = current_zip.read(name)
                probs, sols = self.derive_sgf_content(sgf_content)
                all_probs.extend(probs)
                all_sols.extend(sols)
            print(name)
        return all_probs, all_sols

    def get_total_samples_in_dir(self):
        sgf_zips = find_files(self.sgf_dir)
        for sgf_zip in sgf_zips:
            probs, sols = self.get_total_samples_in_zip(sgf_zip)
            yield probs, sols
