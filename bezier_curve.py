import numpy as np
from matplotlib import pyplot as plt

points = np.array([[0, 0, 0],[.5,0,.25],[.5,0,.25],[0,0,0]])
times = np.arange(0,1,0.01)



def bezierCurve(times: np.array,points: np.array, degree):
    if degree == 3:
        print(times)
        return np.asarray([points[0]*(1-time)**2 + 2*points[1]*time*(1-time)+ points[2]*((time)**2)   for time in times] )
    else:
        return  np.asarray([points[0]*((1-time)**3) + points[1]*3*((1-time)**2)*time + points[2]*3*(1-time)*(time**2) + points[3]*(time**3) for time in times])



def bezierCurveFit(resolution, begin, height, f_dist, s_dist):
    points = np.array([[0.0]*3]*3)
    points[0] = begin
    points[2] = np.array(begin) + np.array([f_dist, 0, s_dist])
    midpoint = np.array([begin[0]+(f_dist/2), begin[1]+height, begin[2]+(s_dist/2)])
    print(np.array(begin) + np.array([f_dist, 0, s_dist]))
    print(midpoint)
    print(points)
    points[1] = 2 * midpoint - points[0]/2 - points[2]/2
    return bezierCurve(np.linspace(0,1,resolution), points, 3)




curve = bezierCurveFit(100,points[0], 1,1,0.1) #bezierCurve(times, points)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
print(curve)
ax.plot([x[0] for x in curve], [x[1] for x in curve],[x[2] for x in curve] )
fig.savefig('test.png')