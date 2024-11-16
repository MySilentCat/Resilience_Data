# 构建静态贝叶斯网络
# 获取当前目录
import os
import sys
import json
current_path = os.path.abspath(os.path.dirname(__file__))
# 将当前目录的上级目录加入到sys.path中
sys.path.append(os.path.abspath(os.path.join(current_path, os.pardir)))
from Input_process.deal_plantUML import *
from Static_Bayesian_network.cal_bayesian_network import *
from Input_process.cal_CPT import *

visited = []
trace = []
has_circle = False
all_trace = []
merge_list = []
num = 1
attacked = []
to_restoration = []
to_reliability = []

def dfs(name, com):
    global has_circle
    global all_trace
    if name in visited:
        if name in trace:
            has_circle = True
            new_trace = trace
            all_trace.append(new_trace)
            for t in new_trace:
                for m in merge_list:
                    if t == m:
                        merge_list.remove(m)
            merge_node(new_trace, com)
            name = merge_list[len(merge_list) - 1]
            return
        return

    visited.append(name)
    trace.append(name)

    if name != None:
        for parent in com.parents[name]:
            dfs(parent, com)
    trace.pop()


def merge_node(circle, com):
    global num
    merge_parents = []
    merge_children = []
    nodes_name = []
    for node in circle:
        nodes_name.append(node)
    for j in range(len(circle)):
        for k in range(len(com.parents[circle[j]])):
            if com.parents[circle[j]][k] not in nodes_name:
                merge_parents.append(com.parents[circle[j]][k])
    for j in range(len(circle)):
        for k in range(len(com.children[circle[j]])):
            if com.children[circle[j]][k] not in nodes_name:
                merge_children.append(com.children[circle[j]][k])

    for i in range(len(circle)):
        com.names.remove(circle[i])
        del com.parents[circle[i]]
        del com.children[circle[i]]
        del com.variables_dict[circle[i]]

    name = "merge_node" + str(num)
    com.names.append(name)
    num += 1
    com.parents[name] = merge_parents
    com.children[name] = merge_children
    ##print(len(com.name))
    index_list = [i for i in range(len(com.names))]
    com.variables_dict = dict(zip(com.names, index_list))

    for l in range(len(merge_parents)):
        for node in circle:
            for child in com.children[merge_parents[l]]:
                if node == child:
                    com.children[merge_parents[l]].remove(child)
        if name not in com.children[merge_parents[l]]:
            com.children[merge_parents[l]].append(name)

    for c in range(len(merge_children)):
        for node in circle:
            for parent in com.parents[merge_children[c]]:
                if node == parent:
                    com.parents[merge_children[c]].remove(parent)
        if name not in com.parents[merge_children[c]]:
            com.parents[merge_children[c]].append(name)
    global attacked
    global to_restoration
    global to_reliability
    for node in attacked:
        if node in circle:
            attacked.remove(node)
            attacked.append(name)
    attacked = list(set(attacked))
    for node in to_restoration:
        if node in circle:
            to_restoration.remove(node)
            to_restoration.append(name)
    to_restoration = list(set(to_restoration))
    for node in to_reliability:
        if node in circle:
            to_reliability.remove(node)
            to_reliability.append(name)
    to_reliability = list(set(to_reliability))

    merge_list.append(name)

import networkx as nx
def merge_circle_node(comp):
    # 将组件图存入到networkx的有向图中
    G = nx.DiGraph()
    for i in range(len(comp.names)):
        G.add_node(comp.names[i])
    for i in range(len(comp.names)):
        for j in range(len(comp.names)):
            if comp.adjacency_matrix[i][j] == 1:
                G.add_edge(comp.names[i],comp.names[j])

    # 获取所有的循环依赖
    circle_list = list(nx.simple_cycles(G))
    

    # 遍历circle_list，将有重叠的循环依赖合并
    for i in range(len(circle_list)):
        for j in range(i+1, len(circle_list)):
            if len(set(circle_list[i]) & set(circle_list[j])) != 0:
                print('合并环')
                circle_list[i] = list(set(circle_list[i]) | set(circle_list[j]))
                circle_list[j] = []

    # print(circle_list)
    # # 删除空的循环依赖
    # for circle in circle_list:
    #     if circle == []:
    #         circle_list.remove(circle)

    # 将循环依赖合并
    for circle in circle_list:
        if circle!=[]:
            merge_node(circle, comp)

    print(comp.names)
    for c in comp.names:
        comp.parents[c] = list(set(comp.parents[c]))
        comp.children[c] = list(set(comp.children[c]))

    #raise ValueError

    return comp


