#!/usr/local/bin/python3

def read_file_into_2d_array(location):
  lines = []
  with open(str(location), 'r') as file:
    for line in file:
       lines.append(list(line.rstrip()))
  return lines

def process_slope(input, h_move, v_move):
  debug = False
  lines = read_file_into_2d_array(input)
  total_depth = len(lines)
  input_width = len(lines[0])
  v_move = int(v_move)
  h_move = int(h_move)
  current_depth = 0
  current_width = 0
  total_trees = 0

  while current_depth + v_move < total_depth:
    current_width += h_move
    current_depth += v_move
    current_char = lines[current_depth][current_width % input_width]

    if debug:
      print(str(current_width % input_width).zfill(3) + " - " + str(current_depth).zfill(3) + " - " + current_char)

    if current_char == "#":
      total_trees += 1
  print(input + " - R:" + str(h_move) + " - D:" + str(v_move)  + " Total Trees: " + str(total_trees))
  return total_trees

def process_slopes(input, slopes):
  total = 1
  for x, y in slopes:
    total *= process_slope(input, x, y)
  print("Tree multiplication: " + str(total))

process_slope("03-test.txt", 3, 1)
process_slope("03-input.txt", 3, 1)

print("----------------------")

slopes = list([(1,1), (3,1), (5,1), (7,1), (1,2)])

process_slopes("03-test.txt", slopes)

print("----------------------")

process_slopes("03-input.txt", slopes)
