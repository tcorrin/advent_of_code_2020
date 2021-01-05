#!/usr/local/bin/python3

def encrypt(subject_number, loop_size, z):
  z = 1
  for _ in range(loop_size):
    z = (z * subject_number) % 20201227
  return z

def find_loop_size(subject, public_key):
  loop_size = 1
  z = 1
  completed = False
  while not completed:
    z = (z * subject) % 20201227
    print(str(loop_size) + " - " + str(z))
    if z != public_key:
      loop_size += 1
    else:
      completed = True
  return loop_size

def calculate_encryption_key(cpk, dpk):
  subject = 7
  c_loop = find_loop_size(subject, cpk)
  d_loop = find_loop_size(subject, dpk)
  c_encryption_key = encrypt(cpk, d_loop, 1)
  d_encryption_key = encrypt(dpk, c_loop, 1)

  print("Card encryption key: " + str(c_encryption_key) + " Door encryption key: " + str(d_encryption_key))

calculate_encryption_key(5764801, 17807724)
calculate_encryption_key(12092626, 4707356)
    
