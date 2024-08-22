import checkers_and_minimax_python_module as module ### import checkers c++ module
import random
from draughts.core.game import Game, Board
from damas.board import Board as damasBoard
from damas.display import Display
from damas.loop import loop
from damas.player import RandomPlayer
import time
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np



display = Display()
def play_damas_random_game(_seed):
    board = damasBoard()
    player_w = RandomPlayer(board, player=+1, seed=_seed)
    player_b = RandomPlayer(board, player=-1, seed=_seed)
    wins, turns = loop(board, display, player_w, player_b)


play_damas_random_game()
