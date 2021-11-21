import time, json

def loadData(file : str) -> list:
    """loads data from json file.\n
        returns a numpy array
    """
    import json
    with open(file, "r") as f:
        data = json.loads(f.write())
    return data

    
def dayMonthYearTime(date : str):
    return int(time.mktime(time.strptime(date, "%d %b %Y")))

def yearTime(year : str):
    return int(time.mktime(time.strptime(year, "%Y")))

def fetchHistorial(props):
    """{ symbol : str, interval : str, startTime: int, endTime: int }"""
    import binanceWrapper as binance
    props["startTime"] = 1000 * props["startTime"]
    props["endTime"] = 1000 * props["endTime"]
    klines = []
    while props["startTime"] < props["endTime"]:
        print("getting ", props["startTime"])
        klines.extend(binance.symbolKlines(props["symbol"], props["interval"], 1000, props["startTime"]))
        props["startTime"] = klines[-1][0]
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
    startText = time.strftime("%Y %b %d", time.gmtime(props['startTime']))
    endText = time.strftime("%Y %b %d", time.gmtime(props['endTime']))
    path = f"historial/{props['symbol']}/{props['interval']}/{startText} to {endText}.json"
    try:
        historial = readHistorial(path)
        return historial
    except (FileNotFoundError):
        historial = fetchHistorial(props)
        writeHistorial(path, historial)
        return historial
    

def filterDups(history : list[list]):
    filter = set()
    for bar in history:
        if bar[0] not in filter:
            filter.add(bar[0])
            yield bar 
