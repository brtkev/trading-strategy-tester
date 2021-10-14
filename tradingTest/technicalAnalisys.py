


from typing import List


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


def singleSMA(data : list[list] , window : int = 9, index : int = None, use : int = 4) -> list:
    if not index: index = len(data)
    split = [float(data[i][use]) for i in range(index-window, index)]
    return sum(split) / len(split)

def SMA(data : list[list] , size : int = None, window : int = 9, index : int = None, use : int = 4):
    if not index : index = len(data)
    if not size: size = len(data) - window
    return [ singleSMA(data, window, i, use) for i in range(index - size, index)]



