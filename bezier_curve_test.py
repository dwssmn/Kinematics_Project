import unittest
import numpy as np

from bezier_curve import bezierCurve
from bezier_curve import bezierCurveFit

class TestCurve(unittest.TestCase):
    points = np.array([[0.25, -0.4, 0],[.5,0,.25],[.5,0,.25],[0.25,0,0]])
    times = np.arange(0,1.01,0.01)
    begin = np.array([0.25, -0.37, 0])
    def test_b_curve(self):
        c = bezierCurve(self.times, self.points, 4)
        self.assertEqual(c[50][2], 0.1875)
        self.assertEqual(c[0][0], 0.25)
        self.assertEqual(c[100][0], 0.25)
    def test_b_height(self):
        c = bezierCurveFit(15,self.begin, 0.3,.75,0) 
        self.assertEqual(c[7][2], 0.3)
        self.assertEqual(c[14][1],0.38)
    