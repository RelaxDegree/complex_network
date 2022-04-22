"""
力引导图布局

版本v0.5 有社区分划
有部分链路预测
10种颜色



"""

import math
from matplotlib import pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from pylab import *
import predict
import random
import bezier
from matplotlib.collections import LineCollection
# 模型参数
K_r = 300000       # 斥力系数
K_s = 0.001     # 引力系数
L = 5          # 弹簧初始长度
delta_t = 50
MaxLength = 50  #点与点最大距离
iterations = 2000
color = ['red', 'green', 'blue', 'orange']
flag = 1
original_max_posx = 1000
original_max_posy = 1000
# 图形容器
Edge = []
Node_force = {}
Node_position = {}
# 节点大小用来反映节点的度
Node_degree = []
colorlist = ['#EEA2A4', '#EE334D', '#FA7E23', '#2177B8', '#66A9C9', '#12A182', '#E3BD8D', '#C3D7DF', '#D2568C', '#61649F']
            #   牡丹粉       茶红        焦橙      中蓝          浅蓝      蓝绿        浅棕         韵白        紫红      青紫
# 与采样退火有关的参数
Displacement_list = []  # 用于采样的列表
scale = 3  # 采样的范围；
G_copy = []     # 图的副本 在链路路径函数中使用

def init(G):
    import random
    Node_num = len(G.nodes())
    print("nodeNum:", Node_num)
    for i in G.nodes:  # 随机生成点坐标,初始化力

        posy = random.uniform(0, original_max_posy)  # 初始化点坐标和受力
        posx = random.uniform(0, original_max_posx)
        Node_position[i] = (posx, posy)
        Node_force[i] = (0, 0)
    for e in G.edges:
        i = e[0]
        j = e[1]
        Edge.append((i, j))
        Edge.append((j, i))


def compute_repulsion(G):  # 计算每两个点之间的斥力
    for i in G.nodes:
        for j in G.nodes:
            if (i == j):
                continue
            dx = Node_position[j][0] - Node_position[i][0]
            dy = Node_position[j][1] - Node_position[i][1]
            if dx != 0 or dy != 0:
                distanceSquared = dx * dx + dy * dy
                distance = math.sqrt(distanceSquared)
                R_force = K_r / distanceSquared
                fx = R_force * dx / distance    # 斥力水平分力
                fy = R_force * dy / distance    # 斥力垂直分力
                fi_x = Node_force[i][0]         # 原水平分力
                fi_y = Node_force[i][1]         # 原垂直分力
                Node_force[i] = (fi_x - fx, fi_y - fy)  # 更新i节点
                fj_x = Node_force[j][0]
                fj_y = Node_force[j][1]
                Node_force[j] = (fj_x + fx, fj_y + fy)  # 更新j节点


def compute_string(G):  # 计算每两个相邻点和吸引力
    for i in G.nodes:   # 取出其邻居
        neighbors = [n for n in G[i]]  # 对每一个邻居，计算斥力；j
        for j in neighbors:
            dx = Node_position[j][0] - Node_position[i][0]
            dy = Node_position[j][1] - Node_position[i][1]
            if dx != 0 or dy != 0:
                distance = math.sqrt(dx * dx + dy * dy)
                S_force = K_s * (distance - L) * G[i][j]["weight"]
                fx = S_force * dx / distance
                fy = S_force * dy / distance  # 更新受力
                fi_x = Node_force[i][0]
                fi_y = Node_force[i][1]
                Node_force[i] = (fi_x + fx, fi_y + fy)
                fj_x = Node_force[j][0]
                fj_y = Node_force[j][1]
                Node_force[j] = (fj_x - fx, fj_y - fy)


def update_position(G,times):  # 更新坐标
    Displacement_sum = 0
    for i in G.nodes:
        m = G.degree[i] + 1
        dx = delta_t * Node_force[i][0] / m
        dy = delta_t * Node_force[i][1] / m
        displacementSquard = dx * dx + dy * dy
        # 随迭代次数增加，MaxLength逐渐减小；

        current_MaxLength = MaxLength / (times + 0.1)

        if (displacementSquard > current_MaxLength):
            s = math.sqrt(current_MaxLength / displacementSquard)
            dx = dx * s
            dy = dy * s
        (newx, newy) = (Node_position[i][0] + dx, Node_position[i][1] + dy)
        Displacement_sum += math.sqrt(dx * dx + dy * dy)
        Node_position[i] = (newx, newy)
    return Displacement_sum


def show_graph(G):
    init(G)  # 初始化节点得坐标和图中的边
    for i in G.nodes:
        Node_degree.append(pow(G.degree(i), 2))
    start = time.perf_counter()
    iteration_time = 0
    for times in range(0, 1 + iterations):
        for i in G.nodes:
            Node_force[i] = (0, 0)
        compute_repulsion(G)
        compute_string(G)
        # 记录本次迭代移动距离：
        Displacement_sum = update_position(G, times)
        Displacement_list.append(Displacement_sum)
        #print(Displacement_sum)
        # if len(Displacement_list) > scale:
        #     last = np.mean(Displacement_list[times - 4:times - 1])
        #     now = np.mean(Displacement_list[times - 3:times])
        #     if (last - now) / last < 0.01:
        #         break
        iteration_time = times
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    print('最终迭代次数:', iteration_time)
    return

