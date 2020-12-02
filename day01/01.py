#!/usr/local/bin/python3

numbers = []

with open('01.txt', 'r') as file:
  for line in file:
    numbers.append(int(line.strip()))

for x in numbers:
  for y in numbers:
      if x + y  == 2020:
        print(x * y)
        break

for x in numbers:
  for y in numbers:
    for z in numbers:
      if x + y + z == 2020:
        print(x * y * z)
        break
