'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

from Parameter import *
from CRF import *
from DataStruct import *
class MaxEnt:
    def __init__(self):
        self.m_param = Parameter()

    def packEvent(self, tokens, p_Param, test):
        ev = Events()
        fval = 1.0
        fstr = ""
        i = 0
        for iter in tokens:
            if i == 0 :
                tok = iter.split(' ')
                if len(tok) > 1:
                    fval = float(tok[1])
                    fstr = tok[0]

                oid = p_Param.findState(iter)
                if oid >= 0:
                     ev.label = p_Param.findState(fstr)
                else:
                    ev.label = p_Param.sizeStateVec()
                ev.fval = fval
                i+=1
            else:
                tok = iter.split(':')
                fstr = iter
                fval = 1.0
                if len(tok) > 1:
                    fval = float(tok[1])
                    fstr = tok[0]
                pid= p_Param.findObs(fstr)
                if pid >= 0:
                    temp = (pid, fval)
                    ev.obs.append(temp)
        return ev