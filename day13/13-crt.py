#!/usr/local/bin/python3

import copy

def load_notes(location):
  bus_ids = []
  with open(str(location), 'r') as file:
    for line in file:
      bus_ids.append(line.split(","))
  return bus_ids

def calculate_mods(line):
  ids = dict()
  for i, id in enumerate(line):
    if id != "x":
      ids[int(id)] = calc_offset(i, int(id))
  return ids

def calc_offset(i, id):
  x = i
  while x % id != 0:
    x += 1
  return x - i

def calculate_part(value, id, mod):
  for x in range(1, id + 1):
    if (value * x) % id == mod:
      return value * x

def process_notes(location):
  bus_ids = load_notes(location)
  for line in bus_ids:
    parts = []
    ids = calculate_mods(line)
    for k,v in ids.items():
      x = 1
      y = 1
      for id in ids.keys():
        y *= id
        if id != k:
          x *= id
      parts.append(calculate_part(x, k, v))
    print("t:" + str(sum(parts) % y))

process_notes("13-input-pt2.txt")
