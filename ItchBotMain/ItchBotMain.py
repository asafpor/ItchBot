
'''
Created on Nov 25, 2017

@author: user
'''

from bitStampWrapper import BitStampWrapper
from CoinMarketWrapper import CoinMarketUpWrapper
from BittrexBot import BittrexBot
import time

if __name__ == '__main__':

    coinsMarket = CoinMarketUpWrapper()
    bittrexBot = BittrexBot()
    
    while (True):
       
        #bitcoin = coinsMarket.QueryBitCoin()
        #print(bitcoin.getTime(), bitcoin.m_priceUsd)
        #bitcoin = bittrexBot.getCurrenciesBTC()
        #print (bitcoin)

        bittrexBot.run()

        time.sleep(1)                
        


