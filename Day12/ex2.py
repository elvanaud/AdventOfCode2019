lines = open("input.txt").read().splitlines()
lines = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>".splitlines()
moons = [[[int(var.split("=")[1]) for var in line[1:-1].split(",")],[0,0,0]] for line in lines]
import copy
moons_save = []
timestep = 0
while True:
  moons_copy = []
  for i_moon in range(len(moons)):
    moon = moons[i_moon]
    velocity = moon[1]
    for i_neighbor in range(i_moon+1,len(moons)):
      neighbor = moons[i_neighbor]
      #if neighbor[0] == moon[0]:
        #continue
      if neighbor[0][0] > moon[0][0]:
        velocity[0]+=1
        neighbor[1][0]-=1
      elif neighbor[0][0] < moon[0][0]:
        velocity[0]-=1
        neighbor[1][0]+=1
      if neighbor[0][1] > moon[0][1]:
        velocity[1]+=1
        neighbor[1][1]-=1
      elif neighbor[0][1] < moon[0][1]:
        velocity[1]-=1
        neighbor[1][1]+=1
      if neighbor[0][2] > moon[0][2]:
        velocity[2]+=1
        neighbor[1][2]-=1
      elif neighbor[0][2] < moon[0][2]:
        velocity[2]-=1
        neighbor[1][2]+=1
    moons_copy.append([moon[0][i]+velocity[i] for i in range(len(velocity))])
    #moons_copy.append([[moon[0][i]+velocity[i] for i in range(len(velocity))],list(velocity)])
  #moons = [[moons_copy[i],moons[i][1]] for i in range(len(moons))]
  #print(moons)
  #print(moons_save)
  for i in range(len(moons_copy)):
    moons[i][0] = moons_copy[i]
  
  #negative number???
  """
  hashmoon = [(moon[0][0]*10**20)+(moon[0][1]*10**16)+(moon[0][2]*10**12)+(moon[1][0]*10**8)+(moon[1][1]*10**4)+(moon[1][2]*10**0)for moon in moons]
  if timestep % 1000000 == 0:
    print(moons)
    if hashmoon in moons_save:
      print("YO:",timestep)
      break
    print(timestep)
  moons_save.append(hashmoon)
  
  """
  if timestep % 10000 == 0:
    print(moons)
    if moons in moons_save:
      print("YO:",timestep)
      break
    print(timestep)
  
  moons_save.append(copy.deepcopy(moons))#time

  timestep+=1


print(moons)
print(sum([sum([abs(v) for v in moon[0]])*sum([abs(v) for v in moon[1]]) for moon in moons]))