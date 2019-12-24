
def isCode(num):
  prev_digit = num % 10
  num = int(num / 10)
  double = False
  dd = 1
  for _ in range(6-1):
    digit = num % 10
    if digit > prev_digit:
      return False
    if digit == prev_digit:
      dd += 1
    else:
      if dd == 2:
        double = True
      dd = 1
    prev_digit = digit
    num = int(num / 10)
  if dd == 2:
    return True
  return double

cpt = 0
for i in range(284639,748759+1):
  if isCode(i):
    cpt += 1
print(cpt)
