from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances

# Store NASDAQ file into array and sort list
file = open("input/NASDAQ2.txt", "r")
text = file.read()
listOfSymbols = text.split("\r\n")
listOfSymbols.sort()

# Final list of symbols
finalList = []


# If volume is > 250,000
def getVol():
    for symbol in listOfSymbols:
        ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
        try:
            data, meta_data = ts.get_intraday(symbol)
        except Exception:
            continue
 
        if (data.volume == 250000).all:
            finalList.append(symbol)

    # Testing 
    print finalList


# If SMA is > quote
def getSMA():
    for symbol in finalList:
        ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
        data, meta_data = ti.get_sma(symbol)

        if(data.SMA > data.close):
            finalList.append(symbol)

        # Testing
        print finalList


# If MACD is > 0
#def getMACD():


# If Stochastic is > 75
#def getSto():


# Return list if symbol passes Vol, SMA, MACD, and Stochastic
#def returnList():
   #print finalList 


# returnList()

# TESTING
# ------------------
getVol()
#getSMA()
#getMACD()
#getSto()
