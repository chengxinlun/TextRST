import glob
import pickle
import re
import os
import matplotlib.pyplot as plt
from hmInterface import loadDiscTree
from ngram import nGram


class nGramRST(nGram):
    def __init__(self, n, tagSet, ngList, delta=0.001):
        super().__init__(n, tagSet, ngList, delta)
        # All kinds of remapping dictionaries
        self.renameDict = {}
        self.combineDict = dict.fromkeys(['Cause', 'Result'], 'Cr')
        self.combineDict.update(dict.fromkeys(['Condition', 'Temporal',
                                               'Location'], 'Ctl'))
        self.combineDict.update(dict.fromkeys(['Attribution',
                                               'Text-preparation'], 'Atp'))
        self.combineDict.update(dict.fromkeys(['Comparison', 'Contrast'], 'Cc'))
        self.combineDict.update(dict.fromkeys(['Sequence', 'Joint'], 'Sj'))
        self.combineDict.update(dict.fromkeys(['Enablement', 'Purpose'], 'Ep'))

    def remap(self, key):
        if key in self.renameDict:                      # Simple renaming
            return self.renameDict[key]
        elif key in self.combineDict:                   # Simple combining
            return self.combineDict[key]
        elif not(re.match(r'Arg-.+', key) is None):     # Arg-.+
            return 'Argument'
        elif not(re.match(r'Elab-.+', key) is None):    # Elab-.+
            if key.endswith('aspect'):
                return 'Elab-aspect'
            else:
                return 'Elab-other'
        else:                                           # Does not need remap
            return key

    def segment(self, inStr):
        return re.findall(r'[A-Z#*][^A-Z#*]*', inStr)


def getNGProto(depFile, n=3):
    g = loadDiscTree(depFile)
    g.parse(doPlot=False, show=False)
    return g.ngram(n)


def cvNG(tagSet, depTrain, depTest, n_min, n_max, saveDir, adName):
    testResult = {}
    for i in range(n_min, n_max):
        trainList = []
        for each in depTrain:
            trainList.extend(getNGProto(each, n=i))
        ngrst = nGramRST(i, tagSet, trainList)
        ngrst.toDict()
        ngrst.normalization()
        f = open(os.path.join(saveDir, str(i) + adName + ".ngrst"), "wb")
        pickle.dump(ngrst, f)
        f.close()
        for j in range(len(depTest)):
            testList = getNGProto(depTest[j], n=i)
            if not (j in testResult):
                testResult[j] = list()
            testResult[j].append(ngrst.perplexity(testList))
    return testResult


tagSet = ['Root', 'Atp', 'Background', 'Cr', 'Cc', 'Elab-other', 'Elab-aspect',
          'Ep', 'Argument', 'Sj', 'Progression', 'Question-answer',
          'Summary-local', 'Summary-global', 'Means', 'Same-unit', 'Ctl',
          'Evaluation', 'Text-restatement', 'List', 'Non-sequiturs', 'Gap']
aList = []
bList = []
iList = []
aDepList = glob.glob("../RST_annotation_results/RST_Annotation_Results/coherent_texts_DEP/CA*.dep")
bDepList = glob.glob("../RST_annotation_results/RST_Annotation_Results/coherent_texts_DEP/CB*.dep")
iDepList = glob.glob("../RST_annotation_results/RST_Annotation_Results/incoherent_texts_DEP/*.dep")
trainSet = []
trainSet.append(aDepList[:-1])
trainSet[0].extend(bDepList[:-1])
trainSet.append(iDepList[:-1])
testSet = [aDepList[-1], bDepList[-1], iDepList[-1]]
print("Train on a & b:")
cRes = cvNG(tagSet, trainSet[0], testSet, 2, 6, "../nGram", "_C")
print("Train on i:")
iRes = cvNG(tagSet, trainSet[1], testSet, 2, 6, "../nGram", "_I")
'''
# Post processing: combining the first two
cVal = []
iVal = []
for i in range(len(cRes[0])):
    cVal.append(0.5 * (cRes[0][i] + cRes[1][i]))
    iVal.append(0.5 * (iRes[0][i] + iRes[1][i]))
plt.plot(list(range(2, 6)), cVal, 'o-')
plt.plot(list(range(2, 6)), cRes[2], 'o-')
plt.plot(list(range(2, 6)), iVal, 'o-')
plt.plot(list(range(2, 6)), iRes[2], 'o-')
plt.legend(["Train C, Test C", "Train I, Test I",
            "Train I, Test C", "Train C, Test I"], fontsize=16)
plt.xlabel("N", fontsize=18)
plt.ylabel("Perplexity", fontsize=18)
plt.show()
'''
f = open("../nGram/3_I.ngrst", "rb")
c3 = pickle.load(f)
f.close()
c3.rank()
print(c3.rankNgram[::-1])
print(c3.rankProb[::-1])
