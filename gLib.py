
#Holds market data and makes buy/sell decisions
class gLibEngine:
    def __init__(self, buyThreshold, sellThreshold, USDmtm=None, BTCmtm=None, pollTime=None, USDmtms=[], BTCmtms=[], pollTimes=[], USDslopes=[], BTCslopes=[], USDslopeSum=0, BTCslopeSum=0):
        #this has some buggy parameter combos - deal with it
        self.buyThreshold = buyThreshold
        self.sellThreshold = sellThreshold
        
        self.USDmtms = USDmtms
        self.BTCmtms = BTCmtms
        self.pollTimes = pollTimes
        self.USDslopes = USDslopes
        self.BTCslopes = BTCslopes
        self.USDslopeSum = USDslopeSum
        self.BTCslopeSum = BTCslopeSum
        self.shouldUpdate = False
        
        self.addMarketDataAndUpdateSlope(USDmtm, BTCmtm, pollTime)
    
    def addMarketDataAndUpdateSlope(self, USDmtm, BTCmtm, pollTime):
		#TODO: handle market too shallow
        self.addMarketData(USDmtm, BTCmtm, pollTime)
        self.updateSlopeForOnePoint()
        self.updateSlopeSums()
        
    def addMarketData(self, USDmtm, BTCmtm, pollTime):
        if USDmtm != None and BTCmtm != None and pollTime != None:
            #all or nothing baby
            self.USDmtms.append(USDmtm)
            self.BTCmtms.append(BTCmtm)
            self.pollTimes.append(pollTime)
            self.shouldUpdate = True
        else:
            #TODO: throw error maybe? maybe if one is missing? i.e. market too shallow
            pass
            

    def updateSlopeForOnePoint(self):
        if self.shouldUpdate:
            if len(self.USDmtms) == (len(self.USDslopes) + 1) and len(self.BTCmtms) == (len(self.BTCslopes) + 1):
                if len(self.pollTimes) > 1 and self.pollTimes[-1] != self.pollTimes[-2]:
                    self.USDslopes.append( (self.USDmtms[-1] - self.USDmtms[-2])/(self.pollTimes[-1] - self.pollTimes[-2]) )
                    self.BTCslopes.append( (self.BTCmtms[-1] - self.BTCmtms[-2])/(self.pollTimes[-1] - self.pollTimes[-2]) )
                else:
                    self.USDslopes.append( 0 )
                    self.BTCslopes.append( 0 )
                
    def updateSlopeSums(self):
        if self.shouldUpdate:            
            if len(self.USDslopes) > 1:
            
                USDslopeSign = self.calcSlopeSign( self.USDslopes )
                BTCslopeSign = self.calcSlopeSign( self.BTCslopes )
                
                if self.USDslopes[-1] > 0:
                    if USDslopeSign == 'n':
                        self.USDslopeSum = self.USDslopes[-1]
                    elif USDslopeSign == 'p':
                        self.USDslopeSum += self.USDslopes[-1]
                elif self.USDslopes[-1] < 0:
                    if USDslopeSign == 'p':
                        self.USDslopeSum = self.USDslopes[-1]
                    elif USDslopeSign == 'n':
                        self.USDslopeSum += self.USDslopes[-1]
                
                if self.BTCslopes[-1] > 0:
                    if BTCslopeSign == 'n':
                        self.BTCslopeSum = self.BTCslopes[-1]
                    elif BTCslopeSign == 'p':
                        self.BTCslopeSum += self.BTCslopes[-1]
                elif self.BTCslopes[-1] < 0:
                    if BTCslopeSign == 'p':
                        self.BTCslopeSum = self.BTCslopes[-1]
                    elif BTCslopeSign == 'n':
                        self.BTCslopeSum += self.BTCslopes[-1]
            self.shouldUpdate = False
            
    def calcSlopeSign( self, slopes ):
        if slopes[-2] >= 0:
            return 'p'
        if slopes[-2] < 0:
            return 'n'
            
            
    def shouldBuyBTC(self):
        if len(self.USDslopes) > 1:
            USDslopeSign = self.calcSlopeSign( self.USDslopes )                
            if self.USDslopeSum > self.buyThreshold and USDslopeSign == 'p':
                return True
            else:
                return False
        else:
            return False
    
    def shouldSellBTC(self):
        if len(self.USDslopes) > 1:
            BTCslopeSign = self.calcSlopeSign( self.BTCslopes )
            if self.BTCslopeSum < self.sellThreshold and BTCslopeSign == 'n':
                return True
            else:
                return False
        else:
            return False
        