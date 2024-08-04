import unittest
import random
from evolutionary_algorithm.preparation.combination_check import check_board
from game.constants import WHITE, BLACK, fields_in_use


def generate_dict(num_keys):
    def generate_keys():
        return tuple(sorted(random.sample(range(64), random.randint(4, 16))))

    def generate_values(size):
        return [random.randint(-1, 2) for _ in range(size)]

    random_dict = {}
    for _ in range(num_keys):
        key = generate_keys()
        value_length = random.randint(3, 5)  # Number of lists in the value
        value = [generate_values(len(key)) for _ in range(value_length)]
        random_dict[key] = value
    return random_dict


def generate_random_board():
    board = [0 for _ in range(64)]
    probability = random.random()
    for field in fields_in_use:
        if random.random() < probability:
            board[field] = 1
    return int(''.join(map(str, board)), 2) << 1


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
        board = int(0b0000000001000000000000000000000000000000000000000000000000000000)
        d = {(0, 1, 8, 9):
                 [[0, -1, -1, 2],
                  [1, -1, -1, 1],
                  [1, -1, -1, 2],
                  [2, -1, -1, 0],
                  [2, -1, -1, 1]],
             (10, 11, 12, 18, 19, 20, 26, 27, 28):
                 [[-1, 0, -1, 0, -1, 0, -1, 0, -1],
                  [-1, 0, -1, 0, -1, 0, -1, 1, -1],
                  [-1, 2, -1, 0, -1, 2, -1, 0, -1],
                  [-1, 2, -1, 0, -1, 2, -1, 1, -1],
                  [-1, 2, -1, 0, -1, 2, -1, 2, -1],
                  [-1, 2, -1, 1, -1, 0, -1, 0, -1],
                  [-1, 2, -1, 1, -1, 2, -1, 0, -1],
                  [-1, 2, -1, 2, -1, 0, -1, 0, -1]],
             (8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27, 32, 33, 34, 35):
                 [[-1, 0, -1, 0, 0, -1, 0, -1, -1, 0, -1, 0, 0, -1, 0, -1],
                  [-1, 0, -1, 0, 0, -1, 2, -1, -1, 0, -1, 0, 0, -1, 2, -1],
                  [-1, 2, -1, 0, 2, -1, 2, -1, -1, 0, -1, 0, 0, -1, 1, -1]]}
        result = int(0b10000000000)
        self.set_params(board, board, d, result)


class RandomTestTwo(unittest.TestCase, BaseCheckTest):
    def setUp(self):
        d = generate_dict(2)
        board_white, board_black = generate_random_board(), generate_random_board()
        result_keys = generate_result(board_white, board_black, d)
        self.set_params(board_white, board_black, d, result_keys)


if __name__ == '__main__':
    unittest.main()
