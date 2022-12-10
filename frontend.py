import numpy as np

import IK
import FK
import leg_model
from bezier_curve import bezierCurveFit
import plotter
from io_files import IOhelper

class inputReader():
    
    def __init__(self):
        """Initial defaults for the leg"""
        self.theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
        alpha = np.array([0,np.pi/2,0,0,0])
        d = np.array([0,0,0.25,0,0])
        r = np.array([0,0,0,1,1])
        base = np.array([0,0,2])
        joints = 5
        self.valid = np.array([True,False,False,True,True])
        self.leg = leg_model.leg_model(self.theta, r,d,alpha,base,joints)
        self.FK = FK.FK_dynamic(self.leg,base,self.valid)
        self.plot = plotter.plotter()
        self.acc = 0.04
        print("Loaded leg with " + str(self.theta))

    def run_loop(self):
        """Runs the loop in the command line until exit is called"""
        isrunning = True
        case = -1
        
        while(isrunning):
            try:
                case = int(input("Options:\n  View Leg (1):\n  Change picture prefix(2)\n  Define joint angles (3):\n  Change Base Point(4)\n  Find End Effector (5):\n  Go to point (6):\n  Define curve (7):\n  Move Leg along Curve (8):\n  Output Leg Data (9):\n  Input Leg Data (10):\nExit(0):  "))
                if case == 0:
                    print("--Exiting--")
                    isrunning = False
                elif case ==1:
                    self.plot.plotLeg(self.FK)
                elif case ==2:
                    self.plot.changeOutput( str(input("Change plotting output destination to: ")))
                elif case == 3:
                    i = 0
                    ntheta = np.array([0.0]*(self.FK.joints))
                    while i < self.FK.joints:
                        if i==0:
                            ntheta[i] = float(input("Define theta "+str(i) +": "))
                            i=i+2
                        else:
                            ntheta[i] = float(input("Define theta "+str(i-2) +": "))
                        i=i+1
                    print(ntheta)
                    self.FK.update_theta(ntheta)
                    self.leg = self.FK.return_leg()
                elif case ==4:
                    base = np.array([0.0]*3)
                    for i in range(3):
                        base[i] = float(input("Define position"+str(i) +": "))
                    self.FK.update_base(base)
                    self.leg = self.FK.return_leg()               
                elif case == 5:
                    print("The end effector is " + str(self.FK.EE_pos()))
                elif case ==6:
                    ik = IK.IK(self.leg, self.leg.base, self.acc, self.valid)
                    print("What position to move to? ")
                    point = np.array([0.0]*3)
                    for i in range(3):
                        point[i] = float(input("Define position"+str(i) +": "))
                    if(ik.Inverse_Kinematics(point)==-1):
                        print("IK Failed: Out of range")
                    else:
                        print("Success: EE at " + str(ik.FKdynamic.EE_pos()))
                        self.FK = ik.FKdynamic
                        self.leg = self.FK.return_leg()
                        self.plot.plotLeg(self.FK)
                elif case ==7:
                    #begin = np.array([0.25, -0.37, 0])
                    begin = np.array([0.0]*3)
                    for i in range(3):
                        begin[i] = float(input("Define position"+str(i) +": "))
                    num = int(input("Define number of points of resolution: "))
                    height = float(input("Define the height: "))
                    f_dist = float(input("Define the forward length: "))
                    s_dist = float(input("Define the sidways length: "))
                    curve = bezierCurveFit(num,begin, height,f_dist,s_dist)
                    self.plot.plotCurve(curve)
                elif case == 8:
                    begin = np.array([0.0]*3)
                    for i in range(3):
                        begin[i] = float(input("Define position"+str(i) +": "))
                    num = int(input("Define number of points of resolution: "))
                    height = float(input("Define the height: "))
                    f_dist = float(input("Define the forward length: "))
                    s_dist = float(input("Define the sidways length: "))
                    curve = bezierCurveFit(num,begin, height,f_dist,s_dist)
                    ik = IK.IK(self.leg, self.leg.base, self.acc, self.valid)
                    self.plot.initMulti()
                    for i in curve:
                        target = i
                        print("Target" + str(i))
                        ik.Inverse_Kinematics(target)
                        
                        self.plot.plotLeg(ik.FKdynamic,multi=True)
                    self.plot.plotCurve(curve, multi=True)
                    self.plot.printMulti()    
                elif case ==9:
                    file = str(input("Filename to output to: ")) + ".txt"
                    IOhelper.outputLeg(self.leg, file)
                elif case ==10:
                    file = str(input("Filename to read from: ")) + ".txt"
                    self.leg = IOhelper.inputLeg(file)
                    self.FK.leg = self.leg
                    self.FK.recalibrate_T()
            except ValueError as e:
                print("Input Error: try again")





run = inputReader()
run.run_loop()


