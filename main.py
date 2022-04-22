import collections as cs
import community as com
import networkx as nx

import chapter as cp
import predict
import visualization as vs
import predict as pre
G = cp.get_map(start=1, end=21, num=80)  # 图的构建
# 图的社区分划
partition = com.best_partition(G)
print (partition)
comm_dict = {}
nodelist = {}
for person in partition:
    if partition[person] not in comm_dict:
        comm_dict[partition[person]] = []
        comm_dict[partition[person]].append(person)
    else:
        comm_dict[partition[person]].append(person)

for i in range(len(comm_dict)):
    for j in comm_dict[i]:
        nodelist[j] = i

vs.draw_graph(G, partition=nodelist, alpha=0.5, node_scale=15, figsize=(16, 6))  # 图的可视化


