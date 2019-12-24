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

map = [[0 for _ in range(1000)] for _ in range(1000)]
pos = [500,500]
map[pos[1]][pos[0]] = 1
inputs.append(1)
orientation = 0
dir = [[0,-1],[1,0],[0,1],[-1,0]]
explored = set([])
while not over:
  tick()
  if len(outputs)==2:
    color = outputs.pop(0)
    dirRequest = outputs.pop(0)
    map[pos[1]][pos[0]] = color
    if dirRequest == 0:
      orientation -= 1
    else:
      orientation += 1
    orientation %= 4
    explored.add(pos[0]*1000+pos[1])
    pos = [pos[0]+dir[orientation][0],pos[1]+dir[orientation][1]]
    inputs.append(map[pos[1]][pos[0]])


print(len(explored))
for line in map[500-5:500+10]:
  print("".join(["#" if c == 1 else " " for c in line[500-5:500+45]]))