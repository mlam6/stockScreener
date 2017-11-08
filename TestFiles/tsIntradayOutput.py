from alpha_vantage.timeseries import TimeSeries

ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='FB')

print(data.head())
