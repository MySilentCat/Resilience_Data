# 构建动态贝叶斯网络
# 时间：2023/10/24
import os
import sys
current_path = os.path.abspath(os.path.dirname(__file__))
# 将当前目录的上级目录加入到sys.path中
sys.path.append(os.path.abspath(os.path.join(current_path, os.pardir)))
from Input_process.deal_plantUML import *
from Static_Bayesian_network.cal_bayesian_network import *
from Static_Bayesian_network.Build_Static_Bayesian_network import *
import networkx as nx
from Input_process.cal_CPT import *
import random
import math

def build_Dynamic_Bayesian_network(comp:Component_diagram, CGBR:[], static_marginal_prob_dict:{},main='',sub = []):
    # 存储到networkx中
    print('存储到networkx中')
    component_graph = nx.DiGraph()
    for i in range(len(comp.names)):
        component_graph.add_node(comp.names[i])
    for i in range(len(comp.names)):
        for j in range(len(comp.children[comp.names[i]])):
            component_graph.add_edge(comp.names[i], comp.children[comp.names[i]][j])

    # 获取所有入度为0的节点
    print('获取所有入度为0的节点')
    zero_in_degree = []
    for i in range(len(comp.names)):
        if component_graph.in_degree(comp.names[i]) == 0:
            zero_in_degree.append(comp.names[i])

    # 获取所有出度为0的节点
    print('获取所有出度为0的节点')
    zero_out_degree = []
    for i in range(len(comp.names)):
        if component_graph.out_degree(comp.names[i]) == 0:
            zero_out_degree.append(comp.names[i])

    # 获取所有从入度为0的节点到出度为0的节点的简单路径
    print('获取所有从入度为0的节点到出度为0的节点的简单路径')
    all_simple_paths = []
    for i in range(len(zero_in_degree)):
        for j in range(len(zero_out_degree)):
            all_simple_paths.extend(list(nx.all_simple_paths(component_graph, zero_in_degree[i], zero_out_degree[j])))
    print('执行路径数量为：',len(all_simple_paths))


    CPT_list = []

    # 构建每个组件节点的条件概率表
    for i in range(len(comp.names)):
        node_name = comp.names[i]
        parents = []
        cpt = [[static_marginal_prob_dict[node_name], 1-static_marginal_prob_dict[node_name]]]
        new_cpt = CPT(node_name, parents, cpt)
        CPT_list.append(new_cpt)
    
    #sub = sub+[main]
    sub_index = [comp.variables_dict[s] for s in sub]
    # 计算路径节点的条件概率表和重要度
    print('计算路径节点的条件概率表和重要度')
    importance_dict = {}
    for i in range(len(all_simple_paths)):
        node_name = 'path'+str(i)
        parents = []
        for node in all_simple_paths[i]:
            parents.append(node)
        parents_CGBR = []
        for node in parents:
            parents_CGBR.append(CGBR[comp.variables_dict[node]])
        cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,sub_index = sub_index,node_name='path')
        new_cpt = CPT(node_name, parents, cpt)
        CPT_list.append(new_cpt)
        importance_dict[node_name] = sum(parents_CGBR)/len(parents_CGBR)
    
    bayes_node = comp.names.copy()
    bayes_node.extend(list(importance_dict.keys()))
    bayes_node.append('Availability')

    # # 构建每个节点的条件概率表
    # for node in comp.names:
    #     new_cpt = CPT(node, [], [1,0])
    #     CPT_list.append(new_cpt)

    # 构建Availability节点的条件概率表
    print('构建Availability节点的条件概率表')
    cpt = get_middle_node(0.6,len(importance_dict),1,list(importance_dict.values()),sum(importance_dict.values()),0,0)
    new_cpt = CPT('Availability', list(importance_dict.keys()), cpt)
    CPT_list.append(new_cpt)

    # 基于条件概率表构建邻接矩阵
    adjacency_matrix = [[0 for j in range(len(bayes_node))] for i in range(len(bayes_node))]

    for i in range(len(bayes_node)):
        for j in range(len(CPT_list[i].parents)):
            adjacency_matrix[bayes_node.index(CPT_list[i].parents[j])][i] = 1

    # 构建贝叶斯网络
    bayesian_network = BayesianNetwork(len(comp.names), len(bayes_node), bayes_node, adjacency_matrix, CPT_list)

    return bayesian_network, importance_dict