# 构建静态贝叶斯网络
def build_Static_Bayesian_network(comp:Component_diagram, Attack_node = None, attack_p = 0.6,main='',sub=[]):
    print(attack_p)
    #raise ValueError
    # 合并循环依赖的节点
    comp = merge_circle_node(comp)
    # 构建新的邻接矩阵
    comp.build_adjacency_matrix()
    node_num = len(comp.names)
    CGBR = cal_CGBR(comp.adjacency_matrix, node_num)
    
    # print(comp.names)
    # print(comp.parents)
    # raise ValueError
    # 获取影响可靠性和可恢复性的节点，以及受到攻击的节点
    get_reliability_restoration(comp, CGBR, Attack_node)
    global attacked
    attacked = list(set(attacked))
    global to_restoration
    to_restoration = list(set(to_restoration))
    global to_reliability
    to_reliability = list(set(to_reliability))
    bayes_nodes = comp.names.copy()
    # 计算节点的条件概率表
    cpt_list = []
    for i in range(comp.count):
        node_name = comp.names[i]
        print(node_name)
        # 该节点的父节点
        parents = comp.parents[node_name]
        # 该节点的父节点的CGRR值
        parents_CGBR = []
        print(comp.variables_dict)
        for parent in parents:
            if parent in comp.names:
                parents_CGBR.append(CGBR[comp.variables_dict[parent]])
            else:
                parents_CGBR.append(0)

        interface_parents = []
        if node_name in comp.interface.keys():
            interface_parents = comp.interface[node_name]

        parent_index_list = []
        for inter in interface_parents:
            print(parents)
            parent_index = parents.index(inter)
            parent_index_list.append(parent_index)
            cgbr = parents_CGBR[parent_index]
            parents_CGBR[parent_index] = cgbr/3
        
        cpt = []
        if len(parents) == 0:
            cpt = [[1,0]]
        # 根据CGBR值计算条件概率表
        else:
            if node_name == main:
                cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,parent_index_list = parent_index_list, node_name='main')
            elif node_name in sub:
                cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,parent_index_list = parent_index_list, node_name='sub')
            else:
                cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,parent_index_list = parent_index_list)
            

        
        print(node_name,'CPT: ', cpt)

        new_cpt = CPT(node_name, parents.copy(), cpt)
        cpt_list.append(new_cpt)

    # 添加攻击节点
    for i in range(len(attacked)):
        attack_node = 'Attack'+str(i)
        print(attack_node)
        bayes_nodes.append(attack_node)
        cpt = CPT(attack_node, [], [[attack_p,1-attack_p]])
        cpt_list.append(cpt)
        for cpt in cpt_list:
            if cpt.variable == attacked[i]:
                pp = attack_p
                if attacked[i].lower() == 'security':
                    pp = attack_p/3
                    print(pp)
                    #raise ValueError
                if attacked[i].lower() == 'database':
                    if 'persistance' in [name.lower() for name in comp.names]:
                        pp = attack_p/3
                print(attacked[i])
                print(cpt.parents)
                if cpt.parents == []:
                    cpt.parents.append(attack_node)
                    cpt.values = [[1,0],[1-pp,pp]]
                else:
                    parents_CGBR = []
                    for parent in cpt.parents:
                        if parent in comp.names:
                            parents_CGBR.append(CGBR[comp.variables_dict[parent]])
                        else:
                            parents_CGBR.append(0)
                    print(cpt.parents)
                    print(parents_CGBR)
                    interface_parents = []
                    if cpt.variable in comp.interface.keys():
                        interface_parents = comp.interface[cpt.variable]

                    parents = cpt.parents
                    parent_index_list = []
                    for inter in interface_parents:
                        parent_index = parents.index(inter)
                        parent_index_list.append(parent_index)
                        cgbr = parents_CGBR[parent_index]
                        parents_CGBR[parent_index] = cgbr/3
                    parents_CGBR.append(0)
                    cpt.parents.append(attack_node)
                    cpt.values = get_middle_node(0.6,len(cpt.parents),1,parents_CGBR,sum(parents_CGBR),0,0,1,parent_index_list = parent_index_list, attack_p = pp)
    
    # 添加可靠性节点
    reliability_node = 'Reliability'
    bayes_nodes.append(reliability_node)
    parents = to_reliability.copy()
    parents_CGBR = []
    for parent in parents:
        parents_CGBR.append(CGBR[comp.variables_dict[parent]])
    cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,node_name='Reliability')
    cpt = CPT(reliability_node, parents, cpt)
    cpt_list.append(cpt)

    Reliability_importance = np.mean(parents_CGBR)

    # 添加可恢复性节点
    restoration_node = 'Restoration'
    bayes_nodes.append(restoration_node)
    parents = to_restoration.copy()
    parents_CGBR = []
    for parent in parents:
        parents_CGBR.append(CGBR[comp.variables_dict[parent]])
    parents.append('Reliability')
    print(parents)
    parents_CGBR.append(Reliability_importance)
    print(parents_CGBR)
    cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,node_name='Reliability')
    print('可恢复性节点的条件概率表：', cpt)
    #raise ValueError
    cpt = CPT(restoration_node, parents, cpt)
    cpt_list.append(cpt)

    # 添加韧性节点
    Resilience_node = 'Resilience'
    bayes_nodes.append(Resilience_node)
    parents = ['Reliability', 'Restoration']
    parents_CGBR = [1,1]
    cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,node_name='Resilience')
    cpt = CPT(Resilience_node, parents, cpt)    
    cpt_list.append(cpt)     

    # 基于条件概率表构建邻接矩阵
    adjacency_matrix = [[0 for j in range(len(bayes_nodes))] for i in range(len(bayes_nodes))]
    for i in range(len(bayes_nodes)):
        print(bayes_nodes[i])
        for j in range(len(cpt_list[i].parents)):
            print(cpt_list[i].parents)
            adjacency_matrix[bayes_nodes.index(cpt_list[i].parents[j])][i] = 1
    
    # 构建新的贝叶斯网络
    bayesian_network = BayesianNetwork(len(comp.names), len(bayes_nodes), bayes_nodes, adjacency_matrix, cpt_list)

    # 计算每个节点为True的概率
    marginal_prob_dict = {}
    for i in range(len(bayes_nodes)):
        marginal_prob_dict[bayes_nodes[i]] = bayesian_network.marginal_prob(bayes_nodes[i], {})
    print(marginal_prob_dict)
    #raise ValueError
    return bayesian_network, marginal_prob_dict, CGBR, comp

