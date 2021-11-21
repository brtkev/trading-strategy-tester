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
        if cls.SMMA20[index-20] >  cls.SMMA200[index - 200]:
            if cls.RSI[index - 21] >= 51 and float(data[index][4]) > cls.SMMA20[index-20]:
                for x in data[index-3:index+1]:
                    if float(x[3]) < cls.SMMA20[index-20]:
                        sl = ta.lastLow(data, index)
                        sl = sl - sl * 0.001
                        tp = float(data[index][4]) + ((float(data[index][4]) - sl) * 2)
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
                    'price' : position['tp'] 
                }
            elif float(data[index][3]) < position['sl']:
                return {
                    'status' : 'loss',
                    'price' : position['sl'] 
                }
        