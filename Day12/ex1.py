lines = open("input.txt").read().splitlines()
lines = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>".splitlines()
moons = [[[int(var.split("=")[1]) for var in line[1:-1].split(",")],[0,0,0]] for line in lines]

moons_save = []
timestep = 0
while True:
  moons_copy = []
  for moon in moons:
    velocity = moon[1]
    for neighbor in moons:
      if neighbor[0] == moon[0]:
        continue
      subVelocity = [-1 if v < 0 else 1 if v > 0 else 0 for v in [neighbor[0][i]-moon[0][i] for i in range(len(moon[0]))]]
      velocity = [velocity[i]+subVelocity[i] for i in range(len(velocity))]
    moons_copy.append([[moon[0][i]+velocity[i] for i in range(len(velocity))],velocity])
  moons = moons_copy
  if moons in moons_save:
    print("YO:",timestep)
    break
  moons_save.append(moons)
  timestep+=1


print(moons)
print(sum([sum([abs(v) for v in moon[0]])*sum([abs(v) for v in moon[1]]) for moon in moons]))