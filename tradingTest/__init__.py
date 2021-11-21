from os import close, truncate

from app import trades_analitics
from . import utils, strategy, technicalAnalisys as ta


class TradingTest():
    def __init__(self):
        self.trades = []
        self.position = None


    def test(self, props : dict) :
        import time
        # get symbol data
        data = utils.getHistorial(props)

        print("len ", len(data))
        print(time.strftime("%Y %b %d", time.gmtime(data[0][0]/1000)))

        strat = strategy.EthScalp
        strat.setup(data)
        

        self.dataLen = len(data)
        # iterate over data
        for i in range(201, len(data)):
            
            #if onTrade get exit validity
            if self.position:
                #if valid exit
                shouldClose = strat.close(self.position, data, i)
                if shouldClose:
                    self.position.update(shouldClose)
                    self.trades.append(self.position)
                    self.position = None


            #if not onTrade get trade validity
            if not self.position:
                #if valid enter trade
                side = strat.open(data, i)
                if side:
                    self.position = self.open(data, i, side)

        self.strat = strat

    def open(self, data, index, side):
        if type(side) == dict:
            side['index'] = index
            side['bar'] = data[index]
            return side
            
        return {
            'bar' : data[index],
            'index' : index,
            'side' : side
        }

    def tradeAnalytics(self):        
        
        def iterateTrades():
            currWinningStreak = currLosingStreak = 0
            for trade in self.trades:
                TradesAnalisys.count += 1
                closeP = float(trade['bar'][4])

                if trade['status'] == 'win':
                    TradesAnalisys.wins += 1
                    TradesAnalisys.gain += 2

                    currLosingStreak = 0
                    currWinningStreak += 1
                else:
                    TradesAnalisys.loses += 1
                    TradesAnalisys.gain -= 1

                    currLosingStreak += 1
                    currWinningStreak = 0

                if TradesAnalisys.losingStreak < currLosingStreak:
                    TradesAnalisys.losingStreak = currLosingStreak
                if TradesAnalisys.winningStreak < currWinningStreak:
                    TradesAnalisys.winningStreak = currWinningStreak

        iterateTrades()
        print("count", TradesAnalisys.count)
        print("wins", TradesAnalisys.wins)
        print("loses", TradesAnalisys.loses)
        print("gain", TradesAnalisys.gain)
        print("winrate", TradesAnalisys.wins/TradesAnalisys.count)
        print()
        print("biggest winning streak", TradesAnalisys.winningStreak)
        print("biggest losing streak", TradesAnalisys.losingStreak)

class TradesAnalisys:
    count = 0
    wins = 0
    loses = 0
    change = 0
    gain  = 0
    losingStreak = 0
    winningStreak = 0