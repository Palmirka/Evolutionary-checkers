import checkers_and_minimax_python_module as module ### import checkers c++ module
import random


engine = module.Engine()
engine.reset()
while(engine.isFinished() < 0):
    engine.act(random.choice(engine.legal_moves_lists(engine)))
    engine.print()
print(engine.isFinished())

