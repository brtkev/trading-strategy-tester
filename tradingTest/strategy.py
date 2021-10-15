from tradingTest import technicalAnalisys as ta

def one(data, index):
    window = 50
    sma = ta.singleSMA(data, window, index)