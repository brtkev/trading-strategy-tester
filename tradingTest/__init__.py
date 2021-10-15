from . import utils


class TradingTest():
    def __init__(self):
        self.trades = []
        self.positions = []

    def isTrading(self):
        return len(self.positions) > 0

    def test(self, props : dict) :
        # get symbol data
        data = utils.getHistorial(props)

            
        # iterate over data
        for i in range(len(data)):

            #if onTrade get exit validity
            if self.isTrading():
                pass
                #if valid exit
            #if not onTrade get trade validity
            else:
                pass
                
                #if valid enter trade
                

            pass



    