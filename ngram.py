from numpy import log10, argsort, array


class nGram:
    def __init__(self, n, tagSet, ngList, delta=0.001):
        '''
        Constructor for nGram class
        n: number of grams
        tagSet: all the tags
        ngList: a list of ngram prototype
        delta: smoothing factor, default 0.001
        '''
        self.n = n
        self.tagSet = tagSet
        self.delta = delta
        self.ngList = ngList

    def remap(self, key):
        '''
        Remap function
        key: input

        Return a string

        Please inherit this class and implement this function yourself
        '''
        raise NotImplemented("Please inherit this class and implement this " +
                             "function by yourself")

    def segment(self, inStr):
        '''
        Segmentation function
        inStr: input string

        Return a list of string

        Please inherit this class and implement this function yourself
        '''
        raise NotImplemented("Please inherit this class and implement this " +
                             "function by yourself")

    def toDict(self):
        '''
        Convert ngram prototype list to dictionary.
        Remapping is done in this step.
        '''
        self.model = {}
        for each in self.ngList:
            # Segment and remap
            tmpOri = self.segment(each)
            if len(tmpOri) != self.n:
                raise ValueError("Inconsistent number of grams")
            tmp = []
            for eachGram in tmpOri:
                tmp.append(self.remap(eachGram))
            # Split into ngram dictionary
            n11Gram = ''.join(tmp[:-1])
            if not (n11Gram in self.model):
                self.model[n11Gram] = {}
            if not (tmp[-1] in self.model[n11Gram]):
                self.model[n11Gram][tmp[-1]] = 1
            else:
                self.model[n11Gram][tmp[-1]] = self.model[n11Gram][tmp[-1]] + 1

    def normalization(self):
        '''
        Normalization and add-delta smoothing
        '''
        for each in self.model:
            denom = self.delta * float(len(self.tagSet)) + \
                float(sum(self.model[each].values()))
            for each11 in self.model[each]:
                self.model[each][each11] = (self.delta + float(
                    self.model[each][each11])) / denom
            self.model[each]['UKN'] = self.delta / denom

    def predict(self, n11Gram, lastGram):
        '''
        Get the predicted probability
        '''
        if not (n11Gram in self.model):
            return 1.0 / float(len(self.tagSet))
        elif not (lastGram in self.model[n11Gram]):
            return self.model[n11Gram]['UKN']
        else:
            return self.model[n11Gram][lastGram]

    def perplexity(self, ngList):
        pp = 0.0
        for each in ngList:
            tmpOri = self.segment(each)
            tmp = []
            for each in tmpOri:
                tmp.append(self.remap(each))
            n11Gram = ''.join(tmp[:-1])
            pp -= log10(self.predict(n11Gram, tmp[-1]))
        return 10.0 ** (pp / len(ngList))

    def rank(self):
        prob = []
        ngram = []
        for each11 in self.model:
            for each in self.model[each11]:
                ngram.append(each11 + each)
                prob.append(self.model[each11][each])
        rankArg = argsort(array(prob))
        self.rankNgram = [ngram[i] for i in rankArg]
        self.rankProb = [prob[i] for i in rankArg]