def convert(bayes,state_list, fail_p, recovery_p, t, attacked_nodes):
    #p1 = math.exp(-(fail_p*t))
    #p2 = 1-p1
    #p3 = math.exp(-(recovery_p*t))
    #p4 = 1-p3
    #print(fail_p)
    #print(recovery_p)
    #print(attacked_nodes)
    new_state_list = {}
    for key,value in state_list.items():
        index_num=bayes.variables.index(key)
        if key not in attacked_nodes:
            continue
        #print(math.exp(-(fail_p[index_num]*t)))
        #print(math.exp(-(recovery_p[index_num]*t)))

        if value == 1:
            if random.random() <= math.exp(-(fail_p[index_num]*t)):
                new_state_list[key]=1
            else:
                new_state_list[key]=0
        if value == 0:
            if random.random() <= math.exp(-(recovery_p[index_num]*t)):
                new_state_list[key]=0
            else:
                new_state_list[key]=1
    #raise ValueError
    return new_state_list

def simulation(bayesian_netwotk:BayesianNetwork,state_dict:{},recovery_rate:[],fail_p_list:[],t,attacked_nodes):
    Availability_list = []
    Availability_list.append(1.0)
    availability = bayesian_netwotk.marginal_prob('Availability', state_dict)
    Availability_list.append(availability)
    if_stablize = False
    last_availability = availability
    count = 0
    while if_stablize == False:
        new_state_dict = convert(bayesian_netwotk,state_dict,fail_p_list,recovery_rate,t,attacked_nodes)
        availability = bayesian_netwotk.marginal_prob('Availability', new_state_dict)
        if availability == last_availability:
            count += 1
        else:
            count = 0
        if count == 6:
            if_stablize = True
        Availability_list.append(availability)
        last_availability = availability
        state_dict = new_state_dict
    return Availability_list

def sub_str(Availability_list):
    count=0
    start=0
    for i in range(2,len(Availability_list)):
        if Availability_list[i+1] == Availability_list[i]:
            count+=1
            start=i
        else:
            count=0
        
        if count==5:
            break
    
    return start-3

def calculation_resilience(num, all_Availability_list):#计算韧性
    A=100
    t1=math.e
    t2=2*math.e
    A3=100
    A2_list=[]
    t3_list=[]
    sum=0
    for i in range(num):
        A2_list.append(all_Availability_list[i][1]*100)
        t3_list.append(sub_str(all_Availability_list[i]))
    
    for i in range(num):
        sum+=(A2_list[i]*A3)/math.log(t3_list[i]*math.e-t2)
    
    re=(A/(math.log(t1)*num))*sum
    
    return re/1000000

# 动态模拟
def Dynamics(bayesian_netwotk:BayesianNetwork,marginal_prob_dict_list:[],attack_nums:int,fail_p_list:[],t, attacked_nodes):

    Availability_list = []
    # 获取第一个时间片的各个节点的状态
    state_dict = {}
    for i in range(bayesian_netwotk.com_nums):
        state_dict[bayesian_netwotk.variables[i]] = 1

    Availability_state1 = bayesian_netwotk.marginal_prob('Availability', state_dict)
    # 获得第二个时间片，不同攻击次数下的各个节点的状态
    attack_fail_p_list = []
    for i in range(1,attack_nums+1):
        attack_fail_p_list.append(i/(attack_nums+1))

    all_state_dict = []
    for i in range(attack_nums):
        # 获取恢复率
        recovery_rate = {}
        for node in bayesian_netwotk.variables:
            if node in marginal_prob_dict_list[i].keys():
                recovery_rate[node] = marginal_prob_dict_list[i][node]
        temp_state_list = [1 for j in range(bayesian_netwotk.com_nums)]
        for node in attacked_nodes:
            if node not in bayesian_netwotk.variables:
                continue
            j = bayesian_netwotk.variables.index(node)
            if random.random() < attack_fail_p_list[i]:
                temp_state_list[j] = 0
            
            # if temp_state_list[j] == 0:
            #     if random.random() < recovery_rate[bayesian_netwotk.variables[j]] * (1-attack_fail_p_list[i]):
            #         temp_state_list[j] = 1
            
        temp = {}
        for j in range(bayesian_netwotk.com_nums):
            temp[bayesian_netwotk.variables[j]] = temp_state_list[j]
        all_state_dict.append(temp)

    # 从第三个时间片开始，进行动态模拟
    all_Availability_list = []
    for i in range(attack_nums):
        recovery_rate = {}
        for node in bayesian_netwotk.variables:
            if node in marginal_prob_dict_list[i].keys():
                recovery_rate[node] = marginal_prob_dict_list[i][node]
        recovery_rate_list = list(recovery_rate.values())
        attacks = i+1
        #print(recovery_rate_list)
        new_recovery_rate_list = [re*(1-attacks/(attack_nums+1)) for re in recovery_rate_list]
        #print(new_recovery_rate_list)
        fail_p_list = [attacks/(100*(attack_nums+1))]*len(recovery_rate_list)
        #print(fail_p_list)
        #raise ValueError
        Availability_list=simulation(bayesian_netwotk,all_state_dict[i],new_recovery_rate_list,fail_p_list,t,attacked_nodes)
        all_Availability_list.append(Availability_list)

    # 计算韧性
    resilience = calculation_resilience(attack_nums, all_Availability_list)

    return resilience

