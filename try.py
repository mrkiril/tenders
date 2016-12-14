print("try py")
import numpy as np
import math
import operator
import matplotlib.pyplot as plt
import collections as cl
import time
import sys

s = "mama papa gaga"
#print(s.find("papa"))
def mnk():
    pass

def pirson(a, b):
    while len(a) < len(b):
        a.append(a[-1])

    while len(b) < len(a):
        b.append(b[-1])

    if len(set(a)) == 1 : 
        for i in range(len(a) ):
            a[i] = a[i]-0.00000001*i

    if len(set(b)) == 1 : 
        for i in range(len(b) ):
            b[i] = b[i]-0.00000001*i
        
    mean_a = np.mean(a)
    mean_b = np.mean(b)
    sum_1 = 0.0
    for i in range(len(a)):
        sum_1 += (a[i] - mean_a) * (b[i] - mean_b)
    sum_2 = 0.0
    sum_3 = 0.0

    for i in range(len(a)):
        sum_2 += (a[i] - mean_a)**2
        sum_3 += (b[i] - mean_b)**2

    sum_4 = math.sqrt(sum_2 * sum_3)
    return sum_1 / sum_4
#print(p)



x = {"la": 2, "lal": 4, "lalk": 3, "lalka": 1, "l": 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1))
#print(x)
#print(sorted_x)
#print( round(0.9534 , 2)  )
a = [4999,  4999, 4999, 4999]
b = [4900,  4900, 4900, 4900]
c = [4480,  4480, 4480, 4480]
d = [4368,  4368, 3190, 3190]
f = [4196.6,4196.6 ,4196.6 ,4196.6]
#pirs = pirson(d, f)
#print( pirs )


x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([0.0, 1.2, 1.9, 3.15])
z = np.polyfit(x, d, 1)
print(z)
p = np.poly1d(z)

#p30 = np.poly1d(np.polyfit(x, d, 1))

xp = np.linspace(-2, 6, 100)

_ = plt.plot(x, d, '.', xp, p(xp), '-')
#plt.ylim(-2,6)

#plt.show()

def slope(y1):
    y = np.array(y1)
    x = np.array([0.0, 1.0, 2.0, 3.0])
    z = np.polyfit(x, d, 1)
    return z[1]/z[0]

    
def intersection(a, b):
    if a[0] > b[0] and a[-1] > b[-1]:
        return 0

    elif a[0] > b[0] and a[-1] < b[-1]:
        return 1

    elif a[0] < b[0] and a[-1] < b[-1]:
        return 0

    elif a[0] < b[0] and a[-1] > b[-1]:
        return 1


num_part = {}
num_part["a"] = { "items": 5  , "count": 105}
num_part["b"] = { "items": 15 , "count": 1}
num_part["c"] = { "items": 25 , "count": 5}
num_part["d"] = { "items": 51 , "count": 150}
num_part["e"] = { "items": 35 , "count": 75}
num_part["f"] = { "items": 14 , "count": 19}

d_descending = sorted(num_part.items(), key=lambda kv: kv[1]['items'], reverse=True)

'''

print( d_descending)
_=input()
with open("partisipants", "wt") as f:
    for i in  range(len(d_descending)):
        k = d_descending[i][0]
        v = d_descending[i][1]
        f.write(  'EDRPOU: %s \t items %.4f \t count %.4f' % ( k, v["items"] , v["count"] )  )
        f.write("\r\n")


'''


for i in range(1000):
    time.sleep(0.1)
    sys.stdout.write("\r%.1f%%" % (i/10))
    sys.stdout.flush()

