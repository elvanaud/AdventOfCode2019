line = open("input.txt").readlines()[0]
prog = [int(i) for i in line.split(",")]
prog.extend([0 for _ in range(10000)]) #un peu dégueux

relBase = 0
human_prompt = False
inputs = []
outputs = []

def read(desc):
  if desc[1] == 1:
    return desc[0] #immediat
  if desc[1] == 2:
    return prog[relBase+desc[0]]
  return prog[desc[0]]
  
def write(desc,data):
  if desc[1] == 2:
    prog[relBase+desc[0]] = data
  else:
    prog[desc[0]] = data

over = False
pc = 0

def inst_add(param):
  write(param[2], read(param[0]) + read(param[1]))
  return 4 #inst size

def inst_mul(param):
  write(param[2], read(param[0]) * read(param[1]))
  return 4

def inst_quit(param):
  global over
  over = True
  return 1

def inst_in(param):
  if human_prompt:
    val = input("Enter value: ")
  else:
    val = inputs.pop(0)
    #print(val," consumed")
  write(param[0],int(val))
  return 2

def inst_out(param):
  val = read(param[0])
  if human_prompt:
    print(val)
  else:
    outputs.append(val)
  return 2

def inst_jump_if_true(param):
  if read(param[0]) != 0:
    global pc
    pc = read(param[1])
    return 0
  return 3

def inst_jump_if_false(param):
  if read(param[0]) == 0:
    global pc
    pc = read(param[1])
    return 0
  return 3

def inst_less_than(param):
  if read(param[0]) < read(param[1]):
    write(param[2],1)
  else:
    write(param[2],0)
  return 4

def inst_equals(param):
  if read(param[0]) == read(param[1]):
    write(param[2],1)
  else:
    write(param[2],0)
  return 4
def inst_relBase_offset(param):
  global relBase
  relBase = relBase + read(param[0])
  return 2

instructions = {
  1: inst_add,
  2: inst_mul,
  99: inst_quit,
  3: inst_in,
  4: inst_out,
  5: inst_jump_if_true,
  6: inst_jump_if_false,
  7: inst_less_than,
  8: inst_equals,
  9: inst_relBase_offset
}
def tick():
  global pc
  opcode = prog[pc]%100

  modeA = int(prog[pc] / 100)%10
  modeB = int(prog[pc] / 1000)%10
  modeC = int(prog[pc] / 10000)%10

  params = [[prog[pc+1],modeA],[prog[pc+2],modeB],[prog[pc+3],modeC]]

  inst_length = instructions[opcode](params)
  pc += inst_length

tiles = {0:" ",1:"X",2:"#",3:"-",4:"O"}
map = [[" " for _ in range(50)] for _ in range(21)]
total_nbTiles = (38*21)-1
curr_nbTiles = 0
prog[0] = 2
prog_base = list(prog)
#cpt = 0
score = 0
base_inputs = []
inputs = list(base_inputs)#[1]
nbZeros = 0

inputs = [1]
for _ in range(138):
  inputs.append(0)
inputs.extend([-1,-1])
for _ in range(680):
  inputs.append(0)
inputs.extend([-1,-1,-1,-1,-1,-1])
for _ in range(40):
  inputs.append(0)
inputs.extend([-1,-1,-1,-1])
for _ in range(170):
  inputs.append(0)
inputs.extend([1,1,1,1,1,1,1,1])
for _ in range(200):
  inputs.append(0)
inputs.extend([-1,-1,-1,-1])
for _ in range(87):
  inputs.append(0)
inputs.extend([1,1,1,1,1,1,1,1,1,1,1,1,1])
#for _ in range(60):
#  inputs.append(0)
#inputs.extend([1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,1,1])
base_inputs=list(inputs)
inputs=list(base_inputs)
i=0
firstIter = True
while True:
  while not over:
    tick()
    if len(outputs) == 3:
      x = outputs.pop(0)
      y = outputs.pop(0)
      tile = outputs.pop(0)
      if x == -1 and y == 0:
        score = tile
        continue
      map[y][x] = tiles[tile]
      curr_nbTiles+=1
    if not firstIter and curr_nbTiles == 1:
      curr_nbTiles = 0
      #for line in map:
      #  print("".join(line))
    if not firstIter and len(inputs) == 0:
      nbZeros+=1
      control = 0
      inputs.append(control)
    if curr_nbTiles == total_nbTiles:
      curr_nbTiles = 0
      firstIter = False
      for line in map:
        print("".join(line))
    if "O" in map[18]: prev_ball_pos = map[18].index("O")
    if "O" in map[19]:
      #ball_pos = map[19].index("O")-prev_ball_pos
      offset = prev_ball_pos-map[19].index("-")
      print("yo",offset)
      for line in map:
        print("".join(line))
      print(nbZeros)
      if offset != 0: #not (-1<=offset<=1):
        for _ in range(nbZeros-(abs(offset))-1):
          base_inputs.append(0)
        val = 1 if offset > 0 else -1
        for _ in range(abs(offset)+1):
          base_inputs.append(val)
        break
  #print(base_inputs)
  prog = list(prog_base)
  inputs = list(base_inputs)
  curr_nbTiles = 0
  over = False
  relBase = 0
  pc=0
  i+=1
  firstIter=True
  if i % 40==0:
    for line in map:
      print("".join(line))

  if sum([len(list(filter(lambda c: c=="#",line))) for line in map]) <= 3:
    print(score)
    print(base_inputs)
    if sum([len(list(filter(lambda c: c=="#",line))) for line in map]) == 0:
      break
  nbZeros=0
  map = [[" " for _ in range(50)] for _ in range(21)]
  #break

#for line in map:
#  print("".join(line))
#print(cpt)
print(len(list(filter(lambda c: c=="#",map[0])))) #w:38,h:21
print(score)
print(len(inputs))