from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
data, meta_data = ts.get_monthly(symbol='FB')
data['close'].plot()
plt.title('Intraday Time Series for the FB4 stock (monthly)')
plt.show()
