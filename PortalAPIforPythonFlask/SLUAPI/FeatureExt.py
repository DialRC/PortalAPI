'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

import sys

ENTITY_INSIDE = 1
ENTITY_OUT  = 2
m_vecEntityClass = ["loc"]

def feature4SlotTrain(entity_sent):
    feature  = []
    entity_list = []
    tokens = []
    sep = ""
    flag = ENTITY_OUT
    words = []
    current_class = "none"
    raw_sent = entity_sent
    target  = ""
    replaced_symbol = "@"
    entity_list = ExtractEntityClassFromUtter(entity_sent)
    for x in m_vecEntityClass:
        target = "<"+x+">"
        entity_sent = entity_sent.replace(target,replaced_symbol)
        raw_sent = raw_sent.replace(target,"")

        target = "</"+x+">"
        entity_sent = entity_sent.replace(target,replaced_symbol)
        raw_sent = raw_sent.replace(target,"")
    #raw_sent =
    #entity_sent =
    tokens = entity_sent.strip().split(" ")
    raw_sent = raw_sent.replace("  "," ")
    words = raw_sent.strip().split(" ")
    num_slot = 0
    #print words
    for i in range(len(words)):
        #print words[i]
        vec  = []
        if tokens[i] == replaced_symbol and flag == ENTITY_OUT:
            current_class = entity_list[num_slot]+"-b"
            tokens.pop(i)
            if tokens[i+1] == replaced_symbol:
                tokens.pop(i+1)
                flag = ENTITY_OUT
                num_slot+=1
            else:
                flag = ENTITY_INSIDE
            vec.append(current_class)

        elif tokens[i] == replaced_symbol and not flag == ENTITY_OUT:
            if tokens[i] == replaced_symbol:
                tokens.pop(i)
                if tokens[i] == replaced_symbol:
                    i-= 1
                    num_slot+=1
                    flag = ENTITY_OUT
                    continue
                else:
                    current_class = "none"
                    num_slot +=1
                    vec.append(current_class)
        elif flag == ENTITY_INSIDE:
            #print entity_list
            #print num_slot
            current_class = entity_list[num_slot]+"-i"
            vec.append(current_class)
        else:
            current_class = "none"
            vec.append(current_class)
        vec.append("word="+words[i])
        if i >0:
            vec.append("word-1="+words[i-1])
            vec.append("prev-word="+words[i-1])
            vec.append("bigram="+words[i-1]+","+words[i])
            if i > 1:
                vec.append("word-2=" + words[i - 2])	#< previous-2 word
                vec.append("prev-word=" + words[i - 2])	#
                vec.append("tigram=" + words[i - 2] + "," + words[i - 1] + "," + words[i])	#< trigram
                vec.append("d2bigram=" + words[i - 2] + "," + words[i])	#< d2bigram
                if  i > 2:
                    vec.append("prev-word=" + words[i - 3])	#
            else:
                vec.append("word-2=<s>")	#< previous-2 word
                vec.append("tigram=<s>," + words[i - 1] + "," + words[i])	#< trigram
                vec.append("d2bigram=<s>," + words[i])	#< d2bigram

        else:
            vec.append("word-1=<s>")	#< previous word
            vec.append("bigram=<s>," + words[i])	#< bigram

            # right context
        if i < len(words) - 1:
            vec.append("word+1=" + words[i + 1])	#< previous word
            vec.append("post-word=" + words[i + 1])	#
            vec.append("+bigram=" + words[i] + "," + words[i + 1])	#< bigram
            if i < len(words) - 2:
                vec.append("word+2=" + words[i + 2])	#< previous-2 word
                vec.append("post-word=" + words[i + 2])	#
                vec.append("+tigram=" + words[i] + "," + words[i + 1] + "," + words[i + 2])	#< trigram
                vec.append("+d2bigram=" + words[i] + "," + words[i + 2])	#< d2bigram
                if i < len(words) - 3:
                    vec.append("post-word=" + words[i + 3])	#
            else:
                vec.append("word+2=</s>")	#< previous-2 word
                vec.append("+tigram=" + words[i] + "," + words[i + 1] + ",</s>")	#< trigram
                vec.append("+d2bigram=" + words[i] + ",</s>")	#< d2bigram
        else:
            vec.append("word+1=</s>")	#< previous word
            vec.append("+bigram=" + words[i] + ",</s>")	#< bigram
        feature.append(vec)	#< appending feature
    return feature

