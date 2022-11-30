import unittest
import numpy as np

from IK import IK
import leg_model

class TestIK(unittest.TestCase):
    theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
    alpha = np.array([0,np.pi/2,0,0,0])
    d = np.array([0,0,0.25,0,0])
    r = np.array([0,0,0,1,1])
    base = np.array([0,0,2])
    valid = np.array([True,False,False,True,True])
    joints = 5
    leg = leg_model.leg_model(theta, r,d,alpha,base,joints)

    def Simple_IK(self):
        acc = 0.02
        ik = IK(self.leg,self.base,acc,self.valid)
        target = np.array([0.25, -0.3, 0])
        ik.Inverse_Kinematics(target)

        ee = ik.FKdynamic.EE_pos()
        self.assertLessEqual(np.sqrt(np.sum(np.square(ee-target))), acc)
    def Ik_acc(self):
        acc = 0.05
        ik = IK(self.leg,self.base,acc,self.valid)
        target = np.array([0.25, -0.3, 0])
        ik.Inverse_Kinematics(target)

        ee = ik.FKdynamic.EE_pos()
        self.assertLessEqual(np.sqrt(np.sum(np.square(ee-target))), acc)
    
    def IK_diverge(self):
        acc = 0.01
        ik = IK(self.leg,self.base,acc,self.valid)
        target = np.array([0.25, -0.8, 0])
        self.assertEqual(ik.Inverse_Kinematics(target),-1)
