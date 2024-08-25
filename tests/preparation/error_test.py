from checkers_and_minimax_python_module import Engine
from game.constants import WHITE, BLACK
import numpy as np
from evolutionary_algorithm.preparation.masking import binary_of_keys
from evolutionary_algorithm.preparation.combination_check import check_board
from evolutionary_algorithm.base_functions.objective import Objective

objective = Objective()
engine = Engine()
engine.reset()

engine.print()
print(objective.dict_pawns)
masks = bin(check_board(engine.white_pieces(), engine.black_pieces(), engine.white_kings(), engine.black_kings(),
                        objective.usage_k, objective.values_white_p_k, objective.values_black_p_k,
                        objective.values_white_k_k, objective.values_black_k_k, objective.size_k))[2:].zfill(objective.size_k)
cpy = Engine(engine)
print(masks)
engine.act(engine.legal_moves()[0])
masks = bin(check_board(engine.white_pieces(), engine.black_pieces(), engine.white_kings(), engine.black_kings(),
                        objective.usage_k, objective.values_white_p_k, objective.values_black_p_k,
                        objective.values_white_k_k, objective.values_black_k_k, objective.size_k))[2:].zfill(objective.size_k)
print(masks)
# cpy.act(cpy.legal_moves()[0])
# masks = bin(check_board(cpy.white_pieces(), cpy.black_pieces(), 0, 0,
#                         objective.usage_p, objective.values_white_p_p, objective.values_black_p_p,
#                         objective.values_white_p_k, objective.values_black_p_k, objective.size_p))[2:].zfill(441)
# print('Cpy   ', masks)
coefficients = np.empty(441)
coefficients.fill(2)

# result = [c if masks[idx] == '1' else 0 for idx, c in enumerate(coefficients)]
# print(coefficients)
# print(result)
