import random


class Variance:
    def __init__(self, base: float, variance: float):
        self.base = base
        self.variance = variance

    def get_float(self):
        result = self.base

        if self.variance > 0.0:
            result += random.uniform(-self.variance, +self.variance)

        return result

    def get_int(self):
        result = int(self.base)

        variance = int(self.variance)
        if variance > 0:
            result += random.randrange(-variance, +variance)

        return result


# transform -- inheritable
#
# parent
#


class CanInheritFromParent:
    pass

class CanBeDirty:
    pass
