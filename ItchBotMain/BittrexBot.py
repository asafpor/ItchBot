'''
Created on Dec 4, 2017

@author: user
'''
import urllib.request
import json
import time
import hashlib
import hmac
import inspect

MARKET_BTC_ETH = "BTC-ETH"
MARKET_BTC_BCC = "BTC-BCC"
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
        self._logLevel = Logger.LOG_LEVEL_REPORT
        self._strings = dict()
        self._strings[Logger.LOG_LEVEL_DEBUG] = "LOG_LEVEL_DEBUG"
        self._strings[Logger.LOG_LEVEL_INFO] = "LOG_LEVEL_INFO"
        self._strings[Logger.LOG_LEVEL_REPORT] = "LOG_LEVEL_REPORT"
        self._strings[Logger.LOG_LEVEL_ERROR] = "LOG_LEVEL_ERROR"

    def log(self, logLevel, msg):        
        if logLevel >= self._logLevel:
            func = inspect.currentframe().f_back.f_code
            fileLine = ("%s in %s:%i" % (func.co_name,func.co_filename, func.co_firstlineno)) 
            self._logFile.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " " + self._strings[logLevel] + ": " + str(msg) + ",  IN:" + fileLine + "\n")
            self._logFile.flush()
        
        
class Statistics:
    
    def __init__(self):
        
        '''
        init
        '''
        self._marketSummary = dict()
        self._marketSummary[MARKET_BTC_ETH] = []
        self._marketSummary[MARKET_BTC_BCC] = []
        self._ordersSummary = []
        t = time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime())
        self._outFile = open('stats' + t + '.txt', 'w')
        
    def addOrders(self,orders):
        self._ordersSummary.append(orders)
        
    def addMarkets(self, marketName, marketVal):
        self._marketSummary[marketName].append(marketVal)
                
    def __str__(self):
        '''
        
        '''
        
    def dump(self):
        '''
        
        '''
               
        if (len(self._marketSummary) == 100):
            for index in range(0,100):                
                json.dump(self._marketSummary[MARKET_BTC_ETH][index].jsonDump(),self._outFile)
                json.dump(self._marketSummary[MARKET_BTC_BCC][index].jsonDump(),self._outFile)
                json.dump(self._ordersSummary[index].jsonDump(),self._outFile)    
                
            self._marketSummary[MARKET_BTC_ETH] = []
            self._marketSummary[MARKET_BTC_BCC] = []
            self._ordersSummary = []
        
            

class BitCoin:
    '''
    classdocs
    '''
    
    def __init__(self, minConfirmation, txFee, isActive, baseAddress):
        '''
        {'Currency': 'BTC', 
        'CurrencyLong': 'Bitcoin', 
        'MinConfirmation': 2, 
        'TxFee': 0.001, 
        'IsActive': True, 
        'CoinType': 'BITCOIN', 
        'BaseAddress': '1N52wHoVR79PMDishab2XmRHsbekCdGquK', 
        'Notice': None},
        '''
        self._minConfirmation = minConfirmation
        self._txFee = txFee
        self._isActive = isActive
        self._baseAddress = baseAddress
        
    def __str__(self):
        return ("MinConfirmation = " +  str(self._minConfirmation) +
                ", TxFee = " +  str(self._txFee) +
                ", IsActive = " +  str(self._isActive) +
                ", BaseAddress = " +  str(self._baseAddress) )
                

class MarketSummary:
    
    def __init__(self, last, volume, bid, openBuyOrders, openSellOrders):
        self._last = last
        self._volume = volume
        self._bid = bid
        self._openBuyOrders = openBuyOrders
        self._openSellOrders = openSellOrders
        
    def __str__(self):        
        return ("last: " + str(self._last) +         
                " volume: " + str(self._volume) +
                " bid: " + str(self._bid) +
                " openBuyOrders: " + str(self._openBuyOrders) +
                " openSellOrders: " + str(self._openSellOrders))
        
    def jsonDump(self):
        return json.dumps([{'last' : str(self._last),         
                            'volume' : str(self._volume),
                            'bid' : str(self._bid),
                            'openBuyOrders' :  str(self._openBuyOrders),
                            'openSellOrders' : str(self._openSellOrders)}], separators=(',', ':'))
                
        
