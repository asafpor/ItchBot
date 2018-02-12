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
import traceback
from BittrexStats import Logger
from BittrexStats import Statistics
from BittrexAPIWrapper import APIWrapper
from socket import timeout


BUY_AMOUNT_USDT = 50
CHANGE_PERCENT = 0.05
CHANGE_PERCENT_MEDIUM = 0.04

#If the buy order did not occur in the last 10 minutes, cancel
CANCEL_PERIOD = 1800



class BittrexBot:
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self._logger = Logger()
        self._statistics = Statistics(self._logger )
        self._apiWrapper = APIWrapper(self._logger)
        
    '''
        For each completed order if it was a buy order sell in price + change percent
    '''
    def processCompletedOrders(self,completedOrders):

        for uuid in completedOrders:
            market = self._state._operations[uuid]._market
            if (market in self._state._markets):
                if self._state._operations[uuid]._type == BittrexBot.Operation.BUY_TYPE:
                    self.placeSellOrder(self._state._operations[uuid]._price, self._state._operations[uuid]._quantity, self._state._operations[uuid]._market, self._state._operations[uuid]._changePercent)
                else:
                    assert(self._state._operations[uuid]._type == BittrexBot.Operation.SELL_TYPE)
                self._state._operations.pop(uuid)
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations - 1
        
    def checkOrderStatus(self):
        '''
        
        '''
        
        while(True):
            completedOrders = []
            toDelete = []
            for uuid in self._state._operations.keys():                
                try:
                    order = self._apiWrapper.sendEncryptedMsg("account/getorder", "&uuid=" + uuid)
                    self._logger.log(Logger.LOG_LEVEL_INFO,str(order))
                    if order['success'] == True and order['result']['IsOpen'] == False:
                        if (order['result']['CancelInitiated'] == True):
                            self._logger.log(Logger.LOG_LEVEL_REPORT, "CANCEL ORDER: " + str(order))
                            market = self._state._operations[uuid]._market
                            toDelete.append(uuid)
                        else:
                            self._logger.log(Logger.LOG_LEVEL_INFO,"DELETE ORDER: " + str(order))
                            completedOrders.append(uuid)
                        continue
                except urllib.error.HTTPError as err:
                    self._logger.log(Logger.LOG_LEVEL_ERROR,"Unexpected error" + err.code)
                    exit(0)                
                self._logger.log(Logger.LOG_LEVEL_INFO,"")
            self.processCompletedOrders(completedOrders)
            for uuid in toDelete:
                market = self._state._operations[uuid]._market
                self._state._operations.pop(uuid)
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations - 1
            return
            
    def verifyOrders(self, market):
        while True:
            order =  '' 
            try:                                          
                order = self._apiWrapper.sendEncryptedMsg("market/getopenorders", "&market=" + market)
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
                        
                        self._state._operations[uuid] = BittrexBot.Operation(orderType, uuid, price, quantity, market, CHANGE_PERCENT)
                        self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1
                        self._logger.log(Logger.LOG_LEVEL_REPORT,"New order has been found:" + str(order))
                    else:
                        if (self._state._operations[uuid].cancelOnTimeout()):
                            self._logger.log(Logger.LOG_LEVEL_REPORT, "Cancel order:" + str(order))
                            self._logger.trans("CANCEL", market, 0, 0)
                            msg = self._apiWrapper.sendEncryptedMsg("market/cancel","&uuid=" + str(uuid))
                            if msg['success'] != True:
                                self._logger.log(Logger.LOG_LEVEL_REPORT, "Cancel failed:" + str(order))
                return
            else:
                continue
        
    class Operation:
        
        BUY_TYPE = 0
        SELL_TYPE = 1
        
        def __init__(self, optype, uuid, price, quantity, market, changePercent):
            self._type = optype
            self._uuid = uuid
            self._price = price
            self._quantity = quantity
            self._market = market
            self._changePercent = changePercent
            self._issuedTime = time.time()

        def cancelOnTimeout(self):
            return (self._type == self.BUY_TYPE and (time.time() - self._issuedTime > CANCEL_PERIOD))
    
    class State:
        
        
        OPERATION_BUY = 0
        OPERATION_SELL = 1

        

        class MarketInfo:

            MARKET_TYPE_LONG_TERM = 0
            MARKET_TYPE_PUMP_AND_DUMP = 1
            MARKET_TYPE_RSI = 1

            def __init__(self, buyQunatity,changePercent, type):
                self._buyQunatity = buyQunatity
                self._numberOfOperations = 0
                self._lastOpTime = time.time()
                self._changePercent = changePercent
                self._type= type
        
        def __init__(self):
            
            self._operations = dict()
            self._markets = dict()
            self._numberOfRiskyOperations = 0
            
            
        def addMarket(self, market, buyQunatity ,changePercent,  type):
            if (market not in self._markets):
                self._markets[market] = self.MarketInfo( buyQunatity,changePercent, type)

        def removeMarket(self, market):
            del self._markets[market]


        def getMarket(self, market):
            return self._markets[market]
        
    
    def placeBuyOrder(self, price, quantity, market, changePercent):

        while True:

            self._logger.log(Logger.LOG_LEVEL_REPORT,"BUY:" + market + "buyPrice: "+ str(price))
            #assert (self._state.getMarket(market)._lastBoughtPrice <= self._lastMarket[market]._last)
            order = ''
            try:
                order = self._apiWrapper.sendEncryptedMsg("market/buylimit", "&market=" + market + "&quantity=" + str(quantity) +  "&rate=" + str(price))
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                exit(0)
            self._logger.log(Logger.LOG_LEVEL_REPORT, order)
            if order['success'] == True:
                uuid = order['result']['uuid']
                self._state.getMarket(market)._lastOpTime = time.time()
                self._state._operations[uuid] = BittrexBot.Operation(BittrexBot.Operation.BUY_TYPE, uuid, price, quantity, market, changePercent)
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1
                self._logger.trans("BUY", market, quantity, price)
                return True
            elif order['success'] == False and order['message'] == 'INSUFFICIENT_FUNDS':
                self._logger.log(Logger.LOG_LEVEL_ERROR,'INSUFFICIENT_FUNDS')
                return False
            else:
                continue
    
    def placeSellOrder(self, boughtAtPrice, quantity, market, changePercent):

        while True:
            sellPrice = boughtAtPrice* (1 + changePercent)
            self._logger.log(Logger.LOG_LEVEL_REPORT,"SELL:" + market + "sellPrice: " + str(sellPrice) + " lastPrice = " + str(self._marketSummary[market]._last) + "boughtAtPrice = " + str(boughtAtPrice) + " quantity = " + str(quantity))
            if (sellPrice < self._marketSummary[market]._last):
                sellPrice = (self._marketSummary[market]._last) * (1 + changePercent)
                self._logger.log(Logger.LOG_LEVEL_REPORT,"SELL: PRICE MODIFED" + market + "sellPrice: "+  str(sellPrice))
            order =  '' 
            try:                                          
                order = self._apiWrapper.sendEncryptedMsg("market/selllimit", "&market=" + market + "&quantity=" + str(quantity) + "&rate=" + str(sellPrice))
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR,err.code)
                time.sleep(10)
                continue
            self._logger.log(Logger.LOG_LEVEL_REPORT,order)           
            if order['success'] == True:
                uuid = order['result']['uuid']                
                self._state._operations[uuid] = BittrexBot.Operation(BittrexBot.Operation.SELL_TYPE, uuid, sellPrice, quantity, market, CHANGE_PERCENT)
                self._state.getMarket(market)._numberOfOperations = self._state.getMarket(market)._numberOfOperations + 1
                self._state.getMarket(market)._lastOpTime = time.time()
                self._logger.trans("SELL", market, quantity, sellPrice)
                return
            else:
                continue

    def run(self):
        
        '''
        
        '''
        self._statistics.initMarketsInfo( self._apiWrapper.getmarketSummeries())

        self._markets = []
        self._state = BittrexBot.State()
        for market in self._apiWrapper.getmarketSummeries():
            marketName = market["MarketName"]
            if ("USDT-" in market["MarketName"] and "NXT" not in market["MarketName"]):
                self._markets.append(marketName)
                self._state.addMarket(marketName,
                                      (BUY_AMOUNT_USDT / market["Last"]),
                                      CHANGE_PERCENT,
                                      BittrexBot.State.MarketInfo.MARKET_TYPE_RSI)
        self._statistics.initMarketsSummary(self._markets)
        self._marketSummary = dict()
        for marketName in self._markets:

            self._marketSummary[marketName] = self._apiWrapper.getmarketSummary(marketName)
            if self._marketSummary[marketName] != None :
                self._statistics.addMarkets(marketName, self._marketSummary[marketName])


        self._statistics.dump(self._markets)
        lastUpdate = time.time()
        while (True):
            try:

                balance = ''
                try:
                    balance = self._apiWrapper.sendEncryptedMsg("account/getbalance", "&currency=USDT")
                except urllib.error.HTTPError as err:
                    self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
                    time.sleep(10)
                    continue

                if (balance['success'] == True and balance['result']['Balance'] != None):
                    assert (balance["result"]["Currency"] == "USDT")
                    self.checkOrderStatus()
                    self._logger.log(Logger.LOG_LEVEL_INFO, balance)
                    self._statistics.addMarketState(self._apiWrapper.getmarketSummeries())

                    for marketName in self._markets:
                        if ( self._state.getMarket(marketName)._type != BittrexBot.State.MarketInfo.MARKET_TYPE_RSI):
                            continue


                        self.verifyOrders(marketName)
                        self._logger.log(Logger.LOG_LEVEL_INFO,"")
                        #self._lastOrder = self.getOrdersUSDT_BTC()
                        self._marketSummary[marketName] = self._apiWrapper.getmarketSummary(marketName)
                        if self._marketSummary[marketName] != None:
                            self._statistics.addMarkets(marketName, self._marketSummary[marketName])

                        self._logger.log(Logger.LOG_LEVEL_INFO,"last price" + marketName + ":" + str(self._marketSummary[marketName]._last))

                        if (balance['result']['Balance'] > 50 and self._statistics.isUltBuy(
                                marketName) and self._state.getMarket(marketName)._numberOfOperations < 3 and
                                (time.time() - self._state.getMarket(marketName)._lastOpTime > 3600)):
                            print("BUY-U:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                   time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))
                            self.placeBuyOrder(self._marketSummary[marketName]._last,
                                               self._state.getMarket(marketName)._buyQunatity, marketName,
                                               (CHANGE_PERCENT*2))
                        elif (self._statistics.isUltBuy(marketName)):
                            print("did not BUY-U:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                           time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))

                        if (balance['result']['Balance'] > 50 and self._statistics.isSStrongBuy(
                                marketName) and self._state.getMarket(marketName)._numberOfOperations < 3 and
                                (time.time() - self._state.getMarket(marketName)._lastOpTime > 3600)):
                            print("BUY-SS:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                   time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))
                            self.placeBuyOrder(self._marketSummary[marketName]._last,
                                               self._state.getMarket(marketName)._buyQunatity, marketName,
                                               (CHANGE_PERCENT + 0.02))
                        elif (self._statistics.isSStrongBuy(marketName)):
                            print("did not BUY-SS:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                           time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))

                        if (balance['result']['Balance'] > 60 and self._statistics.isStrongBuy(marketName) and self._state.getMarket(marketName)._numberOfOperations < 3 and
                            (time.time() - self._state.getMarket(marketName)._lastOpTime  > 3600)):
                            print("BUY-S:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                         time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))
                            self.placeBuyOrder(self._marketSummary[marketName]._last, self._state.getMarket(marketName)._buyQunatity, marketName, CHANGE_PERCENT)
                        elif (self._statistics.isStrongBuy(marketName)):
                            print("did not BUY-S:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(self._state.getMarket(marketName)._numberOfOperations) +" balance=" +
                                  str(balance['result']['Balance']))

                        if (balance['result']['Balance'] > 200 and self._statistics.isMediumBuy(marketName) and self._state.getMarket(marketName)._numberOfOperations < 2 and
                                (time.time() - self._state.getMarket(marketName)._lastOpTime  > 3600)):
                            print("BUY-<:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                         time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(
                                self._state.getMarket(marketName)._numberOfOperations) + " balance=" +
                                  str(balance['result']['Balance']))
                            self.placeBuyOrder(self._marketSummary[marketName]._last, self._state.getMarket(marketName)._buyQunatity, marketName, CHANGE_PERCENT_MEDIUM)
                        elif (self._statistics.isMediumBuy(marketName)):
                            print("did not BUY-M:" + str(marketName) + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " price = " + str(
                                self._marketSummary[marketName]._last) + " numberOfOperations=" + str(self._state.getMarket(marketName)._numberOfOperations) +" balance=" +
                                  str(balance['result']['Balance']))


                        self._statistics.dump(self._markets)


                time.sleep(10)
                if (time.time() - lastUpdate > 600):
                    print (time.strftime('%Y_%m-%d_%H_%M_%S', time.localtime()))
                    lastUpdate = time.time()
            except Exception as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR,traceback.format_exc())

                self._logger.log(Logger.LOG_LEVEL_ERROR, e.__doc__)
                print (str(e))
                time.sleep(10)
                continue
           

            
        
        