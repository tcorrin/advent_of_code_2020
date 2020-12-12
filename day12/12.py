#!/usr/local/bin/python3

import re

def load_instructions(location):
  instruction_list = []
  with open(str(location), 'r') as file:
    for line in file:
      match = re.search("^([NSEWLRF])(\d*)$", line.rstrip())
      instruction_list.append((match[1], int(match[2])))
  return instruction_list

def process_instruction(instruction, x, y, direction):
  directions = ["N", "E", "S","W"]
  command = instruction[0]
  value = instruction[1]
  if command in directions:
    x, y = move(x, y, command, value)
  elif command == "F":
    x, y = move(x, y, direction, value)
  elif command == "R":
    direction = directions[ (directions.index(direction) + int(value / 90)) % len(directions)]
  elif command == "L":
    direction = directions[ (directions.index(direction) - int(value / 90)) % len(directions)]
  return x, y, direction

def process_waypoint(instruction, ship_x, ship_y, waypoint_x, waypoint_y):
  directions = ["N", "E", "S","W"]
  command = instruction[0]
  value = instruction[1]
  if command in directions:
    waypoint_x, waypoint_y = move(waypoint_x, waypoint_y, command, value)
  elif command == "F":
    ship_x += waypoint_x * value
    ship_y += waypoint_y * value
  else:
    turns = int(value / 90)
    for _ in range(turns):
      temp_x = waypoint_x
      temp_y = waypoint_y
      if command == "R":
        waypoint_x = temp_y
        waypoint_y = -temp_x
      elif command == "L":
        waypoint_x = -temp_y
        waypoint_y = temp_x
  return ship_x, ship_y, waypoint_x, waypoint_y

def move(x, y, direction, value):
  if direction == "N":
    y += value
  elif direction == "S":
    y -= value
  elif direction == "E":
    x += value
  elif direction == "W":
    x -= value
  return x, y

def process_file_stage01(location):
  instruction_list = load_instructions(location)
  x = 0
  y = 0
  direction = "E"
  for i in instruction_list:
    print("Command: " +  i[0] + " Value: " + str(i[1]))
    x, y, direction = process_instruction(i, x, y, direction)
    print("x: " + str(x) + " y: " + str(y) + " direction: " + direction)
  print(location + " - " + "Manhattan distance: " + str(abs(x) + abs(y)))

def process_file_stage02(location):
  instruction_list = load_instructions(location)
  ship_x = 0
  ship_y = 0
  waypoint_x = 10
  waypoint_y = 1
  for i in instruction_list:
    print("Command: " +  i[0] + " Value: " + str(i[1]))
    ship_x, ship_y, waypoint_x, waypoint_y = process_waypoint(i, ship_x, ship_y, waypoint_x, waypoint_y)
    print("ship_x: " + str(ship_x) + " ship_y: " + str(ship_y) + " waypoint_x:" + str(waypoint_x) + " waypoint_y:" + str(waypoint_y))
  print(location + " - " + "Manhattan distance: " + str(abs(ship_x) + abs(ship_y)))

process_file_stage01("12-test.txt")
process_file_stage01("12-input.txt")
process_file_stage02("12-test.txt")
process_file_stage02("12-input.txt")
