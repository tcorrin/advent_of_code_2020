#!/usr/local/bin/python3

import re, copy, math

def calc_last_axis(match_edge, end):
  if match_edge == "S" or match_edge == "N":
    if end:
      return "x"
    else: 
      return "y"
  else:
    if end:
      return "y"
    else:
      return "x"

def load_tiles(location):
  tiles = dict()
  current_id = 0
  current_tile = []
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      match = re.search("^Tile (\d+):$", line)
      if match != None:
        if current_id != 0:
          tiles[current_id] = current_tile
          current_tile = []
        current_id = int(match[1])
      elif line != "":
        current_tile.append(list(line))
  tiles[current_id] = current_tile
  return tiles

def display_tile(id, tile):
  print("Tile: " + str(id))
  for r in tile:
    print(r)
  print("")

def generate_edge_list(id, tile, edge_list):
  edge_list[str(id) + "-NF"]= "".join(tile[0])
  edge_list[str(id) + "-NB"]= "".join(tile[0][::-1])
  edge_list[str(id) + "-SF"]= "".join(tile[-1])
  edge_list[str(id) + "-SB"]= "".join(tile[-1][::-1])
  edge_list[str(id) + "-EF"] = ""
  edge_list[str(id) + "-WF"] = ""
  for i in range(0,len(tile)):
    edge_list[str(id) + "-EF"] += tile[i][-1]
    edge_list[str(id) + "-WF"] += tile[i][0]
  edge_list[str(id) + "-EB"] = edge_list[str(id) + "-EF"][::-1]
  edge_list[str(id) + "-WB"] = edge_list[str(id) + "-WF"][::-1]
  return edge_list

def calculate_adjacent_tiles(edge_matches, id):
  adjacent_tiles = []
  for k, v in edge_matches.items():
    regex = "^(\d+)-([NSEW])([FB])$"
    tile_match = re.search(regex, k)
    match_match = re.search(regex, v[0])
    tile_id = int(tile_match[1])
    tile_edge = tile_match[2]
    tile_direction = tile_match[3]
    match_id = int(match_match[1])
    match_edge = match_match[2]
    match_direction = match_match[3]
    
    if tile_id == id and match_id not in [a_tile[0] for a_tile in adjacent_tiles]:
      flipped = match_direction != tile_direction
      adjacent_tiles.append((match_id, tile_edge, match_edge, flipped, v[1]))
  return adjacent_tiles

def calculate_tile_direction(x, y, tile_id, tile_grid):
  if x + 1 < len(tile_grid[0]) and tile_grid[y][x+1] == tile_id:
    return "E"
  elif y + 1 < len(tile_grid) and tile_grid[y+1][x] == tile_id:
    return "S"
  elif x - 1 >= 0 and tile_grid[y][x-1] == tile_id:
    return "W"
  elif y - 1 >= 0 and tile_grid[y-1][x] == tile_id:
    return "N"

def x_flip_tile(tile):
  new_tile = []
  for row in tile:
    new_tile.append(row[::-1])
  return new_tile

def y_flip_tile(tile):
  return tile[::-1]

def rotate_tile(tile, rotation):
  number_of_turns = int(rotation / 90)
  for _ in range(number_of_turns):
    new_tile = list(zip(*tile[::-1]))
    tile = []
    for row in new_tile:
      tile.append(list(row))
  return tile    

def trim_tile(tile):
  new_tile = []
  for row in tile[1:-1]:
    new_tile.append(row[1:-1])
  return new_tile

def build_edges(tile):
  edges = dict()
  edges["N"] = "".join(tile[0])
  edges["S"] = "".join(tile[-1])
  edges["E"] = "" 
  edges["W"] = ""
  for i in range(len(tile)):
    edges["E"] += tile[i][-1]
    edges["W"] += tile[i][0]
  return edges

def check_adjacent_tiles(edges, adjacent_tiles):
  result = True
  for tile in adjacent_tiles:
    actual_edge = tile[4]
    direction = tile[5]
    if edges[direction] != actual_edge and edges[direction] != actual_edge[::-1]:
      result = False
  return result

def check_rotations(tile, adjacent_tiles):
  for r in [0,90,180,270]:
    new_tile = rotate_tile(tile, r)
    edges = build_edges(new_tile)
    if check_adjacent_tiles(edges, adjacent_tiles):
      return new_tile
    else:
      x_flip = x_flip_tile(new_tile)
      edges = build_edges(x_flip)
      if check_adjacent_tiles(edges, adjacent_tiles):
        return x_flip
      else:
        y_flip = y_flip_tile(new_tile)
        edges = build_edges(y_flip)
        if check_adjacent_tiles(edges, adjacent_tiles):
          return y_flip
        else:
          total_flip = y_flip_tile(x_flip)
          edges = build_edges(total_flip)
          if check_adjacent_tiles(edges, adjacent_tiles):
            return total_flip
  print("Error could not fit tile")
  exit()
 
def add_tile_to_final_grid(y, tile_id, tiles, final_grid, adjacent_tiles):
  tile_size = 8
  y_offset = (y + 1) * tile_size
  tile = tiles[tile_id]
  print("Tile: " + str(tile_id))
  transformed_tile = check_rotations(tile, adjacent_tiles)
  tile = trim_tile(transformed_tile)
  if y_offset == len(final_grid):
    for t in range(tile_size):
      final_grid[(y*tile_size)+t].extend(list(tile[t]))
  else:
    for t in range(tile_size):
      final_grid.append(list(tile[t]))
  return final_grid

