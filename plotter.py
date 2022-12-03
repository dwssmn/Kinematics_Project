from matplotlib import pyplot as plt
import numpy as np



import FK
class plotter():
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.output = "default"
    def plotLeg(self, fk:FK.FK,multi=False):
        ee = np.array([[0.0]*3]*(fk.joints+1))
        for i in range(fk.joints+1):
            ee[i] = fk.j_point(i)
        self.ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
        self.setLimits(fk.basepoint[0]-1, fk.basepoint[1]-1, fk.basepoint[2]-3, fk.basepoint[0]+1, fk.basepoint[1]+1, fk.basepoint[2]+1)
        if not multi:
            self.fig.savefig(self.output + "_Leg"+ ".png")
            plt.clf()
    def plotCurve(self, curve,multi=False):
        self.ax.plot([x[0] for x in curve], [x[1] for x in curve],[x[2] for x in curve] )
        self.setLimits(-1,-1,0,1,1,2.5)
        if not multi:
            self.fig.savefig(self.output + "_curve"+ ".png")
            plt.clf()
    def printMulti(self):
        self.fig.savefig(self.output + "_multi"+ ".png")
        plt.clf()
    def changeOutput(self, out):
        self.output = out
    def setLimits(self, xl,yl,zl,xh,yh,zh):
        self.ax.axes.set_xlim3d(left=xl, right=xh) 
        self.ax.axes.set_ylim3d(bottom=yl, top=yh) 
        self.ax.axes.set_zlim3d(bottom=zl, top=zh)
