'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

from CRF import *
from DataStruct import *
from operator import itemgetter
from collections import OrderedDict

class SLU:
    def __init__(self):
        self.act = CRF()
        self.goal = CRF()
        self.slot = CRF()
        self.m_act = []
        self.m_slot = []
        self.m_isCRF = True

    def loadModel(self, file):
        self.slot.loadModel(file + ".model.slot")
        self.act.loadModel(file + ".model.act")

    def classifyActNbest(self, feature):
        return self.act.eval2me(feature)

    def feature4Slot(self, sent):
        feature = []
        words = sent.split(' ')

        for i in range(len(words)):
            vec = []
            vec.append("o")
            # current singleton feature
            vec.append("word=" + words[i])	#/< current word

            # left context
            if i > 0:            
                vec.append("word-1=" + words[i - 1])	#/< previous word
                vec.append("prev-word=" + words[i - 1])	#/
                vec.append("bigram=" + words[i - 1] + "," + words[i])	#/< bigram
                if i > 1:
                
                    vec.append("word-2=" + words[i - 2])	#/< previous-2 word
                    vec.append("prev-word=" + words[i - 2])	#/
                    vec.append("tigram=" + words[i - 2] + "," + words[i - 1] + "," + words[i])	#/< trigram
                    vec.append("d2bigram=" + words[i - 2] + "," + words[i])	#/< d2bigram
                    if i > 2:
                        vec.append("prev-word=" + words[i - 3])	#/
                else:
                    vec.append("word-2=<s>")	#/< previous-2 word
                    vec.append("tigram=<s>," + words[i - 1] + "," + words[i])	#/< trigram
                    vec.append("d2bigram=<s>," + words[i])	#/< d2bigram

            else:
                vec.append("word-1=<s>")	#/< previous word
                vec.append("bigram=<s>," + words[i])	#/< bigram
            

            # right context
            if i < len(words)- 1:
                vec.append("word+1=" + words[i + 1])	#/< previous word
                vec.append("post-word=" + words[i + 1])	#/
                vec.append("+bigram=" + words[i] + "," + words[i + 1])	#/< bigram
                if i < len(words) - 2:
                    vec.append("word+2=" + words[i + 2])	#/< previous-2 word
                    vec.append("post-word=" + words[i + 2])	#/
                    vec.append("+tigram=" + words[i] + "," + words[i + 1] + "," + words[i + 2])	#/< trigram
                    vec.append("+d2bigram=" + words[i] + "," + words[i + 2])	#/< d2bigram
                    if i < len(words) - 3:
                        vec.append("post-word=" + words[i + 3])	#/
                else:
                    vec.append("word+2=</s>")	#/< previous-2 word
                    vec.append("+tigram=" + words[i] + "," + words[i + 1] + ",</s>")	#/< trigram
                    vec.append("+d2bigram=" + words[i] + ",</s>")	#/< d2bigram
            else:
                vec.append("word+1=</s>")	#/< previous word
                vec.append("+bigram=" + words[i] + ",</s>")	#/< bigram
            feature.append(vec)	#/< appending feature
        return feature

    def feature4Class(self, sent):
        sent = sent.replace(".","")
        sent = sent.replace("?","")
        sent = sent.replace("!","").lower()
        feature =[]
        vec = []
        vec.append("o")
        for x in sent.split(" "):
            vec.append(x)
        feature.append(vec)
        return feature

    def extract(self, user_input):
        class_input = user_input.query
        feature = self.feature4Class(class_input)
        m_act = self.classifyActNbest(feature)
        result = {}
        for act in m_act:
            result[act.intent] = float(act.score)
        sorted_x = OrderedDict(sorted(result.items(), key=itemgetter(1), reverse=True))
        return sorted_x

        
    def extractSlot(self, user_input):
        frame = []
        class_feature = []
        slot_feature = []
        time = []
        class_input = ""
        slot_input = ""
        sent = ""

        class_input = user_input.query
        slot_input = user_input.query

        token = slot_input.split(' ')

        for i in range(len(token)):
            tok = token[i].split('/')
            if len(tok) > 0:
                sent += tok[0] + " "
                if len(tok) > 1:
                    time.append(float(str(tok[1])))
                else:
                    time.append(-1.0)

        sent = sent.strip()
        slot_feature = self.feature4Slot(sent.strip())

        slot_frame = []
        slot_frame = self.extractSlots(sent, slot_feature, time)

        for i in range(len(slot_frame)):
            frame.append(slot_frame[i])
        class_input = user_input.query
        slot = Entities()
        user_input.entities = []

        for i in range(len(frame)):
            named_entity = EntityUnit()
            named_entity.type = frame[i].name
            named_entity.entity = frame[i].entity
            named_entity.score = frame[i].score
            user_input.entities.append(named_entity)

    def extractSlots(self, sent, feature, time):
        frame = []	# semantic frame
        label = []

        word = sent.split(' ')

        label = self.slot.eval2(feature, label)	# sequential labeling
        slot_name = ""
        slot_value = ""
        
        slot_start = 0.0 
        slot_end = 0.0
        prob = 0.0
        isInside = False
        for i in range(len(word)):    
            str = label[i].intent.split('-')
            if len(str) < 2:
                if slot_name != "" and slot_value != "":
                    entities = Entities()
                    entities.name = slot_name 
                    entities.entity = slot_value 
                    entities.score = prob
                    entities.start = slot_start 
                    entities.end = slot_end
                    frame.append(entities)
                
                slot_name = ""
                slot_value = ""
                prob = label[i].score
                isInside = False
            
            elif str[1] == "b" or str[1] == "B":
                if slot_name != "" and slot_value != "":
                    entities = Entities()
                    entities.name = slot_name
                    entities.entity = slot_value
                    entities.score = prob
                    entities.start = slot_start
                    entities.end = slot_end
                    frame.append(entities)
                    #frame.push_back(make_pair(slot_name, slot_value))
                
                slot_name = str[0]
                slot_value = word[i]
                prob = label[i].score
                if i > 0:
                    slot_start = time[i - 1] + 1
                else:
                    slot_start = 0
                slot_end = time[i]
                isInside = True
            
            elif isInside:
             # if inside
                if slot_name != str[0]:
                
                    if slot_name != "" and slot_value != "":
                        entities = Entities()
                        entities.name = slot_name
                        entities.entity = slot_value
                        entities.score = prob
                        entities.start = slot_start
                        entities.end = slot_end
                        frame.append(entities)
                        #frame.push_back(make_pair(slot_name, slot_value))
                    
                    slot_name = str[0]
                    slot_value = word[i]
                    prob = label[i].score
                    if i > 0:
                        slot_start = time[i - 1] + 1
                    else:
                        slot_start = 0
                    slot_end = time[i]
                
                else:
                
                    slot_value += " " + word[i]
                    prob *= label[i].score
                    slot_end = time[i]
                
            
            else:
                if slot_name != "" and slot_value != "":
                    entities = Entities()
                    entities.name = slot_name
                    entities.entity = slot_value
                    entities.score = prob
                    entities.start = slot_start
                    entities.end = slot_end
                    frame.append(entities)
                    #frame.push_back(make_pair(slot_name, slot_value))
                
                slot_name = str[0]
                slot_value = word[i]
                prob = label[i].score
                if i > 0:
                    slot_start = time[i - 1] + 1
                else:
                    slot_start = 0
                slot_end = time[i]
                isInside = True

        if slot_name != "" and slot_value != "":
            entities = Entities()
            entities.name = slot_name
            entities.entity = slot_value
            entities.score = prob
            entities.start = slot_start
            entities.end = slot_end
            frame.append(entities)

        return frame
