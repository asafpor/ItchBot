
'''
Created on Nov 25, 2017

@author: user
'''

from bitStampWrapper import BitStampWrapper
from CoinMarketWrapper import CoinMarketUpWrapper

if __name__ == '__main__':
    print("hello world")
    print ("hello world2")
    bsw = BitStampWrapper()
    print(bsw.myTestFunc("btcusd"))
    print(bsw.myTestFunc("xrpusd"))
    print(bsw.myTestFunc("ethusd"))
    
    
    
    coinsMarket = CoinMarketUpWrapper()
    coinsMarket.QueryBitCoin()

