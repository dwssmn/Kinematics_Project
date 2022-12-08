import numpy as np
from matplotlib import pyplot as plt


from IK import IK
import leg_model





def bezierCurve(times: np.array,points: np.array, degree):
    """Either a three point bezier curve or a 4-point bezier curve"""
    if degree == 3:
        return np.asarray([points[0]*(1-time)**2 + 2*points[1]*time*(1-time)+ points[2]*((time)**2)   for time in times] )
    else:
        return  np.asarray([points[0]*((1-time)**3) + points[1]*3*((1-time)**2)*time + points[2]*3*(1-time)*(time**2) + points[3]*(time**3) for time in times])



def bezierCurveFit(resolution, begin, height, f_dist, s_dist):
    """Generates a bezier curve with the given beginning point and distances"""
    points = np.array([[0.0]*3]*3)
    points[0] = begin
    points[2] = np.array(begin) + np.array([s_dist, f_dist, 0])
    midpoint = np.array([begin[0]+(s_dist/2), begin[1]+(f_dist/2), begin[2]+height]) #[begin[0]+(f_dist/2), begin[1]+height, begin[2]+(s_dist/2)])
    points[1] = 2 * midpoint - points[0]/2 - points[2]/2
    #print(points)
    return bezierCurve(np.linspace(0,1,resolution), points, 3)
