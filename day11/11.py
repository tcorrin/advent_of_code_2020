#!/usr/local/bin/python3

import copy

debug = False

def load_seat_plan(location):
  seat_plan = []
  with open(str(location), 'r') as file:
    for line in file:
       seat_plan.append(list(line.rstrip()))
  return seat_plan

def check_seat(x, y, seat_plan, changed, new_seat_plan, part_one):
  current_state = seat_plan[y][x]
  adjacent_seats = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
  adjacent_seat_count = 0
  empty_adjacent_seat_count = 0
  occupied_adjacent_seat_count = 0
  occupied_tol = 5
  for seat in adjacent_seats:
    new_x = x + seat[0]
    new_y = y + seat[1]
    while -1 < new_x < len(seat_plan[0]) and -1 < new_y < len(seat_plan):
      seat_state = seat_plan[new_y][new_x]
      if seat_state != ".":
        adjacent_seat_count += 1
        if seat_state == "L":
          empty_adjacent_seat_count += 1
        elif seat_state == "#":
          occupied_adjacent_seat_count += 1
        break
      if part_one:
        new_x = -1
        new_y = -1
        occupied_tol = 4
      else:
        new_x += seat[0]
        new_y += seat[1]
      
  if current_state == "L" and adjacent_seat_count == empty_adjacent_seat_count:
    changed = True
    new_seat_plan[y][x] = "#"
  elif current_state == "#" and occupied_adjacent_seat_count >= occupied_tol:
    changed = True
    new_seat_plan[y][x] = "L"
  
  return new_seat_plan, changed

def run_round(seat_plan, new_seat_plan, part_one):
  changed = False
  for x in range(0, len(seat_plan[0])):
    for y in range(0, len(seat_plan)):
      new_seat_plan, changed = check_seat(x, y, seat_plan, changed, new_seat_plan, part_one)
  return changed, new_seat_plan

def print_seat_plan(seat_plan):
  for line in seat_plan:
    print(str(line))

def process_seat_plan(location, part_one):
  changed = True
  rounds = 0
  seat_plan = load_seat_plan(location)
  new_seat_plan = copy.deepcopy(seat_plan)
  
  while changed:
    changed, new_seat_plan = run_round(seat_plan, new_seat_plan, part_one)
    seat_plan = copy.deepcopy(new_seat_plan)
    rounds += 1
    if debug:
      print("Changed: " + str(changed))
      print_seat_plan(seat_plan)
  
  print(location + " - stable after " + str(rounds)  + " rounds")
  print(location + " - Total occupied seats: " + str(sum(row.count("#") for row in seat_plan)))

process_seat_plan("11-test.txt", True)
process_seat_plan("11-input.txt", True)
process_seat_plan("11-test.txt", False)
process_seat_plan("11-input.txt", False)
