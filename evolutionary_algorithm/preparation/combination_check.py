from game.constants import WHITE, BLACK
from evolutionary_algorithm.preparation.masking import binary_of_keys


def dictionary_size(dictionary):
    return sum([len(values) for values in dictionary.values()])


def check_board(board_white, board_black, dictionary):
    """
        Checks which combinations are present on board

        :param int board_white:     Board situation from white player perspective
        :param int board_black:     Board situation from black player perspective
        :param int dict dictionary: Combinations data
        :return:                    Mask of combinations which are present on board
        :rtype:                     int
    """
    MAX = (1 << dictionary_size(dictionary)) - 1

    def get_single_check(board, color):
        binary_keys, binary_values = binary_of_keys(dictionary, color)
        combination_check = MAX
        for key, value in binary_values.items():
            usage = binary_keys[key]
            mask = MAX if (board >> 63 - key) % 2 else 0
            combination_check &= ~(mask ^ value) | ~usage
        return combination_check

    return get_single_check(board_white, WHITE) & get_single_check(board_black, BLACK)
