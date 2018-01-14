
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
            line = inspect.currentframe().f_back.f_lineno
            fileLine = ("%s in %s:%i" % (func.co_name, func.co_filename, line))
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

    class RSI:
        NUMBER_OF_VALS = 14

        def __init__(self, periodInSeconds):
            self._periodInSeconds = periodInSeconds
            self._updatePeriod = periodInSeconds / self.NUMBER_OF_VALS
            self._priceHistory = []
            self.lastUpdateTime = time.time()
            self.nextUpdateSlot = 0
            t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
            self._rsiLogFile = open('rsi' + str(periodInSeconds) + "_" + t + '.txt', 'w')


        def getRSI(self):
            sumOfGains = 0
            sumOfLoss = 0
            if (len(self._priceHistory) != self.NUMBER_OF_VALS):
                return 100 # 100 is the biggest val of RSI and thus no operation will happen with this value
            for index in range(1,self.NUMBER_OF_VALS-1):
                diff = self._priceHistory[index+1] - self._priceHistory[index]
                if diff > 0:
                    sumOfGains += diff
                else:
                    sumOfLoss += diff

            if (sumOfLoss > 0):
                rs = (sumOfGains/14)/(sumOfLoss/14)
                rsi = (100-(100/(1+rs)))
                return rsi
            else:
                return 100

        def updatePrice(self, price):
            if (time.time() - self.lastUpdateTime > self._updatePeriod):
                if len(self._priceHistory) == self.nextUpdateSlot:
                    self._priceHistory.append(price)
                else:
                    self._priceHistory[self.nextUpdateSlot] = price
                self.nextUpdateSlot = ((self.nextUpdateSlot + 1) % self.NUMBER_OF_VALS)
                rsi = self.getRSI()
                self._rsiLogFile.write(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ": " +str(rsi) + "\n")



    class MarketInfo:
        def __init__(self,marketName):
            self._marketName = marketName
            self._hourAndHalfRsi = Statistics.RSI(3600*1.5)
            self._threeHoursRsi = Statistics.RSI(3600*3)
            self._sixHoursRsi = Statistics.RSI(3600*6)
            self._twelveHoursRsi = Statistics.RSI(3600*12)

            self._pointsByCoin = 0
            self._sellBuyStatusByCoin = 0

        def updatePrice(self,price):
            self._hourAndHalfRsi.updatePrice(price)
            self._threeHoursRsi.updatePrice(price)
            self._sixHoursRsi.updatePrice(price)
            self._twelveHoursRsi.updatePrice(price)



    def __init__(self, logger):

        '''
        init
        '''
        self._marketSummary = dict()
        self._logger = logger

        self._ordersSummary = []
        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._outFile = open('stats' + t + '.txt', 'w')

        self._marketInfo = dict()

        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._file = open('tryBuyByVolume' + t + '.txt', 'w')

    def initMarketsSummary(self, markets):
        for market in markets:
            self._marketSummary[market] = []

    def addOrders(self, orders):
        self._ordersSummary.append(orders)

    def addMarkets(self, marketName, marketVal):
        self._marketSummary[marketName].append(marketVal)

    def initMarketsInfo(self, markets):
        for market in markets:
            if ("USDT-" in market["MarketName"]):
                self._marketInfo[market["MarketName"]] = self.MarketInfo(market["MarketName"])


    def isStrongBuy(self, marketName):
        return (self._marketInfo[marketName]._hourAndHalfRsi.getRSI() <= 30 and
                self._marketInfo[marketName]._threeHoursRsi.getRSI() >= 40 and self._marketInfo[marketName]._threeHoursRsi.getRSI() <= 80 and
                self._marketInfo[marketName]._sixHoursRsi.getRSI() >= 40 and self._marketInfo[marketName]._sixHoursRsi.getRSI() <= 80 and
                self._marketInfo[marketName]._twelveHoursRsi.getRSI() >= 40 and self._marketInfo[marketName]._twelveHoursRsi.getRSI() <= 80)


    def addMarketState(self, markets):

        for market in markets:
            marketName = market["MarketName"]
            if (marketName in self._marketInfo):
                self._marketInfo[marketName].updatePrice(market["Last"])


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