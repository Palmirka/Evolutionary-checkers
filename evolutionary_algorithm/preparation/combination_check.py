def check_board(board_white, board_black, board_w_king, board_b_king, usage, values_white, values_black,
                values_w_king, values_b_king, size):
    """
        Checks which combinations are present on board

        :param int board_white:     Placement of white pieces
        :param int board_black:     Placement of black pieces
        :param int board_w_king:    Placement of white kings
        :param int board_b_king:    Placement of white kings
        :param dict usage:          Usage of fields in certain combination
        :param dict values_white:   Binary combination data of white pieces
        :param dict values_black:   Binary combination data of black pieces
        :param dict values_w_king:  Binary combination data of white kings pieces
        :param dict values_b_king:  Binary combination data of black kings pieces
        :param int size:            Number of combinations

        :return:                    Mask of combinations which are present on board
        :rtype:                     int
    """
    MAX = (1 << size) - 1

    def get_single_check(board, binary_values):
        combination_check = MAX
        for key, value in binary_values.items():
            usage_mask = usage[key]
            mask = MAX if (board >> 63 - key) % 2 else 0
            combination_check &= ~(mask ^ value) | ~usage_mask
        return combination_check

    return get_single_check(board_white, values_white) & get_single_check(board_black, values_black) & \
        get_single_check(board_w_king, values_w_king) & get_single_check(board_b_king, values_b_king)
