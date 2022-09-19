import numpy as np
from valuation_class import ValuationClass



class ValuationEurOptions(ValuationClass):
    """ Class to value European options with arbitrary payoff by single-factor Monte Carlo simulation.
        Methods
        =======
        generate_payoff:
            returns payoffs given the paths and the payoff function
        present_value:
            returns present value (Monte Carlo estimator)
        delta:
            returns the delta of the derivative
        vega:
            returns the vega of the derivative
    """
    def __init__(self):
        super().__init__()



    def delta(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value / 50.
        value_left = self.present_value(fixed_seed=True)
        initial_del = self.underlying.initial_value + interval
        self.underlying.update(initial_value=initial_del)
        value_right = self.present_value(fixed_seed=True)
        self.underlying.update(initial_value=initial_del - interval)
        delta = (value_right - value_left) / interval
        if delta < -1.0:
            return -1.0
        elif delta > 1.0:
            return 1.0
        else:
            return round(delta, accuracy)

    def vega(self, interval=0.01, accuracy=4):
        if interval < self.underlying.volatility / 50.:
            interval = self.underlying.volatility / 50.
        value_left = self.present_value(fixed_seed=True)
        vola_del = self.underlying.volatility + interval
        self.underlying.update(volatility=vola_del)
        value_right = self.present_value(fixed_seed=True)
        self.underlying.update(volatility=vola_del - interval)
        vega = (value_right - value_left) / interval
        return round(vega, accuracy)