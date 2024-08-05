import unittest
from game.constants import WHITE, BLACK
from evolutionary_algorithm.preparation.masking import binary_of_keys
from tests.preparation.static_data import DICTIONARY, USAGE, DICTIONARY_BLACK, DICTIONARY_WHITE
from tests.preparation.data_generator import generate_dict


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
        self.set_params(DICTIONARY, (USAGE, DICTIONARY_WHITE, DICTIONARY_BLACK))


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
