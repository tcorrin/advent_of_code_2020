#!/usr/local/bin/python3

debug = False

def load_adapters(location):
  adapters = []
  with open(str(location), 'r') as file:
    for line in file:
      adapters.append(int(line.rstrip()))
  return adapters

def calculate_jumps(adapters):
  valid_jumps = { 1:0, 2:0, 3:0 }
  current_joltage = 0
  while current_joltage < max(adapters):
    for jump in valid_jumps.keys():
      if current_joltage + jump in adapters:
        current_joltage += jump
        valid_jumps[jump] += 1
        break
    if debug:
      print("current_joltage: " + str(current_joltage) + " valid_jumps: " + str(valid_jumps))
  #add_final_adapter
  current_joltage += 3
  valid_jumps[3] += 1
  return valid_jumps, current_joltage

def process_node(node, number_of_paths, graph):
  value = graph[node]
  if value:
    number_of_paths += (len(value) - 1)
  for new_node in value:
      number_of_paths = process_node(new_node, number_of_paths, graph)
  return number_of_paths

def calculate_number_of_paths(adapters):
  adapters.insert(0,0)
  adapters.sort()
  graph = dict()
  valid_jumps = [1,2,3]
  for adapter in adapters:
    jumps = []
    for jump in valid_jumps:
      if adapter + jump in adapters:
        jumps.append(adapter + jump)
    graph[adapter] = jumps
  number_of_paths = process_node(0, 1, graph)
  return number_of_paths

def process_adapter_bag(location):
  adapters = load_adapters(location)
  jumps, outlet_joltage = calculate_jumps(adapters)
  print(location + " - Oulet Joltage: " + str(outlet_joltage)  + "  - one jolt jumps: " + str(jumps[1]) + " - three jolt jumps: " + str(jumps[3]) + " - Product: " + str(jumps[1] * jumps [3]))
  number_of_paths = calculate_number_of_paths(adapters)
  print(location + " - Number of paths: " + str(number_of_paths))

process_adapter_bag("10-test01.txt")  
process_adapter_bag("10-test02.txt")  
process_adapter_bag("10-input.txt")  

