# -*- coding: utf-8 -*-

class trainTag:
    trainSents = []         # sentences array
    sentsNum = 0            # sentences num
    wordNum = 0             # words num
    wordPosFreq = {}        # wordPosFreq[word] = {pos1:fre1,pos2:fre2}
    posFreq = {}            # posFreq[pos] = fre
    posTransFreq = {}       # posTransFreq[pos] = {pos1:frq1,pos2:frq2}
    posTransPro = {}        # posTransPro[pos] = {pos1:pro1,pos2:pro2}
    wordPosHeadFreq = {}    # wordPosHeadFreq[word] = {pos1:fre1,pos2:fre2}
    wordPosHeadPro = {}     # wordPosHeadPro[word] = {pos1:pro1,pos2:pro2}

    def __init__(self, sents):
        self.trainSents = sents
        self.sentsNum = len(sents)

    def train(self):
        print 'training:'
        for sent in self.trainSents:
            prePos = ''
            currPos = ''

            index = -1
            pairList = sent.split('  ')# list of word/pos
            for pair in pairList:
                self.wordNum += 1
                index += 1

                word = pair.split('/')[0]# word
                pos = pair.split('/')[1]# pos

                # calculate the pos frequency
                if self.posFreq.has_key(pos):
                    self.posFreq[pos] += 1
                else:
                    self.posFreq[pos] = 1

                # calculate the pos frequency for a specific word
                if self.wordPosFreq.has_key(word):
                    # get the post list for a word
                    posList = self.wordPosFreq[word].keys()
                    if pos in posList:
                        self.wordPosFreq[word][pos] += 1
                    else:
                        self.wordPosFreq[word][pos] = 1
                else:
                    # creat the word dict at the first time occurance
                    self.wordPosFreq[word] = {}
                    self.wordPosFreq[word][pos] = 1

                # calculate the transition frequency
                if index == 0:
                    currPos = pos
                    if self.wordPosHeadFreq.has_key(word):
                        posList = self.wordPosHeadFreq[word].keys()
                        if pos in posList:
                            self.wordPosHeadFreq[word][pos] += 1
                        else:
                            self.wordPosHeadFreq[word][pos] = 1
                    else:
                        self.wordPosHeadFreq[word] = {}
                        self.wordPosHeadFreq[word][pos] = 1
                else:
                    prePos = currPos
                    currPos = pos
                    if self.posTransFreq.has_key(prePos):
                        toPosList = self.posTransFreq[prePos].keys()
                        if currPos in toPosList:
                            self.posTransFreq[prePos][currPos] += 1
                        else:
                            self.posTransFreq[prePos][currPos] = 1
                    else:
                        self.posTransFreq[prePos] = {}
                        self.posTransFreq[prePos][currPos] = 1

        # calculate the pos transition probability
        for fromPos in self.posTransFreq.keys():
            posTransDic = self.posTransFreq[fromPos]
            posSum = sum(posTransDic.values())
            self.posTransPro[fromPos] = {}
            for toPos in posTransDic.keys():
                self.posTransPro[fromPos][toPos] = 1.0 * posTransDic[toPos] / posSum

        # calculate the pos probability for the first word of the sentence
        for word in self.wordPosHeadFreq.keys():
            posHeadDic = self.wordPosHeadFreq[word]
            posSum = sum(posHeadDic.values())
            self.wordPosHeadPro[word] = {}
            for pos in posHeadDic.keys():
                self.wordPosHeadPro[word][pos] = 1.0 * posHeadDic[pos] / posSum
