#!/usr/local/bin/python3

import re, copy

def load_notes(location):
  ranges = dict()
  your_ticket = None
  nearby_tickets = []

  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      ticket_match = re.search("^(\d+,)+\d+$", line)
      range_match = re.search("^(.+): (\d+)-(\d+) or (\d+)-(\d+)$", line)
      if range_match != None:
        ranges[range_match[1]] = [(int(range_match[2]),int(range_match[3])),(int(range_match[4]),int(range_match[5]))]
      elif ticket_match != None:
        if your_ticket == None:
          your_ticket = list(map(int, line.split(",")))
        else:
          nearby_tickets.append(list(map(int, line.split(","))))
  return ranges, your_ticket, nearby_tickets

def is_valid_ticket(ticket, lower_bound, upper_bound):
  result = True
  invalid_values = []
  for value in ticket:
    if not lower_bound < value <= upper_bound:
      invalid_values.append(value)
      result = False
      break
  return result, invalid_values

def calculate_range_bounds(ranges):
  lower_bound = 1000
  upper_bound = 0
  for range_group in ranges.values():
    if range_group[0][0] < lower_bound:
      lower_bound = range_group[0][0]
    elif range_group[1][1] > upper_bound:
      upper_bound = range_group[1][1]
  return lower_bound, upper_bound


def process_notes(location):
  invalid_values = []
  ranges, your_ticket, nearby_tickets = load_notes(location)
  lower_bound, upper_bound = calculate_range_bounds(ranges)
  for ticket in nearby_tickets:
    valid, ticket_invalid_values = is_valid_ticket(ticket, lower_bound, upper_bound)
    invalid_values.extend(ticket_invalid_values)
  print(location + " - Ticket scanning error rate: " + str(sum(invalid_values)) )

def process_notes_pt2(location):
  ranges, your_ticket, nearby_tickets = load_notes(location)
  lower_bound, upper_bound = calculate_range_bounds(ranges)
  invalid_tickets = []
  for i, ticket in enumerate(nearby_tickets):
    valid, ticket_invalid_values = is_valid_ticket(ticket, lower_bound, upper_bound)
    if not valid:
      invalid_tickets.append(i)
  range_index_mapping = ranges.fromkeys(ranges, None)
 
  for i in range(0, len(your_ticket)):
    for range_name in list(sorted(ranges.keys(), reverse = True)):
        range_match = True
        for x, valid_ticket in enumerate(nearby_tickets):
          if x not in invalid_tickets:
            range_group_match = False
            invalid_values = []
            invalid_values.extend(range(0,ranges[range_name][0][0]))
            invalid_values.extend(range(ranges[range_name][0][1] + 1, ranges[range_name][1][0]))
            invalid_values.extend(range(ranges[range_name][1][1], 1000))
            if valid_ticket[i] in invalid_values:
              range_match = False
              break
        if range_match:
          if range_index_mapping[range_name] == None:
            range_index_mapping[range_name] = [i]
          else:
            range_index_mapping[range_name].append(i)
  
  for range_name, index_list in range_index_mapping.items():
    print(range_name.ljust(25) + " - " + str(index_list))
  
  seen = []
  while len(seen) < len(range_index_mapping):
    for range_name, index_list in range_index_mapping.items():
      if len(index_list) == 1 and range_name not in seen:
        seen.append(range_name)
        for range_name_x, index_list_x in range_index_mapping.items():
          if index_list[0] in index_list_x and range_name_x != range_name:
            index_list_x.remove(index_list[0])
          
  print("-".ljust(25,"-") )
  for range_name, index_list in range_index_mapping.items():
    print(range_name.ljust(25) + " - " + str(index_list))
  
  result = 1
  for k,v in range_index_mapping.items():
    if "departure" in k:
      print("range:" + k + " ticket_value: " + str(your_ticket[v[0]]))
      result *= your_ticket[v[0]]
  print(location + " - Result: " + str(result))
      
process_notes("16-test.txt")
process_notes_pt2("16-test-02.txt")
process_notes("16-input.txt")
process_notes_pt2("16-input.txt")
  
        
