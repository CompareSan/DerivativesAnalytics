import datetime as dt
import matplotlib.pyplot as plt
from constant_short_rate import ConstantShortRate
from market_environment import MarketEnvironment
from geometric_brownian_motion import GBM

dates = [dt.datetime(2020, 1, 1),
         dt.datetime(2020, 7, 1),
         dt.datetime(2021, 1, 1)]

me_gbm = MarketEnvironment('me_gbm', dt.datetime(2020, 1, 1))
me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2020, 12, 31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'M')
me_gbm.add_constant('paths', 10000)
csr = ConstantShortRate("csr", 0.06)
me_gbm.add_curve('discount_curve', csr)

gbm = GBM('gbm', me_gbm)
gbm.generate_time_grid()

paths_1 = gbm.get_instrument_values()
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()

plt.figure(figsize=(10, 6))
p1 = plt.plot(gbm.time_grid, paths_1[:, :50], 'b')
p2 = plt.plot(gbm.time_grid, paths_2[:, :50], 'r-.')
l1 = plt.legend([p1[0], p2[0]], ['low volatility', 'high volatility'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()
