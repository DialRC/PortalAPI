# SLU API

#Example
```python
from SLU import *

class RunSLU:
    def __init__(self):
        self.mslu = SLU()
        self.mslu.loadModel("model.useronly") #filename should be "model.useronly.model.slot"

    def GetSlots(self, inputs):
        input = UserInput()
        input.query = inputs
        self.mslu.extractSlot(input)
        return input.entities

if __name__ =="__main__":
    hSLU = RunSLU()
    entities  = hSLU.GetSlots("from cmu to market")
    for val in entities:
        print val.entity
        print val.score
```
