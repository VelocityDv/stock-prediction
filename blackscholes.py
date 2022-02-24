import numpy as np
from math import log, sqrt, pi, exp
from scipy.stats import norm

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

    def d2(self):
        return self.d1-self.sigma*sqrt(self.t)

    def call(self):
        return self*norm.cdf(self.d1(self.St, self.k, self.r, self.t, self.sigma))-self.k*exp(-self.r*self.t)*norm.cdf(self.d2(self.St, self.k, self.r, self.t, self.sigma))

    def put(self):
        pass

    # binary options. either all or nothing