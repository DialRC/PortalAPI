'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

class EntityUnit:
    def __init__(self):
        type = ""
        entity = ""
        score = 0.0

class Act:
    def __init__(self):
        intent = ""
        score = 0.0

class Events:
    def __init__(self):
        self.label = 0
        self.fval = 0.0
        self.obs = []

class ObsParam:
    def __init__(self):
        self.y = 0
        self.fid = 0
        self.fval = 0.0

class StateParam:
    def __init__(self):
        self.y1, self.y2, self.fid =0,0,0
        self.fval =0.0

class UserInput:
    def __init__(self):
        self.query = ""
        self.dialog_act = Act()
        self.agent =""
        self.domain=""
        self.entities = []
        self.intents = []
        self.dialog_act.intent =  ""
        self.dialog_act.score =  0.0
        self.query = ""

class Entities:
    def __init__(self):
        name =""
        entity = ""
        score = 0.0
        start = 0.0
        end =0.0
        isFilled = 0
