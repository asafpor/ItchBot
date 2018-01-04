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
from BittrexStats import Logger
from BittrexStats import Statistics


MARKET_BTC_ETH = "BTC-ETH"
BUY_AMOUNT_BTC_ETH = 0.03
CHANGE_PERCENT_BTC_ETH = 0.02
LAST_BOUGHT_PRICE_BTC_ETH = 0.06355998
BUY_QUANTITY_BTC_ETH = (LAST_BOUGHT_PRICE_BTC_ETH/BUY_AMOUNT_BTC_ETH)


MARKET_BTC_BCC = "BTC-BCC"
BUY_AMOUNT_BTC_BCC = 0.01
CHANGE_PERCENT_BTC_BCC = 0.02
LAST_BOUGHT_PRICE_BTC_BCC = 0.15779998
BUY_QUANTITY_BTC_BCC = (LAST_BOUGHT_PRICE_BTC_BCC/BUY_AMOUNT_BTC_BCC)

MARKET_BTC_XRP = "BTC-XRP"
BUY_AMOUNT_BTC_XRP = 0.04
CHANGE_PERCENT_BTC_XRP = 0.05
LAST_BOUGHT_PRICE_BTC_XRP = 0.00019224
BUY_QUANTITY_BTC_XRP = (LAST_BOUGHT_PRICE_BTC_XRP/BUY_AMOUNT_BTC_XRP)

MARKET_BTC_NEO = "BTC-NEO"
BUY_AMOUNT_BTC_NEO = 0.02
CHANGE_PERCENT_BTC_NEO = 0.02
LAST_BOUGHT_PRICE_BTC_NEO = 0.00721166
BUY_QUANTITY_BTC_NEO = (LAST_BOUGHT_PRICE_BTC_NEO/BUY_AMOUNT_BTC_NEO)

MARKET_BTC_DASH = "BTC-DASH"
BUY_AMOUNT_BTC_DASH = 0.01
CHANGE_PERCENT_BTC_DASH = 0.02
LAST_BOUGHT_PRICE_BTC_DASH = 0.07520800
BUY_QUANTITY_BTC_DASH = (LAST_BOUGHT_PRICE_BTC_DASH/BUY_AMOUNT_BTC_DASH)

MARKET_BTC_ADA = "BTC-ADA"
BUY_AMOUNT_BTC_ADA = 0.01
CHANGE_PERCENT_BTC_ADA = 0.03
LAST_BOUGHT_PRICE_BTC_ADA = 0.00007914
BUY_QUANTITY_BTC_ADA = (LAST_BOUGHT_PRICE_BTC_ADA/BUY_AMOUNT_BTC_ADA)

MARKET_BTC_LTC = "BTC-LTC"
BUY_AMOUNT_BTC_LTC = 0.01
CHANGE_PERCENT_BTC_LTC = 0.02
LAST_BOUGHT_PRICE_BTC_LTC = 0.01550000
BUY_QUANTITY_BTC_LTC = (LAST_BOUGHT_PRICE_BTC_LTC/BUY_AMOUNT_BTC_LTC)

MARKET_BTC_XLM = "BTC-XLM"
BUY_AMOUNT_BTC_XLM = 0.02
CHANGE_PERCENT_BTC_XLM = 0.02
LAST_BOUGHT_PRICE_BTC_XLM = 0.00005217
BUY_QUANTITY_BTC_XLM = (LAST_BOUGHT_PRICE_BTC_XLM/BUY_AMOUNT_BTC_XLM)

MARKET_BTC_XMR = "BTC-XMR"
BUY_AMOUNT_BTC_XMR = 0.02
CHANGE_PERCENT_BTC_XMR = 0.02
LAST_BOUGHT_PRICE_BTC_XMR = 0.02463628
BUY_QUANTITY_BTC_XMR = (LAST_BOUGHT_PRICE_BTC_XMR/BUY_AMOUNT_BTC_XMR)

