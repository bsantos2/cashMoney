# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:38:32 2018

@author: bsantos
"""

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

#Rename your lib/functions here
stockData = iexFunctions.iexScan()
fetchData = getData.getJson()
ind = stockIndicators.Indicators()

def parseJson(array,label):
    data = []
    for x in range(0,length(array)):
        data.append(array[x][label])
    return data

def stockList():
    url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json"
    snp500 = fetchData.fetchIt(url)
    url = "https://pkgstore.datahub.io/core/nyse-other-listings/nyse-listed_json/data/e8ad01974d4110e790b227dc1541b193/nyse-listed_json.json"
    nyse = fetchData.fetchIt(url)
    stock = parseJson(snp500, 'Symbol')
    stock = stock.append(nyse, 'ACT Symbol')
    return stock

