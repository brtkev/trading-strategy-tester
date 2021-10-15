def percentChange(startValue : float, endValue : float) -> float:
    """returns percent change between two points

    Args:
        startValue (float): starting point
        endValue (float): ending point

    Returns:
        float: percent change
    """
    try:
        x = (endValue - startValue)/abs(startValue) *100
        if x == 0.0:
            return 0.0000000001
        else:
            return x
    except ZeroDivisionError:
        return 0.0000000001


def singleSMA(data : list[list] , window : int = 9, index : int = None, use : int = 4) -> float:
    if not index: index = len(data)
    split = [float(data[i][use]) for i in range(index-window, index)]
    return sum(split) / len(split)

def SMA(data : list[list] , size : int = None, window : int = 9, index : int = None, use : int = 4) -> list:
    if not index : index = len(data)
    if not size: size = len(data) - window
    return [ singleSMA(data, window, i, use) for i in range(index - size, index)]

def singleEMA(data : list[list], smoothing : int = 2, window : int = 9, index : int = None, use : int = 4, lastEma : int = None) -> float:
    if not index : index = len(data)
    if not lastEma : lastEma = singleSMA(data, window, index-1, use)
    return (float(data[index-1][use]) * (smoothing / (1 + window))) + lastEma * (1 - (smoothing / (1 + window)))

def EMA(data : list[list] , smoothing : int = 2, size : int = None, window : int = 9, index : int = None, use : int = 4) -> list:
    if not index : index = len(data)
    if not size: size = len(data) - window
    def getEMA(lastEma = None): 
        for i in range(index - size, index):
            lastEma = singleEMA(data, smoothing, window, i, use, lastEma)
            yield lastEma
    return list(getEMA())

def singleTR(data : list[list], index : int = None) -> float:
    if not index : index = len(data)
    h = float(data[index - 1][2])
    l = float(data[index - 1][3])
    cp = float(data[index - 2][4])
    return max(h - l, abs(h - cp), abs(l - cp))
        
def singleATR(data : list[list], window : int = 14, index : int = None):
    if not index : index = len(data)
    tr = [ singleTR(data, index-i) for i in range(window)]
    return sum(tr) / len(tr)

def ATR(data : list[list], size : int = None, window : int = 14,  index : int = None):
    if not index : index = len(data)
    if not size: size = len(data) - window
    return [ singleATR(data, window, i) for i in range(index - size, index)]





