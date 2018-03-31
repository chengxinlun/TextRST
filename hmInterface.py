import io
import json
from eduDGraph import eduDGraph


def loadDiscTree(fName):
    # Load a human annotated discourse tree
    f = io.open(fName, 'r', encoding='utf-8-sig')
    dataDict = json.load(f)
    f.close()
    # Extract the tree out
    # Filter out root and empty
    treeList = dataDict['root']
    if treeList[0]['text'] == 'ROOT':
        treeList = treeList[1:]
    if treeList[-1]['text'].strip() == '':
        treeList = treeList[:-1]
    # Reconstruct the nodes
    g = eduDGraph(fName, [])
    for each in treeList:
        if each['text'].strip() == '':
            continue
        g.diGraph.add_node(each['id'] - 1, edu=each['text'].strip('\r'))
    # Reconstruct the edges
    for each in treeList:
        if each['parent'] == 0 or each['text'].strip() == '':
            continue
        else:
            g.diGraph.add_edge(each['parent'] - 1, each['id'] - 1, weight=1.0,
                               relation=each['relation'])
    return g
