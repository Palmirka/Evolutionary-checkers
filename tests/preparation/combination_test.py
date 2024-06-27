import unittest
from evolutionary_algorithm.preparation.combinations import Twos, Threes, Fourths
from game.constants import fields_in_use


class BaseCombinationsTest(object):
    """Base class for testing combinations"""
    def set_params(self, obj, expected_length):
        self.obj = obj
        self.expected_length = expected_length

    def testLength(self):
        """Checks whether number of combination is equal calculated one"""
        self.assertEqual(len(self.obj.combination(debug=True)), self.expected_length)

    def testValuesLength(self):
        """Checks whether single value is right size"""
        self.obj.combination()
        for key, value in self.obj.result.items():
            for v in value:
                self.assertEqual(len(key), len(v))

    def testValidFields(self):
        """Checks whether invalid fields are set correctly"""
        self.obj.combination()
        for key, value in self.obj.result.items():
            expected = -len(value)
            result = [sum(t) for t in zip(*value)]
            for field in key:
                r_sum = result[key.index(field)]
                if field in fields_in_use:
                    self.assertGreater(r_sum, expected, msg=f'Assertion fails: {self.obj.__class__.__name__} at key: {key} at value {field}')
                else:
                    self.assertEqual(r_sum, expected, msg=f'Assertion fails: {self.obj.__class__.__name__} at key: {key} at value {field}')


class CombinationsTwosTest(unittest.TestCase, BaseCombinationsTest):
    def setUp(self):
        self.set_params(Twos(), 49 * 3 ** 2)


class CombinationsThreesTest(unittest.TestCase, BaseCombinationsTest):
    def setUp(self):
        self.set_params(Threes(), 18 * 3 ** 4 + 18 * 3 ** 5)


class CombinationsFourthsTest(unittest.TestCase, BaseCombinationsTest):
    def setUp(self):
        self.set_params(Fourths(), 25 * (3 ** 8 - 8 * 2 - 2 ** 8 - 1))


if __name__ == '__main__':
    unittest.main()
