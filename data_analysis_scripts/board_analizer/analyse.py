from pydraughts.draughts.core.game import Game
from pydraughts.draughts.PDN import PDNReader
from typing import List, Dict, Any
import pickle
from collections import Counter

file_path = "boards_analyse_4x4_32897_games.txt"
file_path_3x3 = "boards_analyse_3x3_32897_games.txt"
file_path_2x2 = "boards_analyse_2x2_32897_games.txt"

range_to_delete = 50 # pozycje któe wystąpiły mniej niż {range_to_delete} 
                     # razy, zostana usuniete


with open(file_path, 'rb') as handle:
    dictionary = pickle.loads(handle.read())
with open(file_path_3x3, 'rb') as handle:
    dictionary_3x3 = pickle.loads(handle.read())
with open(file_path_2x2, 'rb') as handle:
    dictionary_2x2 = pickle.loads(handle.read()) 
# for key1 in dictionary.keys():
#     for key2 in dictionary[key1].keys():
#         if dictionary[key1][key2] <= 10 :
#                 print(str(key1) + " " + str(key2) + ":" + str(dictionary[key1][key2]))

all_counter = 0
for key1 in dictionary.keys():
    all_counter += len(dictionary[key1].keys())
print("wszystkie kombinacje:    ", all_counter)

all_with_statement_counter = 0
# for key1 in dictionary.keys():
#     print(Counter(dictionary[key1].values()))
#     for r in range(range_to_delete+1):
#         all_with_statement_counter += Counter(dictionary[key1].values())[r]
        
for key1 in dictionary.keys():
    for key2 in dictionary[key1].keys():
        if dictionary[key1][key2] <= range_to_delete :
                all_with_statement_counter+=1
                # print(str(key1) + " " + str(key2) + ":" + str(dictionary[key1][key2]))
print("Kombinacje do usunięcia: ", all_with_statement_counter)
print("Zostanie kombinacji:     ", all_counter-all_with_statement_counter)

all_counter_3x3 = 0
for key1 in dictionary_3x3.keys():
    all_counter_3x3 += len(dictionary_3x3[key1].keys())
print("wszystkie kombinacje:    ", all_counter_3x3)
all_with_statement_counter = 0
for key1 in dictionary_3x3.keys():
    for key2 in dictionary_3x3[key1].keys():
        if dictionary_3x3[key1][key2] <= range_to_delete :
                all_with_statement_counter+=1
print("Kombinacje do usunięcia: ", all_with_statement_counter)
print("Zostanie kombinacji:     ", all_counter_3x3-all_with_statement_counter)

all_counter_2x2 = 0
for key1 in dictionary_2x2.keys():
    all_counter_2x2 += len(dictionary_2x2[key1].keys())
print("wszystkie kombinacje:    ", all_counter_2x2)
all_with_statement_counter = 0
for key1 in dictionary_2x2.keys():
    for key2 in dictionary_2x2[key1].keys():
        if dictionary_2x2[key1][key2] <= range_to_delete :
                all_with_statement_counter+=1
print("Kombinacje do usunięcia: ", all_with_statement_counter)
print("Zostanie kombinacji:     ", all_counter_2x2-all_with_statement_counter)

print("4x4")
for r in range(1, 15):
    all_with_statement_counter = 0
    my_range = 2 ** r
    for key1 in dictionary.keys():
        for key2 in dictionary[key1].keys():
            if dictionary[key1][key2] <= my_range :
                    all_with_statement_counter+=1
    print("zakres: " + str(my_range) + " zostanie: " + str(all_counter-all_with_statement_counter))

print("3x3") 
for r in range(1, 15):
    all_with_statement_counter = 0
    my_range = 2 ** r
    for key1 in dictionary_3x3.keys():
        for key2 in dictionary_3x3[key1].keys():
            if dictionary_3x3[key1][key2] <= my_range :
                    all_with_statement_counter+=1
    print("zakres: " + str(my_range) + " zostanie: " + str(all_counter_3x3-all_with_statement_counter))

print("2x2")    
for r in range(1, 15):
    all_with_statement_counter = 0
    my_range = 2 ** r
    for key1 in dictionary_2x2.keys():
        for key2 in dictionary_2x2[key1].keys():
            if dictionary_2x2[key1][key2] <= my_range :
                    all_with_statement_counter+=1
    print("zakres: " + str(my_range) + " zostanie: " + str(all_counter_2x2-all_with_statement_counter))