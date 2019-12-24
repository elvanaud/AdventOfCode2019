def computer(state,inputs):
  prog = state[0]
  pc = state[1]

  return_value = -1
  over = False
  pause_exec = False

  def read(desc):
    if desc[1] == 1:
      return desc[0] #immediat
    return prog[desc[0]]
    
  def write(adr,data):
    prog[adr] = data
  def write(desc,data):
    prog[desc[0]] = data
  
  def inst_add(param):
    write(param[2], read(param[0]) + read(param[1]))
    return 4 #inst size
  
  def inst_mul(param):
    write(param[2], read(param[0]) * read(param[1]))
    return 4
  
  def inst_quit(param):
    nonlocal over
    over = True
    return 1
  
  def inst_in(param):
    #val = input("Enter value: ")
    val = inputs[0]
    del inputs[0]
    write(param[0],int(val))
    return 2
  
  def inst_out(param):
    val = read(param[0])
    #print(val)
    nonlocal return_value,pause_exec
    return_value = val
    pause_exec = True
    return 2
  
  def inst_jump_if_true(param):
    if read(param[0]) != 0:
      nonlocal pc
      pc = read(param[1])
      return 0
    return 3
  
  def inst_jump_if_false(param):
    if read(param[0]) == 0:
      nonlocal pc
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
  
  instructions = {
    1: inst_add,
    2: inst_mul,
    99: inst_quit,
    3: inst_in,
    4: inst_out,
    5: inst_jump_if_true,
    6: inst_jump_if_false,
    7: inst_less_than,
    8: inst_equals
  }
  while not over:
    opcode = prog[pc]%100
  
    modeA = int(prog[pc] / 100)%10
    modeB = int(prog[pc] / 1000)%10
    modeC = int(prog[pc] / 10000)%10
  
    params = [[prog[pc+1],modeA],[prog[pc+2],modeB],[prog[pc+3],modeC]]
  
    inst_length = instructions[opcode](params)
    pc += inst_length
    if over:
      state[2] = 1
      return_value = -2
    if pause_exec:
      state[1] = pc
      break
  return return_value

line = open("input.txt").readlines()[0]

available_num = range(5,10)
import itertools
perms = list(itertools.permutations(available_num))

prog = [int(i) for i in line.split(",")]
prog.extend([0,0,0,0]) #un peu dégueux

signals = []
for amplifiers in perms:
  amplifiers = [[amp,[list(prog),0,0]] for amp in amplifiers] #state of each amplifier program
  ret = 0
  loopOver = False
  firstIter = True
  while not loopOver:
    for seq_num in amplifiers: #goes through each program
      inputs = [ret]
      if firstIter:
        inputs = [seq_num[0],ret] #the first iteration needs the two inputs
      retp = computer(seq_num[1],inputs)
      if seq_num[1][2] == 1: #indicates the state of the process (written by the process itself)
        loopOver = True #it's a form of cooperating multitasking
        retp = ret
      ret = retp
    firstIter = False
  signals.append(ret)

print(max(signals))

#cooperative scheduling:
#computer is called and manages its own segment
#cyclic execution of all those tasks until all are finished
#plus code to manage init inputs and "pipes" between processes, plus behavior when finished
#need to communicate through a state "object"
#state = ->(memory+pc, inputs), <-(outputs,state)
#sending list of inputs and expecting an output: behavior in user func ?
#pipe object:pipe(a,b): setState(b).input = getState(a).output
#for scheduling_order in perms: schedule(scheduling_order) #passing some state as a return value(signal)?