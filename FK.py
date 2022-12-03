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



    def __init__(self, leg: leg_model, basepoint):
        self.basepoint = basepoint
        self.joints = leg.joints
        self.T = np.zeros((self.joints+1,4,4))
        self.T[0] = np.identity(4)
        for i in range(self.joints):
            self.T[i+1] = np.round(np.matmul(self.T[i],FK.DHMatrix(leg.theta[i], leg.alpha[i], leg.r[i],leg.d[i])),decimals=5)
            #print(self.T[i+1])
    
    def j_Transform(self,j): 
        """gets Transform matrix to j point, with 0 being base and self.joints being end effector"""
        try:
            if j > self.joints:
                raise ValueError("non-valid index")
        except ValueError as e:
            print(e)
            return
        return self.T[j]

    def j_point(self,j):
        try:
            if j > self.joints:
                raise ValueError("non-valid index")
        except ValueError as e:
            print(e)
            return -1
        return self.basepoint + self.T[j][:3,3:].reshape(1,3)

    def EE_pos(self):
        return self.basepoint + self.T[self.joints][:3,3:].reshape(1,3)
    
class FK_dynamic(FK):

    def __init__(self, leg: leg_model, basepoint, valid_points):
        """stores the DH values to be able to do multiple """
        super().__init__(leg, basepoint)
        self.model = leg
        self.valid = valid_points
    
    def recalibrate_T(self):
        """Reinitialize the transformation matrix"""
        for i in range(self.joints):
            self.T[i+1] = np.round(np.matmul(self.T[i],FK.DHMatrix(self.model.theta[i], self.model.alpha[i], self.model.r[i],self.model.d[i])),decimals=5)
    def update_theta(self,theta):
        """update the joint position"""
        self.model.theta = theta
        self.recalibrate_T()
    def update_base(self,base):
        self.basepoint = base
        self.recalibrate_T()
    def return_leg(self):
        return self.model
    #def update_alpha(self,alpha): #will not be modifying alpha will always be pi/2, 0, 0, since it defines the leg
    #    """update the joint position"""
    #    self.alpha = alpha
    #    self.recalibrate_T(self)
    
        
"""
theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
alpha = np.array([0,np.pi/2,0,0,0])
d = np.array([0,0,0.25,0,0])
r = np.array([0,0,0,1,1])
base = np.array([0,0,2])
joints = 5
valid = np.array([True,False,False,True,True])
leg = leg_model.leg_model(theta, r,d,alpha,base,joints)
 
forward  = FK(leg, base)
ee = np.array([[0.0]*3]*(leg.joints+1))
for i in range(leg.joints+1):
    ee[i] = forward.j_point(i)


print(a)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
ax.axes.set_xlim3d(left=-1, right=1) 
ax.axes.set_ylim3d(bottom=-1, top=1) 
ax.axes.set_zlim3d(bottom=0, top=2.5) 
fig.savefig('endeffector.png')

"""