
import time
import inspect
import json

class Logger:
    LOG_LEVEL_DEBUG = 0
    LOG_LEVEL_INFO = 1
    LOG_LEVEL_REPORT = 2
    LOG_LEVEL_ERROR = 3

    def __init__(self):
        '''
        Constructor
        '''
        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._logFile = open('logs' + t + '.txt', 'w')
        self._transFile = open('transactions' + t + '.txt', 'w')
        self._logFileReport = open('logsReport' + t + '.txt', 'w')
        self._logLevel = Logger.LOG_LEVEL_INFO
        self._strings = dict()
        self._strings[Logger.LOG_LEVEL_DEBUG] = "LOG_LEVEL_DEBUG"
        self._strings[Logger.LOG_LEVEL_INFO] = "LOG_LEVEL_INFO"
        self._strings[Logger.LOG_LEVEL_REPORT] = "LOG_LEVEL_REPORT"
        self._strings[Logger.LOG_LEVEL_ERROR] = "LOG_LEVEL_ERROR"

    def trans(self, strType, coin, quantity, price):
        self._transFile.write(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + strType + ": coin= "+ str(coin) + "price=" + str(price) + " quantity=" + str(quantity) + "\n")
        self._transFile.flush()

    def log(self, logLevel, msg):
        if logLevel >= Logger.LOG_LEVEL_INFO:
            func = inspect.currentframe().f_back.f_code
            fileLine = ("%s in %s:%i" % (func.co_name, func.co_filename, func.co_firstlineno))
            self._logFile.write(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + self._strings[logLevel] + ": " + str(
                    msg) + ",  IN:" + fileLine + "\n")
            self._logFile.flush()

        if logLevel >= Logger.LOG_LEVEL_REPORT:
            func = inspect.currentframe().f_back.f_code
            fileLine = ("%s in %s:%i" % (func.co_name, func.co_filename, func.co_firstlineno))
            self._logFileReport.write(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + self._strings[logLevel] + ": " + str(
                    msg) + ",  IN:" + fileLine + "\n")
            self._logFileReport.flush()


class Statistics:

    def __init__(self):

        '''
        init
        '''
        self._marketSummary = dict()

        self._ordersSummary = []
        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._outFile = open('stats' + t + '.txt', 'w')

        self._market = dict()
        self._pointsByCoin = dict()
        self._sellBuyStatusByCoin = dict()
        self._prevIndex = 0
        self._nextIndex = 0
        self._maxIndex = 100
        self._runs = 0
        self._lastTime = time.time()
        self._lastTimeSellBuyPointsUpdate = time.time()
        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._file = open('tryBuyByVolume' + t + '.txt', 'w')

    def initMarketSummary(self, markets):
        for market in markets:
            self._marketSummary[market] = []

    def addOrders(self, orders):
        self._ordersSummary.append(orders)

    def addMarkets(self, marketName, marketVal):
        self._marketSummary[marketName].append(marketVal)

    def initCoinsVolume(self, markets):
        for market in markets:
            if ("BTC-" in market["MarketName"]):
                self._market[market["MarketName"]] = dict()
                self._pointsByCoin[market["MarketName"]] = 0
                self._sellBuyStatusByCoin[market["MarketName"]] = 0

    def isStrongBuy(self, marketName):
        return self._sellBuyStatusByCoin[marketName] > 3
    def addMarketState(self, markets):
        foundMarkets = []
        print(str(time.time()))
        print(str(self._lastTime))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        if (time.time() - self._lastTime > 1200):
            self._lastTime = time.time()
            for market in markets:
                if ("BTC-" in market["MarketName"]):
                    if (market["MarketName"] in self._market):
                        if self._pointsByCoin[market["MarketName"]] > 0:
                            self._pointsByCoin[market["MarketName"]] = self._pointsByCoin[market["MarketName"]] - 1
                        if (self._sellBuyStatusByCoin[market["MarketName"]] < 0):
                            self._sellBuyStatusByCoin[market["MarketName"]] = 0

        for market in markets:
            if ("BTC-XRP" in market["MarketName"]):
                if (market["MarketName"] in self._market):
                    self._logger.log(Logger.LOG_LEVEL_REPORT, 'query: ' + str(query))
                    print(market["MarketName"] + ":" + str(self._sellBuyStatusByCoin[market["MarketName"]]))
        if (time.time() - self._lastTimeSellBuyPointsUpdate > 600):
            self._lastTimeSellBuyPointsUpdate = time.time()

            for market in markets:
                if ("BTC-" in market["MarketName"]):
                    if (market["MarketName"] in self._market):
 #                       print(self._sellBuyStatusByCoin[market["MarketName"]])
                        self._sellBuyStatusByCoin[market["MarketName"]] = self._sellBuyStatusByCoin[market["MarketName"]]/2


        for market in markets:
            if ("BTC-" in market["MarketName"]):

                if (market["MarketName"] in self._market):
                    #print(market["MarketName"] in self._market)
                    #print (market)
                    self._market[market["MarketName"]][self._nextIndex] = market
