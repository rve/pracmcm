#!/usr/bin/env python2
import os

def mdef(s, name, val):
  return s + " -D" + name + "=" + str(val)

if __name__ == "__main__":
  os.system("rm test.out")
  for w in range(1, 10):
      #for c2 in range(5, 40, 5):
        c2 = 20
        s ='g++ main.c pso.c -o a.out'
        s = mdef(s, "W_FUN", w*0.1)
        s = mdef(s, "MC1", c2 * 0.1)
        s = mdef(s, "MC2", c2 * 0.1)
        os.system(s)
        title = ""
        #title += "echo \"w c1 " + str(w*0.1) + " " + str(c2 *0.1) + " \">>test.out"
        print (s)
        os.system(title)
        os.system("./a.out >> test.out")
