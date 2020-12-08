#!/usr/local/bin/python3

import re, copy

debug = False

class Instruction:
  id = 0
  command = None
  modifier = None
  ammount = 0

  def __init__(self, input, id):
    match = re.search("^(acc|nop|jmp) ([+-])(\d*)$", input)
    self.id = id
    self.command = match[1]
    self.modifier = match[2]
    self.ammount = int(match[3])

  def print(self):
    print("Id: " + str(self.id) + " Command: " + self.command + " Modifier: " + self.modifier + " Ammount: " + str(self.ammount))
  
  def execute(self, current_id, accumulator, executed_ids):
    if debug:
      self.print()
      print("Entry - " + str(current_id) + " - " + str(accumulator) + " - " + str(executed_ids))
    executed_ids.append(current_id)
    if self.command == "nop":
      current_id += 1
    elif self.command == "acc":
      if self.modifier == "+":
        accumulator += self.ammount
      elif self.modifier == "-":
        accumulator -= self.ammount
      current_id += 1
    elif self.command == "jmp":
      if self.modifier == "+":
        current_id += self.ammount
      elif self.modifier == "-":
        current_id -= self.ammount
    if debug:
      print("Exit - " + str(current_id) + " - " + str(accumulator) +  " - " + str(executed_ids))
    return current_id, accumulator, executed_ids

def load_boot_code(location):
  code_instructions = []
  with open(str(location), 'r') as file:
    for i, line in enumerate(file):
      instruction = Instruction(line.rstrip(), i)
      code_instructions.append(instruction)
  return code_instructions

def run_boot_code(code_instructions, location):
  current_id = 0
  accumulator = 0
  executed_ids = []

  while current_id not in executed_ids:
    if current_id == len(code_instructions) - 1:
      print(location + " - Program Complete - Accumulator: " + str(accumulator))
      return True
    else:
      # I should be filtering the code_instructions list by id but im lazy and this works
      current_id, accumulator, executed_ids = code_instructions[current_id].execute(current_id, accumulator, executed_ids)
  print(location + " - Accumulator before crash: " + str(accumulator))

def test_command_change(original_command, new_command, code_instructions, location):
  print("change " + original_command + " to " + new_command + " commands")
  for i, instruction in enumerate(code_instructions):
    temp_code_instructions = copy.deepcopy(code_instructions)
    if instruction.command == original_command:
      temp_code_instructions[i].command = new_command
      if run_boot_code(temp_code_instructions, location):
        return True
  return False

def load_and_run_boot_code(location):
  code_instructions = load_boot_code(location)
  run_boot_code(code_instructions, location)
  if test_command_change("nop", "jmp", code_instructions, location):
    return
  if test_command_change("jmp", "nop", code_instructions, location):
    return

load_and_run_boot_code("08-test.txt")
load_and_run_boot_code("08-input.txt")
