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
        return self.d1()-self.sigma*sqrt(self.t)

    def call(self):
        return self*norm.cdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))-self.k*exp(-self.r*self.t)*norm.cdf(self.d2()(self.St, self.k, self.r, self.t, self.sigma))

    def put(self):
        return self.k*exp(-self.r*self.t)-self.St+self.call()

    # the greeks - from differentiation of bs

    def call_delta(self):
        return norm.cdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))
    def call_gamma(self):
        return norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))/(self.St*self.sigma*sqrt(self.t))
    def call_vega(self):
        return 0.01*(self.St*norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))*sqrt(self.t))
    def call_theta(self):
        return 0.01*(-(self.St*norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))*self.sigma)/(2*sqrt(self.t)) - self.r*self.k*exp(-self.r*self.t)*norm.cdf(self.d2()(self.St, self.k, self.r, self.t, self.sigma)))
    def call_rho(self):
        return 0.01*(self.k*self.t*exp(-self.r*self.t)*norm.cdf(self.d2()(self.St, self.k, self.r, self.t, self.sigma)))


    def put_delta(self):
        return -norm.cdf(-self.d1()(self.St, self.k, self.r, self.t, self.sigma))
    def put_gamma(self):
        return norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))/(self.St*self.sigma*sqrt(self.t))
    def put_vega(self):
        return 0.01*(self.St*norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))*sqrt(self.t))
    def put_theta(self):
        return 0.01*(-(self.St*norm.pdf(self.d1()(self.St, self.k, self.r, self.t, self.sigma))*self.sigma)/(2*sqrt(self.t)) + self.r*self.k*exp(-self.r*self.t)*norm.cdf(-self.d2()(self.St, self.k, self.r, self.t, self.sigma)))
    def put_rho(self):
        return 0.01*(-self.k*self.t*exp(-self.r*self.t)*norm.cdf(-self.d2()(self.St, self.k, self.r, self.t, self.sigma)))
