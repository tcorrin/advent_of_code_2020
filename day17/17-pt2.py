#!/usr/local/bin/python3

import copy

neighbours = [(-1, -1, -1, -1),
              (-1, 0, -1, -1),
              (-1, 1, -1, -1),
              (0, -1, -1, -1),
              (0, 1, -1, -1),
              (1, -1, -1, -1),
              (1, 0, -1, -1),
              (1, 1, -1, -1),
              (-1, -1, 0, -1),
              (-1, 0, 0, -1),
              (-1, 1, 0, -1),
              (0, -1, 0, -1),
              (0, 1, 0, -1),
              (1, -1, 0, -1),
              (1, 0, 0, -1),
              (1, 1, 0, -1),
              (-1, -1, 1, -1),
              (-1, 0, 1, -1),
              (-1, 1, 1, -1),
              (0, -1, 1, -1),
              (0, 1, 1, -1),
              (1, -1, 1, -1),
              (1, 0, 1, -1),
              (1, 1, 1, -1),
              (0, 0, -1, -1),
              (0, 0, 1, -1),
              (-1, -1, -1, 0),
              (-1, 0, -1, 0),
              (-1, 1, -1, 0),
              (0, -1, -1, 0),
              (0, 1, -1, 0),
              (1, -1, -1, 0),
              (1, 0, -1, 0),
              (1, 1, -1, 0),
              (-1, -1, 0, 0),
              (-1, 0, 0, 0),
              (-1, 1, 0, 0),
              (0, -1, 0, 0),
              (0, 1, 0, 0),
              (1, -1, 0, 0),
              (1, 0, 0, 0),
              (1, 1, 0, 0),
              (-1, -1, 1, 0),
              (-1, 0, 1, 0),
              (-1, 1, 1, 0),
              (0, -1, 1, 0),
              (0, 1, 1, 0),
              (1, -1, 1, 0),
              (1, 0, 1, 0),
              (1, 1, 1, 0),
              (0, 0, -1, 0),
              (0, 0, 1, 0),
              (0, 0, 0, -1),
              (0, 0, 0, 1),
              (-1, -1, -1, 1),
              (-1, 0, -1, 1),
              (-1, 1, -1, 1),
              (0, -1, -1, 1),
              (0, 1, -1, 1),
              (1, -1, -1, 1),
              (1, 0, -1, 1),
              (1, 1, -1, 1),
              (-1, -1, 0, 1),
              (-1, 0, 0, 1),
              (-1, 1, 0, 1),
              (0, -1, 0, 1),
              (0, 1, 0, 1),
              (1, -1, 0, 1),
              (1, 0, 0, 1),
              (1, 1, 0, 1),
              (-1, -1, 1, 1),
              (-1, 0, 1, 1),
              (-1, 1, 1, 1),
              (0, -1, 1, 1),
              (0, 1, 1, 1),
              (1, -1, 1, 1),
              (1, 0, 1, 1),
              (1, 1, 1, 1),
              (0, 0, -1, 1),
              (0, 0, 1, 1)]
 
def prefill_grid(size):
  grid = []
  for w in range(0,size):
    grid.append([])
    for z in range(0,size):
      grid[w].append([])
      for y in range(0,size):
        grid[w][z].append([])
        for x in range(0,size):
          grid[w][z][y].append(".")
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
      grid[offset][offset][offset + y][offset + x] = c
  return grid
  
def process_node(x, y, z, w, grid, new_grid):
  current_value = grid[w][z][y][x]
  inactive = 0
  active = 0
  for node in neighbours:
    if -1 < w + node[3] < len(grid) and -1 < z + node[2] < len(grid[w]) and -1 < y + node[1] < len(grid[w][z]) and -1 < x + node[0] < len(grid[w][z][y]):
      node_value = grid[w + node[3]][z + node[2]][y + node[1]][x + node[0]]
      if node_value == ".":
        inactive += 1
      elif node_value == "#":
        active += 1
  if current_value == "#" and not 1 < active < 4:
    new_grid[w][z][y][x] = "."
  elif current_value == "." and active == 3:
    new_grid[w][z][y][x] = "#"
  return new_grid

def run_cycle(grid):
  new_grid = copy.deepcopy(grid)
  for w, cube in enumerate(grid):
    for z, layer in enumerate(cube):
      for y, row in enumerate(layer):
        for x, char in enumerate(row):
          new_grid = process_node(x, y, z, w, grid, new_grid)
  return new_grid

def process_grid(location):
  size = 26
  grid = load_grid(location, size)
  for _ in range(0,6):
    grid = run_cycle(grid)
  count = 0
  for cube in grid:
    for layer in cube:
      for row in layer:
        count += row.count("#")
  print(location + " - Active Count: " + str(count))

process_grid("17-test.txt")
process_grid("17-input.txt")

