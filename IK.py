import numpy as np
from itertools import chain
import matplotlib.pyplot as plt

import leg_model
from FK import FK_dynamic
from FK import FK

class IK:

    def __init__(self, model: leg_model,basepoint, accuracy, valid):
        """Initializes the accuracy and leg"""
        self.FKdynamic = FK_dynamic(model, basepoint, valid)
        self.model = model
        self.accuracy = accuracy
    
    def Inverse_Kinematics(self, target: np.array):
        """Attempts to move the leg to the target"""
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
            d_theta = np.transpose(0.01*np.matmul(np.linalg.pinv(self.Jacobian()), np.transpose(target-ee)))[0]
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
                if k>1000:
                    raise ValueError("Inverse Kinematics has not converged -there is an error")
            except ValueError as e:
                print(e)
                self.FKdynamic.update_theta(init_theta)
                return -1
        return

    def Jacobian(self):
        """Jacobian returns the matrix of joint rotations to end effetor translations dx/dtheta for each point"""
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
        """Gets the rotational axes for each significant joint"""
        if i == 0:
            return [0,0,1]
        elif i ==1:
            return [0,0,1]
        elif i >1:
            return [np.sin(self.model.alpha[1])*np.sin(self.model.theta[0]),np.sin(self.model.alpha[1])*np.cos(self.model.theta[0]),np.cos(self.model.alpha[1])]

    def returnFK(self):
        return self.FKdynamic
