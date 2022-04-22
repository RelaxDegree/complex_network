"""
pagerank算法重要程度排序
加权pagerank算法
版本v0.2

 by 张昱昊
"""

import networkx as nx
from pylab import *
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


flag = 0

def pageRank_sort(G, num):
    nodelist = pageRank(G, num)
    G_main = G.subgraph(nodelist).copy()
    return G_main


def pageRank(G, num):
    N = len(G.nodes)
    s = np.zeros([N, N])
    node_num = {}
    node_node = {}
    edge_num = []

    i = 0
    for node in G.nodes:
        node_num[node] = i
        node_node[i] = node
        i += 1
    for edge in G.edges:
        x = node_num[edge[0]]
        y = node_num[edge[1]]
        w = G[edge[0]][edge[1]]["weight"]
        edge_num.append((x, y, w))
        s[x][y] = w
    for j in range(N):
        sum_col = sum(s[:, j])
        for i in range(N):
            if sum_col != 0:
                s[i, j] /= sum_col

    alpha = 0.85
    A = alpha * s + (1 - alpha) / N * np.ones([N, N])
    P_n = np.ones(N) / N
    P_n1 = np.zeros(N)
    e = 100000  # 误差初始化
    k = 0  # 记录迭代次数
    while e > 0.00000001:  # 开始迭代
        P_n1 = np.dot(A, P_n)  # 迭代公式
        e = P_n1 - P_n
        e = max(map(abs, e))  # 计算误差
        P_n = P_n1
        k += 1
    #    print('iteration %s:' % str(k), P_n1,e)
    #print('final result:', P_n)
    p_n_list = P_n.tolist()
    pg_temp = []
    for i in range(N):
        pg_temp.append((p_n_list[i], i))
    pg_temp.sort(reverse=True)
    nodelist = []
    pagelist = []
    num = min(num, N)
    for i in range(num):
        j = pg_temp[i][1]
        node = node_node[j]
        nodelist.append(node)
        pagelist.append(pg_temp[i][0])
    fig = plt.figure()
    plt.barh(nodelist, pagelist, fc='b', height=0.4, color="red")
    plt.xlabel("PageRank值")
    plt.ylabel("人名")
    plt.title("《三国演义》人物PageRank值排名")
    plt.show()
    print(len(nodelist))
    return nodelist

    #可视化 这个矩阵  选择前100 生产字典  返回至
def degreeCentrality(G, num):
    list = []
    for node in G.nodes:
        count = 0
        for j in G[node]:
            count += G[node][j]["weight"]
        list.append((count, node))
    list.sort(reverse=True)
    nodelist = []
    valuelist = []
    for i in range(num):
        nodelist.append(list[i][1])
        valuelist.append(list[i][0])
