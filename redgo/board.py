from .sgf_parser import sgf


class Board:
    def __init__(self):
        pass

    @staticmethod
    def create_board(sgf_content):
        print(type(sgf_content))
        sgf_game = sgf.Sgf_game.from_string(sgf_content)
        print(sgf_game)
        return Board()
