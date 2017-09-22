'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

from SLU import *
#from Spotlight import *

class RunSLU:
    def __init__(self):
        self.mslu = SLU()
        self.mslu.loadModel("./SLUAPI/test") #filename should be "model.useronly.model.slot"

    def GetSlots(self, inputs):
        input = UserInput()
        input.query = inputs
        self.mslu.extractSlot(input)
        acts = self.mslu.extract(input)
        return input.entities, acts
    
    def GetSLU(self, inputs):
        input = UserInput()
        input.query = inputs
        self.mslu.extractSlot(input)
        acts = self.mslu.extract(input)
        value = ""
        if len(input.entities) > 0:
            if  input.entities[0].score > 0.9:
                value = input.entities[0].entity
        return {"act": list(acts)[0],"slot":value}

if __name__ =="__main__":
    hSLU = RunSLU()
    print hSLU.GetSLU("tell me game news")
    #entities,acts  = hSLU.GetSlots("tell me business news")
    #for val in entities:
    #    print val.type, val.entity, val.score

