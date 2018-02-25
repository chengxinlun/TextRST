# This is only a simple test data. There is no relation predictor implemented.
from eduDGraph import eduDGraph

sent = ["Rudyard Kipling once said , ", "\"East is East , and West is West , ",
        "and never the twain shall meet.\"", "However , ", "today , ",
        "Socrates , the representative of the West , and Confucius , the" +
        " representative of the East , are meeting together , ",
        "and they have three questions to ask Kipling . "]
edg = eduDGraph('Test Text', sent)
edg.diGraph.add_edge(1, 5, weight=1.0, relation='bg-compare')
edg.diGraph.add_edge(5, 6, weight=0.6, relation='joint')
edg.diGraph.add_edge(5, 2, weight=0.4, relation='joint')
edg.diGraph.add_edge(1, 0, weight=1.0, relation='attribution')
edg.diGraph.add_edge(1, 2, weight=1.0, relation='joint')
edg.diGraph.add_edge(5, 3, weight=1.0, relation='temporal')
edg.diGraph.add_edge(3, 4, weight=1.0, relation='same-unit')
edg.parse(show=True)
