"""
数据处理
图的构建
版本v0.5


"""
import networkx as nx
import pagerank as pg
from pylab import *
from harvesttext import HarvestText
from harvesttext.resources import get_sanguo_entity_dict, get_sanguo, get_baidu_stopwords
flag = 0
# 挑选主要人物画图
def get_map(start, end, num):
    if flag == 1:
        chapters = get_sanguo()
    else:
        chapters = []
        for i in range(start, end+1):
            s = "txt2\\" + str(i) + ".txt"
            print(s)
            filename = open(s, 'r', encoding='utf-8')
            chapters.append(filename.read())
    entity_type_dict = {'费尔南多·赛鲁罗': '人名', '农齐亚·赛鲁罗': '人名', '莉拉': '人名', '里诺·赛鲁罗': '人名', '莱农': '人名', '佩佩': '人名',
                        '詹尼': '人名', '埃莉莎': '人名', '奥利维耶罗': '人名', '堂·阿奇勒': '人名', '玛丽亚·卡拉奇': '人名', '斯特凡诺': '人名',
                        '皮诺奇娅': '人名', '阿方索': '人名', '阿尔佛雷多·佩卢索': '人名', '朱塞平娜·佩卢索': '人名', '帕斯卡莱·佩卢索': '人名', '卡梅拉·佩卢索': '人名',
                        '梅丽娜': '人名', '艾达': '人名', '安东尼奥': '人名', '多纳托·萨拉托雷': '人名', '莉迪亚·萨拉托雷': '人名', '尼诺': '人名',
                        '玛丽莎·萨拉托雷': '人名', '皮诺': '人名', '克莱利亚': '人名', '西罗': '人名', '尼科拉·斯坎诺': '人名', '阿孙塔·斯坎诺': '人名',
                        '恩佐': '人名', '西尔维奥·索拉拉': '人名', '曼努埃拉·索拉拉': '人名', '马尔切洛': '人名', '米凯莱': '人名', '吉耀拉': '人名',
                        '吉诺': '人名', '费拉罗': '人名', '内拉·因卡尔多': '人名'
                        }
    entity_mention_dict = {'费尔南多·赛鲁罗': ['费尔南多·赛鲁罗','费尔南多'], '农齐亚·赛鲁罗': ['农齐亚·赛鲁罗', '农齐亚'], '莉拉': ['拉法埃拉·赛鲁罗', '莉拉', '莉娜', '拉法埃拉'],
                           '里诺·赛鲁罗': ['里诺·赛鲁罗','里诺'],'莱农': ['莱农', '埃莱娜', '莱农奇娅', '莱诺', '莱农', '格雷科', '我'], '佩佩': ['佩佩'],
                        '詹尼': ['詹尼'], '埃莉莎': ['埃莉莎'], '奥利维耶罗': ['奥利维耶罗'], '堂·阿奇勒': ['堂·阿奇勒·卡拉奇', '堂·阿奇勒'],
                           '玛丽亚·卡拉奇': ['玛丽亚·卡拉奇', '玛丽亚'], '斯特凡诺·卡拉奇': ['斯特凡诺', '斯特凡诺'],
                        '皮诺奇娅': ['皮诺奇娅'], '阿方索': ['阿方索'], '阿尔佛雷多·佩卢索': ['阿尔佛雷多·佩卢索', '阿尔佛雷多'], '朱塞平娜·佩卢索': ['朱塞平娜·佩卢索', '朱塞平娜'],
                           '帕斯卡莱': ['帕斯卡莱·佩卢索', '帕斯卡莱'], '卡梅拉·佩卢索': ['卡梅拉'], '玛丽莎·萨拉托雷': ['玛丽莎·萨拉托雷', '玛丽莎'],
                        '梅丽娜': ['梅丽娜'], '艾达': ['艾达·卡普乔', '艾达'], '安东尼奥': ['安东尼奥·卡普乔', '安东尼奥'], '多纳托·萨拉托雷': ['多纳托·萨拉托雷', '多纳托', '萨拉托雷'],
                           '莉迪亚·萨拉托雷': ['莉迪亚·萨拉托雷', '莉迪亚'], '尼诺': ['尼诺·萨拉托雷', '尼诺'], '皮诺': ['皮诺'],
                        '克莱利亚': ['克莱利亚'], '西罗': ['西罗'], '尼科拉·斯坎诺': ['尼科拉·斯坎诺', '尼科拉'], '阿孙塔·斯坎诺': ['阿孙塔·斯坎诺'],
                        '恩佐': ['恩佐·斯坎诺', '恩佐'], '西尔维奥·索拉拉': ['西尔维奥·索拉拉'], '曼努埃拉·索拉拉': ['曼努埃拉·索拉拉', '曼努埃拉'],
                           '马尔切洛': ['马尔切洛', '马尔切洛·索拉拉'], '米凯莱': ['米凯莱', '米凯莱·索拉拉'], '吉耀拉': ['吉耀拉', '吉耀拉·斯帕纽洛'],
                        '吉诺': ['吉诺'], '费拉罗': ['费拉罗'], '内拉·因卡尔多': ['内拉·因卡尔多']
                           }
    # entity_mention_dict, entity_type_dict = get_sanguo_entity_dict()
    print(entity_mention_dict)
    #mention 是称谓字典，即存放着别称
    #type 是类型字典，存放着人名或者势力的类型
    ht = HarvestText()
    ht.add_entities(entity_mention_dict, entity_type_dict) #加载字典
    G_total = []
    G_global = nx.Graph()
    for chapter in chapters[0:end - start + 1]:
        sentences = ht.cut_sentences(chapter)       #句子

        docs = [sentences[i] + sentences[i + 1] for i in range(len(sentences) - 1)]
        ht.set_linking_strategy("freq")  # 参数“freq”表示连接策略为“按频率连接”

        G_total.append(ht.build_entity_graph(sentences, used_types=["人名"]))
        #合并子图
        for g in G_total:
            for (s, t) in g.edges:
                if (G_global.has_edge(s, t)):
                    G_global[s][t]["weight"] += g[s][t]["weight"]
                else:
                    G_global.add_edge(s, t, weight=g[s][t]["weight"])
            # for edge in G_global.edges:
            #     i = edge[0]
            #     j = edge[1]
            #     if G_global[i][j]["weight"] != 0:
            #         G_global[i][j]["weight"] -= 0.3
            #     if G_global[j][i]["weight"] != 0:
            #         G_global[j][i]["weight"] -= 0.3
            #排除小的联通分量，获得最大的联通分量
        # largest_comp = max(nx.connected_components(G_global), key=len)
        # G_global = G_global.subgraph(largest_comp).copy()
    if G_global.has_node('千万'):
        G_global.remove_node('千万')
    if G_global.has_node('许昌'):
        G_global.remove_node('许昌')
    if G_global.has_node('来历'):
        G_global.remove_node('来历')
    if G_global.has_node('封赏'):
        G_global.remove_node('封赏')
    return pg.pageRank_sort(G_global, num)




