import numpy as np
from sn_random_numbers import sn_random_numbers
from simulation_class import SimulationClass


class GBM(SimulationClass):
    """ Class to generate simulated paths based on
    the Black-Scholes-Merton geometric Brownian motion model.
    Attributes
    ==========
    name: string
        name of the object
    mar_env: instance of market_environment
        market environment data for simulation
    corr: Boolean
        True if correlated with other model simulation object
    Methods
    =======
    update:
        updates parameters
    generate_paths:
        returns Monte Carlo paths given the market environment
    get_instrument_values:
         returns the current instrument values (array)
    """

    def __init__(self, name, mar_env, corr=False):
        super().__init__(name, mar_env, corr)

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            # method from generic simulation class
            self.generate_time_grid()
        # number of dates for time grid
        m = len(self.time_grid)
        # number of paths
        i = self.paths
        # ndarray initialization for path simulation
        paths = np.zeros((m, i))
        # initialize first date with initial_value
        paths[0] = self.initial_value
        if not self.correlated:
            # if not correlated, generate random numbers
            rand = sn_random_numbers((1, m, i),
                                     fixed_seed=fixed_seed)
        else:
            # if correlated, use random number object as provided # in market environment
            rand = self.random_numbers
        short_rate = self.discount_curve.short_rate  # get short rate for drift of process
        for t in range(1, len(self.time_grid)):
            # select the right time slice from the relevant # random number set
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]

            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            paths[t] = paths[t - 1] * np.exp((short_rate - 0.5 *
                                              self.volatility ** 2) * dt +
                                             self.volatility * np.sqrt(dt) * ran)
        self.instrument_values = paths

    def get_instrument_values(self, fixed_seed=True):
        if self.instrument_values is None:
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        return self.instrument_values
