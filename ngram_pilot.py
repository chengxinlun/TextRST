import glob
# import pickle
import re
from hmInterface import loadDiscTree
from ngram import nGram


class nGramRST(nGram):
    def __init__(self, n, tagSet, ngList, delta=0.001):
        super().__init__(n, tagSet, ngList, delta)
        # All kinds of remapping dictionaries
        self.renameDict = {"Bg-syntax": "Background"}
        self.combineDict = dict.fromkeys(['Cause', 'Result'], 'Cause-result')
        self.combineDict.update(dict.fromkeys(['Temporal', 'Location'],
                                'Time-place'))

    def remap(self, key):
        if key in self.renameDict:                      # Simple renaming
            return self.renameDict[key]
        elif key in self.combineDict:                   # Simple combining
            return self.combineDict[key]
        elif not(re.match(r'Intro-.+', key) is None):   # Intro-.+
            return 'Introduction'
        elif not(re.match(r'Arg-.+', key) is None):     # Arg-.+
            return 'Argument'
        elif not(re.match(r'Elab-.+', key) is None):    # Elab-.+
            return 'Elaboration'
        else:                                           # Does not need remap
            return key

    def segment(self, inStr):
        return re.findall(r'[A-Z#*][^A-Z#*]*', inStr)


def getNGProto(depFile):
    g = loadDiscTree(depFile)
    g.parse(show=False)
    return g.ngram(3)


tagSet = ['Root', 'Attribution', 'Introduction', 'Background', 'Cause-result',
          'Comparison', 'Contrast', 'Condition', 'Elaboration', 'Enablement',
          'Argument', 'Joint', 'Progression', 'Summary-local', 'Summary-global',
          'Manner-means', 'Same-unit', 'Time-place']
a3List = []
b3List = []
aDepList = glob.glob("../RST_annotation_results/180420/HQS/HQS_A*.dep")
bDepList = glob.glob("../RST_annotation_results/180420/HQS/HQS_B*.dep")
for each in aDepList:
    a3List.extend(getNGProto(each))
for each in bDepList:
    b3List.extend(getNGProto(each))
ngrst = nGramRST(3, tagSet, a3List)
ngrst.toDict()
ngrst.normalization()
print(ngrst.model)
# Picklebility test
'''
f = open("test.pkl", "wb")
pickle.dump(ngrst, f)
f.close()
f = open("test.pkl", "rb")
ngrst = pickle.load(f)
f.close()
print(ngrst.model)
'''
