
'''
Created on Nov 25, 2017

@author: user
'''

from bitStampWrapper import BitStampWrapper
from CoinMarketWrapper import CoinMarketUpWrapper
import time

if __name__ == '__main__':
    print("hello world")
    print ("hello world2")
    bsw = BitStampWrapper()
    print(bsw.myTestFunc("btcusd"))
    print(bsw.myTestFunc("xrpusd"))
    print(bsw.myTestFunc("ethusd"))
    
    coinsMarket = CoinMarketUpWrapper()
    while (True):
       
        bitcoin = coinsMarket.QueryBitCoin()
        print(bitcoin.getTime(), bitcoin.m_priceUsd)
        
        time.sleep(120)                
        

