#!/usr/local/bin/python3

import re

class BoardingCard:
  row_string = None
  row_location = None
  column_string = None
  column_location = None
  seat_id = 0

  def __init__(self, input):
    match = re.search("^([BF]{7})([RL]{3})$", input)
    self.row_string = match[1].replace("B","1").replace("F","0")
    self.column_string = match[2].replace("R","1").replace("L","0")
    self.row_location = int(self.row_string, 2)
    self.column_location = int(self.column_string, 2)
    self.seat_id = self.row_location * 8 + self.column_location
    
  def print(self):
    print("Row Location(binary): " + self.row_string + " Column Location(binary): " + self.column_string)
    print("Row Location        : " + str(self.row_location).zfill(7) + " Column Location        : " + str(self.column_location).zfill(3))
    print("Seat Id: " + str(self.seat_id).zfill(3))

def load_boarding_cards(location):
  boarding_cards = []
  with open(str(location), 'r') as file:
    for line in file:
      card = BoardingCard(line.rstrip())
      boarding_cards.append(card)
  return boarding_cards

def process_file(location, part_2):
  debug = False
  max_seat_id = 0
  boarding_cards = load_boarding_cards(location)
  boarding_cards.sort(key=lambda c: c.seat_id)
  if debug:
    for boarding_card in boarding_cards:
      boarding_card.print()
  max_seat_id = boarding_cards[-1].seat_id
  print(location + " - Max Seat Id: " + str(max_seat_id))
  if part_2:
    i = 0
    while i < max_seat_id:
      if boarding_cards[i+1].seat_id > boarding_cards[i].seat_id + 1:
        print("Missing seat id: " + str(boarding_cards[i].seat_id + 1).zfill(3))
        break;
      i += 1

process_file("05-test.txt", False)
process_file("05-input.txt", True)
