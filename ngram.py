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
