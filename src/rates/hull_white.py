import numpy as np

""" 
HW is a mean-reversion model with time-dependent drift 

dr_t = [θ(t) - a*r_t]dt + sigma*dW_t

where:
a: mean reversion speed
sigma: volatility
θ(t): calibrated to fit yield curve
"""

class HullWhite:

    def __init__(
            self,
            a: float,
            sigma: float,
            initial_rate: float,
            theta: float
    ):
        
        self.a = a
        self.sigma = sigma
        self.r0 = initial_rate
        self.theta = theta

    
    def simulate_paths(
            self,
            n_paths: int,
            n_steps: int,
            dt: float            
    ):
        
        """ Simulating short-rate paths using HW model parameters """
        rates = np.zeros((n_paths, n_steps))
        rates[:, 0] = self.r0

        for t in range(1, n_steps):
            z = np.random.normal(size = n_paths)
            dr = (
                self.a * (self.theta - rates[:, t-1]) * dt
                + self.sigma * np.sqrt(dt) * z
            )

            rates[:, t] = rates[:, t-1] + dr
        
        return rates