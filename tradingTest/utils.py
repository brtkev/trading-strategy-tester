import time, json

def loadData(file : str) -> list:
    """loads data from json file.\n
        returns a numpy array
    """
    import json
    with open(file, "r") as f:
        data = json.loads(f.write())
    return data




# def gather_data(currency, symbols_list, interval, start, end):
#     if symbols_list:
#         client = Client("", "", { "timeout" : 20})
#         try:
#             os.makedirs(f"instance.db/historial/{currency}/{interval}/{start.replace(' ', '_')}-{end.replace(' ', '_')}")
#         except FileExistsError:
#             pass

#         for symbol in symbols_list:
#             if symbol != currency:
#                 get_historial(client, currency, symbol, interval, start, end)


    
def dayMonthYearTime(date : str):
    return int(time.mktime(time.strptime(date, "%d %b %Y")))

def yearTime(year : str):
    return int(time.mktime(time.strptime(year, "%Y")))

def fetchHistorial(props):
    """{ symbol : str, interval : str, startTime: int, endTime: int }"""
    import binanceWrapper as binance

    klines = []
    while props["startTime"] < props["endTime"]:
        klines.extend(binance.symbolKlines(props["symbol"], props["interval"], 1000, props["startTime"] * 1000))
        props["startTime"] += 60 * 60 * 1000
    return list(filterDups(klines))

def writeHistorial(path : str, historial : list[list]):
    import os
    try:
        pathSplit = path.split('/')
        pathSplit.pop()
        os.makedirs('/'.join(pathSplit))
    except FileExistsError:
        pass
    finally:
        with open(path, "w") as f:
            f.write(json.dumps(historial))

def readHistorial(path) -> list[list]:
    with open(path ,"r") as f:
            return json.loads(f.read())    

def getHistorial(props : dict) -> list[list]:
    """{ symbol : str, interval : str, startTime: int, endTime: int }"""
    path = f"historial/{props['symbol']}/{props['interval']}/{props['endTime']}.json"
    try:
        historial = readHistorial(path)
    except (FileNotFoundError):
        historial = fetchHistorial(props)
        writeHistorial(path, historial)
    finally:
        return historial
    

def filterDups(history : list[list]):
    filter = set()
    for bar in history:
        if bar[0] not in filter:
            filter.add(bar[0])
            yield bar 
