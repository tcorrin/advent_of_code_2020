#!/usr/local/bin/python3

import re

def load_bag_rules(location):
  bag_rules = dict()
  with open(str(location), 'r') as file:
    for line in file:
      inner_colours_list = dict()
      first_match = re.search("^(.*) bags contain (.*)\.$", line.rstrip())
      bag_colour = first_match[1]
      inner_colours = first_match[2]
      if inner_colours != "no other bags":
        inner_colours = inner_colours.split(", ")
        for inner_colour in inner_colours:
          inner_match = re.search("^(\d) (.*) bags?$", inner_colour)
          inner_colours_list[inner_match[2]] = int(inner_match[1])
      bag_rules[bag_colour] = inner_colours_list
  return bag_rules

def generate_bag_list(base_bag_type, bag_rules):
  bag_list = []
  bag_list.append(base_bag_type)
  new_bag_list = []
  finished = False
  while not finished:
    for outer_bag, inner_bags in bag_rules.items():
      for inner_bag_type in inner_bags.keys():
        if inner_bag_type in bag_list and outer_bag not in new_bag_list and outer_bag not in bag_list:
          new_bag_list.append(outer_bag)
    if len(new_bag_list) == 0:
      finished = True
    else:
      bag_list.extend(new_bag_list)
      new_bag_list = []
  bag_list.remove(base_bag_type)
  return bag_list

def count_bags_in_type(bag_type, bag_rules, count):
  count += 1
  for inner_bag_type, inner_bag_count in bag_rules[bag_type].items():
    for _ in range(inner_bag_count):
      count = count_bags_in_type(inner_bag_type, bag_rules, count)
  return count

def process_bag_rule_list(location):
  bag_rules = load_bag_rules(location)
  bag_list = generate_bag_list("shiny gold", bag_rules)
  print("Total bags in bag list: " + str(len(bag_list)))
  bag_count = count_bags_in_type("shiny gold", bag_rules, 0)
  # don't include the original gold bag
  bag_count -= 1
  print("Bags in shiny gold bag: " + str(bag_count))

process_bag_rule_list("07-test.txt")
process_bag_rule_list("07-test-02.txt")
process_bag_rule_list("07-input.txt")
