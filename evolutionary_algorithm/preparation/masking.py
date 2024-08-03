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
    for key in dict.keys():
        combinations = len(dict[key])
        if combinations:
            for idx in result_value.keys():
                result_value[idx] <<= combinations
                result_usage[idx] <<= combinations
                mask_key = 2 ** combinations - 1
                if idx in key:
                    mask_value = 0
                    result_usage[idx] += mask_key
                    for c in dict[key]:
                        mask_value <<= 1
                        if c[key.index(idx)] == color:
                            mask_value += 1
                    result_value[idx] += mask_value
    return result_usage, result_value
