# from pydraughts.draughts.core.board import Board
from pydraughts.draughts.core.game import Game
# from pydraughts.draughts.core.move import StandardMove
from pydraughts.draughts.PDN import PDNReader
import re
from typing import List, Dict, Any
import time
import pickle
import os
from tqdm import tqdm 
from typing import Set

path_to_pdn_directory = "..\\dataset_downloader\\games"

GLOBAL_DICT = {}
GLOBAL_DICT_2x2 = {}
GLOBAL_DICT_3x3 = {}
VISITED: Set[str] = set()

notation_board_checkers = [29,-1,30,-1,31,-1,32,-1,
                           -1,25,-1,26,-1,27,-1,28,
                           21,-1,22,-1,23,-1,24,-1,
                           -1,17,-1,18,-1,19,-1,20,
                           13,-1,14,-1,15,-1,16,-1,
                           -1, 9,-1,10,-1,11,-1,12,
                            5,-1, 6,-1, 7,-1, 8,-1,
                           -1, 1,-1, 2,-1, 3,-1, 4]

def flatmove(move):
    flat = re.split('-|x', move)
    #print(flat)
    _from = flat[0]
    _to = flat[1]
    if(len(_from) == 1 ): _from = f'0{_from}'
    if(len(_to) == 1 ): _to = f'0{_to}'
    return [[int(_from), int(_to)]]

def get_sequence(move, moves):
    seq = moves
    for s in seq[0]:
        if len(s)>1:
            if move[0][0] == s[0][0] and move[-1][-1] == s[-1][-1]:
                return s
    return flatmove(m)


def make_all_combinations_first():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
            for c in range(0,3):
                for d in range(0,3):
                    for e in range(0,3):
                        for f in range(0,3):
                            for g in range(0,3):
                                for h in range(0,3):
                                    dict.update({(a,-1,b,-1, -1,c,-1,d, e,-1,f,-1, -1,g,-1,h):0})
    return dict

def make_all_combinations_second():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
            for c in range(0,3):
                for d in range(0,3):
                    for e in range(0,3):
                        for f in range(0,3):
                            for g in range(0,3):
                                for h in range(0,3):
                                    dict.update({(-1,a,-1,b, c,-1,d,-1, -1,e,-1,f, g,-1,h,-1):0})
    return dict                                   
    
def make_all_combinations_first_2x2():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
            for c in range(0,3):
                for d in range(0,3):
                    for e in range(0,3):
                        dict.update({(a,-1,b, -1,c,-1, d,-1,e):0})
    return dict

def make_all_combinations_first_3x3():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
            for c in range(0,3):
                for d in range(0,3):
                    for e in range(0,3):
                        dict.update({(a,-1,b, -1,c,-1, d,-1,e):0})
    return dict

def make_all_combinations_second_3x3():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
            for c in range(0,3):
                for d in range(0,3):
                    for e in range(0,3):
                        dict.update({(-1,a,-1, b,-1,c, -1,e,-1):0})
    return dict                                  

def make_all_combinations_first_2x2():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
                        dict.update({(a,-1, -1,b):0})
    return dict 

def make_all_combinations_second_2x2():
    dict = {}
    for a in range(0,3):
        for b in range(0,3):
                        dict.update({(-1,a, b,-1):0})
    return dict 

def make_dict():
    dict = {}
    f = make_all_combinations_first()
    s = make_all_combinations_second()
    for k in range(0,5):
            for i in range(k*8,(k*8)+5):
                if (k%2==0 and i%2==0) or (k%2==1 and i%2==1):
                    dict.update({(i,i+1,i+2,i+3, i+8,i+8+1,i+8+2,i+8+3, i+16,i+16+1,i+16+2,i+16+3, i+24,i+24+1,i+24+2,i+24+3):f.copy()})
                else:
                    dict.update({(i,i+1,i+2,i+3, i+8,i+8+1,i+8+2,i+8+3, i+16,i+16+1,i+16+2,i+16+3, i+24,i+24+1,i+24+2,i+24+3):s.copy()})
    return dict

def make_dict_3x3():
    dict = {}
    f = make_all_combinations_first_3x3()
    s = make_all_combinations_second_3x3()
    for k in range(0,6):
            for i in range(k*8,(k*8)+6):
                if (k%2==0 and i%2==0) or (k%2==1 and i%2==1):
                    dict.update({(i,i+1,i+2, i+8,i+8+1,i+8+2, i+16,i+16+1,i+16+2):f.copy()})
                else:
                    dict.update({(i,i+1,i+2, i+8,i+8+1,i+8+2, i+16,i+16+1,i+16+2):s.copy()})
    return dict

def make_dict_2x2():
    dict = {}
    f = make_all_combinations_first_2x2()
    s = make_all_combinations_second_2x2()
    for k in range(0,7):
            for i in range(k*8,(k*8)+7):
                if (k%2==0 and i%2==0) or (k%2==1 and i%2==1):
                    dict.update({(i,i+1, i+8,i+8+1):f.copy()})
                else:
                    dict.update({(i,i+1, i+8,i+8+1):s.copy()})
    return dict               

    

