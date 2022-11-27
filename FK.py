import leg_model
import numpy as np
from matplotlib import pyplot as plt

class FK:

    @staticmethod
    def DHMatrix(theta, alpha, r, d):

        return np.array([   [np.cos(theta), -np.sin(theta)*np.cos(alpha),np.sin(theta)*np.sin(alpha), r*np.cos(theta)],
                            [np.sin(theta), np.cos(theta)*np.cos(alpha),  -np.cos(theta)*np.sin(alpha), r*np.sin(theta) ],
                            [0            , np.sin(alpha)            ,   np.cos(alpha)          ,  d],
                            [0,0,0,1]
                            ])



    def FK(self, leg: leg_model, basepoint):
        points = np.empty((leg.joints+1,3))
        points[0] = basepoint
        self.basepoint = basepoint
        self.T = np.array([[0]*4]*4)
        for i in range(leg.joints):
            if i == 0:
                T = np.round(FK.DHMatrix(leg.theta[i], leg.alpha[i], leg.r[i],leg.d[i]),decimals=5)
            else: 
                T = np.round(np.matmul(T,FK.DHMatrix(leg.theta[i], leg.alpha[i], leg.r[i],leg.d[i])),decimals=5)
            print(T)
            
            points[i+1] = T[:3,3:].reshape(1,3) + points[0]
            
        return points
    
    def i_j_Transform(i,j): 
        
        for k in range(i+1,j):
        return 

    def EE_pos():


theta = np.array([-np.pi/2,np.pi/4,-1*np.pi/2])
alpha = np.array([np.pi/2,0,0])
d = np.array([0,0,0])
r = np.array([0.25,1,1])
base = np.array([0,2,0])
joints = 3
leg = leg_model.leg_model(theta, r,d,alpha,base,joints)
ee = FK.FK(leg, base)
print(ee)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
fig.savefig('endeffector.png')
