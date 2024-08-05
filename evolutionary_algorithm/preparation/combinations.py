import numpy as np
from game.constants import NOT_USED, EMPTY, WHITE, BLACK, fields_in_use

board_size = 8
game_board = np.empty(board_size*board_size)
values = [EMPTY, WHITE, BLACK]

MIN_PAWNS = 2
MAX_PAWNS = 7


class _Combinations:
    """Base class for generating all possible subboard outcomes"""
    def __init__(self, size, val):
        self.size = size
        self.count = board_size - self.size + 1
        self.subboards = self.get_subboards()
        self.values = val
        self.result = {}

    def get_single(self, start):
        """Returns key for single subboard"""
        return tuple([start + y + x * board_size for x in range(self.size) for y in range(self.size)])

    def get_subboards(self):
        """Returns list of all keys"""
        return [self.get_single(x * board_size + y) for x in range(self.count) for y in range(self.count)]

    def fun(self, board):
        """Returns all possible values for single subboard"""
        acc = [[]]
        for elem in board:
            if elem not in fields_in_use:
                acc = [a + [NOT_USED] for a in acc]
            else:
                acc = [a + [v] for v in self.values for a in acc]
        return acc

    def filter_function(self, x):
        """Placeholder for board conditions"""
        return True

    def combination(self, debug=False):
        """
        Sets final result to *result* attribute
            If debug variable is set to true, returns list with all values apart keys
        """
        def fold(f, lst, acc):
            if len(lst) == 0:
                return acc
            return fold(f, lst[1:], acc + f(lst[0]))
        if debug:
            return fold(lambda x: list(filter(self.filter_function, self.fun(x))), self.subboards, [])
        else:
            self.result = {x: list(filter(self.filter_function, self.fun(x))) for x in self.subboards}


class Twos(_Combinations):
    def __init__(self):
        super().__init__(size=2, val=values)


class Threes(_Combinations):
    def __init__(self):
        super().__init__(size=3, val=values)


class Fourths(_Combinations):
    def __init__(self):
        super().__init__(size=4, val=values)

    def filter_function(self, x):
        return MIN_PAWNS <= self.size * self.size * 0.5 - x.count(EMPTY) <= MAX_PAWNS
