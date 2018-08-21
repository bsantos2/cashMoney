# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 17:49:04 2018

@author: bsantos
https://codereview.stackexchange.com/questions/70510/calculating-exponential-moving-average-in-python
"""
class Indicators:
    def sma(self, data, window):
        if len(data) < window:
            #raise ValueError("data is too short")
            current_sma = -999
        else:
            current_sma = sum(data[-window:]) / float(window)
        return current_sma
    
    def ema(self, data, window):
        if len(data) < 2 * window:
            #raise ValueError("data is too short")
            current_ema = -999
        else:
            c = 2.0 / (window + 1)
            current_ema = self.sma(data[-window*2:-window], window)
            for value in data[-window:]:
                current_ema = (c * value) + ((1 - c) * current_ema)
        return current_ema
    
    def insideCheck(self,openPriceArray, closePriceArray, window):
        if len(openPriceArray) < window and len(closePriceArray) < window:
            #raise ValueError("data is too short")
            check = 0
        else:
            dataSize = len(closePriceArray) - 1
        currRange = abs(closePriceArray[dataSize] - openPriceArray[dataSize])
        currHigh = closePriceArray[dataSize]
        currLow = openPriceArray[dataSize]
        prevRange = abs(closePriceArray[dataSize - window] - openPriceArray[dataSize - window])
        prevHigh = closePriceArray[dataSize - window]
        prevLow = openPriceArray[dataSize - window]
        if currRange < prevRange and currHigh < prevHigh and currLow > prevLow and currHigh > currLow and prevHigh > prevLow:
            check = 1
        else:
            check = 0
        return check
    
    def insideTightCheck(self, openPriceArray, closePriceArray, window):
        if len(openPriceArray) < window and len(closePriceArray) < window:
            #raise ValueError("data is too short")
            check = 0
        else:
            dataSize = len(closePriceArray) - 1
        currRange = abs(closePriceArray[dataSize] - openPriceArray[dataSize])
        currHigh = closePriceArray[dataSize]
        meas = currRange/currHigh
        if meas <= 0.02:
            check = 1
        else:
            check = 0
        return check
                
                
            