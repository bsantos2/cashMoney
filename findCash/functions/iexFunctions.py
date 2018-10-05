# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 16:49:53 2018

@author: bsantos
"""

import time
import getData

fetchData = getData.getJson()

class iexScan: 
    def __init__(self):
        self.base = "https://api.iextrading.com/1.0"
        return
    def getKeyStats(self,ticker):     
        #get price open/close
        obj = []
        url = self.base + "/stock/" + "%s"%(ticker) + "/quote"
        data = fetchData.fetchIt(url)
        obj.append(data['open'])
        obj.append(data['close'])   
        obj.append(data['avgTotalVolume'])
        #get precalculated ema's
        url = self.base + "/stock/" + "%s"%(ticker) + "/stats"
        data = fetchData.fetchIt(url)
        obj.append(data['week52low'])
        obj.append(data['week52high'])
        return obj
    def getDaily(self,ticker,dailyParam):
        obj = []
        url = self.base + "/stock/" + "%s"%(ticker) + "/chart/2y"
        data = fetchData.fetchIt(url)
        attempts = 10
        length = len(data)
        while attempts:
            try:
                for x in range(0,length):
                    obj.append(data[x][dailyParam])
                break
            except KeyError:
                print("Error fetching; retrying in 5 SECS")
                time.sleep(5)
                attempts = attempts - 1
                data = fetchData.fetchIt(url)
                length -= 1            
        return obj
    
        