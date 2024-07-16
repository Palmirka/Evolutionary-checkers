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
