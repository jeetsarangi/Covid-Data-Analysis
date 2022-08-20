import json
import pandas as pd

with open('neighbor-districts-modified.json') as jsonfile:
    neigh = json.load(jsonfile)

dist1 = []
dist2 = []
for key in neigh:
    near = neigh[key]
    for secondlevel in near:
        itslist = neigh[secondlevel]
        itslist.remove(key)
        dist1.append(key)
        dist2.append(secondlevel)
edge_graph = {"District One":dist1,"District two":dist2}
df = pd.DataFrame(edge_graph)
df.to_csv('edge-graph.csv', index=False)