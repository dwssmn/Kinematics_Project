from leg_model import leg_model
import numpy as np
class IOhelper():
    def outputLeg(leg :leg_model,filepath):
        """Writes to a file specified by filepath the data of the leg"""
        fd = open(filepath, 'w')
        fd.write(str(leg.joints)+"\n")
        for i in leg.theta:
            fd.write(str(i)+" ")
        fd.write("\n")
        for i in leg.alpha:
            fd.write(str(i)+" ")
        fd.write("\n")
        for i in leg.d:
            fd.write(str(i)+" ")
        fd.write("\n")
        for i in leg.r:
            fd.write(str(i)+" ")
        fd.write("\n")
        for i in range(3):
            fd.write(str(leg.base[i])+" ")
        fd.close()
    def inputLeg(filepath):
        """Reads from the filepath and returns the leg"""
        fd = open(filepath, 'r')
        joint = int(fd.readline())
        theta = np.array([0.0]*joint)
        alpha = np.array([0.0]*joint)
        r = np.array([0.0]*joint)
        d = np.array([0.0]*joint)
        base = np.array([0.0]*3)
        line = fd.readline().split(" ")
        for i in range(joint):
            theta[i] = float(line[i])
        line = fd.readline().split(" ")
        for i in range(joint):
            alpha[i] = float(line[i])
        line = fd.readline().split(" ")
        for i in range(joint):
            r[i] = float(line[i])
        line = fd.readline().split(" ")
        for i in range(joint):
            d[i] = float(line[i])
        line = fd.readline().split(" ")
        for i in range(3):
            base[i] = float(line[i])
        fd.close()
        return leg_model(theta,r,d,alpha,base,joint)

    

