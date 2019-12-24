lines = open("input.txt").read().splitlines()
orbitsOn = {l.split(")")[1]:l.split(")")[0] for l in lines}

def computeSum(star):
  star = orbitsOn[star]
  sum = 1
  while star != "COM":
    sum += 1
    star = orbitsOn[star]
  return sum

sum = 0
for star in orbitsOn:
  sum += computeSum(star)
print(sum)

def computeRootPath(star):
  star = orbitsOn[star]
  path = [star]
  while star != "COM":
    star = orbitsOn[star]
    path.append(star)
  path.reverse()
  return path

pathYou = computeRootPath("YOU")
pathSan = computeRootPath("SAN")
i = 0
while pathSan[i] == pathYou[i]:
  i+=1
shortestPath = len(pathSan)+len(pathYou)-2*i
print(shortestPath)