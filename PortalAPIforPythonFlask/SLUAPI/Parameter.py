'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

import CRF
class Parameter:
    def __init__(self):
        self.n_weight = 0
        self.m_Count = []
        self.m_weight = []
        self.m_Gradient = []
        self.m_StateIndex = []
        self.m_ParamIndex = []
        self.m_StateVec = []
        self.m_FeatureVec = []
        self.m_StateMap = {}
        self.m_FeatureMap = {}
        self.mEDGE = "@"

    def load(self, filename):
        strLIne = ""
        count = 0
        srFile = open(filename)
        strLIne = srFile.readline()
        strLIne = srFile.readline()
        strLIne = srFile.readline()
        strLIne = srFile.readline()
        strLIne = srFile.readline()

        strLIne = srFile.readline()
        word = strLIne.split(' ')
        count = int(word[3])
        for i in range(count):
            strLIne = srFile.readline()
            self.m_StateMap[strLIne.strip()] = i
            self.m_StateVec.append(strLIne.strip())

        strLIne = srFile.readline()
        word = strLIne.split(' ')
        count = int(word[3])
        for i in range(count):
            strLIne = srFile.readline()
            self.m_FeatureMap[strLIne.strip()] = i
            self.m_FeatureVec.append(strLIne.strip())
        strLIne = srFile.readline()
        word = strLIne.split(' ')
        count = int(word[3])

        fid = 0

        for i in range(count):
            param = []
            strLIne = srFile.readline()
            word = strLIne.split(' ')
            for j in range(1, len(word)-1):
                param.append((int(word[j]),fid))
                fid+=1
            self.m_ParamIndex.append(param)

        strLIne = srFile.readline()
        self.n_weight = fid
        for i in range(fid):
            strLIne = srFile.readline()
            self.m_weight.append(float(strLIne))

        for i in range(self.n_weight):
            self.m_Count.append(0.0)
        return True

    def findState(self, key):
        oid = -1
        if key in self.m_StateMap:
            oid = self.m_StateMap
        return oid

    def findObs(self, key):
        pid = -1
        if key in self.m_FeatureMap:
            pid = self.m_FeatureMap[key]
        return pid

    def sizeStateVec(self):
        return len(self.m_StateVec)

    def getState(self):
        return self.m_StateMap, self.m_StateVec

    def getWeight(self):
        return self.m_weight

    def makeObsIndex1(self, obs):
        obs_param = []
        for iter in obs:
            param = self.m_ParamIndex[iter[0]]
            for p in param:
                element = CRF.ObsParam()
                element.y = p[0]
                element.fid = p[1]
                element.fval= iter[1]
                obs_param.append(element)

        return obs_param

    def makeObsIndex2(self, obs):
        obs_param = []
        pid = 0
        for iter in obs:
            pid = self.findObs(iter.intent)
            if pid >= 0:
                param = self.m_ParamIndex[pid]
                for p in param:
                    element = CRF.ObsParam()
                    element.y = p[0]
                    element.fid = p[1]
                    element.fval = iter.score
                    obs_param.append(element)
        return obs_param

    def makeStateIndex1(self):
        # Make state index
        self.m_StateIndex = []
        for y1 in range(self.sizeStateVec()):
            fi = self.mEDGE + self.m_StateVec[y1]
            if fi in self.m_FeatureMap:
                pid = self.m_FeatureMap[fi]
                param = self.m_ParamIndex[pid]
                for i in range(len(param)):
                    element = CRF.StateParam()
                    element.y1 = y1
                    element.y2 = param[i][0]
                    element.fid = param[i][1]
                    element.fval = 1.0
                    self.m_StateIndex.append(element)

    def makeStateIndex2(self,y1):
        state_param = []
        fi = self.mEDGE+self.m_StateVec[y1]
        if fi in self.m_FeatureMap:
            pid = self.m_FeatureMap[fi]
            param = self.m_ParamIndex[pid]
            for i in range(len(param)):
                element = CRF.StateParam()
                element.y1 = y1
                element.y2 = param[i][0]
                element.fid = param[i][1]
                element.fval = 1.0
                self.m_StateIndex.append(element)