def ExtractEntityClassFromUtter(utterance):
    #print utterance
    flag = 0
    entity_class = ""
    entity_class_list =[]
    so = 0
    eo = 0
    for i in range(len(utterance)):
        if utterance[i] == '<' and flag == 0:
            flag = 1
            so = i
        elif utterance[i] == ">" and flag == 1:
            eo = i
        elif utterance[i] == '<' and flag == 1:
            flag = 0
            #print so+1, eo-so-1
            #print utterance
            entity_class = utterance[so+1: so+1+eo-so-1].strip()
            entity_class_list.append(entity_class)
    #print entity_class_list
    return entity_class_list

def feature4Slot(sent):
    feature = []
    words = sent.split(" ")
    for i in range(len(words)):
        vec = []
        vec.append("o")
        vec.append("word="+words[i])
        if i >0:
            vec.append("word-1="+words[i-1])
            vec.append("prev-word="+words[i-1])
            vec.append("bigram="+words[i-1]+","+words[i])        
            if i > 1:                
                vec.append("word-2=" + words[i - 2])	#< previous-2 word
                vec.append("prev-word=" + words[i - 2])	#
                vec.append("tigram=" + words[i - 2] + "," + words[i - 1] + "," + words[i])	#< trigram
                vec.append("d2bigram=" + words[i - 2] + "," + words[i])	#< d2bigram
                if  i > 2:
                    vec.append("prev-word=" + words[i - 3])	#
            else:
                vec.append("word-2=<s>")	#< previous-2 word
                vec.append("tigram=<s>," + words[i - 1] + "," + words[i])	#< trigram
                vec.append("d2bigram=<s>," + words[i])	#< d2bigram

        else:
            vec.append("word-1=<s>")	#< previous word
            vec.append("bigram=<s>," + words[i])	#< bigram

            # right context
        if i < len(words) - 1:
            vec.append("word+1=" + words[i + 1])	#< previous word
            vec.append("post-word=" + words[i + 1])	#
            vec.append("+bigram=" + words[i] + "," + words[i + 1])	#< bigram
            if i < len(words) - 2:
                vec.append("word+2=" + words[i + 2])	#< previous-2 word
                vec.append("post-word=" + words[i + 2])	#
                vec.append("+tigram=" + words[i] + "," + words[i + 1] + "," + words[i + 2])	#< trigram
                vec.append("+d2bigram=" + words[i] + "," + words[i + 2])	#< d2bigram
                if i < len(words) - 3:
                    vec.append("post-word=" + words[i + 3])	#
            else:
                vec.append("word+2=</s>")	#< previous-2 word
                vec.append("+tigram=" + words[i] + "," + words[i + 1] + ",</s>")	#< trigram
                vec.append("+d2bigram=" + words[i] + ",</s>")	#< d2bigram
        else:
            vec.append("word+1=</s>")	#< previous word
            vec.append("+bigram=" + words[i] + ",</s>")	#< bigram
        feature.append(vec)	#< appending feature
    return feature

def GetFeature():
    f = open("C:\\Users\\kyusongl\\Desktop\\DialolgSystem\\DSTC1\\DSTC1\\main\\letsgo\\corpus.ner.train.useronly2")
    fw = open("corpus.ner.feature.train.useronly","w")
    lines = f.readlines()
    for sent in lines:
        try:
            data = feature4SlotTrain(sent)

            for x in data:
                fw.write( " ".join(x)+"\n")
            fw.write("\n")
        except:
            pass


GetFeature()