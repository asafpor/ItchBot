'''
Created on Dec 2, 2017

@author: user
'''

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
        m_rank = rank
        m_priceUsd = priceUsd 
        m_priceBtc = priceBtc 
        m_24_volumeUsd = _24_volumeUsd
        m_marketCapUsd = marketCapUsd
        m_availableSupply = availableSupply 
        m_totalSupply = totalSupply 
        m_maxSupply = maxSupply
        m_percentChange1h = percentChange1h
        m_percentChange24h = percentChange24h 
        m_percentChange7d = percentChange7d 
        m_lastUpdated = lastUpdated
        
        
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
         
     