lines = open("input.txt").read().splitlines()

asteroids = [(x,y) for y in range(len(lines)) for x in range(len(lines[y])) if lines[y][x] == "#"] 
import math
reachable = []
trajectories = {}
def update(src,dst):
  vec = [dst[0]-src[0],dst[1]-src[1]]
  if vec == [0,0]:
    return 0
  dist = math.sqrt(vec[0]**2+vec[1]**2)
  vec[0],vec[1] = round(vec[0]/dist,5),round(vec[1]/dist,5)

  if tuple(vec) in trajectories:
    if trajectories[tuple(vec)][0] > dist:
      trajectories[tuple(vec)] = [dist,dst]
    return 0
  else:
    trajectories[tuple(vec)] = [dist,dst]
    return 1

coords = []
for asteroid in asteroids:
  sum = 0
  for neighbor in asteroids:
    sum+=update(asteroid,neighbor)
  reachable.append(sum)
  coords.append(asteroid)
  trajectories = {}

print(max(reachable))
startingCoord = coords[reachable.index(max(reachable))]
print(startingCoord)
nbDestroyed = 0

import numpy as np

def unit_vector(vector):
    return vector / np.linalg.norm(vector)
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    r= np.arccos(np.dot(v1_u, v2_u))
    dot = np.dot(v1_u,v2_u)
    det = np.linalg.det([v1_u,v2_u])
    return np.arctan2(det,dot)

while True:
  for neighbor in asteroids:
    update(startingCoord,neighbor)
  destroyed = [i[1] for i in trajectories.values()]
  if len(destroyed)+nbDestroyed > 200:
    angles = [angle_between([0,-1],[d[0]-startingCoord[0],-(d[1]-startingCoord[1])]) for d in destroyed]
    indexes = sorted(range(len(angles)),key=lambda k: angles[k])
    sortedDest = [destroyed[i] for i in indexes]
    sortedDest.reverse()
    print(sortedDest[200-nbDestroyed-1])
    break
  else:
    asteroids.remove(destroyed)
    nbDestroyed += len(destroyed)
  trajectories = {}