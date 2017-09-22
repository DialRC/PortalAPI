'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 02/16/2017
    Date last modified: 02/16/201
    Python Version: 2.7
'''

from MaxEnt import *
from operator import itemgetter, attrgetter
import math
from DataStruct import *

class CRF(MaxEnt):
    def __init__(self):
        MaxEnt.__init__(self)
        self.m_M = []
        self.m_R = []
        self.m_Alpha = []
        self.m_Beta = []
        self.m_state_size = 0
        self.m_seq_size = 0
        self.m_default_oid = 0

    def __MAT2(self,I,X):
        return (self.m_state_size*I)+X

    def __MAT3(self,I,X, Y):
        return ((self.m_state_size * self.m_state_size * (I)) + (self.m_state_size * (X)) + Y)

    def loadModel(self, filename):
        ret = self.m_param.load(filename)
        self.m_param.makeStateIndex1()
        self.m_state_size = self.m_param.sizeStateVec()
        return ret

    def forward(self):
        self.m_Alpha = []
        for i in range(self.m_seq_size * self.m_state_size):
            self.m_Alpha.append(0.0)

        for j in range(self.m_state_size):
            self.m_Alpha[self.__MAT2(0, j)] += self.m_R[self.__MAT2(0, j)] * self.m_M[self.__MAT3(0, self.m_default_oid, j)]

        for i in range(1,self.m_seq_size): # time line : t
            for j in range(self.m_state_size):      # y(t)
                for k in range(self.m_state_size): # y(t-1)
                    self.m_Alpha[self.__MAT2(i, j)] += self.m_Alpha[self.__MAT2(i - 1, k)] * self.m_R[self.__MAT2(i, j)] * self.m_M[self.__MAT3(i, k, j)];

    def backward(self):
        self.m_Beta = []
        for i in range(self.m_seq_size * self.m_state_size):
            self.m_Beta.append(0.0)

        self.m_Beta[self.__MAT2(self.m_seq_size - 1, self.m_default_oid)] = 1.0

        for i in range(self.m_seq_size-1,0, -1): # (int i = m_seq_size - 1; i >= 1; i--)
            for j in range(self.m_state_size):
                for k in range(self.m_state_size):
                    self.m_Beta[self.__MAT2(i - 1, j)] += self.m_R[self.__MAT2(i, k)] * self.m_M[self.__MAT3(i, j, k)] * self.m_Beta[self.__MAT2(i, k)];

    def getPartitionZ(self):
        return self.m_Alpha[self.__MAT2(self.m_seq_size - 1, self.m_default_oid)]

    def viterbiSearch(self, prob):
        psi = []
        delta = []
        for i in range(self.m_seq_size):
            psi_i = []
            delta_i = []
            for j in range(self.m_state_size):
                max = -10000.0
                max_k = 0
                if i == 0:
                    max = self.m_R[self.__MAT2(i, j)] * self.m_M[self.__MAT3(i, self.m_default_oid, j)]
                    max_k = self.m_default_oid
                else:
                    p = self.m_R[self.__MAT2(i, j)]
                    for k in range(self.m_state_size):
                        val = delta[i - 1][k] * self.m_M[self.__MAT3(i, k, j)] * p
                        if val > max:
                            max = val
                            max_k = k
                delta_i.append(max)
                psi_i.append(max_k)
            delta.append(delta_i)
            psi.append(psi_i)

            # Back-tracking
        y_seq = []
        prev_y = self.m_default_oid
        for i in range(self.m_seq_size - 1, 0, -1):
            y = psi[i][prev_y]
            y_seq.append(y)
            prev_y = y
        y_seq.reverse()
        prob = delta[self.m_seq_size - 1][self.m_default_oid]
        return y_seq

    def viterbi4me(self, prob):
        y_seq = []
        j = 0
        prob = 1.0
        for i in range(1):
            outList = []
            for j in range(self.m_state_size):
                outList.append((self.m_R[self.__MAT2(i, j)], j))
            #outList.Sort(new cTmpComparer());
            sorted(outList, key=itemgetter(0))
            for j in range(self.m_state_size):
                y_seq.append(outList[j][1])
            prob *= outList[0][0]
        return y_seq

    def eval2me(self, event_line, result):
        result = []
        seq = []

        state_vec = []
        state_vec = self.m_param.getState()[1]

        for t in range(len(event_line)):
            ev = self.packEvent(event_line[t], self.m_param, True)
            seq.append(ev)

        self.calculateFactors(seq)
        self.forward()
        self.backward()
        zval = self.getPartitionZ()
        dummy_prob =0.0
        y_seq = self.viterbi4me(dummy_prob)
        i = 0
        for s in seq:
            item = Act()
            item.intent = state_vec[y_seq[i]]
            item.score = self.m_Alpha[self.__MAT2(0, y_seq[i])] * self.m_Beta[self.__MAT2(0, y_seq[i])] / zval
            result.append(item)
            i = i + 1
        return result


    def eval2(self, event_line, result):
        result = []
        seq = []

        state_vec = []
        state_vec = self.m_param.getState()[1]

        for t in range(len(event_line)):
            ev = self.packEvent(event_line[t], self.m_param, True)
            seq.append(ev)

        self.calculateFactors(seq)
        self.forward()
        self.backward()
        zval = self.getPartitionZ()
        dummy_prob =0.0
        y_seq = self.viterbiSearch(dummy_prob)
        i = 0
        for s in seq:
            item = Act()
            item.intent = state_vec[y_seq[i]]
            item.score = self.m_Alpha[self.__MAT2(i, y_seq[i])] * self.m_Beta[self.__MAT2(i, y_seq[i])] / zval
            result.append(item)
            i = i + 1
        return result

    def eval2me(self, event_line):
        result = []

        seq = []
        state_vec = []
        state_vec = self.m_param.getState()[1]
        for t in range(len(event_line)):
            ev = self.packEvent(event_line[t], self.m_param, True) # < observation features
            seq.append(ev)

        self.calculateFactors(seq)
        self.forward()
        self.backward()

        zval = self.getPartitionZ()
        dummy_prob =0.0

        y_seq = self.viterbi4me(dummy_prob)

        for i in range(len(y_seq)):
            item = Act()
            item.intent = state_vec[y_seq[i]]
            item.score = self.m_Alpha[self.__MAT2(0, y_seq[i])] * self.m_Beta[self.__MAT2(0, y_seq[i])] / zval
            result.append(item)
        return result

    def calculateFactors(self, seq):
        # Initialization
        self.m_seq_size = len(seq) + 1	#< sequence length

        theta = self.m_param.getWeight()

        # Factor matrix initialization
        self.m_M = []
        self.m_R = []

        for i in range(self.m_seq_size * self.m_state_size):
            self.m_R.append(1.0)

        for i in range(self.m_seq_size * self.m_state_size * self.m_state_size):
            self.m_M.append(1.0)

        for i in range(self.m_seq_size-1):
            obs_param = self.m_param.makeObsIndex1(seq[i].obs)

            for iter in obs_param:
                self.m_R[self.__MAT2(i, iter.y)] *= math.exp(theta[iter.fid] * iter.fval)

            if i > 0:
                for iter in self.m_param.m_StateIndex:
                    self.m_M[self.__MAT3(i, iter.y1, iter.y2)] *= math.exp(theta[iter.fid] * iter.fval)
