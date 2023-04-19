import  subprocess

c1 = subprocess.call(['python','b1.py'])
c1.wait()
c2 = subprocess.call(['python','b2.py'])
c2.wait()
c3 = subprocess.call(['python','b3.py'])  

print("Total_distruction")
