#!/usr/local/bin/python3

import re, copy

def load_transmission(location):
  rules = dict()
  messages = []
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip().replace('"','')
      rule_match = re.search("^(\d+): (.+)$", line)
      if rule_match != None:
        rules[rule_match[1]] = rule_match[2].split(" ")
      elif line != "":
        messages.append(line)
  return rules, messages

def process_rule(rules, process_queue):
  x = process_queue.pop(0)
  new_rules = dict()
  for k, v in rules.items():
    new_rule, replaced = rule_lookup_and_replace(x, v, rules[x], False)
    if replaced:
      new_rules[k] = new_rule
      process_queue.append(k)
    else:
      new_rules[k] = v
  return new_rules, process_queue

def generate_valid_message_list(rule):
  result = [""]
  offset = 0
  count = 0
  for x in rule:
    if type(x) is list:
      new_message_list = generate_valid_message_list(x)
      new_result = copy.deepcopy(result[:offset])
      for r in result[offset:]:
        for nm in new_message_list:
          new_result.append(r + nm)
      result = new_result
    elif x == "|":
      offset = len(result)
      result.extend([""])
    else:
      for i, m in enumerate(result[offset:], offset):
        result[i] += x
      count += 1
  return result

def rule_lookup_and_replace(x, v, new_value, replaced):
  new_rule = []
  if x in new_value:
    return [], False
  for y in v:
    if type(y) is list:
      z, replaced = rule_lookup_and_replace(x, y, new_value, replaced)
      new_rule.append(z)
    elif x == y:
      if new_value == ["a"]:
        new_value = "a"
      elif new_value == ["b"]:
        new_value = "b"
      new_rule.append(new_value)
      replaced = True
    else:
      new_rule.append(y)
  return new_rule, replaced

def process_transmission(location):
  rules, messages = load_transmission(location)
  process_queue = []

  for k, v in rules.items():
    if "a" in v:
      process_queue.append(k)
    if "b" in v:
      process_queue.append(k)

  while len(process_queue) > 0:
    rules, process_queue = process_rule(rules, process_queue)
  fourty_two_valid_message_list = generate_valid_message_list(rules["42"])
  thirty_one_valid_message_list = generate_valid_message_list(rules["31"])

  mcount = 0
  for m in messages:
    fourty_two_count = 0
    thirty_one_count = 0
    part_two = False
    failed = False
    message_length = len(m)
    substring_length = len(fourty_two_valid_message_list[0])
    if message_length % substring_length == 0:
      for t in range(0, message_length, substring_length):
        test_string = m[t:]
        if t + substring_length < message_length:
          test_string = m[t:t+substring_length]
        if test_string in fourty_two_valid_message_list:
          if part_two:
            failed = True
            break
          else:
            fourty_two_count += 1
        elif test_string in thirty_one_valid_message_list:
          if not part_two:
            part_two = True
          thirty_one_count += 1
        else:
          failed = True
          break
         
    if not failed and fourty_two_count > 0 and thirty_one_count > 0 and fourty_two_count > thirty_one_count:
       mcount += 1
        
  print(location + " - Valid message count: " + str(mcount))

process_transmission("19-test-02.txt")
process_transmission("19-input-02.txt")
