import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx


class eduDGraph:
    # Text represented as a directional graph
    # Node:
    #   edu: the edu this node stands for
    # Edge:
    #   relation: the relation between connecting nodes (edus)
    #   weight: the probability of this relation
    def __init__(self, gName, eduList):
        # n: number of EDUs (nodes) in the graph
        # eduList: initialize node::edu with the list
        self.gName = gName
        self.diGraph = nx.DiGraph()
        for i in range(1, len(eduList) + 1):
            self.diGraph.add_node(i, edu=eduList[i])

    def save(self, fName):
        # Save the graph to fName
        nx.write_gpickle(self.diGraph, fName)

    def load(self, fName):
        # Load the graph from fName
        self.diGraph = nx.read_gpickle(fName)

    def connect(self, relPred):
        # Predict and initialize all the edges between EDUs
        # relPred: EDU relation predictor
        for i in range(1, len(self.diGraph) + 1):
            for j in range(1, len(self.diGraph) + 1):
                res, prob = relPred(self.diGraph.nodes[i]['edu'],
                                    self.diGraph.nodes[j]['edu'])
                self.diGraph.add_edge(i, j, weight=prob, relation=res)

    def parse(self, show=False, fName=None):
        # Parse the most probable RST of the give text with maximum spanning
        # tree
        tmp = nx.algorithms.tree.branchings.Edmonds(self.diGraph)
        self.mst = tmp.find_optimum()
        # Copy the attributes and put them into formatted labels
        # probDict = nx.get_edge_attributes(self.diGraph, 'weight')
        relDict = nx.get_edge_attributes(self.diGraph, 'relation')
        valDict = {}
        for each in self.mst.edges():
            valDict[each] = "%s" % (relDict[each])
        # Draw the mst properly
        fig = plt.figure(figsize=(32, 20))
        plt.suptitle("Discourse tree for " + self.gName)
        gs = gridspec.GridSpec(1, 2)
        ax1 = plt.subplot(gs[0])
        pos = nx.drawing.nx_agraph.graphviz_layout(self.mst, prog='dot')
        # Node labels
        nx.draw(self.mst, pos, with_labels=True, arrows=True)
        nx.draw_networkx_edge_labels(self.mst, pos, valDict)
        plt.draw()
        ax2 = plt.subplot(gs[1])
        ax2.axis('off')
        caption = ""
        for each in self.diGraph.nodes(data=True):
            caption = caption + str(each[0]) + ": " + each[1]['edu'] + "\n"
        plt.text(0.0, 0.0, caption, ha='left', wrap=True,
                 transform=ax2.transAxes)
        if show:
            plt.show()
        else:
            plt.savefig(fName)

    def ngram(self, n):
        # Extract ngram from the parse tree
        # First find root node
        nRoot = nx.topological_sort(self.mst)[0]
        # Parent dictionary
        prtDict = nx.dfs_predecessors(self.mst, nRoot)
        # Non-terminal node list
        ntList = prtDict.values()
        # Relation dictionary
        relDict = nx.get_edge_attributes(self.diGraph, 'relation')
        # Extract ngram list
        ngList = []
        for each in range(1, len(self.diGraph) + 1):
            ngStr = ''
            if each == nRoot:
                # Root node
                ngStr = '#' * (n - 1)
                ngStr = ngStr + 'Root'
                i = n
            else:
                # Any other node
                i = 0
                start = each
            while i < n:
                if start != nRoot:
                    prtNode = prtDict[start]
                    tmp = relDict[(prtNode, start)].lower().capitalize()
                    addStr = tmp
                    addNum = 1
                    start = prtNode
                else:
                    addStr = '#' * (n - i - 1)
                    addStr = addStr + 'Root'
                    addNum = n - i
                ngStr = addStr + ngStr
                i = i + addNum
            ngList.append(ngStr)
            if not (each in ntList):  # Terminal node
                start = each
                ngStr = '*'
                i = 1
                while i < n:
                    if start != nRoot:
                        prtNode = prtDict[start]
                        tmp = relDict[(prtNode, start)].lower().capitalize()
                        addStr = tmp
                        addNum = 1
                        start = prtNode
                    else:
                        addStr = '#' * (n - i - 1)
                        addStr = addStr + 'Root'
                        addNum = n - i
                    ngStr = addStr + ngStr
                    i = i + addNum
                ngList.append(ngStr)
        return ngList
