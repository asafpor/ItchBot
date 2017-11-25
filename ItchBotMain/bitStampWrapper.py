import urllib.request

class BitStampWrapper:
 
    def __init__(self):
       print("BitStampWrapper init") 
    
    def myTestFunc(self, stolk):
        return  urllib.request.urlopen("https://www.bitstamp.net/api/v2/ticker/" + stolk).read()
