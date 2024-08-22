import os
import numpy as np
import pickle
from evolutionary_algorithm.preparation.combination_check import check_board
from evolutionary_algorithm.preparation.masking import binary_of_keys
from checkers_and_minimax_python_module import Engine


class Objective:
    def __init__(self):
        path2x2 = '/../../data_analysis_scripts/board_analizer/boards_analyse_2x2_32897_games_cut.txt'
        path3x3 = '/../../data_analysis_scripts/board_analizer/boards_analyse_3x3_32897_games_cut.txt'
        path4x4 = '/../../data_analysis_scripts/board_analizer/boards_analyse_4x4_32897_games_cut.txt'

        with open(os.path.dirname(__file__) + path2x2, 'rb') as handle:
            self.dict = pickle.load(handle)
        with open(os.path.dirname(__file__) + path3x3, 'rb') as handle:
            self.dict.update(pickle.load(handle))
        with open(os.path.dirname(__file__) + path4x4, 'rb') as handle:
            self.dict.update(pickle.load(handle))
        self.size, self.usage, self.values_white, self.values_black, self.values_w_king, self.values_b_king = binary_of_keys(self.dict)
        print(self.size)

    def function(self, game: Engine, coefficients: np.ndarray) -> float:
        """Fitness function that grades actual board state"""

        masks = bin(check_board(game.white_pieces(), game.black_pieces(), game.white_kings(), game.black_kings(),
                                self.usage, self.values_white, self.values_black, self.values_w_king, self.values_b_king,
                                self.size))[2:].zfill(self.size)
        result = sum([c if masks[idx] == '1' else 0 for idx, c in enumerate(coefficients)])
        # result = bin(game.white_pieces()).count('1') - bin(game.black_pieces()).count('1')
        return result
