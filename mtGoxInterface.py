import requests
import time
import json

class mtGoxInterface:
    def __init__(self):
        #TODO: Do something else with these URL's (put in a config file?)
        self.tickerRequestURL = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
        self.recentTradesRequestURL = 'http://data.mtgox.com/api/1/BTCUSD/trades/fetch'
        self.marketDepthRequestURL = 'https://data.mtgox.com/api/1/BTCUSD/depth/fetch'
    
    def getMarketDepthAsJson(self):
        return requests.get(self.marketDepthRequestURL).json()
        
    def getTickerAsJson(self):
        return requests.get(self.tickerRequestURL).json()
        
    def getRecentTradesAsJson(self):
        return requests.get(self.recentTradesRequestURL).json()
    
    def placeBuyBTCOrder(self):
        #TODO
        print("Placing buy order")
        
    def placeSellBTCOrder(self):
        #TODO
        print("Placing Sell order")
