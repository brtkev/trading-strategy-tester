from tradingTest import technicalAnalisys as ta

class One():
    window = 50
    @classmethod
    def open(cls, data, index):
        sma = ta.singleSMA(data, cls.window, index)
        atr = ta.singleATR(data, index=index)
        if float(data[index][4]) > sma + atr * 2: 
            return 'LONG'
        elif float(data[index][4]) < sma - atr * 2:
            return 'SHORT'
        
    @classmethod
    def close(cls, position, data, index):
        sma = ta.singleSMA(data, cls.window, index)
        atr = ta.singleATR(data, index=index)
        if position['side'] == 'LONG' and float(data[index][4]) < sma - atr * 2:
            return True
        elif position['side'] == 'SHORT' and float(data[index][4]) > sma + atr * 2:
            return True
        return False

