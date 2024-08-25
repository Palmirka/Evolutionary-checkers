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
        path2x2_kings = '/../../data_analysis_scripts/board_analizer/boards_analyse_2x2_32897_games_with_kings_cut.txt'
        path3x3_kings = '/../../data_analysis_scripts/board_analizer/boards_analyse_3x3_32897_games_with_kings_cut.txt'
        path4x4_kings = '/../../data_analysis_scripts/board_analizer/boards_analyse_4x4_32897_games_with_kings_cut.txt'

        with open(os.path.dirname(__file__) + path2x2, 'rb') as handle:
            self.dict_pawns = pickle.load(handle)
        with open(os.path.dirname(__file__) + path3x3, 'rb') as handle:
            self.dict_pawns.update(pickle.load(handle))
        with open(os.path.dirname(__file__) + path4x4, 'rb') as handle:
            self.dict_pawns.update(pickle.load(handle))
        with open(os.path.dirname(__file__) + path2x2_kings, 'rb') as handle:
            self.dict_kings = pickle.load(handle)
        with open(os.path.dirname(__file__) + path3x3_kings, 'rb') as handle:
            self.dict_kings.update(pickle.load(handle))
        with open(os.path.dirname(__file__) + path4x4_kings, 'rb') as handle:
            self.dict_kings.update(pickle.load(handle))
        self.size_p, self.usage_p, self.values_white_p_p, self.values_black_p_p, _, _ = binary_of_keys(
            self.dict_pawns)
        self.size_k, self.usage_k, self.values_white_p_k, self.values_black_p_k, \
            self.values_white_k_k, self.values_black_k_k = binary_of_keys(self.dict_kings)
        print('Size pawns, size kings: ', self.size_p, self.size_k)

    def function(self, game: Engine, coefficients: np.ndarray, diff: int, is_king: bool) -> float:
        """Fitness function that grades actual board state"""
        if is_king:
            masks = bin(check_board(game.white_pieces(), game.black_pieces(), game.white_kings(), game.black_kings(),
                                    self.usage_k, self.values_white_p_k, self.values_black_p_k, self.values_white_k_k,
                                    self.values_black_k_k, self.size_k))[2:].zfill(self.size_k)
        else:
            masks = bin(check_board(game.white_pieces(), game.black_pieces(), 0, 0,
                                    self.usage_p, self.values_white_p_p, self.values_black_p_p, {i: 0 for i in range(64)}, {i: 0 for i in range(64)},
                                    self.size_p))[2:].zfill(self.size_p)
            # print(masks)

        result = sum([c if masks[idx] == '1' else 0 for idx, c in enumerate(coefficients)])
        result += diff * (2 * bin(game.white_pieces()).count('1') + 3 * bin(game.white_kings()).count('1') -
                          2 * bin(game.black_pieces()).count('1') - 3 * bin(game.black_kings()).count('1'))

        return result
