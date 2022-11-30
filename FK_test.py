import unittest
import numpy as np

from FK import FK
from FK import FK_dynamic
import leg_model

class TestFK(unittest.TestCase):
    theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
    alpha = np.array([0,np.pi/2,0,0,0])
    d = np.array([0,0,0.25,0,0])
    r = np.array([0,0,0,1,1])
    base = np.array([0,0,2])
    joints = 5
    valid = np.array([True,False,False,True,True])
    leg = leg_model.leg_model(theta, r,d,alpha,base,joints)
    f = FK(leg, base)
    def test_init(self):
        self.assertEqual(self.f.joints, self.joints)
    def test_FK(self):
        
        self.assertEqual(np.round(self.f.EE_pos()[0][0], decimals=5), 0.25)
        self.assertEqual(np.round(self.f.EE_pos()[0][1], decimals=5), -0.70711)
        self.assertEqual(np.round(self.f.EE_pos()[0][2], decimals=5),0.29289)
    
    def test_i(self):
        self.assertEqual(np.round(self.f.j_point(4)[0][0], decimals=5), 0.25)
        self.assertEqual(np.round(self.f.j_point(4)[0][1], decimals=5), 0)
        self.assertEqual(np.round(self.f.j_point(4)[0][2], decimals=5), 1)       

    def test_i_ill(self):
        self.assertEqual(self.f.j_point(8), -1)