#!/usr/local/bin/python3

import re

def load_homework(location):
  homework = []
  with open(str(location), 'r') as file:
    for line in file:
       homework.append(list(line.rstrip().replace(" ", "")))
  return homework

def process_homework_line(line, i):
  result = 0
  current_operator = ""
  precedence = False
  precedence_result = 0
  while i < len(line):
    number_match = re.search("^([0-9]+).*$", ''.join(line[i:]))
    operation_match = re.search("^([\+\*])(\d+).*$", ''.join(line[i:]))
    if number_match != None:
      result = int(number_match[1])
      i += len(number_match[1]) - 1
    if operation_match != None:
      if operation_match[1] == "+":
        if precedence:
          precedence_result += int(operation_match[2])
        else:
          result += int(operation_match[2])
      elif operation_match[1] == "*":
        if precedence:
          result *= precedence_result
          precedence_result = int(operation_match[2])
        else:
          precedence_result = int(operation_match[2])
          precedence = True
      i += len(operation_match[1]) + len(operation_match[2])
    elif line[i] == ")":
      i += 1
      if precedence:
        result *= precedence_result
      return i, result
    elif line[i] == "(":
      i += 1
      i, x = process_homework_line(line, i)
      if current_operator == "+":
        if precedence:
          precedence_result += x
        else:
          result += x
      elif current_operator == "*":
        if precedence:
          result *= precedence_result
          precedence_result = x
        else:
          precedence_result = x
          precedence = True
      else:
        result = x
    else:
      current_operator = line[i]
      i += 1
  if precedence:
    result *= precedence_result
  return i, result


def process_homework(location):
  homework = load_homework(location)
  result = 0
  for line in homework:
    _, line_result = process_homework_line(line, 0)
    print(location + " - Line Result: " + str(line_result))
    result += line_result
  print(len(homework))
  print(location + " - Homework Result: " + str(result))
    
process_homework("18-test.txt")    
process_homework("18-input.txt")
    
    

  
