import requests
import time
import json
from pricerGA import *
from gLib import *
from mtGoxInterface import *

#config variables
resultsFileName = "results_3.txt"
tickerRequestURL = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
recentTradesRequestURL = 'http://data.mtgox.com/api/1/BTCUSD/trades/fetch'
marketDepthRequestURL = 'https://data.mtgox.com/api/1/BTCUSD/depth/fetch'

#initial conditions
USD_nominal = 100.0
BTC_nominal = 0

#historical data in memory
BTCmtm = 0
USDmtm = 0

#thresholds
BUY_THRESHOLD = 1.0
SELL_THRESHOLD = -1.0

#gLib engine
theSmhi = gLibEngine(BUY_THRESHOLD, SELL_THRESHOLD)

#index
i=0


while (1==1):
    #requests to mtgox
    theAmbassador = mtGoxInterface()
    
    ticker = theAmbassador.getTickerAsJson()
    recentTrades = theAmbassador.getRecentTradesAsJson()
    marketDepth = theAmbassador.getMarketDepthAsJson()
    
    #attempt to mtm
    singleServingPricer = pricerGA(marketDepth)
    try:
        BTCmtm = singleServingPricer.priceUSDtoBTC(USD_nominal) 
    except marketDepthTooShallow as e:
        BTCmtm = ( 'Market depth too shallow: ' + str(e.remainingVolume) + ' volume remaining' )
    try:
        USDmtm = singleServingPricer.priceBTCtoUSD(BTC_nominal) 
    except marketDepthTooShallow as e:
        USDmtm = ('Market depth too shallow: ' + str(e.remainingVolume) + ' volume remaining' )
 
    pollTime = time.time()
    
    #write to file
    f = open(resultsFileName, "a+")
    f.write(str(BTCmtm) + ',' + str(USDmtm) + ',' + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()) + "\n" )
    f.close()
    i=i+1
    
    #attempt to make a trading decision
    theSmhi.addMarketDataAndUpdateSlope(USDmtm, BTCmtm, pollTime)
    
    if theSmhi.shouldBuyBTC():
        theAmbassador.placeBuyBTCOrder()
        #buy - eventually would want to replace this
        USD_nominal = 0
        BTC_nominal = BTCmtm - BTCmtm*.006 #trading fee
    
    if theSmhi.shouldSellBTC():
        theAmbassador.placeSellBTCOrder()
        #sell - eventually would want to replace this
        USD_nominal = USDmtm - USDmtm*.006 #trading fee
        BTC_nominal = 0
    
    time.sleep(300)

    #this is rewriting the file


