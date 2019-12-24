def exec(a,b):
  line = open("input.txt").readlines()[0]
  #line = "1,1,1,4,99,5,6,0,99"
  val = [int(i) for i in line.split(",")]
  val[1] = a
  val[2] = b
  for i in range(0,len(val),4):
    #print(i)
    if val[i] == 1:
      val[val[i+3]] = val[val[i+1]] + val[val[i+2]]
    elif val[i] == 2:
      val[val[i+3]] = val[val[i+1]] * val[val[i+2]]
    else:
      #val[i]==99 or invalid opcode
      #print("out")
      break;
  
  #print(val)
  return val[0]

for i in range(0,100):
  over = False
  for j in range(0,100):
    if(19690720==exec(i,j)):
      print("i=",i,"j=",j)
      over = True
      break;
  if over:
    break