#                    print(market["MarketName"] + ":" + str(self._market[market["MarketName"]][self._nextIndex]["OpenBuyOrders"]))
 #                   print(market["MarketName"] + ":" + str(
 #                       self._market[market["MarketName"]][self._nextIndex]["OpenSellOrders"]))
                    if (self._market[market["MarketName"]][self._nextIndex]["OpenBuyOrders"] >
                            self._market[market["MarketName"]][self._nextIndex]["OpenSellOrders"]):
                        self._sellBuyStatusByCoin[market["MarketName"]] = self._sellBuyStatusByCoin[market["MarketName"]] + 1
                    else:
                        self._sellBuyStatusByCoin[market["MarketName"]] = self._sellBuyStatusByCoin[market["MarketName"]] - 1
                    if (self._runs > 30 and
                            self._market[market["MarketName"]][self._nextIndex]["Volume"] >
                            self._market[market["MarketName"]][self._prevIndex]["Volume"] and
                            self._market[market["MarketName"]][self._nextIndex]["OpenBuyOrders"] >
                            self._market[market["MarketName"]][self._nextIndex]["OpenSellOrders"]):

                        if (self._market[market["MarketName"]][self._nextIndex]["Last"] >
                            self._market[market["MarketName"]][(self._nextIndex - 10 + self._maxIndex) % self._maxIndex]["Last"] and
                            self._market[market["MarketName"]][self._nextIndex]["Last"] >
                            self._market[market["MarketName"]][(self._nextIndex - 20 + self._maxIndex) % self._maxIndex]["Last"]):

                            print(market["MarketName"] + ": " + str(self._pointsByCoin[market["MarketName"]]))
                            self._pointsByCoin[market["MarketName"]] = self._pointsByCoin[market["MarketName"]] + 1
                            if (self._pointsByCoin[market["MarketName"]] > 5):
                                self._pointsByCoin[market["MarketName"]] = 0
                                foundMarkets.append(market["MarketName"])
                                self._file.write(
                                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + "BUY:" + market[
                                        "MarketName"] + " PRICE: " + str(market["Ask"]) + "\n")
                                self._file.flush()


        self._prevIndex = self._nextIndex
        self._nextIndex = self._nextIndex + 1
        if (self._nextIndex == self._maxIndex):
            self._nextIndex = 0
        self._runs = self._runs + 1

        return foundMarkets

    def __str__(self):
        '''

        '''

    def dump(self, markets):
        '''

        '''

        if (len(self._marketSummary) == 100):
            for index in range(0, 100):
                for market in markets:
                    json.dump(self._marketSummary[market][index].jsonDump(), self._outFile)

                #json.dump(self._ordersSummary[index].jsonDump(), self._outFile)
            for market in markets:
                print(market)
                self._marketSummary[market] = []
            #self._ordersSummary = []
