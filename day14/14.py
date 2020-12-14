#!/usr/local/bin/python3

import re

def load_program(location):
  bitmasks = []
  bitmask = None
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      match = re.search("^mask = (.{36})$", line)
      if match != None:
        if bitmask != None:
          bitmasks.append(bitmask)
        bitmask = (process_bitmask(match[1]), [])
      else:
        match = re.search("^mem\[(\d*)\] = (\d*)$", line)
        bitmask[1].append((int(match[1]), int(match[2])))
  bitmasks.append(bitmask)
  return bitmasks

def process_bitmask(bitmask):
  result = []
  for i, c in enumerate(bitmask):
    if c != "X":
      result.append((int(c), int(len(bitmask) - (i + 1))))
  return result

def set_bit(value, bit_index):
  return value | (1 << bit_index)

def clear_bit(value, bit_index):
  return value & ~(1 << bit_index)

def apply_bitmask(value, bitmask):
  for i in bitmask:
    if i[0] == 1:
      value = set_bit(value, i[1])
    elif i[0] == 0:
      value = clear_bit(value, i[1])
  return value

def find_base_value(value, bitmask):
  bin_value = list(str(bin(value))[2:].zfill(36))
  for i, c in enumerate(bitmask):
    if c == "1":
      bin_value[i] = "1"
    elif c == "X":
      bin_value[i] = "0"
    value = int("".join(bin_value), 2)
  return value

def generate_or_list(bitmask):
  or_list = []
  for i, c in enumerate(bitmask):
    if c == "X":
      or_list.append(1 << i)
  return or_list

def calculate_locations(value, bitmask):
  locations = []
  current_mask = ""
  bit_positions = [i[1] for i in bitmask]
  bit_values = [i[0] for i in bitmask]
  for i in range(0, 36):
    if i not in bit_positions:
      current_mask += "X"
    else:
      current_mask +=  str(bit_values[bit_positions.index(i)])
  print(current_mask[::-1])
  base_value = find_base_value(value, current_mask[::-1])
  print(str(base_value))
  locations.append(base_value)
  or_list = generate_or_list(current_mask)
  print(or_list)
  prev_results = []
  for x in or_list:
    temp_list = []
    locations.append(base_value | x)
    for y in prev_results:
      locations.append(base_value | x + y)
      temp_list.append(x + y)
    temp_list.append(x)
    prev_results.extend(temp_list)
  return locations

def process_program(location):
  memory = dict()
  bitmasks = load_program(location)
  for bitmask in bitmasks:
    for mem_operation in bitmask[1]:
      memory[mem_operation[0]] = apply_bitmask(mem_operation[1], bitmask[0])
  print(location + " - Memory sum: " + str(sum(memory.values())))

def process_program_pt2(location):
  memory = dict()
  bitmasks = load_program(location)
  for bitmask in bitmasks:
    for mem_operation in bitmask[1]:
      locations = calculate_locations(mem_operation[0], bitmask[0])
      print(locations)
      for l in locations:
        memory[l] = mem_operation[1]
  print(location + " - Memory sum: " + str(sum(memory.values())))
  
process_program("14-test.txt")
process_program("14-input.txt")
process_program_pt2("14-test-02.txt")
process_program_pt2("14-input.txt")
