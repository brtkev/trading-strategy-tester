from tradingTest import technicalAnalisys as ta

class One():
    window = 50
    atrLen = 5
    @classmethod
    def open(cls, data, index):
        sma = ta.singleSMA(data, cls.window, index)
        atr = ta.singleATR(data, index=index)
        if float(data[index][4]) > sma + atr * cls.atrLen: 
            return 'LONG'
        elif float(data[index][4]) < sma - atr * cls.atrLen:
            return 'SHORT'
        
    @classmethod
    def close(cls, position, data, index):
        sma = ta.singleSMA(data, cls.window, index)
        atr = ta.singleATR(data, index=index)
        if position['side'] == 'LONG' and float(data[index][4]) < sma - atr * cls.atrLen:
            return True
        elif position['side'] == 'SHORT' and float(data[index][4]) > sma + atr * cls.atrLen:
            return True
        return False


class Two():
    trend = 100
    window = 50
    small = 20
    @classmethod
    def open(cls, data, index):
        small = ta.singleSMA(data, window= cls.small, index=index) 
        trend = ta.singleSMA(data, window= cls.trend, index=index) 
        sma = ta.singleSMA(data, window=cls.window, index=index)
        atr = ta.singleATR(data, index=index)
        if  small > sma > trend and  small > float(data[index][4]) > trend: 
            return 'LONG'
        elif small < sma < trend and small < float(data[index][4]) < trend:
            return 'SHORT'

    @classmethod
    def close(cls, position, data, index):
        atr = ta.singleATR(data, index=position['index'])
        if position['side'] == 'LONG':
            if float(data[index][4]) < float(position['bar'][4]) - atr * 4:
                return True

            elif float(data[index][4]) > float(position['bar'][4]) + atr * 4: 
                return True
        elif position['side'] == 'SHORT':
            if float(data[index][4]) > float(position['bar'][4]) + atr * 4:
                return True

            elif float(data[index][4]) < float(position['bar'][4]) - atr * 4: 
                return True
        
        return False


class EthScalp():
    count = 0
    
    @classmethod
    def setup(cls, data):
        cls.RSI = ta.RSI(data, window=21)
        cls.SMMA200 = ta.SMMA(data, window = 200)
        cls.SMMA20 = ta.SMMA(data , window=20)

    @classmethod
    def open(cls, data, index):
        closePrice = float(data[index][4])
        if cls.SMMA20[index-20] >  cls.SMMA200[index - 200]:
            if cls.RSI[index - 21] >= 51 and closePrice > cls.SMMA20[index-20]:
                for x in data[index-3:index+1]:
                    if float(x[3]) < cls.SMMA20[index-20]:
                        sl = ta.lastLow(data, index)
                        sl = sl - sl * 0.001
                        tp = closePrice + ((closePrice - sl) * 2)
                        # if ta.percentChange(sl, closePrice) < 1: return
                        return {
                            'side' : 'BUY',
                            'sl' : sl,
                            'tp' : tp,
                        }

    @classmethod
    def close(cls, position, data, index):
        if position['side'] == 'BUY':

            if float(data[index][2]) > position['tp']:
                return {
                    'status' : 'win',
                    'price' : position['tp'],
                    'closeIndex' : index
                }
            elif float(data[index][3]) < position['sl']:
                return {
                    'status' : 'loss',
                    'price' : position['sl'],
                    'closeIndex' : index
                }



class rideLong():

    trades = []
    position = None

    @classmethod
    def setup(cls, data):
        window = 100
        cls.SMA50 = [0 for i in range(window)]
        cls.SMA50.extend(ta.SMA(data, window=window))
        cls.ATR = [0 for i in range(14)]
        cls.ATR.extend(ta.ATR(data))

    @classmethod
    def shouldOpen(cls, index, data):

        close = float(data[index][4])
        if close > cls.SMA50[index-1] + cls.ATR[index-1] * 2:
            cls.position = {
                'entry' : close,
                'entryIndex': index,
            }

    @classmethod
    def shouldClose(cls, index, data):
        close = float(data[index][4])
        if close < cls.SMA50[index-1] - cls.ATR[index-1] * 2:
            cls.position.update({
                'exit' : close,
                'exitIndex' : index
            })
            cls.trades.append(cls.position)
            cls.position = None

    @classmethod
    def getStats(cls, dataLen):
        account = 100
        wins = loses = count = fees = avgCandles = net = 0
        currLosingStreak = currWinningStreak = losingStreak = winningStreak = biggestWin = biggestLoss = 0
        netArray = []
        for trade in cls.trades:
            count += 1
            tradeSize = account
            fees += tradeSize * 0.2 / 100
            avgCandles += trade['exitIndex'] - trade['entryIndex']

            entry = trade['entry']
            exit = trade['exit']
            if trade['entry'] < trade['exit']:
                wins += 1
                percentChange = ta.percentChange(entry, exit)
                profit = account * percentChange/100
                net += profit
                account += profit

                if percentChange > biggestWin:
                    biggestWin = percentChange

                currLosingStreak = 0
                currWinningStreak += 1
            else:
                loses += 1
                percentChange = ta.percentChange(exit, entry)
                lose = account * percentChange/100
                net -= lose
                account -= lose

                if percentChange > biggestLoss:
                    biggestLoss = percentChange

                currLosingStreak += 1
                currWinningStreak = 0

            if losingStreak < currLosingStreak:
                losingStreak = currLosingStreak
            if winningStreak < currWinningStreak:
                winningStreak = currWinningStreak
            
            netArray.append(net)

        avgCandles /= count
        
        return
        import json
        with open('stats.json', 'a') as f:
            f.write(json.dumps({
                'wins' : wins,
                'loses' : loses,
                'count' : count,
                'net' : net,
                'fees' : fees,
                'avgCandles' : avgCandles,
                'dataLen' : dataLen,
                'losingStreak' : losingStreak,
                'winningStreak' : winningStreak,
                'biggestLoss' : biggestLoss,
                'biggestWin' : biggestWin


            }, indent=4))