from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

ti = TechIndicators(key='MUH2E79GT7RUTFE6', output_format='pandas')
data, meta_data = ti.get_stoch(symbol='FB', interval='1min')
data.plot()
plt.title('Stochastic for Facebook stock (1min)')
plt.show()