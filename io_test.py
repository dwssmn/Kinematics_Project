import unittest
import numpy as np

from leg_model import leg_model
from io_files import IOhelper

class TestCurve(unittest.TestCase):
    theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
    alpha = np.array([0,np.pi/2,0,0,0])
    d = np.array([0,0,0.25,0,0])
    r = np.array([0,0,0,1,1])
    base = np.array([0,0,2])
    joints = 5
    valid = np.array([True,False,False,True,True])
    leg = leg_model(theta, r,d,alpha,base,joints)     

    def test_IO(self):
        IOhelper.outputLeg(self.leg,"test.txt")   
        leg2 = IOhelper.inputLeg("test.txt")
        self.assertEqual(leg2.joints, self.leg.joints)
        self.assertEqual(leg2.alpha[0], self.leg.alpha[0])
        self.assertEqual(leg2.theta[self.joints-1], self.leg.theta[self.joints-1])
    