def check_for_sea_monster(final_grid):
  rough_water_count = 0
  monster_count = 0 
  offsets = [(1,-1),(4,-1),(5,0),(6,0,),(7,-1),(10,-1),(11,0),(12,0),(13,-1),(16,-1),(17,0),(18,0),(18,1),(19,0)]
  for y in range(len(final_grid)):
    for x in range(len(final_grid[y])):
      monster = True
      if final_grid[y][x] == "#":
        rough_water_count += 1
        for value in offsets:
          if -1 < y + value[1] < len(final_grid) and -1 < x + value[0] < len(final_grid[0]):
            if final_grid[y + value[1]][x + value[0]] != "#":
              monster = False
              break
          else:
            monster = False
            break
      else:
        monster = False
      if monster:
        monster_count += 1
  return rough_water_count, monster_count
      
def check_monster_rotations(final_grid):
  rough_water_count = 0
  monster_count = 0
  for r in [0, 90, 180, 270]:
    new_grid_tuples = rotate_tile(final_grid, r)
    new_grid = []
    for t in list(new_grid_tuples):
      new_grid.append(list(t))
    rough_water_count, monster_count = check_for_sea_monster(new_grid)
    if monster_count > 0:
      break
  return rough_water_count, monster_count

def process_tiles(location):
  tiles = load_tiles(location)
  grid_size = int(math.sqrt(len(tiles)))
  tile_grid = []
  for g in range(0, grid_size):
    tile_grid.append([])
  edge_list = dict()
  edge_matches = dict()
  adjacent_tiles = dict()
  tile_locations = dict()
  corner_tiles = []
  final_grid = []

  for k,v in tiles.items():
    edge_list = generate_edge_list(k, v, edge_list)
  
  for k, v in edge_list.items():
   # print(k + " - " + v)
    for x, y in edge_list.items():
      if v == y and k != x:
        edge_matches[k] = (x, y)
  
  for k, v in edge_matches.items():
    print(k + " - " + str(v))
  
  for tile in tiles.keys():
    adjacent_tiles[tile] = calculate_adjacent_tiles(edge_matches, tile)

  for k, v in adjacent_tiles.items():
    if len(v) == 2:
      corner_tiles.append(k)
  
  tile_grid[0].append(corner_tiles[0])
  
  last_axis = "x"
  last_row_axis = "x"
  for y in range(0, grid_size):
    for x in range(0, grid_size):
      for tile in adjacent_tiles[tile_grid[y][x]]:
        matching_tile_id = tile[0]
        tile_edge = tile[1]
        match_edge = tile[2]
        flipped = tile[3]
        if matching_tile_id != tile_grid[y][x-1] and ((last_axis == "x" and (tile_edge == "W" or tile_edge == "E")) or (last_axis == "y" and (tile_edge == "S" or tile_edge == "N"))):
          tile_grid[y].append((matching_tile_id))
          if x == 0:
            last_row_axis = last_axis
          last_axis = calc_last_axis(match_edge, False)
          break
        
      if x == grid_size - 1: 
        for tile in adjacent_tiles[tile_grid[y][0]]:
          matching_tile_id = tile[0]
          tile_edge = tile[1]
          match_edge = tile[2]
          flipped = tile[3]
          if y - 1 < 0 or matching_tile_id != tile_grid[y-1][0] and ((last_row_axis == "x" and (tile_edge == "S" or tile_edge == "N")) or (last_row_axis == "y" and (tile_edge == "E" or tile_edge == "W"))): 
            tile_grid[y+1].append((matching_tile_id))
            last_axis = calc_last_axis(match_edge, True)
            break

  print("")
   
  for row in tile_grid:
    print(row)
    for tile in row:
      tile_locations[tile] = (tile_grid.index(row), row.index(tile))

  new_adjacent_tiles = dict() 
  for k, v in adjacent_tiles.items():
    new_adjacent_tiles[k] = []
    for tile in v:
      direction = calculate_tile_direction(tile_locations[k][1], tile_locations[k][0], tile[0], tile_grid)
      new_adjacent_tiles[k].append((tile[0], tile[1], tile[2], tile[3], tile[4], direction))

  adjacent_tiles = new_adjacent_tiles
  
  for k, v in adjacent_tiles.items():
    print("tile_id: " + str(k) + " - " + str(v))
  
  for row in tile_grid:
    for tile in row:
       final_grid = add_tile_to_final_grid(tile_grid.index(row), tile, tiles, final_grid, adjacent_tiles[tile])

  display_tile("Final", final_grid)
  
  rough_water_count, monster_count = check_monster_rotations(final_grid)
  if monster_count == 0:
    x_flipped_grid = x_flip_tile(final_grid)
    rough_water_count, monster_count = check_monster_rotations(x_flipped_grid)

    if monster_count == 0:
      y_flipped_grid = y_flip_tile(final_grid)
      rough_water_count, monster_count = check_monster_rotations(y_flipped_grid)

      if monster_count == 0:
        totally_flipped_grid = x_flip_tile(y_flipped_grid)
        rough_water_count, monster_count = check_monster_rotations(totally_flipped_grid)
 
  result = 1
  for ct in corner_tiles:
    result *= ct
  
  print(location + " - result: " + str(result))
  print("Monsters: " + str(monster_count))
  print("Total Rough Water:" + str(rough_water_count))
  print(location + " - rough_water_count:" + str(rough_water_count - monster_count * 15))

process_tiles("20-test.txt")
process_tiles("20-input.txt")
