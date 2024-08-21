import requests                     # pip install requests
from bs4 import BeautifulSoup       # pip install beautifulsoup4
from tqdm import tqdm               # pip install tqdm
import ctypes
import os
from urllib import request

personalToken = 'k3EueV0EUmx6hdgn'  # Token wygenerowany dla konta

p_type = 'brazilian'                # rodzaj partii jakie rozpatrujemy
number_of_players = 200             # liczba graczy od któych pobierzemy partie - n pierwszych w rankingu
max_games = 500                     # max liczba gier pobieranych od jednego gracza
color = None                        # preferencja koloru rozgrywanej partii

# Parametry żądania
game_params = {
            'max':max_games,     
            'perfType':p_type,   
            'color': color,   
            'algebraic' : False   
          } 

# Nagłówki żądania zawierające token autoryzacyjny
headers = {
    'Authorization': 'Bearer ' + personalToken
}

# wczytywanie graczy
players = []
url_players = 'https://lidraughts.org/player/top/' + str(number_of_players) + '/' + str(p_type)
player_response = requests.get(url_players, timeout=20, headers=headers)
if player_response.status_code == 200:
    soup = BeautifulSoup(player_response.content, 'html.parser')
    find = soup.select('a[class*="user"]')
    for link in find:
        players.append(link.get("href")[3:])
else:
    print("Błąd:", player_response.status_code)
    print("Dla wczytywania graczy")

if os.name == 'nt':
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # blokuje wygaszanie ekranu/blokady od braku użytkowania
                                                                # (program przerwałby pobieranie)
                                                                # FUNKCJA WINDOWS

# wczytywanie gier graczy
f = open("dataset.txt", "w")
# players = players[160:]
# print(players)
for username,i in zip(players, tqdm (range (len(players)), desc="Loading…",  ascii=False, ncols=75)):
    print("\nWczytywanie partii gracza: " + username)
    url = 'https://lidraughts.org/api/games/user/' + username
    try:
        response = requests.get(url, headers=headers, params=game_params)
    except:
        print("Błąd podczas wysyłania żądania do partii gracza: " + username)
        print("Gracz pominięty")
        pass
    if response.status_code == 200:  
        # try:
        #     data = response.text
        #     for line in data.splitlines():
        #         if (not line.startswith('[')):
        #             if line.strip():
        #                 f.write(line + '\n')
        try:
            with open("games/"+username+".pdn", 'wb')as file:
                file.write(response.content)
        except:
            print("Błąd wczytania jednej partii gracza: " + username)
            pass
    else:
        print("Błąd:", response.status_code)
        print("Dla partii gracza:", username)
    print("Zakończenie wczytywania partii gracza: " + username)
   
print("Pobieranie zakończone")     
f.close()
if os.name == 'nt':
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000) # włącza na powrót wygaszanie