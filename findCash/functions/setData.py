# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:06:07 2018

@author: bsantos
"""
import pickle

class setData:
    def __init__(self, stock, inWeek, inDay, tightWeek, tightDay, buyMe, weight):
        self.stock = stock
        self.inWeek = inWeek
        self.inDay = inDay
        self.tightWeek = tightWeek
        self.tightDay = tightDay
        self.buyMe = buyMe
        self.weight = weight    
        
    def pickled_items(filename):
        """ Unpickle a file of pickled data. """
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    
