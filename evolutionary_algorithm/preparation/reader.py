import pickle


def read_file(file_path, range_to_delete):
    """
    Read file with game analize

    :param str file_path: Path to file with game analize
    :param int range_to_delete: how often an item must occur to be counted
    :return[0]: dict in form {(square): [[psoition1],[position2],...]}
    :return[1]: number of poses counted
    :rtype[0]: dict
    :rtype[1]: int
    """
    counter = 0
    result = {}
    with open(file_path, 'rb') as handle:
        dictionary = pickle.loads(handle.read())
    for key1 in dictionary.keys():
        value_list = []
        for key2, value in dictionary[key1].items():
            if dictionary[key1][key2] > range_to_delete:
                value_list.append(list(key2))
                counter += 1
        result[key1] = value_list
    return result, counter


# file_path_4x4 = "boards_analyse_4x4_32897_games.txt"
# file_path_3x3 = "boards_analyse_3x3_32897_games.txt"
# file_path_2x2 = "boards_analyse_2x2_32897_games.txt"
#
# dict_2x2 = read_file(file_path_2x2, 0)
# dict_3x3 = read_file(file_path_3x3, 512)
# dict_4x4 = read_file(file_path_4x4, 2048)
# print(dict_2x2[0])
