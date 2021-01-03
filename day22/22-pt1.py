#!/usr/local/bin/python3

import re


def load_cards(location):
  player_one = []
  player_two = []
  player_one_finished = False
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      if line is "":
        player_one_finished = True
      else:
        match = re.search("^\d+$", line)
        if match is not None:
          if player_one_finished:
            player_two.append(int(line))
          else:
            player_one.append(int(line))
  return player_one, player_two

def play_round(player_one, player_two):
  player_one_card = player_one.pop(0)
  player_two_card = player_two.pop(0)
  
  if player_one_card > player_two_card:
    player_one.extend([player_one_card, player_two_card])
  elif player_two_card > player_one_card:
    player_two.extend([player_two_card, player_one_card])
  return player_one, player_two


def run_game(location):
  player_one, player_two = load_cards(location)
  winner = None
  winning_hand = None
  print("Player One: " + str(player_one)) 
  print("Player Two: " + str(player_two)) 
  game_complete = False
  while not game_complete:
    player_one, player_two = play_round(player_one, player_two)
    if len(player_one) == 0:
      winner = "player_two"
      winning_hand = player_two
      game_complete = True
    elif len(player_two) == 0:
      winner = "player_one"
      winning_hand = player_one
      game_complete = True

  print("Winner: " + winner)
  score = 0
  i = 1
  for card in winning_hand[::-1]:
    score += card * i
    i += 1
  print("Score: " + str(score))
  
  

run_game("22-test.txt")
run_game("22-input.txt")
