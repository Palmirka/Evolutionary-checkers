from game.constants import fields_in_use
from game.constants import WHITE, BLACK
from evolutionary_algorithm.preparation.reader import read_file

# file_path_4x4 = "boards_analyse_4x4_32897_games.txt"
# file_path_3x3 = "boards_analyse_3x3_32897_games.txt"
# file_path_2x2 = "boards_analyse_2x2_32897_games.txt"
#
# dict_2x2 = read_file(file_path_2x2, 0)
# dict_3x3 = read_file(file_path_3x3, 512)
# dict_4x4 = read_file(file_path_4x4, 2048)
#
# print(dict_4x4)
#
d = {(0, 1, 8, 9): [[0, -1, -1, 0], [0, -1, -1, 1], [0, -1, -1, 2], [1, -1, -1, 0], [1, -1, -1, 1], [1, -1, -1, 2],
                    [2, -1, -1, 0], [2, -1, -1, 1], [2, -1, -1, 2]],
     (1, 2, 9, 10): [[-1, 0, 0, -1], [-1, 0, 1, -1], [-1, 0, 2, -1], [-1, 1, 0, -1], [-1, 1, 1, -1], [-1, 1, 2, -1],
                     [-1, 2, 0, -1], [-1, 2, 1, -1], [-1, 2, 2, -1]],
     (12, 13, 20, 21): [[-1, 0, 0, -1], [-1, 0, 1, -1], [-1, 0, 2, -1], [-1, 1, 0, -1], [-1, 1, 1, -1], [-1, 1, 2, -1],
                        [-1, 2, 0, -1], [-1, 2, 1, -1], [-1, 2, 2, -1]]}

board = 11529215046068731905
# print(bin(board)[2:].zfill(64))

MAX = 2 ** 64 - 1


def binary_of_keys(dict, color):
    """
        Change representation of data to binary. Each volume in

        :param dict dict: Original data in dictionary representation
        :param int color: Player color
        :return[0]:       binary mask representing starting points of each key in result_value
        :return[1]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes player color pawn on this field
        :rtype[0]:        int
        :rtype[1]:        {int : int} dict
    """

    result_key = 0
    result_value = {idx: 0 for idx in range(64)}
    dict = {key: value for key, value in dict.items() if value}
    for key in dict.keys():
        combinations = len(dict[key])
        if combinations:
            result_key = (result_key + 1) << combinations + 1
            for idx in result_value.keys():
                result_value[idx] <<= combinations
                if idx in key:
                    mask = 0
                    for c in dict[key]:
                        mask <<= 1
                        if c[key.index(idx)] == color:
                            mask += 1
                    result_value[idx] += mask
    return result_key >> 1, result_value


def check_board(board):
    pass


def debug(dict, n):
    binary_keys, binary_white = binary_of_keys(dict, WHITE)
    binary_keys, binary_black = binary_of_keys(dict, BLACK)
    print(bin(binary_keys))
    print(binary_white)
    print({key: bin(value) for key, value in binary_white.items()})
    binary_white = {key: ~value ^ (value & (MAX if (board >> key) % 2 else 0))
                    for key, value in binary_white.items()}
    binary_black = {key: ~value ^ (value & (MAX if (board >> key) % 2 else 0))
                    for key, value in binary_black.items()}
    # print({key: bin(value)[2:].zfill(n) for key, value in binary_white.items()})


# dict = {}
# dict.update(dict_2x2[0])
# dict.update(dict_3x3[0])
# dict.update(dict_4x4[0])

# debug(dict, dict_2x2[1] + dict_3x3[1] + dict_4x4[1])

debug(d, 27)