def Draw_Dynamic_Bayesian_network(comp:Component_diagram, marginal_prob_dict, CGBR, importance_dict, bayesian_network: BayesianNetwork, js_path, re, comp_id):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "Component Node" # 组件节点
        },
        {
            "name": "Execute Path Node" # 韧性子属性节点
        },
        {
            "name": "Availability Node" # 韧性属性节点
        }
    ]

    link_nodes = set()
    for i in range(len(bayesian_network.graph)):
        for j in range(len(bayesian_network.graph[i])):
            if bayesian_network.graph[i][j] == 1:
                link = {}
                link["source"] = bayesian_network.variables[i] + '_'+str(comp_id)
                link_nodes.add(link["source"])
                link["target"] = bayesian_network.variables[j] + '_'+str(comp_id)
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
        data["id"] = comp.names[i]  + '_'+str(comp_id) # 节点id
        data["symbolSize"] = 45
        data["category"] = 0
        data["CGBR"] = CGBR[i] # 节点的CGBR值
        data["marginal_prob"] = marginal_prob_dict[comp.names[i]] # 节点为True的概率
        data["fixed"] = False
        data["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        data_list.append(data)

    # 添加贝叶斯网络其他节点
    for node in bayesian_network.variables:
        if node not in comp.names:
            if node+ '_'+str(comp_id) not in link_nodes:
                continue
            data = {}
            data["name"] = node+ '_'+str(comp_id)
            data["id"] = node + '_'+str(comp_id)
            data["symbolSize"] = 45
            if node == "Availability":
                data["category"] = 2
            else:
                data["category"] = 1
            if node in importance_dict.keys():
                data["CGBR"] = importance_dict[node]
            data["marginal_prob"] = None

            data["fixed"] = False
            data["itemStyle"] = {
                "normal": {
                    "opacity": 1
                }
            }
            data_list.append(data)

    # 添加边

                # 绘制贝叶斯网络
    
    json_data = {}
    json_data["data"] = data_list
    json_data["categories"] = categories
    json_data["links"] = link_list
    json_data["resilience"] = round(re, 5)

    return json_data

    # 写入js文件
    # json_file = 
    with open(js_path, 'w') as f:
        # 变量名为graph

        f.write('var graph = ')
        json.dump(json_data, f, indent=4)

def Dynamic_Bayesian_network_MAIN(comp:Component_diagram, static_bayesian_network_path, dynamic_Bayesian_network_path, Attack_node = None, comp_id = None, main='',sub=[]):
    # 计算静态贝叶斯网络边缘概率
    # 静态贝叶斯网络的存储路径
    # 计算静态贝叶斯网络边缘概率
    # 静态贝叶斯网络的存储路径
    static_marginal_prob_dict_list, CGBR, comp, attacked_nodes, static_js_data = Static_Bayesian_network_MAIN(comp, static_bayesian_network_path, Attack_node, comp_id,main = main,sub=sub)

    print('静态贝叶斯网络评估结束')
    #raise ValueError
    # 构建动态贝叶斯网络
    bayesian_network, importance_dict = build_Dynamic_Bayesian_network(comp, CGBR, static_marginal_prob_dict_list[0],main=main,sub=sub)

    fail_p_list = [0.01] * len(comp.names)

    # 动态模拟
    # resilience = Dynamics(bayesian_network, static_marginal_prob_dict, 9, fail_p_list, math.e)

    Simulation_times = 100
    resilience_list = []
    for i in range(Simulation_times):
        print('第',i+1,'次模拟......')
        resilience_list.append(Dynamics(bayesian_network, static_marginal_prob_dict_list, 9, fail_p_list, math.e, attacked_nodes))

    # 绘制动态贝叶斯网络
    Dynamic_js_data = Draw_Dynamic_Bayesian_network(comp, static_marginal_prob_dict_list[0], CGBR, importance_dict, bayesian_network, dynamic_Bayesian_network_path, np.mean(resilience_list), comp_id)

    print(resilience_list)
    print(np.mean(resilience_list))

    return static_js_data, Dynamic_js_data

if __name__ == "__main__":
    
    file1=r"E:\Graduation_Design\Input_process\网上商城系统.wsd"
    comp = comp_wsd_to_txt(file1)


