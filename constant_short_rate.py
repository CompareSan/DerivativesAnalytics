from get_year_deltas import *


class ConstantShortRate:
    """ Class for constant short rate discounting.
        Attributes
        ==========
        name: string
            name of the object
        short_rate: float (positive)
            constant rate for discounting
        Methods
        =======
        get_discount_factors:
            get discount factors given a list/array of datetime objects
            or year fractions
    """

    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate

    def get_discount_factors(self, date_list, dtobjects=True):
        if dtobjects:
            date_list = get_year_deltas(date_list)
        else:
            date_list = np.array(date_list)

        dflist = np.exp(self.short_rate * np.sort(-date_list))
        return np.array((date_list, dflist)).T
