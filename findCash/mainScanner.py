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
import botFunctions
import urllib
import string
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
stockData = iexFunctions.iexScan()
fetchData = getData.getJson()
ind = stockIndicators.Indicators()
bot = botFunctions.groupMeBot()

#For Quick SNP 500 search, make isQuick true
#False for entire NYSE and Nasdaq
isQuick = False

#Array of stocks
url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json"
snp500 = fetchData.fetchIt(url)
url = "https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_json/data/e8ad01974d4110e790b227dc1541b193/nyse-listed_json.json"
nyse = fetchData.fetchIt(url)
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed-symbols_json/data/5c10087ff8d283899b99f1c126361fa7/nasdaq-listed-symbols_json.json"
nasdaq = fetchData.fetchIt(url)

if isQuick:
    stock = fetchData.parseJson(snp500,'Symbol')
else:
    stock = fetchData.parseJson(nyse, 'ACT Symbol')
    stock = stock + fetchData.parseJson(nasdaq, 'Symbol')

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
x = 0
attempts = 5000
while attempts:
    try:
        while x < len(stock):
            statusString = stock[x]
            if any(char in invalidChars for char in stock[x]):
                statusString = statusString + ' Invalid char in ticker'
                print(statusString)
            else:
                data = stockData.getKeyStats(stock[x])
                openPrice = data[0]
                currentPrice = data[1] #also the close price
                avgVol = data[2]
                low52 = data[3]
                high52 = data[4]
                if any(y is None for y in data):
                    statusString = statusString + ' cannot retrieve data'
                    print(statusString)
                elif currentPrice < 12: #NOW CONSIDERING 12 DOLLA STOCKS
                    statusString = statusString + ' better luck next time'
                    print(statusString)
                elif avgVol < 500000:
                    statusString = statusString + ' better luck next time'
                    print(statusString)
                elif currentPrice >= 20:
                    dailyData = stockData.getDaily(stock[x], 'close')
                    ema50 = ind.ema(dailyData,50) 
                    ema150 =ind.ema(dailyData,150)#cant calc
                    ema200 = ind.ema(dailyData,200)#cant calc
                    condition = 0
                    statusString = stock[x]
                    if (currentPrice > ema200) and (currentPrice > 0.35*high52) and (currentPrice >= low52) and (currentPrice <= low52*3) and (currentPrice >= 0.25*high52) and (ema50 > ema200) and (currentPrice > ema50) and (ema50 > ema150) and (ema150 > ema200) and (currentPrice > ema150):
                        #Do thorough checks
                        #Add to Watchlist
                        watchMe.append(stock[x])
                        statusString = statusString + ' added to watchlist;'
                        #Do volatility contraction checks: IF IT PASSES, ADD to WATCHME and do more checks
                        #1. Calc if inside day, ADD TO INSIDEDAY
                        #2. Calc if inside week, ADD TO INSIDEWEEK
                        #3. Calc 8sma and 14sma: if 8sma > 14sma and open price > 8sma, ADD TO BUYME
                        sma8 = ind.sma(dailyData,8)
                        sma14 = ind.sma(dailyData,14)
                        lowPriceArr = stockData.getDaily(stock[x], 'low') #FIGURE OUT HOW TO SORT REVERSELY
                        highPriceArr = stockData.getDaily(stock[x], 'high') 
                        insideDay = ind.insideCheck(lowPriceArr, highPriceArr,1)
                        insideWeek = ind.insideCheck(lowPriceArr, highPriceArr,5)
                        if insideWeek == 1:
                            inWeek.append(stock[x])
                            statusString = statusString + ' inside week;'
                        if insideDay == 1:
                            inDay.append(stock[x])
                            statusString = statusString + ' inside day;'
                        if sma8 > sma14 and sma8 > openPrice:
                            buyMe.append(stock[x])
                            statusString = statusString + ' A BUY!!!'
                        if ind.insideTightCheck(lowPriceArr,highPriceArr,1,1) ==  1:
                            tightDay.append(stock[x])
                            statusString = statusString + ' tight'
                        if ind.insideTightCheck(lowPriceArr,highPriceArr,5,1) ==  1:  
                            tightWeek.append(stock[x])
                            statusString = statusString + ' tight'
                        print(statusString)
                    else:
                        statusString = statusString + ' better luck next time'
                        print(statusString)
            x = x + 1            
        else:
            break
    except urllib.error.URLError:
        print('Skipping this ticker ' + stock[x])
        attempts -= 1
        x = x + 1
        
        
highTier = set(inWeek).intersection(tightWeek) 
highTier = highTier.union(set(buyMe).intersection(tightWeek))
highTier = highTier.union(set(buyMe).intersection(inWeek))
highTier = highTier.union(set(buyMe).intersection(inDay))

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

#Selective shit; gotta be picky if you don't want to lose money
if isQuick:
    messageImportant = 'SNP500 WATCHLIST\n'
else:
    messageImportant = 'NASDAQ AND NYSE WATCHLIST\n'
messageImportant = messageImportant +' '.join(highTier).lower() + '\n'
#BotPost
bot.botPost('Selective shit; gotta be picky if you do not want to lose money\n')
bot.botPost(messageImportant)

#Miscellaneous shit; go here if you run out of ideas lol
message = 'now for some miscellaneous shit \n'
message = message + 'INSIDE WEEK: ' + ','.join(inWeek).lower() + '\n'
message = message + 'TIGHT WEEK: ' + ','.join(tightWeek).lower() + '\n'
message = message + 'INSIDE DAY: ' + ','.join(inDay).lower() + '\n'
message = message + 'BUY ME: ' + ','.join(buyMe).lower() + '\n'
message = message + 'MISCELLANEOUS WATCH LIST: ' + ','.join(watchMe).lower() + '\n'

#Split string every 450 chars
n = 450
message = [message[i:i + n] for i in range(0, len(message), n)]
#BotPost
for i in range(0, len(message)): bot.botPost(message[i])


    
        