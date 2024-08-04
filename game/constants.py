NOT_USED = -1
EMPTY = 0
WHITE = 1
BLACK = 2
UNKNOWN = 3

BOARD_SIZE = 64

fields_in_use = [0, 2, 4, 6,
                 9, 11, 13, 15,
                 16, 18, 20, 22,
                 25, 27, 29, 31,
                 32, 34, 36, 38,
                 41, 43, 45, 47,
                 48, 50, 52, 54,
                 57, 59, 61, 63]

titles = {0: 'pawns',
          1: 'kings',
          2: 'safe pawns',
          3: 'attacking pawns',
          4: 'centrally positioned pawns',
          5: 'centrally positioned kings',
          6: 'king on double diagonal',
          7: 'bridge patterns',
          8: 'oreo patterns',
          9: 'triangle patterns',
          10: 'dog patterns',
          11: 'king in corner patters'}
