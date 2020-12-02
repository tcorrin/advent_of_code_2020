#!/usr/local/bin/python3

import re

def read_file_into_array(location):
  lines = []
  with open(str(location), 'r') as file:
    for line in file:
      lines.append(line.rstrip())
  return lines

def process_line(line, stage):
  debug = False
  result = 0
  line = str(line)
  stage = int(stage)
  matches = re.search('^(\d+)-(\d+) ([a-z]): ([a-z]+)$', line)
  first_number = int(matches.group(1))
  second_number = int(matches.group(2))
  rule = matches.group(3)
  password = matches.group(4)
  count = password.count(rule)
  
  if stage == 1:
    if count >= first_number and count <= second_number:
      if debug:
        print("valid - " + line)
      result = 1
    else:
      if debug:
        print("invalid - " + line)
  elif stage == 2:
    match = 0
    for i, c in  enumerate(password):
      i += 1
      if c == rule and (i == first_number or i == second_number):
        match += 1
    if match == 1:
      if debug:
        print("valid - " + line)
      result = 1
    else:
      if debug: 
        print("invalid - " + line)

  return result
  
def process_file(location):
  total = 0
  lines = read_file_into_array(location)
  for line in lines:
    total += process_line(line, 1)
  print("Stage01 - " + location + " - " + str(total))
  total = 0
  for line in lines:
    total += process_line(line, 2)
  print("Stage02 - " + location + " - " + str(total))

process_file("02-test.txt")
process_file("02-input.txt")


