#!/usr/local/bin/python3

import copy

neighbours = [(-1, -1, -1),
              (-1, 0, -1),
              (-1, 1, -1),
              (0, -1, -1),
              (0, 1, -1),
              (1, -1, -1),
              (1, 0, -1),
              (1, 1, -1),
              (-1, -1, 0),
              (-1, 0, 0),
              (-1, 1, 0),
              (0, -1, 0),
              (0, 1, 0),
              (1, -1, 0),
              (1, 0, 0),
              (1, 1, 0),
              (-1, -1, 1),
              (-1, 0, 1),
              (-1, 1, 1),
              (0, -1, 1),
              (0, 1, 1),
              (1, -1, 1),
              (1, 0, 1),
              (1, 1, 1),
              (0, 0, -1),
              (0, 0, 1)]
 
def prefill_grid(size):
  grid = []
  for z in range(0,size):
    grid.append([])
    for y in range(0,size):
      grid[z].append([])
      for x in range(0,size):
        grid[z][y].append(".")
  return grid
  
def load_grid(location, size):
  grid = prefill_grid(size)
  offset = int(size / 2)
  input = []
  with open(str(location), 'r') as file:
    for line in file:
       input.append(list(line.rstrip()))
  for y, l in enumerate(input):
    for x, c in enumerate(l):
      grid[offset][offset + y][offset + x] = c
  return grid
  
def process_node(x, y, z, grid, new_grid):
  current_value = grid[z][y][x]
  inactive = 0
  active = 0
  for node in neighbours:
    if -1 < z + node[2] < len(grid) and -1 < y + node[1] < len(grid[x]) and -1 < x + node[0] < len(grid[x][y]):
      node_value = grid[z + node[2]][y + node[1]][x + node[0]]
      if node_value == ".":
        inactive += 1
      elif node_value == "#":
        active += 1
  if current_value == "#" and not 1 < active < 4:
    new_grid[z][y][x] = "."
  elif current_value == "." and active == 3:
    new_grid[z][y][x] = "#"
  return new_grid

def run_cycle(grid):
  new_grid = copy.deepcopy(grid)
  for z, layer in enumerate(grid):
    for y, row in enumerate(layer):
      for x, char in enumerate(row):
        new_grid = process_node(x, y, z, grid, new_grid)
  return new_grid

def process_grid(location):
  size = 26
  grid = load_grid(location, size)
  for _ in range(0,6):
    grid = run_cycle(grid)
  count = 0
  for layer in grid:
    for row in layer:
      count += row.count("#")
  print(location + " - Active Count: " + str(count))

process_grid("17-test.txt")
process_grid("17-input.txt")