def fill_dict(game):
    position_pieces = game.board.searcher.position_pieces
    searcher = game.board.searcher
    def fd(id):
        pos = notation_board_checkers[id]
        if pos == -1:
            return -1
        elif(position_pieces.get(pos) is not None):
            return position_pieces.get(pos).player
        else:
            return 0
    def isKing(l):
        for pos in l:
            # piece = searcher.get_piece_by_position(notation_board_checkers[pos])
            piece = position_pieces.get(notation_board_checkers[pos])
            if piece is not None and piece.king == True:
                if pos//8 == 0 and piece.player == 1: #promocja czarnych
                    return True
                if pos//8 == 7 and piece.player == 2: #promocja bialych
                    return True
        return False
    for k in range(0,7):
        for i in range(k*8,(k*8)+7):
            if k<5 and i<(k*8)+5:
                key   = (i,i+1,i+2,i+3, i+8,i+8+1,i+8+2,i+8+3, i+16,i+16+1,i+16+2,i+16+3, i+24,i+24+1,i+24+2,i+24+3)
                value = (fd(i),fd(i+1),fd(i+2),fd(i+3), fd(i+8),fd(i+8+1),fd(i+8+2),fd(i+8+3), fd(i+16),fd(i+16+1),fd(i+16+2),fd(i+16+3), fd(i+24),fd(i+24+1),fd(i+24+2),fd(i+24+3))
                GLOBAL_DICT[key][value] += 1
                if k == 4 and isKing([i+24,i+24+1,i+24+2,i+24+3]):
                    # print("4x4: ", i)
                    GLOBAL_DICT[key][value] += 1000
                if k == 0 and isKing([i,i+1,i+2,i+3]):
                    # print("4x4: ", i)
                    GLOBAL_DICT[key][value] += 1000
            if k<6 and i<(k*8)+6:
                key3x3   = (i,i+1,i+2, i+8,i+8+1,i+8+2, i+16,i+16+1,i+16+2)
                value3x3 = (fd(i),fd(i+1),fd(i+2), fd(i+8),fd(i+8+1),fd(i+8+2), fd(i+16),fd(i+16+1),fd(i+16+2))
                GLOBAL_DICT_3x3[key3x3][value3x3] += 1
                if k == 5 and isKing([i+16,i+16+1,i+16+2]):
                    # print("3x3: ", i)
                    GLOBAL_DICT_3x3[key3x3][value3x3] += 1000
                if k == 0 and isKing([i,i+1,i+2]):
                    # print("3x3: ", i)
                    GLOBAL_DICT_3x3[key3x3][value3x3] += 1000
            key2x2   = (i,i+1, i+8,i+8+1)
            value2x2 = (fd(i),fd(i+1), fd(i+8),fd(i+8+1))
            GLOBAL_DICT_2x2[key2x2][value2x2] += 1
            if k == 6 and isKing([i+8,i+8+1]):
                # print("2x2: ", i)
                GLOBAL_DICT_2x2[key2x2][value2x2] += 1000
            if k == 0 and isKing([i,i+1]):
                # print("2x2: ", i)
                GLOBAL_DICT_2x2[key2x2][value2x2] += 1000
    #return [[key,value], [key3x3, value3x3], [key2x2, value2x2]]
            
  
  
GLOBAL_DICT = make_dict()
GLOBAL_DICT_3x3 = make_dict_3x3()
GLOBAL_DICT_2x2 = make_dict_2x2()


pdn_files = os.listdir(path_to_pdn_directory)
# pdn_files = ["1.pdn"]

files_counter = len(pdn_files)
counter = 0
for pdn_file,i in zip(pdn_files, tqdm (range(files_counter), desc="Loading…",  ascii=False, ncols=75)):
    games = PDNReader(filename=path_to_pdn_directory + "\\" + pdn_file)
    for game1 in games.games:
        #game1 = games.games[0]
        fen = game1.tags['FEN']
        link = game1.tags['Site']
        if link in VISITED:
            pass
        else:
            VISITED.add(link)
        moves = game1.moves
        game = Game(variant='brazilian', fen=fen)
        fill_dict(game)
        for m in moves:
            promotion_in_that_move = False
            try:
                _move = flatmove(m)
                piece_to_move = game.board.searcher.get_piece_by_position(_move[0][0])
                is_king_to_move = piece_to_move.king
                if is_king_to_move == True: # ruch damką
                    break
                game.push(get_sequence(_move, game.legal_moves()))
            #     piece_after_move = game.board.searcher.get_piece_by_position(move[-1][-1])
            #     is_king_after_move = piece_after_move.king
            #     if is_king_after_move == True and is_king_to_move == False: # promocja na damke
            #         promotion_in_that_move = True
            except:
                pass
            # keys = fill_dict(game)
            # if promotion_in_that_move == True:
            #     GLOBAL_DICT[keys[0]][keys[1]] += 1000
            fill_dict(game)
        counter += 1
        if counter%1000 == 0:
            with open('boards_analyse_' + str(counter) + '_games.txt', 'wb') as handle:
                pickle.dump(GLOBAL_DICT, handle)

with open('boards_analyse_4x4_' + str(counter) + '_games.txt', 'wb') as handle:
  pickle.dump(GLOBAL_DICT, handle)
  
with open('boards_analyse_3x3_' + str(counter) + '_games.txt', 'wb') as handle:
  pickle.dump(GLOBAL_DICT_3x3, handle)
  
with open('boards_analyse_2x2_' + str(counter) + '_games.txt', 'wb') as handle:
  pickle.dump(GLOBAL_DICT_2x2, handle)



# with open('file.txt', 'rb') as handle:
#     b = pickle.loads(handle.read())
    
# for key1 in b.keys():
#     for key2 in b[key1].keys():
#         if b[key1][key2] >= 20 :
#                 print(str(key1) + " " + str(key2) + ":" + str(b[key1][key2]))


