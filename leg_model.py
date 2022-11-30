class leg_model:
    def __init__(self,rotations, r, d, alpha,base,joints):
        self.theta = rotations[0:joints]
        self.r = r[0:joints]
        self.d = d[0:joints]
        self.alpha = alpha[0:joints]
        self.base = base
        self.joints = joints
    def get_rotation(self):
        return self.rotations
    