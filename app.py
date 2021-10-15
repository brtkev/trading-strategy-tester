# import logging
# logging.basicConfig(filename='testing/test.log', format='[%(asctime)s] - %(levelname)s - {%(filename)s:%(lineno)d} - %(name)s - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')


# def do():
    
#     from testing.components.tester import data_getter as dg, Iterator
#     currency = 'USDT'
#     symbol = ['BTC', 'ETH']

#     interval = '1h'
#     start = '1 1 2020'
#     end = '1 1 2021'
#     strat = 4
#     risk = 3
#     cap = 100
    
#     iterator = Iterator(currency, symbol, interval, start, end)

#     iterator.run( cap ,risk,strat)





def trades_analitics():
    import os, sys, json

    tradesPath = "instance.db/trades"

    tradeFilePaths = os.listdir(tradesPath)

    tradesForFile = []

    for path in tradeFilePaths:
        with open( f"{tradesPath}/{path}" , "r") as f:
            tradesForFile.append( json.loads(f.read()) ) 


    count = sumOfGains = 0
    
    for trades in tradesForFile:
        
        for trade in trades:
            # if trade['in_order']['symbol'] == 'BTCUSDT':
            sumOfGains += trade['gain']
            count += 1


    print("count is : ",count)
    print("sum of gains is : ", sumOfGains)



import sys, time, json

import binanceWrapper

if __name__ == "__main__":
    # do()
    from tradingTest import utils, technicalAnalisys as ta
    hist = utils.getHistorial({"symbol" : "BTCUSDT", "interval" : "1h", "startTime" : utils.yearTime("2010"), "endTime" : utils.dayMonthYearTime("1 jul 2021")})
    data = []
    for x in range(100):
        data.append(["time", "open", "high" , "low", x])
    # res = ta.singleSMA(hist, 50)
    # print(res)
    # res = ta.EMA(hist, 10, size=50, window=50)
    # print(res)
    # for x ,y in zip(res, hist[-50:]):
    #     if x <  float(y[4]): print("below")
    #     else: print("above")
    # print(hist[-1][4])
    # print(len(res))
    # print(len(hist))

    res =  ta.ATR(hist, 10)
    print(res)
    print(len(res))