'''
Created on Nov 30, 2017

@author: user
'''
import urllib.request
import json
from Coins import *
      
        
class CoinMarketUpWrapper:
 
    def __init__(self):
        print("CoinMarketUpWrapper init") 
        
    
    
    def QueryBitCoin(self):
        """Query bitcoin status.

            Arguments:
            {'id': 'bitcoin', 
            'name': 'Bitcoin', 
            'symbol': 'BTC', 
            'rank': '1', ?????
            'price_usd': '11025.9', 
            'price_btc': '1.0', 
            '24h_volume_usd': '6883870000.0', 
            'market_cap_usd': '184293089156', 
            'available_supply': '16714562.0', ??? 
            'total_supply': '16714562.0', ???? // current mined
            'max_supply': '21000000.0', max amount of bitcoins
            'percent_change_1h': '-0.59', 
            'percent_change_24h': '12.3', 
            'percent_change_7d': '32.05', 
            'last_updated': '1512198853'}
        """
        
        query = json.loads(urllib.request.urlopen(" https://api.coinmarketcap.com/v1/ticker/bitcoin/").read())
        
        bitcoin = query[0]        
        assert(bitcoin['id'] == 'bitcoin')
        assert(bitcoin['name'] == 'Bitcoin')
        assert(bitcoin['symbol'] == 'BTC')
        ret = BitCoin(bitcoin['rank'],
                       bitcoin['price_usd'], 
                       bitcoin['price_btc'],
                       bitcoin['24h_volume_usd'], 
                       bitcoin['market_cap_usd'], 
                       bitcoin['available_supply'],
                       bitcoin['total_supply'],
                       bitcoin['max_supply'],
                       bitcoin['percent_change_1h'], 
                       bitcoin['percent_change_24h'], 
                       bitcoin['percent_change_7d'], 
                       bitcoin['last_updated'])
        return ret
    
