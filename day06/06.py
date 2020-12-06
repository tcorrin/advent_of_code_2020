#!/usr/local/bin/python3

def load_groups(location):
  groups = []
  current_group = []
  with open(str(location), 'r') as file:
    for line in file:
      if line == "\n":
        groups.append(current_group)
        current_group = []
      else:
        current_group.append(line.rstrip())
  groups.append(current_group)
  return groups

def process_answers(group):
  answers = dict()
  for form in group:
    for c in form:
      if c in answers.keys():
        answers[c] += 1
      elif c not in answers.keys():
        answers[c] = 1
  return answers

def all_said_yes(answers, group_size):
  result = 0
  for count in answers.values():
    if count == group_size:
      result += 1
  return result

def process_file(location):
  total_unique_answers = 0
  total_all_group_answers = 0
  groups = load_groups(location)
  for group in groups:
    answers = process_answers(group)
    total_all_group_answers += all_said_yes(answers, len(group))
    total_unique_answers += len(answers)
  print(location + " - Total Unique Answers: " + str(total_unique_answers) + " - Total All Group Answers: " + str(total_all_group_answers))
    
process_file("06-test.txt")
process_file("06-input.txt")

  
