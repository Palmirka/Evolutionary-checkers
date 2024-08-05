import unittest
from evolutionary_algorithm.preparation.combination_check import check_board
from game.constants import WHITE, BLACK
from tests.preparation.static_data import DICTIONARY, BOARD
from tests.preparation.data_generator import generate_dict, generate_random_board


def generate_result(board_white, board_black, d):
    result_white = 0
    result_black = 0
    for key, values in d.items():
        for value in values:
            for idx in range(len(key)):
                v = value[idx]
                result_white <<= 1
                result_black <<= 1
                if board_white >> (63 - key[idx]) % 2 and v == WHITE or \
                        board_white >> (63 - key[idx]) % 2 and v <= 0:
                    result_white += 1
                elif board_black >> (63 - key[idx]) % 2 and v == BLACK or \
                        board_black >> (63 - key[idx]) % 2 and v <= 0:
                    result_black += 1
    return result_white & result_black


class BaseCheckTest(object):
    """Base class for testing combination check"""

    def set_params(self, board_white, board_black, dictionary, result):
        self.result = result
        self.combinations = check_board(board_white, board_black, dictionary)

    def testValues(self):
        self.assertEqual(self.combinations, self.result,
                         'Different keys for different color and same data')


class StaticTest(unittest.TestCase, BaseCheckTest):
    def setUp(self):
        result = int(0b10000000000)
        self.set_params(BOARD, BOARD, DICTIONARY, result)


class RandomTestTwo(unittest.TestCase, BaseCheckTest):
    def setUp(self):
        d = generate_dict(2)
        board_white, board_black = generate_random_board(), generate_random_board()
        result_keys = generate_result(board_white, board_black, d)
        self.set_params(board_white, board_black, d, result_keys)


class RandomTestFour(unittest.TestCase, BaseCheckTest):
    def setUp(self):
        d = generate_dict(4)
        board_white, board_black = generate_random_board(), generate_random_board()
        result_keys = generate_result(board_white, board_black, d)
        self.set_params(board_white, board_black, d, result_keys)


if __name__ == '__main__':
    unittest.main()
