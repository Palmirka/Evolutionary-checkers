from game.constants import BOARD_SIZE


def binary_of_keys(dict, color):
    """
        Change representation of data to binary

        :param dict dict: Original data in dictionary representation
        :param int color: Player color
        :return[0]:       directory of binary masks, each record includes single field. 1 is set when field is used in
                          certain combination
        :return[1]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes player color pawn on this field
        :rtype[0]:        {int : int} dict
        :rtype[1]:        {int : int} dict
    """

    result_usage = {idx: 0 for idx in range(64)}
    result_value = {idx: 0 for idx in range(64)}
    dict = {key: value for key, value in dict.items() if value}

    for key, combinations in dict.items():
        combinations_len = len(combinations)
        mask_usage = (1 << combinations_len) - 1
        if not combinations:
            continue
        for idx in range(BOARD_SIZE):
            result_usage[idx] <<= combinations_len
            mask_value = 0
            if idx in key:
                result_usage[idx] += mask_usage
                for c in combinations:
                    mask_value = (mask_value << 1) + (1 if c[key.index(idx)] == color else 0)
            result_value[idx] = (result_value[idx] << combinations_len) + mask_value
    return result_usage, result_value