text1 = ""
text2 = ""
predictlist = []

def curved_line(x0, y0, x1, y1, eps=0.7, pointn=100):    # 曲线

    x2 = (x0+x1)/2.0 + 0.01 ** (eps+abs(x0-x1)) * (-1) ** (random.randint(1, 4))
    y2 = (y0+y1)/2.0 + 0.01 ** (eps+abs(y0-y1)) * (-1) ** (random.randint(1, 4))
    nodes = np.asfortranarray([
        [x0, x2, x1],
        [y0, y2, y1]
    ])
    curve = bezier.Curve(nodes,
                         degree=2)
    s_vals = np.linspace(0.0, 1.0, pointn)
    data=curve.evaluate_multi(s_vals)
    x=data[0]
    y=data[1]
    segments =[]
    for index in range(0,len(x)):
        segments.append([x[index],y[index]])
    segments = [segments]
    return  segments

def draw_graph(G, partition, alpha, node_scale, figsize):
    print(len(G.nodes))
    # partition['赵云'] = partition['刘备']
    # partition['张飞'] = partition['刘备']
    # partition['诸葛亮'] = partition['刘备']
    # partition['周瑜'] = partition['孙权']
    # partition['鲁肃'] = partition['孙权']

    global G_copy

    G_copy = G
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    node_color = []
    edge_color = []
    for node in G.nodes:
        node_color.append(colorlist[partition[node]])
    for edge in G.edges:
        if partition[edge[0]] == partition[edge[1]]:
            edge_color.append(colorlist[partition[edge[0]]])
        else:
            edge_color.append('#ABABAB')

    plt.figure(figsize=figsize, dpi=80)

    if flag == 1:
        pos = nx.spring_layout(G)       #用Fruchterman-Reingold算法排列节点（样子类似多中心放射状）
        for p in pos.values():
            p[0] *= 1
            p[1] *= 1
        for edge in G.edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            segs = curved_line(x0, y0, x1, y1)
            if partition[edge[0]] == partition[edge[1]]:
                lc = LineCollection(segs, edgecolors=colorlist[partition[edge[0]]], linewidths=1)
            else:
                lc = LineCollection(segs, edgecolors='#ABABAB', linewidths=0.5)

            plt.gca().add_collection(lc)
            plt.gca().autoscale_view()

        nx.draw_networkx_nodes(G, pos, node_size=[G.degree[x]*node_scale*0.5 + 430 for x in G.nodes], node_color='black')
        nx.draw_networkx_nodes(G, pos, node_size=[G.degree[x]*node_scale*0.5 + 410 for x in G.nodes], node_color=node_color)
        # nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=1, alpha=alpha)
        nx.draw_networkx_labels(G, pos, font_size=15)

    else:
        show_graph(G)
        nx.draw_networkx_nodes(G, Node_position, node_size=[G.degree[x] * node_scale * 0.5 + 330 for x in G.nodes],node_color='black')
        nx.draw_networkx_nodes(G, Node_position, node_size=[G.degree[x] * node_scale * 0.5 + 300 for x in G.nodes],node_color=node_color)
        nx.draw_networkx_edges(G, Node_position, edge_color=edge_color, width=1, alpha=alpha)
        nx.draw_networkx_labels(G, Node_position, font_size=10)
    plt.subplots_adjust(bottom=0.1)
    axpre = plt.axes([0.1, 0.03, 0.05, 0.03])       # 链路预测的按钮
    btnpre = Button(axpre, '链路预测', color='khaki', hovercolor='grey')
    btnpre.on_clicked(show_prelink)
    axclear = plt.axes([0.2, 0.03, 0.05, 0.03])     # 链路清楚的按钮
    btnclear = Button(axclear, '清空路径', color='khaki', hovercolor='grey')
    btnclear.on_clicked(clear_prelink)

    axtext1 = plt.axes([0.3, 0.03, 0.10, 0.05])     # 第一个文本框
    textbox1 = TextBox(ax=axtext1, label='人名1:', initial='曹操', color='lightblue')
    textbox1.on_submit(gettext1)

    axtext2 = plt.axes([0.5, 0.03, 0.10, 0.05])  # 第二个文本框
    textbox2 = TextBox(ax=axtext2, label='人名2:', initial='刘备', color='lightblue')
    textbox2.on_submit(gettext2)

    axtext3 = plt.axes([0.7, 0.03, 0.10, 0.05])  # 标签框
    textbox3 = TextBox(ax=axtext3, label='')
    global predictlist
    predictlist = predict.prelinks(G)  # 链路预测

    plt.axis("off")
    plt.show()


def show_prelink(event):
    print(text1, text2)
    global predictlist
    global G_copy
    for node in predictlist:
        if text1 == node[0] and text2 == node[1]:
            text = text1 + "与" + text2 + "认识的概率为：" + str(node[2]*100) + "%"
            print(text)
            break
    links = predict.findlinks(G_copy, text1, text2)

    print(links)



def clear_prelink(event):
    print("清空")


def gettext1(expression):
    global text1
    text1 = expression

def gettext2(expression):
    global text2
    text2 = expression
