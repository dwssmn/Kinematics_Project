import numpy as np
from matplotlib import pyplot as plt


from IK import IK
import leg_model


points = np.array([[0.25, -0.4, 0],[.5,0,.25],[.5,0,.25],[0.25,0,0]])
times = np.arange(0,1,0.01)



def bezierCurve(times: np.array,points: np.array, degree):
    if degree == 3:
        return np.asarray([points[0]*(1-time)**2 + 2*points[1]*time*(1-time)+ points[2]*((time)**2)   for time in times] )
    else:
        return  np.asarray([points[0]*((1-time)**3) + points[1]*3*((1-time)**2)*time + points[2]*3*(1-time)*(time**2) + points[3]*(time**3) for time in times])



def bezierCurveFit(resolution, begin, height, f_dist, s_dist):
    points = np.array([[0.0]*3]*3)
    points[0] = begin
    points[2] = np.array(begin) + np.array([s_dist, f_dist, 0])
    midpoint = np.array([begin[0]+(s_dist/2), begin[1]+(f_dist/2), begin[2]+height]) #[begin[0]+(f_dist/2), begin[1]+height, begin[2]+(s_dist/2)])
    points[1] = 2 * midpoint - points[0]/2 - points[2]/2
    #print(points)
    return bezierCurve(np.linspace(0,1,resolution), points, 3)


"""
begin = np.array([0.25, -0.37, 0])
num = 14
curve = bezierCurveFit(num,begin, 0.3,.75,0) #bezierCurve(times, points)
print(curve)
theta = np.array([np.pi/2,0,0,-np.pi/2,-np.pi/4])
alpha = np.array([0,np.pi/2,0,0,0])
d = np.array([0,0,0.25,0,0])
r = np.array([0,0,0,1,1])
base = np.array([0,0,2])
valid = np.array([True,False,False,True,True])
joints = 5
leg = leg_model.leg_model(theta, r,d,alpha,base,joints)
ik = IK(leg,base,0.04,valid)
ee = np.array([[0.0]*3]*(ik.FKdynamic.joints+1))
print("Bezier curve")
k=num+1
for i in curve:
    target = i
    print("Target" + str(i))
    ik.Inverse_Kinematics(target)

    for j in range(ik.FKdynamic.joints+1):
        ee[j] = ik.FKdynamic.j_point(j)
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot([x[0] for x in ee], [x[1] for x in ee],[x[2] for x in ee] )
    ax.axes.set_xlim3d(left=-1, right=1) 
    ax.axes.set_ylim3d(bottom=-1, top=1) 
    ax.axes.set_zlim3d(bottom=0, top=2.5) 
    name = "ee_"+str(k)
    fig.savefig(name)
    k=k-1


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot([x[0] for x in curve], [x[1] for x in curve],[x[2] for x in curve] )
ax.axes.set_xlim3d(left=-1, right=1) 
ax.axes.set_ylim3d(bottom=-1, top=1) 
ax.axes.set_zlim3d(bottom=0, top=2.5) 
fig.show()

"""