f = open("pageRank.txt")
lines = f.readlines()

graphs = []


for line in lines:
    dude, likes = line.split()
    new_graph = False
    for graph in graphs:
        if dude in graph:
            if likes not in graph:
                graph.append(likes)
                new_graph = True
                break
        if likes in graph:
            if dude not in graph:
                graph.append(dude)
                new_graph = True
                break
    if new_graph == False:
        graphs.append([dude, likes])
print len(graphs)


f.close()