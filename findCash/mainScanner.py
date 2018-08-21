# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 14:57:56 2018

@author: bsantos
"""

"Get Price"

import sys
import os #specify relative paths
dirname = os.path.dirname(__file__)
funcPath = dirname + '/functions'
sys.path.append(funcPath)
#import botFunctions
#import queryPrice
#import googleSheets
import iexFunctions
import getData
import stockIndicators
import time 
import urllib

stockData = iexFunctions.iexScan()
fetchData = getData.getJson()
ind = stockIndicators.Indicators()

#Array of SP500 and MDY here
url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json"
snp500 = fetchData.fetchIt(url)
#snp500 = [{"Name": "Equinix", "Sector": "Real Estate", "Symbol": "EQIX"}]
watchMe = []
inWeek = []
inDay = []
buyMe = []



#Initialize final watchlist
#NO DATA FOR 150
attempts = 1000
while attempts:
    try:
        for x in range(0,len(snp500)):
            data = stockData.getKeyStats(snp500[x]['Symbol'])
            openPrice = data[0]
            currentPrice = data[1] #also the close price
            low52 = data[2]
            high52 = data[3]
            dailyData = stockData.getDaily(snp500[x]['Symbol'], 'close')
            ema50 = ind.ema(dailyData,50) 
            ema150 = ind.ema(dailyData,150)#cant calc
            ema200 = ind.ema(dailyData,200)#cant calc
            condition = 0
            statusString = snp500[x]['Symbol']
            if currentPrice > ema200: 
                condition = condition + 1
            if (currentPrice > 0.35*high52) and (currentPrice >= low52) and (currentPrice <= low52*3) and (currentPrice >= 0.25*high52):
                condition = condition + 1
            if ema50 > ema200: 
                condition = condition + 1
            if currentPrice > ema50: 
                condition = condition + 1
            #need one more case that ema 200 is up the last month; preferably 4-5 months though
            if condition == 4:
                #Do thorough checks
                if ema50 > ema150 and ema150 > ema200 and currentPrice > ema150:
                    #Add to Watchlist
                    watchMe.append(snp500[x]['Symbol'])
                    statusString = statusString + ' added to watchlist;'
                    print(statusString)
                    #Do volatility contraction checks: IF IT PASSES, ADD to WATCHME and do more checks
                    #1. Calc if inside day, ADD TO INSIDEDAY
                    #2. Calc if inside week, ADD TO INSIDEWEEK
                    #3. Calc 8sma and 14sma: if 8sma > 14sma and open price > 8sma, ADD TO BUYME
                    sma8 = ind.sma(dailyData,8)
                    sma14 = ind.sma(dailyData,14)
                    openPriceArr = stockData.getDaily(snp500[x]['Symbol'], 'open') #FIGURE OUT HOW TO SORT REVERSELY
                    insideDay = ind.insideCheck(openPriceArr, dailyData,1)
                    insideWeek = ind.insideCheck(openPriceArr, dailyData,5)
                    if insideWeek == 1:
                        inWeek.append(snp500[x]['Symbol'])
                        statusString = statusString + ' inside week;'
                    if insideDay == 1:
                        inDay.append(snp500[x]['Symbol'])
                        statusString = statusString + ' inside day;'
                    if sma8 > sma14 and sma8 > openPrice:
                        buyMe.append(snp500[x]['Symbol'])
                        statusString = statusString + ' A BUY!!!'
                    if ind.insideCheck(openPriceArr,dailyData,1) ==  1 or  ind.insideCheck(openPriceArr, dailyData , 5) ==1:
                        buyMe.append(snp500[x]['Symbol'])
                        statusString = statusString + ' tight'
            else:
                statusString = statusString + ' better luck next time'
                print(statusString)
        break
    except urllib.error.URLError:
        time.sleep(120)
        attempts -= 1
        print('Lost Connection. Wait to reconnect')
        
print("=WATCHLIST=")
print(watchMe)
print("=INSIDE DAY=")
print(inDay)
print("=INSIDE WEEK=")
print(inWeek)
print("=BUY ME=")
print(buyMe)


    
        