import pickle
import checkers_and_minimax_python_module as module
import dill
import random

def print_legal_moves(e):
    for m in e.legal_moves():
        print("["+str(getattr(m, "from"))+","+str(m.to)+"("+str(m.type)+")"+"],")


engine = module.Engine()
engine.reset()
for _ in range(0, 10):
    engine.act(random.choice(engine.legal_moves_lists(engine)))


with open('pickle', 'wb') as handle:
    pickle.dump(engine, handle)


with open('pickle', 'rb') as handle:
    unpickled_engine = pickle.loads(handle.read())

unpickled_engine.print()
print_legal_moves(unpickled_engine)


minimax = module.Minimax()
print(minimax.minimax_move(engine, 3, module.Color.WHITE).to)

with open('pickle_minimax', 'wb') as handle:
    pickle.dump(minimax, handle)


with open('pickle_minimax', 'rb') as handle:
    unpickled_minimax = pickle.loads(handle.read())

print(unpickled_minimax.minimax_move(engine, 3, module.Color.WHITE).to)
