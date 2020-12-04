#!/usr/local/bin/python3

import re

def load_passports(location):
  passports = []
  current_passport = dict()

  with open(str(location), 'r') as file:
    for i, line in enumerate(file):
      if line == "\n":
        passports.append(current_passport)
        current_passport = dict()
      else:
        kvps = line.rstrip().split()
        for result in kvps:
          kvp = result.split(":")
          current_passport[kvp[0]] = kvp[1]
  
  passports.append(current_passport)
  return passports

def check_passport_field_presence(passports):
  required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
  valid_passports = []
  for passport in passports:
    if all(item in passport.keys() for item in required_fields):
      valid_passports.append(passport)
  return valid_passports

def check_passport_field_validity(passports):
  debug = False
  valid_passports = []
  for passport in passports:
    result = True
    for item in passport.items():
      field_result = check_field(item[0], item[1])
      if debug:
        print(str(item)  + " - " + str(field_result) + " - " + str(result) )
      result = result and field_result
      
    if result:
      valid_passports.append(passport)
  return valid_passports
    
def check_field(field, value):
  result = False
  if field == "cid":
    result = True
  elif field == "byr":
    result = len(value) == 4 and int(value) >= 1920 and int(value) <= 2002
  elif field == "iyr":
    result = len(value) == 4 and int(value) >= 2010 and int(value) <= 2020
  elif field == "eyr":
    result = len(value) == 4 and int(value) >= 2020 and int(value) <= 2030
  elif field == "hgt":
    r = re.search("^(\d+)(cm|in)$", value)
    result = r != None and ((r[2] == "cm" and int(r[1]) >= 150 and int(r[1]) <= 193) or (r[2] == "in" and int(r[1]) >= 59 and int(r[1]) <= 76))
  elif field == "hcl":
    result = re.search("^#[a-f0-9]{6}$", value) != None
  elif field == "ecl":
    result = re.search("^amb|blu|brn|gry|grn|hzl|oth$", value) != None
  elif field == "pid":
    result = re.search("^\d{9}$", value) != None 
  
  return result

def process_passport_batch_file(location):
  passports = load_passports(location)
  print(location + " - Total number of passports = " + str(len(passports)))
  valid_passports = check_passport_field_presence(passports)
  valid_passports = check_passport_field_validity(valid_passports)
  print(location + " - Total number of VALID passports = " + str(len(valid_passports)))

process_passport_batch_file("04-test.txt")  
process_passport_batch_file("04-input.txt")  
process_passport_batch_file("04-invalid-list.txt")
process_passport_batch_file("04-valid-list.txt")


