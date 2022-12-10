from matplotlib import pyplot as plt
import numpy as np



import FK
class plotter():
    def __init__(self):
        self.output = "default"
    def plotLeg(self, fk:FK.FK,multi=False):
        """Plots a single leg"""
        if not multi:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(projection='3d')
        ee = np.array([[0.0]*3]*(fk.joints+1))
        for i in range(fk.joints+1):
            ee[i] = fk.j_point(i)
        self.ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
        self.setLimits(fk.basepoint[0]-1, fk.basepoint[1]-1, fk.basepoint[2]-3, fk.basepoint[0]+1, fk.basepoint[1]+1, fk.basepoint[2]+1)

        #if not plotting multiple legs, output and clear
        if not multi:
            self.fig.savefig(self.output + "_Leg"+ ".png")
            plt.clf()
    def plotCurve(self, curve,multi=False):
        """Plots a curve along a range"""
        if not multi:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(projection='3d')
        self.ax.plot([x[0] for x in curve], [x[1] for x in curve],[x[2] for x in curve] )
        self.setLimits(-1,-1,0,1,1,2.5)

        #if not plotting multiple legs/curves, output and clear
        if not multi:
            self.fig.savefig(self.output + "_curve"+ ".png")
            plt.clf()
    def initMulti(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
    def printMulti(self):
        """Print the result of multiple plots and clear"""
        self.fig.savefig(self.output + "_multi"+ ".png")
        plt.clf()
    def changeOutput(self, out):
        """Changes the prefix to output to"""
        self.output = out
    def setLimits(self, xl,yl,zl,xh,yh,zh):
        """sets the plotting limits"""
        self.ax.axes.set_xlim3d(left=xl, right=xh) 
        self.ax.axes.set_ylim3d(bottom=yl, top=yh) 
        self.ax.axes.set_zlim3d(bottom=zl, top=zh)
