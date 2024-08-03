import unittest
import random
from game.constants import WHITE, BLACK
from evolutionary_algorithm.preparation.masking import binary_of_keys


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


def generate_result(dictionary, color):
    result_value = {idx: 0 for idx in range(64)}
    for key in dictionary.keys():
        for value in dictionary[key]:
            for idx in result_value.keys():
                result_value[idx] <<= 1
                if idx in key and value[key.index(idx)] == color:
                    result_value[idx] += 1
    return result_value


def generate_result_usage(dictionary):
    result = {idx: 0 for idx in range(64)}
    for key, value in dictionary.items():
        for _ in range(len(value)):
            for result_key in result.keys():
                result[result_key] <<= 1
                if result_key in key:
                    result[result_key] += 1
    return result


class BaseMaskingTest(object):
    """Base class for testing masking"""

    @staticmethod
    def num_to_bin(dictionary):
        return {key: bin(value) for key, value in dictionary.items()}

    def set_params(self, dictionary_data, result):
        self.result_keys, self.result_white_values, self.result_black_values = result
        self.binary_keys_white, self.binary_values_white = binary_of_keys(dictionary_data, WHITE)
        self.binary_keys_black, self.binary_values_black = binary_of_keys(dictionary_data, BLACK)

    def testKeysConsistency(self):
        self.assertEqual(self.binary_keys_white, self.binary_keys_black,
                         'Different keys for different color and same data')

    def testKeysCorrectness(self):
        self.assertEqual(self.binary_keys_white, self.result_keys,
                         'Items separators set incorrectly')

    def testValuesWhite(self):
        self.assertEqual(self.binary_values_white, self.result_white_values,
                         'White values set incorrectly')

    def testValuesBlack(self):
        self.assertEqual(self.binary_values_black, self.result_black_values,
                         'Black values set incorrectly')


class StaticTest(unittest.TestCase, BaseMaskingTest):
    def setUp(self):
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

        result_d_white = {0: int(0b0110000000000000), 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                          8: 0, 9: int(0b0100100000000000), 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                          16: 0, 17: 0, 18: int(0b0000000000110000), 19: 0, 20: 0, 21: 0, 22: 0, 23: 0,
                          24: 0, 25: 0, 26: 0, 27: int(0b0000001010000000), 28: 0, 29: 0, 30: 0, 31: 0,
                          32: 0, 33: 0, 34: int(0b0000000000000001), 35: 0, 36: 0, 37: 0, 38: 0, 39: 0,
                          40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0,
                          52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}

        result_d_black = {0: int(0b0001100000000000), 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                          8: 0, 9: int(0b1010000000000001), 10: 0, 11: int(0b0000000111111000), 12: 0,
                          13: 0, 14: 0, 15: 0, 16: int(0b0000000000000001), 17: 0, 18: int(0b0000000000001011),
                          19: 0, 20: int(0b0000000111010000), 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
                          27: int(0b0000000001000000), 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0,
                          34: int(0b0000000000000010), 35: 0, 36: 0, 37: 0, 38: 0, 39: 0,
                          40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0,
                          52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}

        result_keys = {0: int(0b1111100000000000), 1: int(0b1111100000000000), 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
                       8: int(0b1111100000000111), 9: int(0b1111100000000111), 10: int(0b11111111111),
                       11: int(0b11111111111), 12: int(0b11111111000), 13: 0, 14: 0, 15: 0, 16: int(0b111),
                       17: int(0b111), 18: int(0b11111111111), 19: int(0b11111111111), 20: int(0b11111111000),
                       21: 0, 22: 0, 23: 0, 24: int(0b111), 25: int(0b111), 26: int(0b11111111111),
                       27: int(0b11111111111), 28: int(0b11111111000), 29: 0, 30: 0, 31: 0, 32: int(0b111),
                       33: int(0b111), 34: int(0b111), 35: int(0b111), 36: 0, 37: 0, 38: 0, 39: 0,
                       40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0,
                       52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}
        self.set_params(d, (result_keys, result_d_white, result_d_black))


class RandomTestTwo(unittest.TestCase, BaseMaskingTest):
    def setUp(self):
        d = generate_dict(2)
        result_keys = generate_result_usage(d)
        self.set_params(d, (result_keys, generate_result(d, WHITE), generate_result(d, BLACK)))


class RandomTestFour(unittest.TestCase, BaseMaskingTest):
    def setUp(self):
        d = generate_dict(4)
        result_keys = generate_result_usage(d)
        self.set_params(d, (result_keys, generate_result(d, WHITE), generate_result(d, BLACK)))


if __name__ == '__main__':
    unittest.main()
