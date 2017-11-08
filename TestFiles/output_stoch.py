from alpha_vantage.techindicators import TechIndicators

ti = TechIndicators(key='MUH2E79GT7RUTFE6', output_format='pandas')
data, meta_data = ti.get_stoch(symbol='FB', interval='monthly')

print(data.head())
