from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances
import time
import thread, threading
import Queue
import pickle


class Worker(threading.Thread):
   def __init__(self, threadID, name, func):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.isRunning = False
      self.symbol = None
      self.func = func
   def run(self):
      self.isRunning = True
      #print ("Starting",  self.name, "Processing", self.symbol)
      self.func(self.symbol)
      #print ("Exiting", self.name, "Processed", self.symbol)
      self.isRunning = False

class Generator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            main()
       


# Store symbols that passed tests
finalList = Queue.Queue()

def getAll(func, listOfSymbols):
    global finalList

    nThreads = 100
    threadPool = [None] * nThreads
    for i in range(nThreads):
        threadPool[i] = Worker(i, i, func)
    threadIndex = 0

    for symbol in listOfSymbols:
        if threadPool[threadIndex].isRunning:
            threadPool[threadIndex].join()

        threadPool[threadIndex] = Worker(threadIndex, threadIndex, func)
        threadPool[threadIndex].symbol = symbol
        threadPool[threadIndex].start()
        threadIndex += 1
        if threadIndex == nThreads:
            threadIndex = 0

    for thrd in threadPool:
        if thrd.isRunning:
            thrd.join()

    tempList = list(finalList.queue)
    finalList = Queue.Queue()
    return tempList

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


# If SMA is > quote
def getSMA(sym):
    global finalList

    ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
    ts=TimeSeries(key='GSD3E3P11LSBZG5O', output_format='pandas')
    try:
        data, meta_data = ti.get_sma(sym)
        data2, meta_data2 = ts.get_daily(symbol=sym)
    except Exception:
        return
        
    if len(data) == 0:
        print ("Missing SMA Data!", sym)
        return

    if ((data["SMA"].iloc[-1]) < data2["close"].iloc[-1]).all():
        print ("failed SMA", sym)
    else: 
        finalList.put(sym)
        print("passed SMA", sym)


# If MACD is > 0
def getMACD(sym):
    global finalList
    
    ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
    try:
        data, meta_data = ti.get_macd(symbol=sym, interval='monthly')
    except Exception:
        return

    if len(data) == 0:
        print ("Misssing MACD Data!", sym)
        return        

    if ((data["MACD_Hist"].iloc[-1]) < 0).all():
        print("failed MACD", sym, (data["MACD_Hist"].iloc[-1]))
    else: 
        finalList.put(sym)    
        print("passed MACD", sym)


# If Stochastic is > 75
def getSto(sym):
    global finalList

    ti = TechIndicators(key='GSD3E3P11LSBZG5O', output_format='pandas')
    try:
         data, meta_data = ti.get_stoch(symbol=sym, interval='monthly')
    except Exception:
        return

    if len(data) == 0:
        print ("Misssing Sto Data!", sym)
        return
    if ((data["SlowK"].iloc[-1]) < 75).all():
        print("failed Sto", sym, (data["SlowK"].iloc[-1]))
    else: 
        finalList.put(sym)
        print("passed Sto", sym)

def main():
    # Sort and remove whitespace in NASDAQ file
    file = open("/Users/mlam/Box Sync/fall2017/CSCI 250/StockScreener/mysite/stockScreener/input/NASDAQ.txt", "r")
    text = file.read()
    file.close()
    listOfSymbols = text.split("\n")
    listOfSymbols.sort()
    listOfSymbols = map(lambda x: x.strip(), listOfSymbols)

    listOfSymbols = getAll(getVol, listOfSymbols)
    print ("Vol List:")
    for item in listOfSymbols:
        print item

    listOfSymbols = getAll(getSMA, listOfSymbols)
    print ("SMA List:")
    for item in listOfSymbols:
        print item

    listOfSymbols = getAll(getMACD, listOfSymbols)
    print ("MACD List:")
    for item in listOfSymbols:
        print item

    listOfSymbols = getAll(getSto, listOfSymbols)
    print ("Sto List:")
    for item in listOfSymbols:
        print item

    if len(listOfSymbols) == 0:
        listOfSymbols.append("""We're sorry, we weren't able to find anything that matched your requirements. Please try again. """)

    with open("/Users/mlam/Box Sync/fall2017/CSCI 250/StockScreener/mysite/stockScreener/cache.p", "wb") as f:
        pickle.dump(listOfSymbols, f)

def getResults():
    listOfSymbols = []
    with open("/Users/mlam/Box Sync/fall2017/CSCI 250/StockScreener/mysite/stockScreener/cache.p", "rb") as f:
        listOfSymbols = pickle.load(f)
    return listOfSymbols

generator = Generator()
generator.start()


if __name__ == "__main__":
    main()
