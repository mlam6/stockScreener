from alpha_vantage.techindicators import TechIndicators

ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
data, meta_data = ti.get_sma('FB')

print(data.head())
