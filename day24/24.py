#!/usr/local/bin/python3

import re, copy

def check_adjacent_tiles(tile, tiles):
  x = tile[0]
  y = tile[1]
  z = tile[2]
  colour = tile[3]
  new_colour = colour
  adjacent_tiles = [(0,1,-1),(1,0,-1),(-1,0,1),(0,-1,1),(-1,1,0),(1,-1,0)]
  black = 0
  white = 0
  for at in adjacent_tiles:
    new_x = x + at[0]
    new_y = y + at[1]
    new_z = z + at[2]
    for t in tiles:
      if t[0] == new_x and t[1] == new_y and t[2] == new_z:
        if t[3] == "white":
          white += 1
        elif t[3] == "black":
          black += 1
  if colour == "black" and (black == 0 or black > 2):
    new_colour = "white"
  elif colour == "white" and black == 2:
    new_colour = "black"
  return new_colour

def add_adjacent_tiles(tile, tiles):
  x = tile[0]
  y = tile[1]
  z = tile[2]
  adjacent_tiles = [(0,1,-1),(1,0,-1),(-1,0,1),(0,-1,1),(-1,1,0),(1,-1,0)]
  new_tiles = []
  for at in adjacent_tiles:
    new_x = x + at[0]
    new_y = y + at[1]
    new_z = z + at[2]
    match = False
    for t in tiles:
      if t[0] == new_x and t[1] == new_y and t[2] == new_z:
        match = True
    if not match:
      new_tiles.append((new_x, new_y, new_z, "white"))
  return new_tiles

def load_tiles(location):
  tiles = []
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      match = re.findall("(sw|se|nw|ne|e|w)", line)
      x = 0
      y = 0
      z = 0
      for d in match:
        if d == "ne":
          x += 0
          y += 1
          z += -1
        elif d == "nw": 
          x += 1
          y += 0
          z += -1
        elif d == "se":
          x += -1
          y += 0
          z += 1
        elif d == "sw":
          x += 0
          y += -1
          z += 1
        elif d == "e":
          x += -1
          y += 1
          z += 0
        elif d == "w":
          x += 1
          y += -1
          z += 0
      #tiles.append((x,y,z))
      match = False
      new_tiles = []
      for t in tiles:
        if t[0] == x and t[1] == y and t[2] == z:
          new_tiles.append((t[0],t[1],t[2],t[3] + 1))
          match = True
        else:
          new_tiles.append((t[0],t[1],t[2],t[3]))
      if not match:
        new_tiles.append((x,y,z,1)) 
      tiles = new_tiles
  return tiles

def process_tiles(location):
  tiles = load_tiles(location)
  black = 0
  white = 0
  new_tiles = []
  for tile in tiles:
    if tile[3] % 2 is 0:
      new_tiles.append((tile[0], tile[1], tile[2], "white"))
      white += 1
    elif tile[3] % 2 is 1:
      black += 1
      new_tiles.append((tile[0], tile[1], tile[2], "black"))
  tiles = new_tiles

  print(location + " - pt1 - black: " + str(black) + " - white: " + str(white))

  for i in range(100):
    new_tiles = []
    for tile in tiles:
      adj_tiles = add_adjacent_tiles(tile, tiles)
      for at in adj_tiles:
        match = False
        for t in new_tiles:
          if at == t:
            match = True
            break
        if not match:
          new_tiles.append((at[0], at[1], at[2], at[3]))
      new_tiles.append((tile[0], tile[1], tile[2], tile[3]))
    tiles = new_tiles
    new_tiles = []
    for tile in tiles:
      new_colour = check_adjacent_tiles(tile, tiles)
      new_tiles.append((tile[0], tile[1], tile[2], new_colour))
    tiles = new_tiles
    
    black = 0
    white = 0
    for tile in tiles:
      if tile[3] == "black":
        black += 1
      elif tile[3] == "white":
        white += 1
    print(str(i+1) + " black: " + str(black) + " - white: " + str(white))
  
#process_tiles("24-test.txt")
process_tiles("24-input.txt")
