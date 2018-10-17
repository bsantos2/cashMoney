# -*- coding: utf-8 -*-"
"""
Created on Sat Jun 23 15:45:17 2018

@author: bsantos
"""

import requests

class groupMeBot:
    def __init__(self):
        self.groupMeChatToken = 'VfRA31Cw3ixUTmFIQlM62o7EJByNeX4Ksro1wrs0'
        self.groupMeBotID = "18753f9360664c481631d24607"
        self.groupMeAddr = 'https://api.groupme.com/v3/groups/41642170/messages'
    
    def botPost(self, message):
        request_params = { 'token': self.groupMeChatToken }
        params = {
                    "bot_id"  : self.groupMeBotID,
                    "text"    : message
                 }
        response = requests.get(self.groupMeAddr, params = request_params)
        requests.post('https://api.groupme.com/v3/bots/post', params = params)
        return response