# 获取影响可靠性和可恢复性的节点，以及受到攻击的节点
def get_reliability_restoration(comp:Component_diagram, CGBR, Attack_node = None):
    node_num = comp.count
    print(CGBR)
    #raise ValueError
    # 将CGBR值与高于均值2倍的节点视作重要节点
    importance_dict = []
    for i in range(node_num):
        if CGBR[i] >= np.mean(CGBR):
            importance_dict.append(comp.names[i])
    print(importance_dict)
    global attacked
    global to_restoration
    global to_reliability
    attacked = []
    to_restoration = []
    to_reliability = []
    # 获得所有入度为0和出度为0的节点
    for i in range(node_num):
        print('parent:',comp.parents[comp.names[i]])
        if comp.parents[comp.names[i]] == []:
            attacked.append(comp.names[i])
        if comp.children[comp.names[i]] == []:
            attacked.append(comp.names[i])
    print('attacked:',attacked)
    if Attack_node!=[]:
        attacked = Attack_node
    #attacked.extend(Attack_node)
    attacked = list(set(attacked))
    print(importance_dict)
    #attacked = ['Database', 'Front_end', 'Pay']
    to_restoration = importance_dict
    to_reliability = importance_dict
    print(to_restoration)
    print(to_restoration)
    #raise ValueError

