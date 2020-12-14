#!/usr/local/bin/python3

def load_notes(location):
  departure_time = 0
  bus_ids = []
  with open(str(location), 'r') as file:
    for line in file:
      if "," in line:
        bus_ids = line.split(",")
      else:
        departure_time = int(line.rstrip())
  return departure_time, bus_ids

def load_notes_pt2(location):
  bus_ids = []
  with open(str(location), 'r') as file:
    for line in file:
      bus_ids.append(line.split(","))
  return bus_ids

def process_notes(location):
  departure_time, bus_ids = load_notes(location)
  print(location + " - Departue Time:" + str(departure_time))
  min_wait = departure_time
  bus_to_take = 0
  for id in bus_ids:
    if id != "x":
      id = int(id)
      wait = id - (departure_time % id)
      if wait < min_wait:
        min_wait = wait
        bus_to_take = id
      print("Bus Id: " + str(id) + " Wait: " + str(wait))
  print(location + " - Bus Id: " + str(bus_to_take) + " Wait: " + str(min_wait) + " Result: " + str(bus_to_take * min_wait) )


def process_notes_pt2(location):
  bus_ids = load_notes_pt2(location)
  for line in bus_ids:
    t = int(line[0])
    exit = False
    while not exit: 
#      print("t:" + str(t))
      exit = True
      for i, id in enumerate(line):
#        print("id:" + id)
        if id != "x":
#          print("(t + i) % int(id):" + str((t + i) % int(id)))
          if (t + i) % int(id) == 0 and exit:
            exit = True
          else:
            exit = False
      if not exit:
        t += int(line[0])
    print(location + " - t: " + str(t))

process_notes("13-test.txt")
process_notes_pt2("13-test-pt2.txt")
process_notes("13-input.txt")
process_notes_pt2("13-input-pt2.txt")
