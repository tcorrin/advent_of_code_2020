#!/usr/local/bin/python3

def run_number_game(number_list, limit):
  numbers = dict()
  last_number = 0
  for n in number_list:
    numbers[n] = number_list.index(n)
  for i in range(len(number_list), limit - 1):
    if last_number in numbers.keys():
      temp_number = last_number
      last_number = i - numbers[last_number]
      numbers[temp_number] = i
    else:
      numbers[last_number] = i
      last_number = 0
  print(str(limit) + "th number: " + str(last_number))

for limit in [2020, 30000000]:
  run_number_game([0,3,6], limit)
  run_number_game([1,3,2], limit)
  run_number_game([2,1,3], limit)
  run_number_game([1,2,3], limit)
  run_number_game([2,3,1], limit)
  run_number_game([3,2,1], limit)
  run_number_game([3,1,2], limit)
  run_number_game([20,0,1,11,6,3], limit)
