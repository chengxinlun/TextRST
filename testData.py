# This is only a simple test data. There is no relation predictor implemented.
import glob
# from eduDGraph import eduDGraph
from hmInterface import loadDiscTree

'''
sent = ["Rudyard Kipling once said , ", "\"East is East , and West is West , ",
        "and never the twain shall meet.\"", "However , ", "today , ",
        "Socrates , the representative of the West , and Confucius , the" +
        " representative of the East , are meeting together , ",
        "and they have three questions to ask Kipling . "]
edg = eduDGraph('Test Text', sent)
edg.diGraph.add_edge(1, 5, weight=1.0, relation='bg-compare')
edg.diGraph.add_edge(5, 6, weight=1.0, relation='joint')
edg.diGraph.add_edge(1, 0, weight=1.0, relation='attribution')
edg.diGraph.add_edge(1, 2, weight=1.0, relation='joint')
edg.diGraph.add_edge(5, 3, weight=1.0, relation='temporal')
edg.diGraph.add_edge(3, 4, weight=1.0, relation='same-unit')
edg.parse(show=False, fName='test_1.png')
g = loadDiscTree("../RST_Annotation_Results_180305/ZhengHua/A1_ZH_FLTRP_2013_A_027_OSPL.txt.edu.dep")
g.parse(show=False, fName='test_ZH.png')
g = loadDiscTree("../RST_Annotation_Results_180305/LiYimeng/A1_LYM_FLTRP_2013_A_027_OSPL.txt.edu.dep")
g.parse(show=False, fName='test_LYM.png')
g = loadDiscTree("../RST_Annotation_Results_180305/HuangQiushi/A1_HQS_FLTRP_2013_A_027_OSPL.txt.edu.dep")
g.parse(show=False, fName='test_HQS_A1.png')
g = loadDiscTree("../RST_Annotation_Results_180305/HuangQiushi/A2_HQS_FLTRP_2013_A_049_OSPL.txt.edu.dep")
g.parse(show=False, fName='test_HQS_A2.png')
g = loadDiscTree("../RST_Annotation_Results_180305/HuangQiushi/B1_HQS_FLTRP_2013_A_022_OSPL.txt.edu.dep")
g.parse(show=False, fName='test_HQS_B1.png')
'''
depList = glob.glob("../RST_annotation_results/RST_5/HQS/*.dep")
for each in depList:
    g = loadDiscTree(each)
    g.parse(show=False, fName=each.split(".dep")[0] + ".png")
depList = glob.glob("../RST_annotation_results/RST_5/ZH/*.dep")
for each in depList:
    g = loadDiscTree(each)
    g.parse(show=False, fName=each.split(".dep")[0] + ".png")
