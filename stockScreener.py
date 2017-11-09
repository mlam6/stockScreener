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
      #print ("Starting",  self.name, "Processing", self.symbol)
      getVol(self.symbol)
      #print ("Exiting", self.name, "Processed", self.symbol)
      self.isRunning = False



# Sort and remove whitespace in NASDAQ file
file = open("input/NASDAQ.txt", "r")
text = file.read()
listOfSymbols = text.split("\n")
listOfSymbols.sort()
listOfSymbols = map(lambda x: x.strip(), listOfSymbols)

# Store symbols that passed tests
finalList = Queue.Queue()
garbage = Queue.Queue()

# Split a list 
def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)

    return arrs


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
        #print sym 
    else:
        garbage.put(sym)      


# Threads created to process all the symbols
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

    finalList = list(finalList.queue)
    print ("Final List:")
    for item in finalList:
        print item


# If SMA is > quote
#def getSMA():


# If MACD is > 0
#def getMACD():


# If Stochastic is > 75
#def getSto():


# Return list if symbol passes Vol, SMA, MACD, and Stochastic
#def returnList():


# returnList()

''' TESTING
------------------'''
#getVol()
getVolAll()
#getSMA()
#getMACD()
#getSto()
#split(listOfSymbols, 4)




