import math

import scipy.integrate as integrate

from integration_formula.integration import Integration


class Precise(Integration):
    def integrate(self):
        return integrate.quad(self.phi, self.a, self.b, epsabs=math.pow(10, -13), epsrel=math.pow(10, -13))[0]