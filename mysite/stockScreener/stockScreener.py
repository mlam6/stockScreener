from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances
import time
import thread, threading
import Queue


class Worker(threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.isRunning = False
      self.symbol = None
   def run(self):
      self.isRunning = True
      print ("Starting",  self.name, "Processing", self.symbol)
      getVol(self.symbol)
      print ("Exiting", self.name, "Processed", self.symbol)
      self.isRunning = False


# Sort and remove whitespace in NASDAQ file
file = open("/Users/mlam/Box Sync/fall2017/CSCI 250/StockScreener/mysite/stockScreener/input/NASDAQ.txt", "r")
text = file.read()
file.close()
listOfSymbols = text.split("\n")
listOfSymbols.sort()
listOfSymbols = map(lambda x: x.strip(), listOfSymbols)

# Store symbols that passed tests
finalList = Queue.Queue()


# If volume is > 250,000
def getVol(sym):
    global finalList
    ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
    
    try:
        data, meta_data = ts.get_intraday(symbol = sym)
    except Exception:
        return

    if ((data["volume"].iloc[-1]) > 250000).all():
        finalList.put(sym)

def getVolAll():
    global finalList

    nThreads = 100
    threadPool = [None] * nThreads
    for i in range(nThreads):
        threadPool[i] = Worker(i, i)
    threadIndex = 0

    for symbol in listOfSymbols:
        if threadPool[threadIndex].isRunning:
            threadPool[threadIndex].join()

        threadPool[threadIndex] = Worker(threadIndex, threadIndex)
        threadPool[threadIndex].symbol = symbol
        threadPool[threadIndex].start()
        threadIndex += 1
        if threadIndex == nThreads:
            threadIndex = 0

    for thrd in threadPool:
        thrd.join()

    tempList = list(finalList.queue)
    print ("Vol List:")
    for item in tempList:
        print item

# If SMA is > quote
def getSMA():
    global finalList

    volList = list(finalList.queue)

    for sym in volList:
        ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
        ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
        try:
            data, meta_data = ti.get_sma(sym)
            data2, meta_data2 = ts.get_daily(symbol=sym)
        except Exception:
            return
        
        if len(data) == 0:
            finalList.get(sym)
            print ("Missing SMA Data!", sym)
            continue

        if ((data["SMA"].iloc[-1]) < data2["close"].iloc[-1]).all():
            print ("failed SMA", sym)
            finalList.get(sym)
        else: 
            print("passed SMA", sym)

    tempList = list(finalList.queue)
    print ("SMA List:")
    for item in tempList:
        print item

# If MACD is > 0
def getMACD():
    global finalList
    
    smaList = list(finalList.queue)

    for sym in smaList:
        ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
        try:
            data, meta_data = ti.get_macd(symbol=sym, interval='monthly')
        except Exception:
            return

        if len(data) == 0:
            finalList.get(sym)
            print ("Misssing MACD Data!", sym)
            continue
        
        if ((data["MACD_Hist"].iloc[-1]) < 0).all():
            print("failed MACD", sym, (data["MACD_Hist"].iloc[-1]))
            finalList.get(sym)    
        else: 
            print("passed MACD", sym)

    tempList = list(finalList.queue)
    print ("MACD List:")
    for item in tempList:
        print item


# If Stochastic is > 75
def getSto():
    global finalList

    macdList = list(finalList.queue)
  
    for sym in macdList:
        ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
        try:
             data, meta_data = ti.get_stoch(symbol=sym, interval='monthly')
        except Exception:
            return

        if len(data) == 0:
            print ("Misssing Sto Data!", sym)
            finalList.get(sym)
            continue
        if ((data["SlowK"].iloc[-1]) < 75).all():
            print("failed Sto", sym, (data["SlowK"].iloc[-1]))
            finalList.get(sym)
        else: 
            print("passed Sto", sym)

    finalList = list(finalList.queue)
    print ("Final List:")
    for item in finalList:
        print item


def main():
    getVolAll()
    getSMA()
    getMACD()
    getSto()

    if len(finalList) == 0:
        finalList.append("""We're sorry, we weren't able to find anything that matched your requirements. Please try again. """)
    return finalList

if __name__ == "__main__":
    main()
