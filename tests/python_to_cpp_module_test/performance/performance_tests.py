import checkers_and_minimax_python_module as module ### import checkers c++ module
import random
from draughts.core.game import Game, Board
from damas.board import Board as damasBoard
from damas.display import NoDisplay
from damas.loop import loop
from damas.player import RandomPlayer
import time
from tabulate import tabulate
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def play_pydraughts_random_game():
    game = Game(variant='brazilian', fen="startpos")
    while not game.is_over():
        legal_moves = game.get_possible_moves()
        if legal_moves:
            game.move(random.choice(legal_moves))
        else:
            break

engine = module.Engine()
def play_engine_random_game():
    engine.reset()
    while(engine.isFinished() < 0):
        engine.act(random.choice(engine.legal_moves_lists(engine)))

display = NoDisplay()
def play_damas_random_game(_seed):
    board = damasBoard()
    player_w = RandomPlayer(board, player=+1, seed=_seed)
    player_b = RandomPlayer(board, player=-1, seed=_seed)
    wins, turns = loop(board, display, player_w, player_b)

headers = ["Liczba gier", "Nasz silnik", "Pydraughts", "Damas"]
table = []
round_len = 4
values1 = [0]
values2 = [0]
values3 = [0]
game_laps = [0]

no_laps = 501
for i in range(1,no_laps):
    laps_range = 10
    start1 = time.time()
    for _ in range(0,laps_range ):
        play_engine_random_game()
    end1 = time.time()
    values1.append(round(values1[-1] + (end1-start1), round_len))

for i in range(1,no_laps):
    laps_range = 10
    start2 = time.time()
    for _ in range(0,laps_range ):
        play_pydraughts_random_game()
    end2 = time.time()
    values2.append(round(values2[-1] + (end2-start2), round_len))

for i in range(1,no_laps):
    laps_range = 10
    start3 = time.time()
    for s in range(0,laps_range ):
        play_damas_random_game(s)
    end3 = time.time()
    values3.append(round(values3[-1] + (end3-start3), round_len))


for i in range(1,no_laps):
    laps_range = 10*i
    game_laps.append(laps_range)


    # table.append([laps_range, round(end1 - start1,round_len), round(end2 - start2,round_len), round(end3 - start3,round_len)])
    # print("games: " + str(laps_range) + " " + str() + " " + str(round(end2- start2, 2)))
# print(tabulate(table, headers=headers))

# xpoints = np.array([item[0] for item in table])
# ypoints_1 = np.array([item[1] for item in table])
# ypoints_2 = np.array([item[2] for item in table])
# ypoints_3 = np.array([item[3] for item in table])
# fig, ax = plt.subplots()
# plt.plot(xpoints, ypoints_1, label=headers[1])
# plt.plot(xpoints, ypoints_2, label=headers[2])
# plt.plot(xpoints, ypoints_3, label=headers[3])

xpoints = np.array(game_laps)
ypoints_1 = np.array(values1)
ypoints_2 = np.array(values2)
ypoints_3 = np.array(values3)


matplotlib.rcParams.update({'font.size': 25})
fig, ax = plt.subplots()
plt.plot(xpoints, ypoints_1, label=headers[1])
plt.plot(xpoints, ypoints_2, label=headers[2])
plt.plot(xpoints, ypoints_3, label=headers[3])

ax.set_title( 'Zestawienie czasu działania silników warcabowych')
ax.set_xlabel('Liczba gier')
ax.set_ylabel('Czas w sekundach')
plt.legend(prop={'size': 25})
plt.show()


print(values1[-1])
print(values2[-1])
print(values3[-1])