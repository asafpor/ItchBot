'''
Created on Dec 4, 2017

@author: user
'''
import urllib.request
import json
import time
import hashlib
import hmac


class Logger:
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def log(self, msg):
        print (msg)
        
        
class Statistics:
    
    def __init__(self):
        
        '''
        init
        '''
        self._marketSummary = []
        self._ordersSummary = []
        self._outFile = open('stats.txt', 'w')
        
    def addOrders(self,orders):
        #print(str(orders))        
        self._ordersSummary.append(orders)
        
    def addMarkets(self,market):
        #print(str(market))
        self._marketSummary.append(market)
                
    def __str__(self):
        '''
        
        '''
        
    def dump(self):
        '''
        
        '''
               
        if (len(self._marketSummary) == 100):
            for index in range(0,100):                
                json.dump(self._marketSummary[index].jsonDump(),self._outFile)            
                json.dump(self._ordersSummary[index].jsonDump(),self._outFile)    
                
            self._marketSummary = []
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
        #print ("getCurrenciesBTC start")
        query = json.loads(urllib.request.urlopen(" https://bittrex.com/api/v1.1/public/getcurrencies").read())
        if query['success'] != True:
            self._logger.log("error request did not succeeded")
        query_btc = query['result'][0]
        if query_btc['Currency'] != 'BTC':
            self._logger.log("error request did not succeeded")
        #print ("getCurrenciesBTC end")
        return BitCoin(query_btc['MinConfirmation'], query_btc['TxFee'], query_btc['IsActive'], query_btc['BaseAddress'])
     
        
        
    def getmarketSummaryUSDT_BTC(self):
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
        ##print ("getmarketSummaryUSDT_BTC start")
        params = urllib.parse.urlencode({'market': 'USDT-BTC'})
        
        query = json.loads(urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummary?%s"% params).read())
        if query['success'] != True:
            self._logger.log("error request did not succeeded")
            return None
            
        query_btc = query['result'][0]
        ##print (json.dumps(query, indent=4))
        #print ("getmarketSummaryUSDT_BTC end")
        return MarketSummary(query_btc['Last'], query_btc['Volume'], query_btc['Bid'], query_btc['OpenBuyOrders'], query_btc['OpenSellOrders'])
        
        
        
    def getOrdersUSDT_BTC(self):
        '''
            Request:
            https://bittrex.com/api/v1.1/public/getorderbook?market=USDT-BTC&type=both
        
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
        
        #print ("getOrdersUSDT_BTC start")
        query = json.loads(urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getorderbook?market=USDT-BTC&type=both").read())
        #print (json.dumps(query, indent=4))
        #print ("getOrdersUSDT_BTC end")
        
        if (query['success'] != True):
            return None
            
        buyMin = query['result']['buy'][0]['Rate']
        num = 0        
        avgRateBuy = 0
        for rec in query['result']['buy']:
            avgRateBuy = avgRateBuy + int(rec['Rate']) 
            buyMax = rec['Rate']
            num = num + 1
            #print(rec)
        #print ("min " , buyMin)
        #print ("max" , buyMax)
        avgRateBuy = avgRateBuy /num
        ##print ("avg_rate" , avgRateBuy)
        
        
        
    
        sellMin = query['result']['sell'][0]['Rate']
        num = 0        
        avgRateSell = 0
        for rec in query['result']['sell']:
            avgRateSell = avgRateSell + int(rec['Rate']) 
            sellMax = rec['Rate']
            num = num + 1
            ##print(rec)
        #print ("min " , sellMin)
        ##print ("max" , sellMax)
        avgRateSell = avgRateSell /num
        #print ("avg_rate" , avgRateSell)
        
        return OrdersSummary(buyMin, buyMax, avgRateBuy, sellMin, sellMax, avgRateSell)
        
    
    def waitForOrder(self,uuid):
        '''
        
        '''
        
        while(True):
            try:
                nonce = time.time()
                url = "https://bittrex.com/api/v1.1/account/getorder?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(nonce) + "&uuid=" + uuid
                signing  = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode() , hashlib.sha512)
                headers1 = {'apisign': signing.hexdigest()  }
                req = urllib.request.Request(url, None ,headers1)
                order = ''
                with urllib.request.urlopen(req) as response:
                    the_page = response.read()
                    order = json.loads(the_page)
                print (order)
                print ("IsOpen = " + str(order['result']['IsOpen']))
                if order['success'] == True and order['result']['IsOpen'] == False:                
                    return
            except urllib.error.HTTPError as err:
                print(err.code)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            time.sleep(10)
    
    def run(self):
        
        
        '''
        
        '''
        currentPrice = 18700
        state = "SELL"
        sellPrice = currentPrice*1.03
        while (True):
            lastOrder = self.getOrdersUSDT_BTC()
            lastMarket = self.getmarketSummaryUSDT_BTC()
            if lastOrder != None and lastMarket != None:
                self._statistics.addOrders(lastOrder)
                self._statistics.addMarkets(lastMarket)
                self._statistics.dump()
                
                '''
                Strategy:
                    Sell if the earn 5%, buy if 4.5% than the last value.
                    
                '''
        
               
                #
                nonce = time.time()
                url = "https://bittrex.com/api/v1.1/account/getbalances?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(nonce)
                signing  = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode() , hashlib.sha512)
                headers1 = {'apisign': signing.hexdigest()  }
                req = urllib.request.Request(url, None ,headers1)
                balance = ''
                with urllib.request.urlopen(req) as response:
                    the_page = response.read()
                    balance = json.loads(the_page)
                print (balance)
                
                if (balance['success'] == True):
                    print (balance)                    
                    
                    print ("last price:", lastMarket._last)
                    if state == "SELL":
                        assert(sellPrice >= lastMarket._last)                      
                        print("sellPrice: ", sellPrice)
                        nonce = time.time()
                        
                        url = "https://bittrex.com/api/v1.1/market/selllimit?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(nonce) + "&market=USDT-BTC&quantity=0.1&rate=" + str(sellPrice)  
                        signing  = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode() , hashlib.sha512)
                        headers1 = {'apisign': signing.hexdigest()  }
                        req = urllib.request.Request(url, None ,headers1)
                        order = ''
                        with urllib.request.urlopen(req) as response:
                            the_page = response.read()
                            order = json.loads(the_page)
                        print (order)
                        if order['success'] == True:
                            uuid = order['result']['uuid']
                            self.waitForOrder(uuid)  
                            state = "BUY"
                            currentPrice = sellPrice 
                            buyPrice = currentPrice*0.975
                        else:
                            exit()
                            
                             
                    elif state == "BUY":
                        assert(buyPrice <= lastMarket._last)
                        print("buyPrice: ", buyPrice)
                        nonce = time.time()
                        
                        url = "https://bittrex.com/api/v1.1/market/buylimit?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(nonce) + "&market=USDT-BTC&quantity=0.1&rate=" + str(buyPrice)  
                        signing  = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode() , hashlib.sha512)
                        headers1 = {'apisign': signing.hexdigest()  }
                        req = urllib.request.Request(url, None ,headers1)
                        order = ''
                        with urllib.request.urlopen(req) as response:
                            the_page = response.read()
                            order = json.loads(the_page)
                        print (order)
                        if order['success'] == True:
                            uuid = order['result']['uuid']
                            self.waitForOrder(uuid)  
                            state = "SELL"
                            currentPrice = buyPrice 
                            sellPrice = currentPrice*0.96
                        else:
                            exit()
                            
            time.sleep(10)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            
        
        