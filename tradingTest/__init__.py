from os import close, truncate
from . import utils, strategy, technicalAnalisys as ta


class TradingTest():
    def __init__(self):
        self.trades = []
        self.position = None


    def test(self, props : dict) :
        import time
        # get symbol data
        data = utils.getHistorial(props)
        print(time.strftime("%Y %b %d", time.gmtime(data[0][0]/1000)))

            
        # iterate over data
        oc = cc = nc = 0
        for i in range(201, len(data)):
            
            #if onTrade get exit validity
            if self.position:
                #if valid exit
                if strategy.One.close(self.position, data, i):
                    self.trades.append(self.close(data, i))
                    self.position = None


            #if not onTrade get trade validity
            if not self.position:
                #if valid enter trade
                side = strategy.One.open(data, i)
                if side:
                    self.position = self.open(data, i, side)

    def open(self, data, index, side):
        return {
            'bar' : data[index],
            'index' : index,
            'side' : side
        }

    def close(self, data, index):
        self.position.update({
            'outIndex' : index,
            'outBar' : data[index],
        })
        return self.position

    def tradeAnalytics(self):
        import time

        
        analytics = {
            'percentChange' : 0,
            'gain' : 0,
            'riskFactor' : 3,
            'cap' : 100,
            'nextDouble' : 200,
            'timesDouble' : 0,
            'lowestCap' : 100,
            'highestCap' : 0,
            'biggestLose' : 0,
            'biggestWin' : 0,
        }
        
        for trade in self.trades:
            val = float(trade['bar'][4])
            outVal = float(trade['outBar'][4])
            if trade['side'] == 'LONG':
                perChange = ta.percentChange(val, outVal)
            else:
                perChange = ta.percentChange(outVal, val)

            analytics['cap'] += analytics['cap'] * analytics['riskFactor'] * (perChange / 100)

            if analytics['cap'] > analytics['nextDouble']:
                print(f"{analytics['nextDouble']} day : ", time.strftime("%Y %b %d", time.gmtime(trade['bar'][0]/1000)))
                analytics['timesDouble'] += 1
                analytics['nextDouble'] *= 2

            if perChange > analytics['biggestWin'] : analytics['biggestWin'] = perChange
            elif perChange < analytics['biggestLose'] : analytics['biggestLose'] = perChange

            if analytics['cap'] > analytics['highestCap']: analytics['highestCap'] = analytics['cap']
            elif analytics['cap'] < analytics['lowestCap']: analytics['lowestCap'] = analytics['cap']

            analytics['percentChange'] += perChange
        analytics['avgPercentChange'] = analytics['percentChange'] / len(self.trades)
        analytics['avgCapGain'] = (analytics['cap']-100) / len(self.trades)
        return analytics