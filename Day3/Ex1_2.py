file = open("input.txt").readlines()
line1 = file[0]
line2 = file[1]

point = [0,0]
def evaluate_segment(s):
    length = int(s[1:])
    if s[0] == 'R':
        vec = [1,0]
        direction = 'H'
    elif s[0] == 'L': 
        vec = [-1,0]
        direction = 'H'
    elif s[0] == 'U':
        vec = [0,1]
        direction = 'V'
    elif s[0] == 'D':
        vec = [0,-1]
        direction = 'V'
    segment = [list(point)]
    
    point[0] = point[0] + vec[0] * length
    point[1] = point[1] + vec[1] * length

    segment.append(list(point))
    segment.append(direction)
    segment.append(length)
    segment.append(vec)

    return segment
    

line1 = [evaluate_segment(s) for s in line1.split(",")]
point = [0,0]
line2 = [evaluate_segment(s) for s in line2.split(",")]

#print(line1)
#print(line2)

points = []
num1 = 0
for seg1 in line1:
    num2 = 0
    for seg2 in line2:
        if(seg1[2] == seg2[2]): continue;
        segH = seg1
        segV = seg2
        if seg1[2] == 'V':
            segH = seg2
            segV = seg1

        if segH[0][0] > segH[1][0]:
            segH[0], segH[1] = segH[1], segH[0]
        if segV[0][1] > segV[1][1]:
            segV[0],segV[1] = segV[1],segV[0]
        if segV[0][0] >= segH[0][0] and segV[0][0] <= segH[1][0] and segH[0][1] >= segV[0][1] and segH[0][1] <=segV[1][1]:
            if not(segH[0] == [0,0] and segV[0] == [0,0]) and not(segH[1] == [0,0] and segV[1] == [0,0]):
              point = [segV[0][0],segH[0][1]]
              points.append(list(point))

print(points)

dist = [abs(p[0])+abs(p[1]) for p in points]
print(min(dist))

def tickLength(p,line):
  pos = [0,0]
  sum = 0
  for s in line:
    vec = s[4]
    for _ in range(s[3]):
      pos[0] += vec[0]
      pos[1] += vec[1]
      sum += 1
      if pos == p[0:2]:
        return sum

minTicks = [tickLength(p,line1)+tickLength(p,line2) for p in points]
print(min(minTicks))