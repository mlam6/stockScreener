from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

#SMA
def SMA(sym):
    ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
    data, meta_data = ti.get_sma(sym)

    return(data["SMA"].iloc[-1])

#Vol
def Vol(sym):
    ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
    data, meta_data = ts.get_intraday(sym)

    return(data["volume"].iloc[-1])


#MACD
def MACD(sym):
    ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
    data, meta_data = ti.get_macd(symbol=sym, interval='daily')

    return(data["MACD_Hist"].iloc[-1])

#Sto
def Sto(sym):
    ti = TechIndicators(key='MUH2E79GT7RUTFE6', output_format='pandas')
    data, meta_data = ti.get_stoch(symbol=sym, interval='monthly')

    return(data["SlowK"].iloc[-1])
