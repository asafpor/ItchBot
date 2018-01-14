import urllib.request
import json
import time
import hashlib
import hmac
import inspect
import traceback
from BittrexStats import Logger
from BittrexStats import Statistics
from socket import timeout


class APIWrapper:

    def __init__(self,logger):
        self._logger = logger

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

        def __init__(self, last, volume, bid, ask, openBuyOrders, openSellOrders):
            self._last = last
            self._volume = volume
            self._bid = bid
            self._ask = ask
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
        self._logger.log(Logger.LOG_LEVEL_ERROR, 'query: ' + str(query))
        if query['success'] != True:
            self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
        query_btc = query['result'][0]
        if query_btc['Currency'] != 'BTC':
            self._logger.log(Logger.LOG_LEVEL_ERROR, Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
        return self.BitCoin(query_btc['MinConfirmation'], query_btc['TxFee'], query_btc['IsActive'],
                           query_btc['BaseAddress'])

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
                self._logger.log(Logger.LOG_LEVEL_DEBUG, 'query: ' + str(query))
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
                self._logger.log(Logger.LOG_LEVEL_DEBUG, 'query: ' + str(query))
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

                query = json.loads(
                    urllib.request.urlopen("https://bittrex.com/api/v1.1/public/getmarketsummary?%s" % params).read())
                self._logger.log(Logger.LOG_LEVEL_DEBUG, 'query: ' + str(query))
                if query['success'] != True:
                    self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
                    time.sleep(15)
                    continue

                query_btc = query['result'][0]
                return self.MarketSummary(query_btc['Last'], query_btc['Volume'], query_btc['Bid'], query_btc['Ask'],
                                         query_btc['OpenBuyOrders'], query_btc['OpenSellOrders'])
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: ' + e.reason)
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
                time.sleep(10)
                continue

    # def getOrdersUSDT_BTC(self):
    #     '''
    #         Request:
    #         https://bittrex.com/api/v1.1/public/getorderbook?market=MARKET_BTC_ETH&type=both
    #
    #         Response:
    #             {
    #             "success" : true,
    #             "message" : "",
    #             "result" : {
    #                 "buy" : [{
    #                         "Quantity" : 12.37000000,
    #                         "Rate" : 0.02525000
    #                     }
    #                 ],
    #                 "sell" : [{
    #                         "Quantity" : 32.55412402,
    #                         "Rate" : 0.02540000
    #                     }, {
    #                         "Quantity" : 60.00000000,
    #                         "Rate" : 0.02550000
    #                     }, {
    #                         "Quantity" : 60.00000000,
    #                         "Rate" : 0.02575000
    #                     }, {
    #                         "Quantity" : 84.00000000,
    #                         "Rate" : 0.02600000
    #                     }
    #                 ]
    #             }
    #         }
    #     '''
    #     while True:
    #         try:
    #             query = json.loads(urllib.request.urlopen(
    #                 "https://bittrex.com/api/v1.1/public/getorderbook?market=" + MARKET_BTC_ETH + "&type=both").read())
    #             self._logger.log(Logger.LOG_LEVEL_ERROR, 'query: ' + str(query))
    #             if (query['success'] != True):
    #                 self._logger.log(Logger.LOG_LEVEL_ERROR, "error request did not succeeded")
    #                 time.sleep(0.5)
    #                 continue
    #             if (query['result']['buy'] == None or query['result']['sell'] == None or len(
    #                     query['result']['sell']) == 0 or len(query['result']['buy']) == 0):
    #                 return
    #
    #             buyMin = query['result']['buy'][0]['Rate']
    #             num = 0
    #             avgRateBuy = 0
    #             for rec in query['result']['buy']:
    #                 avgRateBuy = avgRateBuy + int(rec['Rate'])
    #                 buyMax = rec['Rate']
    #                 num = num + 1
    #             avgRateBuy = avgRateBuy / num
    #
    #             sellMin = query['result']['sell'][0]['Rate']
    #             num = 0
    #             avgRateSell = 0
    #             for rec in query['result']['sell']:
    #                 avgRateSell = avgRateSell + int(rec['Rate'])
    #                 sellMax = rec['Rate']
    #                 num = num + 1
    #             avgRateSell = avgRateSell / num
    #
    #             return self.OrdersSummary(buyMin, buyMax, avgRateBuy, sellMin, sellMax, avgRateSell)
    #         except urllib.error.URLError as e:
    #             self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: ' + e.reason)
    #             print('URLError Reason: ', e.reason)
    #             time.sleep(10)
    #             continue
    #         except urllib.error.HTTPError as err:
    #             self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
    #             time.sleep(10)
    #             continue

    def sendEncryptedMsg(self, command, params):
        '''
        encrypted message
        '''

        while True:
            try:
                nonce = time.time()
                url = "https://bittrex.com/api/v1.1/" + command + "?apikey=61beea860ba3409db616ffea34b119ec&nonce=" + str(
                    nonce) + params
                self._logger.log(Logger.LOG_LEVEL_DEBUG, str(url))
                signing = hmac.new(('1cb226bda0e04a51b50bfd776cf0e009').encode(), url.encode(), hashlib.sha512)
                headers1 = {'apisign': signing.hexdigest()}
                req = urllib.request.Request(url, None, headers1)
                msg = ""
                self._logger.log(Logger.LOG_LEVEL_DEBUG, "befoew url open")
                with urllib.request.urlopen(req, timeout=60) as response:
                    self._logger.log(Logger.LOG_LEVEL_DEBUG, "response")
                    the_page = response.read()
                    self._logger.log(Logger.LOG_LEVEL_DEBUG, "json load")
                    msg = json.loads(the_page)

                self._logger.log(Logger.LOG_LEVEL_DEBUG, str(msg))
                return msg
            except urllib.error.URLError as e:
                self._logger.log(Logger.LOG_LEVEL_ERROR, 'Reason: ' + str(e.reason))
                print('URLError Reason: ', e.reason)
                time.sleep(10)
                continue
            except urllib.error.HTTPError as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR, err.code)
                time.sleep(10)
                continue
            except timeout as err:
                self._logger.log(Logger.LOG_LEVEL_ERROR, err.code + "TIMEOUT")
                time.sleep(10)
                continue
