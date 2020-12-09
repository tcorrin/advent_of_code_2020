#!/usr/local/bin/python3

def load_numbers(location):
  numbers = []
  with open(str(location), 'r') as file:
    for line in file:
      numbers.append(int(line.rstrip()))
  return numbers

def find_invalid_number(offset, numbers):
  result = 0;
  for i in range(len(numbers) - offset):
    result = False
    sum = numbers[i + offset]
    for x in range(i,offset + i):
      for y in range(i,offset + i):
        if x != y and numbers[x] + numbers[y] == sum:
          result = True
          break
      if result:
        break
    if not result:
      result = sum
      break
  return result

def find_encryption_weakness(numbers, invalid_number):
  result_list = None
  for offset in range(0, len(numbers) - 1):
    if offset != invalid_number and result_list is None:
      for i in range(0, len(numbers) - 1):
        if invalid_number == sum(numbers[offset:i + 1]):
          result_list = numbers[offset:i + 1]
          break
  encryption_weakness = min(result_list) + max(result_list)
  return encryption_weakness
      
def process_file(location, offset):
  print(location)
  numbers = load_numbers(location)
  invalid_number = find_invalid_number(offset, numbers)
  print("Invalid Number: " + str(invalid_number))
  print("Encryption Weakness: " + str(find_encryption_weakness(numbers, invalid_number)))

process_file("09-test.txt", 5)
process_file("09-input.txt", 25)
