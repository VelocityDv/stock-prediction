import numpy as np
from math import log, sqrt, pi, exp

class BlackScholes():
    def __init__(self):
        # call = true / put = false
        self.call = True
        # spot price of asset
        self.St = 0
        # strike price
        self.k = 0 
        # risk free rate
        self.r = 0
        # time to maturity
        self.t = 0
        # volatility of asset
        self.sigma = 0
        
    def d1(self):
        return (log(self.St/self.k)+((self.r+self.sigma**2/2)*self.t)/self.sigma*sqrt(self.t))