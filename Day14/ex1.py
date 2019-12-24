lines = open("input.txt").read().splitlines()
t = [line.split(" => ") for line in lines]
reactions = {r[1].split(" ")[1]:[int(r[1].split(" ")[0])]+[[[int(elem.split(" ")[0]),elem.split(" ")[1]] for elem in r[0].split(", ")]] for r in t}
available = {r:0 for r in reactions}
print(reactions,available)

import math

def reac(num, res):
  if res=="ORE":
    return num
  if available[res] >= num:
    available[res]-=num
    return 0
  #=> num > available
  num-=available[res]
  available[res] = 0
  N = math.ceil(num / float(reactions[res][0]))
  needed_ore = []
  for _ in range(N):
    needed_ore.extend([reac(reaction[0],reaction[1]) for reaction in reactions[res][1]])
  available[res] = N*reactions[res][0]-num
  #print(needed_ore)
  return sum(needed_ore)

#print(reac(1,"FUEL"))
nb_ore=1000000000000
"""
produced = 0
step = 100
while True:
  consumed = reac(step,"FUEL")
  if nb - consumed < 0:
    break
  produced += step
print(produced)
"""
cost = reac(1,"FUEL")
produced = int(nb_ore/cost)
nb_ore-=produced*cost
print(available)
saved_res = {res:produced*available[res] for res in available if available[res] != 0}
print(saved_res)
available = {r:0 for r in reactions}
o = [reac(saved_res[res],res) for res in saved_res]
print(o)