def Draw_Static_Bayesian_network(comp:Component_diagram, marginal_prob_dict, CGBR, bayesian_network: BayesianNetwork, js_path, comp_id):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "Attack Node" # 攻击节点
        },
        {
            "name": "Component Node" # 组件节点
        },
        {
            "name": "Resilience Sub Attribute Node" # 韧性子属性节点
        },
        {
            "name": "Resilience Node" # 韧性属性节点
        }
    ]

    # 添加边
    link_nodes = set()
    for i in range(len(bayesian_network.variables)):
        for j in range(len(bayesian_network.variables)):
            if bayesian_network.graph[i][j] == 1:
                link = {}
                link["source"] = bayesian_network.variables[i] + '_'+str(comp_id)
                link["target"] = bayesian_network.variables[j] + '_'+str(comp_id)
                link_nodes.add(link["source"])
                link_nodes.add(link["target"])
                link["symbol"] = [
                    "none",
                    "arrow"
                ]
                link["lineStyle"] = {
                    "normal": {
                        "width": 2,
                        "curveness": 0.2,
                        "type": "solid",
                        "opacity": 1
                    }
                }
                link_list.append(link)
    # 添加节点
    # 组件节点
    for i in range(len(comp.names)):
        if comp.names[i]+ '_'+str(comp_id) not in link_nodes:
            continue
        data = {}
        data["name"] = comp.names[i]+ '_'+str(comp_id) # 节点名称
        data["id"] = comp.names[i] + '_'+str(comp_id)  # 节点id
        data["symbolSize"] = 45
        data["category"] = 1
        data["CGBR"] = CGBR[i] # 节点的CGBR值
        # 节点为True的概率, 保留三位小数
        data["marginal_prob"] = round(marginal_prob_dict[comp.names[i]], 5)
        data["fixed"] = False
        data["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        data_list.append(data)
    # 其他贝叶斯网络节点
    for node in bayesian_network.variables:
        if node not in comp.names:
            if node+ '_'+str(comp_id) not in link_nodes:
                continue
            data = {}
            data["name"] = node+ '_'+str(comp_id)
            data["id"] = node + '_'+str(comp_id)
            data["symbolSize"] = 45
            if 'Attack' in node:
                data["category"] = 0
            elif 'Resilience' in node:
                data["category"] = 3
            elif 'Reliability' in node or 'Restoration' in node:
                data["category"] = 2
            data["CGBR"] = None
            data["marginal_prob"] = round(marginal_prob_dict[node], 5)

            data["fixed"] = False
            data["itemStyle"] = {
                "normal": {
                    "opacity": 1
                }
            }
            data_list.append(data)


    # 绘制贝叶斯网络
    json_data = {}
    json_data["data"] = data_list
    json_data["categories"] = categories
    json_data["links"] = link_list

    return json_data

    # 写入js文件
    # json_file = 
    with open(js_path, 'w') as f:
        # 变量名为graph

        f.write('var graph = ')
        json.dump(json_data, f, indent=4)

    # print(comp.name)

def Static_Bayesian_network_MAIN(comp, js_path, Attack_node = None, comp_id = None,main = '',sub=[]):
    # 构建条件概率表
    #cpt_dict = cal_cpt(comp)

    print('开始静态贝叶斯网络评估')
    print('组件数目为：', len(comp.names))
    # 构建贝叶斯网络
    # bayesian_network, marginal_prob_dict, CGBR, comp = build_Static_Bayesian_network(comp, Attack_node)
    # print(bayesian_network.variables)
    marginal_prob_dict_list = []
    CGBR = None

    for i in range(9):
        print(i,'次攻击')
        attack_p = (i+1)/10
        print(attack_p)
        bayesian_network, marginal_prob_dict, CGBR, comp = build_Static_Bayesian_network(comp, Attack_node, attack_p,main = main,sub=sub)
        marginal_prob_dict_list.append(marginal_prob_dict)

    # # 计算每个节点为True的概率
    # marginal_prob_dict = {}
    # for i in range(len(comp.name)):
    #     marginal_prob_dict[comp.name[i]] = bayesian_network.marginal_prob(comp.name[i], {})
    print(marginal_prob_dict)
    avg_marginal_prob_dict = {}
    for key in marginal_prob_dict.keys():
        avg_marginal_prob_dict[key] = np.mean([marginal_prob_dict[key] for marginal_prob_dict in marginal_prob_dict_list])
    

    # # 绘制贝叶斯网络
    json_data = Draw_Static_Bayesian_network(comp, avg_marginal_prob_dict, CGBR, bayesian_network, js_path, comp_id)

    json_data["resilience"] = avg_marginal_prob_dict['Resilience']

    print(marginal_prob_dict_list)
    
    print('韧性评估结果为：',json_data["resilience"])
    global attacked
    print('攻击节点数量为：',len(attacked))
    

    return marginal_prob_dict_list, CGBR, comp, attacked, json_data

if __name__ == "__main__":
    # 读取组件图
    file1=r"E:\Graduation_Design\Input_process\网上商城系统.wsd"
    comp = comp_wsd_to_txt(file1)
    js_path = r"static.js"
    
    Static_Bayesian_network_MAIN(comp, js_path)


    

