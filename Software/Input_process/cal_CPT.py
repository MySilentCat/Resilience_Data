# 计算条件概率表
# 时间：2023/10/24
import numpy as np
from Input_process.deal_plantUML import *
def cal_CGBR(adjacency_matrix, node_num, Iteration_num=200):
    # CGBR Call Graph Based Ranking
    adjacency_matrix = np.array(adjacency_matrix)
    
    # 统计被调用函数的数量
    call_num = 0
    # 将邻接矩阵的每一列求和
    for i in range(node_num):
        call_num += np.sum(adjacency_matrix[:,i])
        # 如果该列的和大于0，说明该函数被调用过

    # 计算阻尼因子
    damping_factor = call_num / node_num**2

    # 初始化CGBR
    CGBR = np.zeros(node_num)
    for i in range(node_num):
        CGBR[i] = 1

    # 迭代计算CGBR
    last_CGBR = CGBR.copy()

    for i in range(Iteration_num):
        #print(i)
        for m in range(node_num):
            summation = 0
            for k in range(node_num):
                # 如果k调用了m
                if adjacency_matrix[k,m] == 1:
                    # k的CGBR值除以k调用其他函数的数量
                    summation += CGBR[k] / np.sum(adjacency_matrix[k,:])
            CGBR[m] = (1 - damping_factor) + damping_factor * summation
        
        # 判断是否收敛
        if np.sum(np.abs(CGBR - last_CGBR)) < 0.0001:
            break
        else:
            last_CGBR = CGBR.copy()

    return CGBR.tolist()

def to_bin(a,long):
    o_bin=bin(a)[2:]
    out_bin=o_bin.rjust(long,'0')
    return out_bin

def get_middle_node(a,node_nums,nn,count,nu,ss,k,if_attacked = 0, parent_index_list = [], attack_p = 0.6, node_name = None,sub_index = []):

    bin_list=[]
    for i in range(pow(2,node_nums)):
        bin_list.append(to_bin(i,node_nums))
    
    p_list=[]
    for b in bin_list:
        one_nums=0
        list_1=[]
        for i in range(node_nums):
            if b[i]=="1":
                one_nums+=1
                list_1.append(i)

        attacked = 0
        if if_attacked == 1 and b[-1] == '1':
            attacked = 1

        #print(b)
        #print(p_list)
        if one_nums==0:
            #p_list.append(0)
            temp = 0
            for inter_index in parent_index_list:
                if node_name == 'sub':
                    temp+=(nn/nu)*count[inter_index]*(0/4)
                else:
                    temp+=(nn/nu)*count[inter_index]*(3/4)
            p_list.append(temp)
        elif one_nums==node_nums:
            p_list.append(1)
        elif one_nums>0 and one_nums<node_nums:
            temp=0
            for nums in list_1:
                temp+=(nn/nu)*count[nums]
            
            for inter_index in parent_index_list:
                if inter_index not in list_1:
                    if node_name == 'sub':
                        temp+=(nn/nu)*count[inter_index]*(0/4)
                    else:
                        temp+=(nn/nu)*count[inter_index]*(3/4)
                    #p_list.append(temp)
            
            if k>0:
                if b[k-1]=="1":
                    temp=round(temp-0.1,4)
            temp1=pow(a,node_nums-len(list_1))
            #temp=(nn/node_nums)*one_nums
            for i in range(node_nums):
                if b[i] == '0' and i not in parent_index_list and node_name == 'main':
                    temp = 0
                if b[i] == '0' and i in sub_index and node_name == 'path':
                    temp = 0
                    
            p_list.append(round(temp,4))
        
        if attacked == 1:
            p_list[-1] -= attack_p
    
    #print(p_list)
    
    p_list_no=[]
    for p in p_list:
        p_list_no.append(round(1-p,4))

    cpt = []
    for i in range(len(p_list)):
        a=round(p_list[i]+ss,4)
        if a>1:
            a=1
        if a<0:
            a=0
        b=round(p_list_no[i]-ss,4)
        if b<0:
            b=0
        if b>1:
            b=1
        if a+b != 1:
            b = round(1-a,4)
        cpt.append([a,b])
    if node_name == 'main':
        print(cpt)
        #raise ValueError
    return cpt

# 计算条件概率表
def cal_cpt(comp:Component_diagram):
    adjacency_matrix = np.array(comp.adjacency_matrix)
    node_num = comp.count
    CGBR = cal_CGBR(adjacency_matrix, node_num)
    #CGBR = CGBR.tolist()

    cpt_dict = {}
    for i in range(node_num):
        node_name = comp.names[i]
        # if node_name == 'Database':
        #     #print()
        
        # 该节点的父节点
        parents = comp.parents[node_name]
        # 该节点的父节点的CGRR值
        parents_CGBR = []
        for parent in parents:
            parents_CGBR.append(CGBR[comp.variables_dict[parent]])
        
        interface_parents = []
        if node_name in comp.interface.keys():
            interface_parents = comp.interface[node_name]

        parent_index_list = []
        for inter in interface_parents:
            parent_index = parents.index(inter)
            parent_index_list.append(parent_index)
            cgbr = parents_CGBR[parent_index]
            parents_CGBR[parent_index] = cgbr/3


        # 根据CGBR值计算条件概率表
        cpt = get_middle_node(0.6,len(parents),1,parents_CGBR,sum(parents_CGBR),0,0,0,parent_index_list)
        cpt_dict[node_name] = cpt

    return cpt_dict

if __name__ == "__main__":

    # 计算CGBR
    file1=r"E:\Graduation_Design_Docker\Input_process\网上商城系统.wsd"
    comp = comp_wsd_to_txt(file1)
    # CGBR = cal_CGBR(comp.adjacency_matrix, comp.count)
    # 二维矩用numpy的array表示
    adjacency_matrix = np.array(comp.adjacency_matrix)

    cpt_dict = cal_cpt(comp)
    #print(cpt_dict)


