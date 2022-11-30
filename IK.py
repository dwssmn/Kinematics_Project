import numpy as np
from itertools import chain
import matplotlib.pyplot as plt

import leg_model
from FK import FK_dynamic
from FK import FK

class IK:

    def __init__(self, model: leg_model,basepoint, accuracy, valid):
        self.FKdynamic = FK_dynamic(model, basepoint, valid)
        self.model = model
        self.accuracy = accuracy
    
    def Inverse_Kinematics(self, target: np.array):
        ee = self.FKdynamic.EE_pos()
        #print("ee: ")
        #print(ee)
        init_theta = self.FKdynamic.model.theta
        k=0
        while(np.sqrt(np.sum(np.square(ee-target)))> self.accuracy):
            #print(np.sqrt(np.sum(np.square(ee-target))))
            #print(self.accuracy)
            #dtheta = J^-1 * dx
            #use pseudoinverse since it is not guaranteed reversible
            #print(np.linalg.pinv(self.Jacobian()))
            #print(target-ee)
            d_theta = np.transpose(0.1*np.matmul(np.linalg.pinv(self.Jacobian()), np.transpose(target-ee)))[0]
            #print("d_theta")
            #update the given theta
            d_theta = np.insert(d_theta, [1,1],[0.0,0.0],axis=0)
            #print(d_theta)
            self.FKdynamic.update_theta(self.FKdynamic.model.theta + d_theta)

            #print("ee_pos")
            ee = self.FKdynamic.EE_pos()
            #print(ee)
            k=k+1
            
            try:
                if k>500:
                    raise ValueError("Inverse Kinematics has not converged -there is an error")
            except ValueError as e:
                print(e)
                self.FKdynamic.update_theta(init_theta)
                return -1
        return

    def Jacobian(self):
        J = np.array([[0.0]*(self.model.joints-2)] *3)
        k = 0
        jpoints = np.arange(0,self.model.joints,1)[self.FKdynamic.valid]
        for i in jpoints:
            for j in range(3):
                J[k][j]= np.cross(self.getRotationAxis(i), (self.FKdynamic.EE_pos()[0]-self.FKdynamic.j_point(i)[0]))[j]
            k = k +1
        #print(J)
        return J

    def getRotationAxis(self,i):
        if i == 0:
            return [0,0,1]
        elif i ==1:
            return [0,0,1]
        elif i >1:
            return [np.sin(self.model.alpha[1])*np.sin(self.model.theta[0]),np.sin(self.model.alpha[1])*np.cos(self.model.theta[0]),np.cos(self.model.alpha[1])]
"""
theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
alpha = np.array([0,np.pi/2,0,0,0])
d = np.array([0,0,0.25,0,0])
r = np.array([0,0,0,1,1])
base = np.array([0,0,2])
valid = np.array([True,False,False,True,True])
joints = 5
leg = leg_model.leg_model(theta, r,d,alpha,base,joints)
ik = IK(leg,base,0.02,valid)
target = np.array([0.25, -0.5, 0])
print(ik.FKdynamic.model.theta)
ik.Inverse_Kinematics(target)
print(ik.FKdynamic.model.theta)

ee = np.array([[0.0]*3]*(leg.joints+1))
for i in range(leg.joints+1):
    ee[i] = ik.FKdynamic.j_point(i)

print(ee)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
ax.axes.set_xlim3d(left=-1, right=1) 
ax.axes.set_ylim3d(bottom=-1, top=1) 
ax.axes.set_zlim3d(bottom=0, top=2.5) 
fig.savefig('IK_end_effector.png')
"""