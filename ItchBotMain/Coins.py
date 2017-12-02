'''
Created on Dec 2, 2017

@author: user
'''
import time
class Coin():
    '''
    classdocs
    '''
    def __init__(self,
                 rank, 
                 priceUsd, 
                 priceBtc, 
                 _24_volumeUsd,
                 marketCapUsd,
                 availableSupply, 
                 totalSupply, 
                 maxSupply, 
                 percentChange1h, 
                 percentChange24h, 
                 percentChange7d, 
                 lastUpdated):
        '''
        Constructor
        '''
        self.m_rank = rank
        self.m_priceUsd = priceUsd 
        self.m_priceBtc = priceBtc 
        self.m_24_volumeUsd = _24_volumeUsd
        self.m_marketCapUsd = marketCapUsd
        self.m_availableSupply = availableSupply 
        self.m_totalSupply = totalSupply 
        self.m_maxSupply = maxSupply
        self.m_percentChange1h = percentChange1h
        self.m_percentChange24h = percentChange24h 
        self.m_percentChange7d = percentChange7d 
        self.m_lastUpdated = lastUpdated
        
    def getTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(self.m_lastUpdated)))
        
        
class BitCoin(Coin):
    
    def __init__(self,
                 rank, 
                 priceUsd, 
                 priceBtc, 
                 _24_volumeUsd,
                 marketCapUsd,
                 availableSupply, 
                 totalSupply, 
                 maxSupply, 
                 percentChange1h, 
                 percentChange24h, 
                 percentChange7d, 
                 lastUpdated):
        Coin.__init__(self,
                      rank, 
                      priceUsd, 
                      priceBtc, 
                      _24_volumeUsd,
                      marketCapUsd,
                      availableSupply, 
                      totalSupply, 
                      maxSupply, 
                      percentChange1h, 
                      percentChange24h, 
                      percentChange7d, 
                      lastUpdated)
                 
     