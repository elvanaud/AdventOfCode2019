line = open("input.txt").readlines()[0]

#line = "0222112222120000"
width = 25
height = 6

layers = [line[i:i+width*height] for i in range(0,len(line),width*height)]
print(layers)
minNbZeros = len(list(filter(lambda c: c == '0',layers[0])))
minLayer = layers[0]
for layer in layers:
  nbZeros = len(list(filter(lambda c: c == '0',layer)))
  if nbZeros < minNbZeros:
    minNbZeros = nbZeros
    minLayer = layer
#print(minLayer)
res = len(list(filter(lambda c: c == '1',minLayer))) * len(list(filter(lambda c: c == '2',minLayer)))

img = ""
for el in zip(*layers):
  for c in el:
    if c != '2':
      img += c
      break
      
for i in range(0,len(img),width):
  print(img[i:i+width])

