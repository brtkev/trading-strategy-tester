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

        strat = strategy.rideLong
        strat.setup(data)
        for i in range( 201, len(data)):
            if strat.position:
                strat.shouldClose(i, data)
            else:
                strat.shouldOpen(i, data)

        strat.getStats(len(data))
        return

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
                tradeSize = ta.qtyToTrade(100, closeP, trade['sl'], 0.5)
                TradesAnalisys.avgTradeSize += tradeSize
                TradesAnalisys.avgChange += ta.percentChange(trade['sl'], closeP)
                TradesAnalisys.fees += tradeSize * 0.02 / 100
                TradesAnalisys.avgCandles += trade['closeIndex'] - trade['index']
                if tradeSize > 100:
                    print(tradeSize, ta.percentChange(trade['sl'], closeP))

                if trade['status'] == 'win':
                    TradesAnalisys.wins += 1
                    TradesAnalisys.gain += 2
                    TradesAnalisys.gainInAsset += 2 * 100 * 0.5/100 

                    currLosingStreak = 0
                    currWinningStreak += 1
                else:
                    TradesAnalisys.loses += 1
                    TradesAnalisys.gain -= 1
                    TradesAnalisys.gainInAsset -= 100 * 0.5 / 100

                    currLosingStreak += 1
                    currWinningStreak = 0

                if TradesAnalisys.losingStreak < currLosingStreak:
                    TradesAnalisys.losingStreak = currLosingStreak
                if TradesAnalisys.winningStreak < currWinningStreak:
                    TradesAnalisys.winningStreak = currWinningStreak
            TradesAnalisys.avgTradeSize /= TradesAnalisys.count
            TradesAnalisys.avgChange /= TradesAnalisys.count
            TradesAnalisys.avgCandles /= TradesAnalisys.count

        iterateTrades()
        print("count", TradesAnalisys.count)
        print("wins", TradesAnalisys.wins)
        print("loses", TradesAnalisys.loses)
        print("gain", TradesAnalisys.gain)
        print("winrate", round(100*TradesAnalisys.wins/TradesAnalisys.count,2))
        print()
        print("biggest winning streak", TradesAnalisys.winningStreak)
        print("biggest losing streak", TradesAnalisys.losingStreak)
        print("avg trade size", TradesAnalisys.avgTradeSize)
        print("avg trade change", TradesAnalisys.avgChange)
        print("avg candles per trade", TradesAnalisys.avgCandles)
        print()
        print("gain in asset", TradesAnalisys.gainInAsset)
        print("fees", TradesAnalisys.fees)
class TradesAnalisys:
    count = 0
    wins = 0
    loses = 0
    change = 0
    gain  = 0
    losingStreak = 0
    winningStreak = 0
    avgChange = 0
    avgCandles = 0

    gainInAsset = 0
    fees = 0
    avgTradeSize = 0