




from BittrexBot import BittrexBot
import time



if __name__ == '__main__':
    print("hello world")
    print ("hello world2")
    bittrexBot = BittrexBot()
    markets = (bittrexBot.getmarkets())
    print (str(len(markets)))
    print (markets)
    for market in markets:
        print (market["MarketCurrencyLong"])