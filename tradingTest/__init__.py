from . import utils


class TradingTest():
    def __init__(self):
        pass

    def test(self, props : dict) :
        # get symbol data
        data = utils.getHistorial(props)

            
        # iterate over data
        for i in range(len(data)):

            #if onTrade get exit validity
                #if valid exit
            
            #if not onTrade get trade validity
                #if valid enter trade
            pass



    