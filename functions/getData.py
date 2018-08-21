# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 17:27:14 2018

@author: bsantos
"""

import urllib.request
import json
import time


class getJson:
    def __init__(self):
        return
    def fetchIt(self,url):
        u = urllib.request.urlopen(url)
        content = u.read().decode('utf-8')
        data = json.loads(content)
        time.sleep(0.1)
        return data