class OrdersSummary:
    
    def __init__(self, buyMin, buyMax, buyAvg, sellMin, sellMax, sellAvg):
        self._buyMin = buyMin
        self._buyMax = buyMax
        self._buyAvg = buyAvg
        self._sellMin = sellMin
        self._sellMax = sellMax 
        self._sellAvg = sellAvg
        
    def __str__(self):
        return ("buyMin: " + str(self._buyMin) +             
                " buyMax: " + str(self._buyMax) +
                " buyAvg: " + str(self._buyAvg) +
                " sellMin: " + str(self._sellMin) +
                " sellMax: " + str(self._sellMax) +
                " sellAvg: " + str(self._sellAvg))
     
    def jsonDump(self):
        return json.dumps([{'buyMin' : str(self._buyMin),         
                            'buyMax' : str(self._buyMax),
                            'buyAvg' : str(self._buyAvg),
                            'sellMin' :  str(self._sellMin),
                            'sellMax' : str(self._sellMax),
                            'sellAvg' : str(self._sellAvg)}], separators=(',', ':'))
        
        
class BittrexBot:
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self._logger = Logger()
        self._statistics = Statistics()
        
    def getCurrenciesBTC(self):
        '''
        /public/getcurrencies
        Used to get all supported currencies at Bittrex along with other meta data.
        
        Parameters
        None
        
        Request:
        https://bittrex.com/api/v1.1/public/getcurrencies    
        Response
        {
            "success" : true,
            "message" : "",
            "result" : [{
                    "Currency" : "BTC",
                    "CurrencyLong" : "Bitcoin",
                    "MinConfirmation" : 2,
                    "TxFee" : 0.00020000,
                    "IsActive" : true,
                    "CoinType" : "BITCOIN",
                    "BaseAddress" : null
                }, {
                    "Currency" : "LTC",
                    "CurrencyLong" : "Litecoin",
                    "MinConfirmation" : 5,
                    "TxFee" : 0.00200000,
                    "IsActive" : true,
                    "CoinType" : "BITCOIN",
                    "BaseAddress" : null
                }
            ]
        }
        '''
        query = json.loads(urllib.request.urlopen(" https://bittrex.com/api/v1.1/public/getcurrencies").read())
        self._logger.log(Logger.LOG_LEVEL_ERROR, 'query: '+ str(query))
        if query['success'] != True:
            self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
        query_btc = query['result'][0]
        if query_btc['Currency'] != 'BTC':
            self._logger.log(Logger.LOG_LEVEL_ERROR, Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
        return BitCoin(query_btc['MinConfirmation'], query_btc['TxFee'], query_btc['IsActive'], query_btc['BaseAddress'])
     
        
        
    def getmarketSummary(self, market):
        '''
            Request:
            https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ltc    
             
            Response:
               {'success': True, 
               'message': '', 
               'result': [{'MarketName': 'USDT-BTC', 
                           'High': 19850.0, 
                           'Low': 17777.0, 
                           'Volume': 8548.0356726, 
                           'Last': 18822.0, 
                           'BaseVolume': 161165141.00033897, 
                           'TimeStamp': '2017-12-18T07:38:13.363', 
                           'Bid': 18822.0, 'Ask': 18849.99999999, 
                           'OpenBuyOrders': 10485,
                           'OpenSellOrders': 5079, 
                           'PrevDay': 19573.0,
                           'Created': '2015-12-11T06:31:40.633'}]}

        '''
        while True:
            try:
                params = urllib.parse.urlencode({'market': market})
                
                query = json.loads(urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummary?%s"% params).read())
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'query: '+ str(query))
                if query['success'] != True:
                    self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
                    time.sleep(15)
                    continue
                    
                query_btc = query['result'][0]
                return MarketSummary(query_btc['Last'], query_btc['Volume'], query_btc['Bid'], query_btc['OpenBuyOrders'], query_btc['OpenSellOrders'])
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: '+ e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue     

        
        
    def getOrdersUSDT_BTC(self):
        '''
            Request:
            https://bittrex.com/api/v1.1/public/getorderbook?market=MARKET_BTC_ETH&type=both
        
            Response:
                {
                "success" : true,
                "message" : "",
                "result" : {
                    "buy" : [{
                            "Quantity" : 12.37000000,
                            "Rate" : 0.02525000
                        }
                    ],
                    "sell" : [{
                            "Quantity" : 32.55412402,
                            "Rate" : 0.02540000
                        }, {
                            "Quantity" : 60.00000000,
                            "Rate" : 0.02550000
                        }, {
                            "Quantity" : 60.00000000,
                            "Rate" : 0.02575000
                        }, {
                            "Quantity" : 84.00000000,
                            "Rate" : 0.02600000
                        }
                    ]
                }
            }
        '''
        while True:
            try:
                query = json.loads(urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getorderbook?market=" + MARKET_BTC_ETH + "&type=both").read())
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'query: '+ str(query))
                if (query['success'] != True):
                    self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
                    time.sleep(15)
                    continue
                if (query['result']['buy'] == 'None' or query['result']['buy'] == 'None'):
                    return    
                buyMin = query['result']['buy'][0]['Rate']
                num = 0        
                avgRateBuy = 0
                for rec in query['result']['buy']:
                    avgRateBuy = avgRateBuy + int(rec['Rate']) 
                    buyMax = rec['Rate']
                    num = num + 1
                avgRateBuy = avgRateBuy /num
            
                sellMin = query['result']['sell'][0]['Rate']
                num = 0        
                avgRateSell = 0
                for rec in query['result']['sell']:
                    avgRateSell = avgRateSell + int(rec['Rate']) 
                    sellMax = rec['Rate']
                    num = num + 1
                avgRateSell = avgRateSell /num
                
                return OrdersSummary(buyMin, buyMax, avgRateBuy, sellMin, sellMax, avgRateSell)
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: '+ e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue     

        
    def sendEncryptedMsg(self, command, params):
        '''
        encrypted message 
        '''
        while True:
            try:
                nonce = time.time()
                url = "https://bittrex.com/api/v1.1/" + command + "?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(nonce) + params
                self._logger.log(Logger.LOG_LEVEL_REPORT, str(url))
                signing  = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode() , hashlib.sha512)
                headers1 = {'apisign': signing.hexdigest()  }
                req = urllib.request.Request(url, None ,headers1)
                msg = ""
                
                with urllib.request.urlopen(req) as response:
                    the_page = response.read()
                    msg = json.loads(the_page)
                            
                self._logger.log(Logger.LOG_LEVEL_INFO,str(msg))        
                return msg
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: '+ e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue     

    def processCompletedOrders(self,completedOrders):
        
        
        for uuid in completedOrders:
            if self._state._operations[uuid]._type == BittrexBot.Operation.BUY_TYPE:
                # Sell
                self.placeSellOrder(self._state._operations[uuid]._price, self._state._operations[uuid]._quantity, self._state._operations[uuid]._market, self._state._operations[uuid]._factor)
            else:
                assert(self._state._operations[uuid]._type == BittrexBot.Operation.SELL_TYPE)
                market = self._state._operations[uuid]._market
                self._state.getMarket(market)._lastBoughtPrice = self._state._operations[uuid]._price*1.2
                if (self._state.getMarket(market)._lastFactor > 1):
                    self._state.getMarket(market)._lastFactor = self._state._operations[uuid]._factor - 1
                
            self._state._operations.pop(uuid)
        
    def checkOrderStatus(self):
        '''
        
        '''
        
        while(True):
            completedOrders = []
            for uuid in self._state._operations.keys():                
                try:
                    order = self.sendEncryptedMsg("account/getorder", "&uuid=" + uuid)
                    self._logger.log(Logger.LOG_LEVEL_REPORT,"IsOpen = " + str(order['result']['IsOpen']))
                    self._logger.log(Logger.LOG_LEVEL_REPORT,str(order))
                    if order['success'] == True and order['result']['IsOpen'] == False: 
                        self._logger.log(Logger.LOG_LEVEL_REPORT,"DELETE ORDER: " + str(order))                        
                        completedOrders.append(uuid)
                        continue
                except urllib.error.HTTPError as err:
                    self._logger.log(Logger.LOG_LEVEL_ERROR,"Unexpected error" + err.code)
                    exit(0)                
                self._logger.log(Logger.LOG_LEVEL_REPORT,"")
            self.processCompletedOrders(completedOrders)
            return
            
    def verifyOrders(self, market):
        while True:
            order =  '' 
            try:                                          
                order = self.sendEncryptedMsg("market/getopenorders", "&market=" + market)
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue
            self._logger.log(Logger.LOG_LEVEL_REPORT,order)           
            if order['success'] == True:
                for order in order['result']:                                       
                    uuid = order['OrderUuid']
                    if uuid not in self._state._operations:
                        quantity = order['Quantity']
                        price = order['Limit']
                        orderType = BittrexBot.Operation.SELL_TYPE
                        if order['OrderType'] == "LIMIT_BUY":
                            orderType = BittrexBot.Operation.BUY_TYPE                    
                        
                        self._state._operations[uuid] = BittrexBot.Operation(orderType, uuid, price, quantity, market, 1)
                        self._logger.log(Logger.LOG_LEVEL_REPORT,"New order has been found:" + str(order))
                return
            else:
                continue
        
    class Operation:
        
        BUY_TYPE = 0
        SELL_TYPE = 1
        
        def __init__(self, optype, uuid, price, quantity, market, factor):
            self._type = optype
            self._uuid = uuid
            self._price = price
            self._quantity = quantity
            self._market = market
            self._factor= factor
    
    class State:
        
        
        OPERATION_BUY = 0
        OPERATION_SELL = 1
        CHANGE_PERCENT = 0.01
        BUY_QUANTITY_BTC_ETH = 0.4
        BUY_QUANTITY_BTC_BCC = 0.05
        
        class MarketInfo:
            def __init__(self, lastBoughtPrice, lastFactor, buyQunatity):
                self._lastBoughtPrice = lastBoughtPrice
                self._lastFactor = lastFactor
                self._buyQunatity = buyQunatity
        
        def __init__(self):
            
            self._operations = dict()
            self._markets = dict()            
            
            
        def addMarket(self, market, lastBoughtPrice, lastFactor, buyQunatity):
            self._markets[market] = self.MarketInfo(lastBoughtPrice, lastFactor, buyQunatity)


        def getMarket(self, market):
            return self._markets[market]
        
    
    def placeBuyOrder(self, price, quantity, market, lastFactor):
        while True:
            self._state.getMarket(market)._lastBoughtPrice = price
            assert(self._state.getMarket(market)._lastBoughtPrice <= self._lastMarket[market]._last)
            self._logger.log(Logger.LOG_LEVEL_REPORT,"buyPrice: "+ str(self._state.getMarket(market)._lastBoughtPrice))
            order = ''
            quantity = quantity * lastFactor
            try:
                order = self.sendEncryptedMsg("market/buylimit", "&market=" + market + "&quantity=" + str(quantity) +  "&rate=" + str(self._state.getMarket(market)._lastBoughtPrice))
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                exit(0)
            self._logger.log(Logger.LOG_LEVEL_REPORT, order)
            if order['success'] == True:
                uuid = order['result']['uuid']
                self._state._operations[uuid] = BittrexBot.Operation(BittrexBot.Operation.BUY_TYPE, uuid, self._state.getMarket(market)._lastBoughtPrice, quantity, market, lastFactor)                                     
                return
            elif order['success'] == False and order['message'] == 'INSUFFICIENT_FUNDS':
                self._logger.log(Logger.LOG_LEVEL_ERROR,'INSUFFICIENT_FUNDS')
                return
            else:
                continue
    
    def placeSellOrder(self, boughtAtPrice, quantity, market, factor):
        while True:
            sellPrice = boughtAtPrice* (1 + BittrexBot.State.CHANGE_PERCENT) 
            assert(sellPrice >= self._lastMarket[market]._last)                      
            self._logger.log(Logger.LOG_LEVEL_REPORT,"sellPrice: "+  str(sellPrice))
            order =  '' 
            try:                                          
                order = self.sendEncryptedMsg("market/selllimit", "&market=" + market + "&quantity=" + str(quantity) + "&rate=" + str(sellPrice))
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue
            self._logger.log(Logger.LOG_LEVEL_REPORT,order)           
            if order['success'] == True:
                uuid = order['result']['uuid']                
                self._state._operations[uuid] = BittrexBot.Operation(BittrexBot.Operation.SELL_TYPE, uuid, sellPrice, quantity, market, factor)
                return
            else:
                continue

    def run(self):
        
        '''
        
        '''
        self._lastOrder = self.getOrdersUSDT_BTC()
        self._lastMarket = dict()
        self._lastMarket[MARKET_BTC_ETH] = self.getmarketSummary(MARKET_BTC_ETH)
        self._lastMarket[MARKET_BTC_BCC]= self.getmarketSummary(MARKET_BTC_BCC)
        if self._lastOrder != None and self._lastMarket[MARKET_BTC_ETH] != None and self._lastMarket[MARKET_BTC_BCC] != None:
            self._statistics.addOrders(self._lastOrder)
            self._statistics.addMarkets(MARKET_BTC_ETH, self._lastMarket[MARKET_BTC_ETH] )
            self._statistics.addMarkets(MARKET_BTC_BCC, self._lastMarket[MARKET_BTC_BCC] )
            self._statistics.dump()                         
        self._state = BittrexBot.State()
        self._state.addMarket(MARKET_BTC_ETH, 0.050, 1, BittrexBot.State.BUY_QUANTITY_BTC_ETH)
        self._state.addMarket(MARKET_BTC_BCC, 0.250, 1, BittrexBot.State.BUY_QUANTITY_BTC_BCC)
        while (True):
            
            '''
            Strategy:
                Sell if the earn 5%, buy if 4.5% than the last value.
                
            '''
            balance = ''
            try:
                balance = self.sendEncryptedMsg("account/getbalances", "")
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                exit(0)
            
            if (balance['success'] == True):
                self.checkOrderStatus()
                self._logger.log(Logger.LOG_LEVEL_REPORT, balance)
                self._logger.log(Logger.LOG_LEVEL_REPORT,"last price BTC_ETH:" + str(self._lastMarket[MARKET_BTC_ETH]._last))
                self._logger.log(Logger.LOG_LEVEL_REPORT,"last price BTC_BCC:" + str(self._lastMarket[MARKET_BTC_BCC]._last))
                        
                         
                if self._lastMarket[MARKET_BTC_ETH]._last < 0.985 * self._state.getMarket(MARKET_BTC_ETH)._lastBoughtPrice:
                    #Place new buy order                     
                    self.placeBuyOrder(self._lastMarket[MARKET_BTC_ETH]._last, self._state.getMarket(MARKET_BTC_ETH)._buyQunatity, MARKET_BTC_ETH, self._state.getMarket(MARKET_BTC_ETH)._lastFactor)
                    self._state.getMarket(MARKET_BTC_ETH)._lastFactor = self._state.getMarket(MARKET_BTC_ETH)._lastFactor + 1
                    
                if self._lastMarket[MARKET_BTC_BCC]._last < 0.985 * self._state.getMarket(MARKET_BTC_BCC)._lastBoughtPrice:
                    #Place new buy order                     
                    self.placeBuyOrder(self._lastMarket[MARKET_BTC_BCC]._last, self._state.getMarket(MARKET_BTC_BCC)._buyQunatity, MARKET_BTC_BCC, self._state.getMarket(MARKET_BTC_BCC)._lastFactor)
                    self._state.getMarket(MARKET_BTC_BCC)._lastFactor = self._state.getMarket(MARKET_BTC_BCC)._lastFactor + 1
                
                
            self.verifyOrders(MARKET_BTC_ETH)
            self.verifyOrders(MARKET_BTC_BCC)
            time.sleep(10)
            self._logger.log(Logger.LOG_LEVEL_REPORT,"")
            self._lastOrder = self.getOrdersUSDT_BTC()
            self._lastMarket[MARKET_BTC_ETH] = self.getmarketSummary(MARKET_BTC_ETH)
            self._lastMarket[MARKET_BTC_BCC] = self.getmarketSummary(MARKET_BTC_BCC)
            if self._lastOrder != None and self._lastMarket[MARKET_BTC_ETH] != None and self._lastMarket[MARKET_BTC_BCC] != None:
                self._statistics.addOrders(self._lastOrder)
                self._statistics.addMarkets(MARKET_BTC_ETH, self._lastMarket[MARKET_BTC_ETH] )
                self._statistics.addMarkets(MARKET_BTC_BCC, self._lastMarket[MARKET_BTC_BCC] )
                self._statistics.dump()

            
        
        