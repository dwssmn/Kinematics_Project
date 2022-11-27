class leg_model:
    def __init__(self,rotations, r, d, alpha,base,joints):
        self.theta = rotations[0:3]
        self.r = r[0:3]
        self.d = d[0:3]
        self.alpha = alpha[0:3]
        self.base = base
        self.joints = joints
    def get_rotation(self):
        return self.rotations
    