'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 09/21/2017
    Date last modified: 09/21/201
    Description: An Example code for DialPort Connection
    Python Version: 2.7
'''

from SLUAPI.RunSLU import *
hslu = RunSLU()

class API(object):
    def __init__(self):
        self.history = []
    
    def GetResponse(self,text):
        slu = hslu.GetSLU(text) #{"act":dialog_act,"slot":named_entity} 
        sysUtter = "sysUtter" 
        imageurl = "imageurl"
        return {"slu":slu,"sys":sysUtter,"imageurl":imageurl} 