MARKET_BTC_XEM = "BTC-XEM"
BUY_AMOUNT_BTC_XEM = 0.04
CHANGE_PERCENT_BTC_XEM = 0.02
LAST_BOUGHT_PRICE_BTC_XEM = 0.00011091
BUY_QUANTITY_BTC_XEM = (LAST_BOUGHT_PRICE_BTC_XEM/BUY_AMOUNT_BTC_XEM)


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

    def getmarkets(self):
        '''
            Request:
            https://bittrex.com/api/v1.1/public/getmarkets

            Response:

        	"success" : true,
              "message" : "",
            "result" : [{
                    "MarketCurrency" : "LTC",
                    "BaseCurrency" : "BTC",
                    "MarketCurrencyLong" : "Litecoin",
                    "BaseCurrencyLong" : "Bitcoin",
                    "MinTradeSize" : 0.01000000,
                    "MarketName" : "BTC-LTC",
                    "IsActive" : true,
                    "Created" : "2014-02-13T00:00:00"
                }, {
                    "MarketCurrency" : "DOGE",
                    "BaseCurrency" : "BTC",

        '''
        while True:
            try:
                query = json.loads(
                    urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getmarkets").read())
                self._logger.log(Logger.LOG_LEVEL_INFO, 'query: ' + str(query))
                if query['success'] != True:
                    self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
                    time.sleep(15)
                    continue
                markets = []
                for market in query['result']:
                    markets.append(market)
                return markets
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: ' + e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
                time.sleep(10)
                continue

    def getmarketSummeries(self):
        '''
            Request:
            https://bittrex.com/api/v1.1/public/getmarketsummaries

            Response:

        	"success" : true,
              "message" : "",
            "result" : [{
                    "MarketName" : "BTC-888",
                    "High" : 0.00000919,
                    "Low" : 0.00000820,
                    "Volume" : 74339.61396015,
                    "Last" : 0.00000820,
                    "BaseVolume" : 0.64966963,
                    "TimeStamp" : "2014-07-09T07:19:30.15",
                    "Bid" : 0.00000820,
                    "Ask" : 0.00000831,
                    "OpenBuyOrders" : 15,
                    "OpenSellOrders" : 15,
                    "PrevDay" : 0.00000821,
                    "Created" : "2014-03-20T06:00:00",
                    "DisplayMarketName" : null
                }, {
                    "MarketCurrency" : "DOGE",
                    "BaseCurrency" : "BTC",

        '''
        while True:
            try:
                query = json.loads(
                    urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummaries").read())
                self._logger.log(Logger.LOG_LEVEL_INFO, 'query: ' + str(query))
                if query['success'] != True:
                    self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
                    time.sleep(15)
                    continue
                markets = []
                for market in query['result']:
                    markets.append(market)
                return markets
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: ' + e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
                time.sleep(10)
                continue


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
                self._logger.log(Logger.LOG_LEVEL_INFO, 'query: '+ str(query))
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
                    time.sleep(0.5)
                    continue
                if (query['result']['buy'] == None or query['result']['sell'] == None or len(query['result']['sell']) == 0 or len(query['result']['buy']) == 0):
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
                self._logger.log(Logger.LOG_LEVEL_INFO,str(url))
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
            market = self._state._operations[uuid]._market
            if self._state._operations[uuid]._type == BittrexBot.Operation.BUY_TYPE:
                # Sell
                self.placeSellOrder(self._state._operations[uuid]._price, self._state._operations[uuid]._quantity, self._state._operations[uuid]._market, self._state._operations[uuid]._factor)
            else:
                assert(self._state._operations[uuid]._type == BittrexBot.Operation.SELL_TYPE)
                if (self._state._operations[uuid]._factor > 1):
                    self._state.getMarket(market)._lastFactor = self._state._operations[uuid]._factor - 0.5
                else:
                    self._state.getMarket(market)._lastFactor = 1
                price = self._state._operations[uuid]._price*0.99
                if price > self._lastMarket[market]._last:
                    price = self._lastMarket[market]._last*0.99
                self.placeBuyOrder(price, self._state.getMarket(market)._buyQunatity, market, self._state.getMarket(market)._numberOfOperations - 1)

            self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations - 1

            self._state._operations.pop(uuid)
        
    def checkOrderStatus(self):
        '''
        
        '''
        
        while(True):
            completedOrders = []
            for uuid in self._state._operations.keys():                
                try:
                    order = self.sendEncryptedMsg("account/getorder", "&uuid=" + uuid)                    
                    self._logger.log(Logger.LOG_LEVEL_INFO,str(order))
                    if order['success'] == True and order['result']['IsOpen'] == False and order['result']['CancelInitiated'] == False: #TODO memory leak, should delete order in case it was canceled 
                        self._logger.log(Logger.LOG_LEVEL_INFO,"DELETE ORDER: " + str(order))                        
                        completedOrders.append(uuid)
                        continue
                except urllib.error.HTTPError as err:
                    self._logger.log(Logger.LOG_LEVEL_ERROR,"Unexpected error" + err.code)
                    exit(0)                
                self._logger.log(Logger.LOG_LEVEL_INFO,"")
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
            self._logger.log(Logger.LOG_LEVEL_INFO,order)           
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
                        self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1
                        self._logger.log(Logger.LOG_LEVEL_INFO,"New order has been found:" + str(order))
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

        

        class MarketInfo:
            def __init__(self, lastBoughtPrice, lastFactor, buyQunatity,changePercent):
                self._lastBoughtPrice = lastBoughtPrice
                self._lastFactor = lastFactor
                self._buyQunatity = buyQunatity
                self._numberOfOperations = 0
                self._changePercent = changePercent
        
        def __init__(self):
            
            self._operations = dict()
            self._markets = dict()            
            
            
        def addMarket(self, market, lastBoughtPrice, lastFactor, buyQunatity,changePercent):
            self._markets[market] = self.MarketInfo(lastBoughtPrice, lastFactor, buyQunatity,changePercent)

        def removeMarket(self, market, lastBoughtPrice, lastFactor, buyQunatity,changePercent):
            del self._markets[market]


        def getMarket(self, market):
            return self._markets[market]
        
    
    def placeBuyOrder(self, price, quantity, market, lastFactor):

        while True:
            prevLastBoughtPrice = self._state.getMarket(market)._lastBoughtPrice
            self._state.getMarket(market)._lastBoughtPrice = price
            self._logger.log(Logger.LOG_LEVEL_REPORT,"BUY:" + market + "buyPrice: "+ str(self._state.getMarket(market)._lastBoughtPrice))
            assert (self._state.getMarket(market)._lastBoughtPrice <= self._lastMarket[market]._last)
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
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1                                     
                return True
            elif order['success'] == False and order['message'] == 'INSUFFICIENT_FUNDS':
                self._state.getMarket(market)._lastBoughtPrice = prevLastBoughtPrice
                self._logger.log(Logger.LOG_LEVEL_ERROR,'INSUFFICIENT_FUNDS')
                return False
            else:
                continue
    
    def placeSellOrder(self, boughtAtPrice, quantity, market, factor):

        while True:
            sellPrice = boughtAtPrice* (1 + self._state.getMarket(market)._changePercent + (factor - 1) / 300)
            self._logger.log(Logger.LOG_LEVEL_REPORT,"SELL:" + market + "sellPrice: "+  str(sellPrice) + " lastPrice = " + str(self._lastMarket[market]._last) + "boughtAtPrice = " + str(boughtAtPrice) + " quantity = " + str(quantity) + " factor = " + str(factor))
            if (sellPrice < self._lastMarket[market]._last):                
                sellPrice = (self._lastMarket[market]._last)*(1 + self._state.getMarket(market)._changePercent)
                self._logger.log(Logger.LOG_LEVEL_REPORT,"SELL: PRICE MODIFED" + market + "sellPrice: "+  str(sellPrice))
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
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1
                return
            else:
                continue

    def run(self):
        
        '''
        
        '''
        self._statistics.initCoinsVolume( self.getmarketSummeries())

        self._markets = []        
        self._markets.append(MARKET_BTC_XRP)
        self._markets.append(MARKET_BTC_ETH)

        self._markets.append(MARKET_BTC_ADA)
        self._markets.append(MARKET_BTC_NEO)
        self._markets.append(MARKET_BTC_DASH)        
        self._markets.append(MARKET_BTC_BCC)
        self._markets.append(MARKET_BTC_XLM)
        self._markets.append(MARKET_BTC_LTC)
        self._markets.append(MARKET_BTC_XMR)
        self._markets.append(MARKET_BTC_XEM)

        self._statistics.initMarketSummary(self._markets)
        self._lastOrder = self.getOrdersUSDT_BTC()
        self._lastMarket = dict()
        for marketName in self._markets:
        
            self._lastMarket[marketName] = self.getmarketSummary(marketName)
            if self._lastOrder != None and self._lastMarket[marketName] != None :
                self._statistics.addOrders(self._lastOrder)
                self._statistics.addMarkets(marketName, self._lastMarket[marketName] )

        self._state = BittrexBot.State()
        self._state.addMarket(MARKET_BTC_ETH, LAST_BOUGHT_PRICE_BTC_ETH, 1,BUY_QUANTITY_BTC_ETH, CHANGE_PERCENT_BTC_ETH)
        self._state.addMarket(MARKET_BTC_BCC, LAST_BOUGHT_PRICE_BTC_BCC, 1,BUY_QUANTITY_BTC_BCC, CHANGE_PERCENT_BTC_BCC)
        self._state.addMarket(MARKET_BTC_XRP, LAST_BOUGHT_PRICE_BTC_XRP, 1,BUY_QUANTITY_BTC_XRP, CHANGE_PERCENT_BTC_XRP)
        self._state.addMarket(MARKET_BTC_NEO,LAST_BOUGHT_PRICE_BTC_NEO, 1, BUY_QUANTITY_BTC_NEO, CHANGE_PERCENT_BTC_NEO)
        self._state.addMarket(MARKET_BTC_DASH,LAST_BOUGHT_PRICE_BTC_DASH, 1,BUY_QUANTITY_BTC_DASH, CHANGE_PERCENT_BTC_DASH)
        self._state.addMarket(MARKET_BTC_ADA,LAST_BOUGHT_PRICE_BTC_ADA, 1, BUY_QUANTITY_BTC_ADA, CHANGE_PERCENT_BTC_ADA)
        self._state.addMarket(MARKET_BTC_LTC,LAST_BOUGHT_PRICE_BTC_LTC, 1, BUY_QUANTITY_BTC_LTC, CHANGE_PERCENT_BTC_LTC)
        self._state.addMarket(MARKET_BTC_XLM, LAST_BOUGHT_PRICE_BTC_XLM, 1, BUY_QUANTITY_BTC_XLM, CHANGE_PERCENT_BTC_XLM)
        self._state.addMarket(MARKET_BTC_XMR, LAST_BOUGHT_PRICE_BTC_XMR, 1, BUY_QUANTITY_BTC_XMR, CHANGE_PERCENT_BTC_XMR)
        self._state.addMarket(MARKET_BTC_XEM, LAST_BOUGHT_PRICE_BTC_XEM, 1, BUY_QUANTITY_BTC_XEM, CHANGE_PERCENT_BTC_XEM)

        self._statistics.dump(self._markets)
        while (True):
            
            '''
            Strategy:
                Sell if the earn 5%, buy if 4.5% than the last value.
                
            '''

            self._statistics.addMarketState(self.getmarketSummeries())

            for marketName in self._markets:

                self.verifyOrders(marketName)
                self._logger.log(Logger.LOG_LEVEL_INFO,"")
                self._lastOrder = self.getOrdersUSDT_BTC()
                self._lastMarket[marketName] = self.getmarketSummary(marketName)
                if self._lastOrder != None and self._lastMarket[marketName] != None:
                    self._statistics.addOrders(self._lastOrder)
                    self._statistics.addMarkets(marketName, self._lastMarket[marketName] )

                balance = ''
                try:
                    balance = self.sendEncryptedMsg("account/getbalance", "&currency=BTC")
                except urllib.error.HTTPError as err:
                    self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                    time.sleep(10)
                    exit(0)

                if (balance['success'] == True):
                    assert(balance["result"]["Currency"] == "BTC")
                    self.checkOrderStatus()
                    self._logger.log(Logger.LOG_LEVEL_INFO, balance)
                    self._logger.log(Logger.LOG_LEVEL_INFO,"last price" + marketName + ":" + str(self._lastMarket[marketName]._last))

                    if (self._lastMarket[marketName]._last < 0.95 * self._state.getMarket(marketName)._lastBoughtPrice and self._state.getMarket(marketName)._numberOfOperations < 3):
                        if ((self.placeBuyOrder(self._lastMarket[marketName]._last, self._state.getMarket(marketName)._buyQunatity, marketName, self._state.getMarket(marketName)._lastFactor)) == True):
                            self._state.getMarket(marketName)._lastFactor = self._state.getMarket(marketName)._lastFactor + 0.5

                    if (self._state.getMarket(marketName)._numberOfOperations < 1):
                        self.placeBuyOrder(self._lastMarket[marketName]._last*0.995, self._state.getMarket(marketName)._buyQunatity, marketName, self._state.getMarket(marketName)._lastFactor)

                self._statistics.dump(self._markets)


            time.sleep(10)

           

            
        
        