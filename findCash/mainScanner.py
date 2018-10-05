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
import string

stockData = iexFunctions.iexScan()
fetchData = getData.getJson()
ind = stockIndicators.Indicators()

#Array of SP500 and MDY here
url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json"
snp500 = fetchData.fetchIt(url)
#url = "https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_json/data/e8ad01974d4110e790b227dc1541b193/nyse-listed_json.json"
#nyse = fetchData.fetchIt(url)
stock = fetchData.parseJson(snp500, 'Symbol')
#stock = fetchData.parseJson(nyse, 'ACT Symbol')
#snp500 = [{"Name": "Time Warner Inc.", "Sector": "Consumer Discretionary", "Symbol": "TWX"}]
watchMe = []
inWeek = []
inDay = []
tightWeek = []
tightDay = []
buyMe = []
highTier = []

#invalidChars list
invalidChars = set(string.punctuation)

#Initialize final watchlist
#NO DATA FOR 150
attempts = 1000
while attempts:
    try:
        for x in range(0,len(stock)):
            if any(char in invalidChars for char in stock[x]):
                statusString = 'Invalid char in ticker'
                print(statusString)
            else:
                data = stockData.getKeyStats(stock[x])
                openPrice = data[0]
                currentPrice = data[1] #also the close price
                avgVol = data[2]
                low52 = data[3]
                high52 = data[4]
                dailyData = stockData.getDaily(stock[x], 'close')
                ema50 = ind.ema(dailyData,50) 
                ema150 = ind.ema(dailyData,150)#cant calc
                ema200 = ind.ema(dailyData,200)#cant calc
                condition = 0
                statusString = stock[x]
                if currentPrice > ema200: 
                    condition = condition + 1
                if (currentPrice > 0.35*high52) and (currentPrice >= low52) and (currentPrice <= low52*3) and (currentPrice >= 0.25*high52):
                    condition = condition + 1
                if ema50 > ema200: 
                    condition = condition + 1
                if currentPrice > ema50: 
                    condition = condition + 1
                if avgVol >= 500000:
                    condition = condition + 1
                #need one more case that ema 200 is up the last month; preferably 4-5 months though
                if condition == 5:
                    #Do thorough checks
                    if ema50 > ema150 and ema150 > ema200 and currentPrice > ema150:
                        #Add to Watchlist
                        watchMe.append(stock[x])
                        statusString = statusString + ' added to watchlist;'
                        print(statusString)
                        #Do volatility contraction checks: IF IT PASSES, ADD to WATCHME and do more checks
                        #1. Calc if inside day, ADD TO INSIDEDAY
                        #2. Calc if inside week, ADD TO INSIDEWEEK
                        #3. Calc 8sma and 14sma: if 8sma > 14sma and open price > 8sma, ADD TO BUYME
                        sma8 = ind.sma(dailyData,8)
                        sma14 = ind.sma(dailyData,14)
                        openPriceArr = stockData.getDaily(stock[x], 'open') #FIGURE OUT HOW TO SORT REVERSELY
                        insideDay = ind.insideCheck(openPriceArr, dailyData,1)
                        insideWeek = ind.insideCheck(openPriceArr, dailyData,5)
                        if insideWeek == 1:
                            inWeek.append(stock[x])
                            statusString = statusString + ' inside week;'
                        if insideDay == 1:
                            inDay.append(stock[x])
                            statusString = statusString + ' inside day;'
                        if sma8 > sma14 and sma8 > openPrice:
                            buyMe.append(stock[x])
                            statusString = statusString + ' A BUY!!!'
                        if ind.insideTightCheck(openPriceArr,dailyData,1,1) ==  1:
                            tightDay.append(stock[x])
                            statusString = statusString + ' tight'
                        if ind.insideTightCheck(openPriceArr,dailyData,5,1) ==  1:  
                            tightWeek.append(stock[x])
                            statusString = statusString + ' tight'
                else:
                    statusString = statusString + ' better luck next time'
                    print(statusString)
        break
    except urllib.error.URLError:
        time.sleep(120)
        attempts -= 1
        print('Lost Connection. Wait to reconnect')
        
highTier = set(inWeek).intersection(tightWeek)
print("=WATCHLIST=")
print(watchMe)
print("=INSIDE DAY=")
print(inDay)
print("=INSIDE WEEK=")
print(inWeek)
print("=BUY ME=")
print(buyMe)
print("=TIGHT WEEK=")
print(tightWeek)
print("=HIGH TIER WATCH=")
print(highTier)


    
        