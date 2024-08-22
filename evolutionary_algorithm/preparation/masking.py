from game.constants import BOARD_SIZE
from game.constants import WHITE, BLACK, WHITE_KING, BLACK_KING


def binary_of_keys(dict):
    """
        Change representation of data to binary

        :param dict dict: Original data in dictionary representation

        :return[0]:       number of combinations
        :return[1]:       directory of binary masks, each record includes single field. 1 is set when field is used in
                          certain combination
        :return[2]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes white pawn on this field
        :return[3]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes black pawn on this field
        :return[4]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes white king on this field
        :return[5]:       directory of binary masks, each record includes single field. 1 is set when combinations
                          includes black king on this field

        :rtype[0]:        int
        :rtype[1]:        {int : int} dict
        :rtype[2]:        {int : int} dict
        :rtype[3]:        {int : int} dict
        :rtype[4]:        {int : int} dict
        :rtype[5]:        {int : int} dict
    """

    result_usage = {idx: 0 for idx in range(64)}
    result_white = {idx: 0 for idx in range(64)}
    result_black = {idx: 0 for idx in range(64)}
    result_w_king = {idx: 0 for idx in range(64)}
    result_b_king = {idx: 0 for idx in range(64)}
    dict = {key: value for key, value in dict.items() if value}
    size = 0

    for key, combinations in dict.items():
        combinations_len = len(combinations)
        size += combinations_len
        mask_usage = (1 << combinations_len) - 1
        if not combinations:
            continue
        for idx in range(BOARD_SIZE):
            result_usage[idx] <<= combinations_len
            mask_black = 0
            mask_white = 0
            mask_b_king = 0
            mask_w_king = 0
            if idx in key:
                result_usage[idx] += mask_usage
                for c in combinations:
                    mask_white = (mask_white << 1) + (1 if c[key.index(idx)] == WHITE else 0)
                    mask_black = (mask_black << 1) + (1 if c[key.index(idx)] == BLACK else 0)
                    mask_w_king = (mask_w_king << 1) + (1 if c[key.index(idx)] == WHITE_KING else 0)
                    mask_b_king = (mask_b_king << 1) + (1 if c[key.index(idx)] == BLACK_KING else 0)
            result_white[idx] = (result_white[idx] << combinations_len) + mask_white
            result_black[idx] = (result_black[idx] << combinations_len) + mask_black
            result_w_king[idx] = (result_w_king[idx] << combinations_len) + mask_w_king
            result_b_king[idx] = (result_b_king[idx] << combinations_len) + mask_b_king
    return size, result_usage, result_white, result_black, result_w_king, result_b_king
