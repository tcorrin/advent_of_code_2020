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

def play_game(player_one, player_two):
  winner = 0
  played_rounds = []
  game_complete = False
  winning_hand = []
  
  while not game_complete:
    if (player_one, player_two) in played_rounds:
      winner = 1
      winning_hand = player_one
      break
    else:
      played_rounds.append((player_one.copy(), player_two.copy()))
    
    player_one, player_two = play_round(player_one, player_two)
 
    if len(player_one) is 0:
      winner = 2
      winning_hand = player_two
      game_complete = True
    elif len(player_two) is 0:
      winner = 1
      winning_hand = player_one
      game_complete = True
  
  return winner, winning_hand

def play_round(player_one, player_two):
  print("player_one deck: " + str(player_one))
  print("player_two deck: " + str(player_two))
  player_one_card = player_one.pop(0)
  player_two_card = player_two.pop(0)
  round_winner = 0
  print("player_one plays: " + str(player_one_card))
  print("player_two plays: " + str(player_two_card))
  

  if len(player_one) >= player_one_card and len(player_two) >= player_two_card:
    print("SUBGAME!")
    round_winner, _ = play_game(player_one[:player_one_card], player_two[:player_two_card])
  elif player_one_card > player_two_card:
    round_winner = 1
  elif player_two_card > player_one_card:
    round_winner = 2

  if round_winner is 1:
    player_one.extend([player_one_card, player_two_card])
  elif round_winner is 2:
    player_two.extend([player_two_card, player_one_card])

  print("Round Winner: " + str(round_winner))
  return player_one, player_two


def run_game(location):
  player_one, player_two = load_cards(location)
  
  winner, winning_hand = play_game(player_one, player_two)

  print("Winner: " + str(winner))
  print("Winning hand: " + str(winning_hand))
  score = 0
  i = 1
  for card in winning_hand[::-1]:
    score += card * i
    i += 1
  print("Score: " + str(score))

run_game("22-test.txt")
run_game("22-test-002.txt")
run_game("22-input.txt")
