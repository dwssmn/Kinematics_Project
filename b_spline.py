
from matplotlib import pyplot as plt
import numpy as np

def C(t,ti,m,P,n,l):
    c = [0]*l
    for k in range(l):
        for i in range(n):
            print(N(t[k],ti,i,m-n-1))
            c[k] += P[i]*N(t[k],ti,i,m-n-1)
    return np.asarray(c)
    

#(t-ti[i])/(ti[i+j] - ti[i]) *N(t,ti,i,j-1) + (ti[i+j+1] -t)/(ti[i+j+1]- ti[i+1]) *N(t,ti,i+1,j-1)

def N(t,ti,i,j):

    if j>0:
        N1 = N(t,ti,i,j-1)
        N2 = N(t,ti,i+1,j-1)
        n=0
        if N1>0:
            n += (t-ti[i])/(ti[i+j] - ti[i]) *N1
        if N2>0:
            n+= (ti[i+j+1] -t)/(ti[i+j+1]- ti[i+1])*N2
        return n
    else:
        return N0(t,ti[i],ti[i+1])

def N0(t, ti,tip1):
    if t<tip1 and t>=ti and ti<tip1:
        return 1
    return 0


ti = [0,0.01,0.05,0.1,0.2,0.3,0.5,0.6,0.7,0.75,0.8,0.9,0.9,0.9,1]
t = [0, 0.1,0.4, 0.5,0.65,0.85,1]
l = len(t)
m = len(ti)
P = np.array([[0,1,0], [1,1,0],[1.2,1,0], [1.2,2,0], [2,3,0]])
n = len(P)
print(C(t,ti,m,P,n,l))

curve = C(t,ti,m,P,n,l)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
print(curve)
ax.plot([x[0] for x in curve], [x[1] for x in curve],[x[2] for x in curve] )
fig.savefig('test.png')