#!/usr/local/bin/python3

import re

def load_food_list(location):
  foods = []
  with open(str(location), 'r') as file:
    for line in file:
      line = line.rstrip()
      match = re.search("^(.*) \(contains (.*)\)$", line)
      foods.append((match[1].split(" "),match[2].split(", ")))
  return foods

def process_foods(location):
  food_list = load_food_list(location)
  safe_ingredient_list = []
  bad_ingredient_list = []
  allergen_list = []
  safe_ingredient_count = 0
  for food in food_list:
    for allergen in food[1]:
      if allergen not in allergen_list:
        allergen_list.append(allergen)

  for food in food_list:
    for ingredient in food[0]:
      if ingredient not in bad_ingredient_list:
        safe = True
        for allergen in food[1]:
          allergen_safe = False
          for food_to_check in food_list:
            allergen_safe = False
            if ingredient not in food_to_check[0] and allergen in food_to_check[1] and food != food_to_check:
              allergen_safe = True
              break
          if not allergen_safe:
            safe = False
        if safe:
          if ingredient not in safe_ingredient_list:
            safe_ingredient_list.append(ingredient)
        else:
          if ingredient in safe_ingredient_list:
            safe_ingredient_list.remove(ingredient)
          bad_ingredient_list.append(ingredient)
  
  for safe_ingredient in safe_ingredient_list:
    for food in food_list:
      if safe_ingredient in food[0]:
        safe_ingredient_count += 1
  
  print(location + " - safe_ingredient_count: " + str(safe_ingredient_count))    

  new_food_list = []
  for food in food_list:
    bad_ingredients = []
    for old_ingredient in food[0]:
      if old_ingredient not in safe_ingredient_list:
        bad_ingredients.append(old_ingredient)
    new_food_list.append((bad_ingredients,food[1]))
   
  food_list = new_food_list
  
  allergen_map = dict()

  for allergen in sorted(allergen_list):
    ingredient_list = []
    for food in food_list:
      if allergen in food[1]:
        if ingredient_list == []:
          ingredient_list.extend(food[0])
        else:
          for ingredient in ingredient_list.copy():
            if ingredient not in food[0]:
              ingredient_list.remove(ingredient)
    allergen_map[allergen] = ingredient_list

  seen = []
  while len(seen) < len(allergen_list):
    new_allergen_map = dict()
    for allergen, ingredients in allergen_map.items():
      if len(ingredients) == 1:
        if ingredients[0] not in seen:
          seen.append(ingredients[0])
        new_allergen_map[allergen] = ingredients
      else:
        new_ingredients = []
        for ingredient in ingredients:
          if ingredient not in seen:
            new_ingredients.append(ingredient)
        new_allergen_map[allergen] = new_ingredients
    allergen_map = new_allergen_map

  sorted_ingredients = []
  for k in sorted(allergen_map.keys()):
    sorted_ingredients.append(allergen_map[k][0])
  print(",".join(sorted_ingredients))
        
        
   
        
 




process_foods("21-test.txt")
process_foods("21-input.txt")


