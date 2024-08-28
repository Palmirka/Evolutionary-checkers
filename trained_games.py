import checkers_and_minimax_python_module as module
import pickle
from game.constants import MAX_POINTS
from game.play import Play
from evolutionary_algorithm.base_functions.objective import Objective
from move_strategies.strategies import MoveStrategy

NO_GAMES = 200
path = 'game/trained_players/coefficients_28_08_evening.txt'

with open(path, 'rb') as handle:
    training = pickle.loads(handle.read())


engine = module.Engine()
engine.reset()
_play = Play(engine, training['pawns'][0], training['kings'][0], training['diff'][0],
              Objective().function, MoveStrategy(depth=3).minimax)

wins = 0
draws = 0
loose = 0
mean = 0
for i in range(0, NO_GAMES):
    result = _play.play(0,1)
    mean += result
    if result > 0:
        wins += 1
    elif result < 0: 
        loose -= 1
    else:
        draws += 1
mean /= NO_GAMES

print("wins: ", wins)
print("draws: ", draws)
print("loose: ", loose)
print("mean value of games: ", mean)