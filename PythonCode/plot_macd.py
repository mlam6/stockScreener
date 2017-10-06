from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
data, meta_data = ti.get_macd(symbol='FB', interval='monthly')
data.plot()
plt.title('Simple Moving Average for FB stock (monthly)')
plt.show()
