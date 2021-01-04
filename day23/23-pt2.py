#!/usr/local/bin/python3

def select_destination(current_cup, pickup):
  cups_max = 1000000
  result =  current_cup - 1
  if result is 0:
      result = cups_max
  while result in pickup:
    result -= 1
    if result is 0:
      result = cups_max
  return result

def play_cup_game(cups, r):
  cup_dict = dict()
  cups_len = len(cups)
  for cup in cups:
    cup_dict[cup] = cups[(cups.index(cup) + 1) % cups_len]
  cup_dict[cups[-1]] = 10
  cups_len = 1000000
  for i in range(10, cups_len + 1):
    cup_dict[i] = i+1
  cup_dict[cups_len] = cups[0]
  current_cup = None
  for t in range(r):
    if current_cup is None:
      current_cup = cups[0]
    else:
      current_cup = cup_dict[current_cup]
    pickup = [cup_dict[current_cup]]
    for _ in range(2):
      pickup.append(cup_dict[pickup[-1]])
    destination = select_destination(current_cup, pickup)
    cup_dict[current_cup] = cup_dict[pickup[-1]]
    temp = cup_dict[destination]
    cup_dict[destination] = pickup[0]
    cup_dict[pickup[-1]] = temp
  print(cup_dict[1])
  print(cup_dict[cup_dict[1]])
  print(cup_dict[1] * cup_dict[cup_dict[1]])

play_cup_game([3,8,9,1,2,5,4,6,7], 10000000)
play_cup_game([4,6,7,5,2,8,1,9,3], 10000000)
