class marketDepthTooShallow(Exception):
    def __init__(self, remainingVolume):
        self.remainingVolume = remainingVolume
    def __str__(self):
        return repr(self.remainingVolume)
         
class pricerGA():
	def __init__(self, marketDepth):
		self.marketDepth = marketDepth
		
	def priceUSDtoBTC(self, USDVolume, i=0):
		#recursively price based off current asks 
		#i is trade level
		if i >= len(self.marketDepth['return']['asks']):
			raise marketDepthTooShallow(USDVolume)
		
		BTCvolumeAvailable = self.marketDepth['return']['asks'][i]['amount']
		pricePerBTCatBTCvolumeAvailable = self.marketDepth['return']['asks'][i]['price']
			
		if USDVolume < BTCvolumeAvailable * pricePerBTCatBTCvolumeAvailable:
			priceInBTC = USDVolume / pricePerBTCatBTCvolumeAvailable
		else:
			priceInBTC = ( BTCvolumeAvailable
							+ self.priceUSDtoBTC( (USDVolume - BTCvolumeAvailable*pricePerBTCatBTCvolumeAvailable), 
											(i+1)))
		
		return priceInBTC
		
	def priceBTCtoUSD(self, BTCVolume, i=0):
		#recursively price based off current bids 
		#i is trade level
		if i >= len(self.marketDepth['return']['bids']):
			raise marketDepthTooShallow(BTCVolume)
		
		BTCvolumeAvailable = self.marketDepth['return']['bids'][i]['amount']
		pricePerBTCatBTCvolumeAvailable = self.marketDepth['return']['bids'][i]['price']
			
		if BTCVolume < BTCvolumeAvailable:
			priceInUSD = BTCVolume * pricePerBTCatBTCvolumeAvailable
		else:
			priceInUSD = ( BTCvolumeAvailable * pricePerBTCatBTCvolumeAvailable 
							+ self.priceBTCtoUSD( (BTCVolume - BTCvolumeAvailable), 
											(i+1)))
		
		return priceInUSD
