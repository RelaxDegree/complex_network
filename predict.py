import visualization as vs
import networkx as nx
import math
import random


def ini(G):
    node_num = {}
    node_node = {}
    i = 0
    for node in G.nodes:
        node_num[node] = i
        node_node[i] = node
        i += 1
    return node_num, node_node, i


def RAA(G, a, b):
    ALF = 0.1
    node_num, node_node, nums = ini(G)
    comon = list(nx.common_neighbors(G, a, b))
    # print(comon)
    tot = 0
    if len(comon) == 0:
        return 0
    else:
        fir, sec, sz = 0, 0, 0
        for node in comon:
            fir = math.pow(G[a][node]["weight"], ALF) + math.pow(G[node][b]["weight"], ALF)
            nb = list(G.neighbors(node))
            # print(nb)
            for nd in nb:
                sz += math.pow(G[node][nd]["weight"], ALF)
            sec = math.log(1 + sz, 10)
            tot += fir / sec
        return tot


def AUC(notedge, isedge):
    N, score = 2000, 0
    for i in range(0, N):
        a = random.randint(0, len(notedge) - 1)
        b = random.randint(0, len(isedge) - 1)

        if notedge[a][0] < isedge[b][0]:
            score += 1
        elif notedge[a][0] == isedge[b][0]:
            score += 0.5
    return score / N


def prelinks(G):
    append_edges = []
    node_num, node_node, nums = ini(G)
    notedge = []
    isedge = []
    for x in range(0, nums - 1):
        for y in range(x + 1, nums):
            if (node_node[x], node_node[y]) not in G.edges:
                score = RAA(G, node_node[x], node_node[y])
                notedge.append((score, node_node[x], node_node[y]))
            else:
                score = RAA(G, node_node[x], node_node[y])
                isedge.append((score, node_node[x], node_node[y]))
    notedge = sorted(notedge, key=lambda x: x[0], reverse=True)
    isedge = sorted(isedge, key=lambda x: x[0])
    s = AUC(notedge, isedge)
    for i in range(0, len(notedge)):
        append_edges.append((notedge[i][1], notedge[i][2], s*(notedge[i][0]/notedge[0][0])))
        append_edges.append((notedge[i][2], notedge[i][1], s*(notedge[i][0]/notedge[0][0])))
    for i in range(0, len(isedge)):
        append_edges.append((isedge[i][1], isedge[i][2], 1))
        append_edges.append((isedge[i][2], isedge[i][1], 1))
    return append_edges

def findlinks(G,a,b):
    links = []
    if (a, b) in G.edges:
        return links
    neighbors=list(nx.common_neighbors(G, a, b))
    for node in neighbors:
        links.append((a,node))
        links.append((node,b))
    print(links)
    return links