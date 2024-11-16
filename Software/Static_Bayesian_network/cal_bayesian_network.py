# 计算贝叶斯网络
# 时间：2023/10/24
from pgmpy.models import BayesianNetwork as pgmpy_BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# 条件概率表数据结构
class CPT:
    def __init__(self, variable, parents, values):
        self.variable = variable # 节点
        self.parents = parents # 父节点
        self.values = values # 条件概率表

# 贝叶斯网络类
class BayesianNetwork:
    def __init__(self, com_nums, nums, variables, graph, cpts = []):
        self.com_nums = com_nums # 构建该贝叶斯网络的组件图的组件数
        self.nums = nums # 贝叶斯网络的节点数
        self.variables = variables # 贝叶斯网络的节点列表
        self.graph = graph # 贝叶斯网络的邻接矩阵
        self.cpts = cpts # 贝叶斯网络的条件概率表列表

        # 创建一个名字与编号的字典，便于查找
        index_list = [i for i in range(self.nums)]
        self.variables_dict = dict(zip(self.variables, index_list))

        self.error = 0 # 0表示没有错误，1表示有错误
        self.exists_nodes = []

        self.bayesian_network = self.build_bayesian_network() # 构建贝叶斯网络

    # 使用pgmpy库构建贝叶斯网络
    def build_bayesian_network(self):
        if len(self.variables) != len(self.cpts):
            # 节点数与条件概率表数不相等
            self.error = 1
            return None

        # 贝叶斯网络结构建模
        nodes = set()
        print(self.graph)
        Link_list = []
        for i in range(self.nums):
            for j in range(self.nums):
                if self.graph[i][j] == 1:
                    Link_list.append((self.variables[i], self.variables[j]))
                    nodes.add(self.variables[i])
                    nodes.add(self.variables[j])
        print(Link_list)
        #raise ValueError
        bayesian_network = pgmpy_BayesianNetwork(Link_list)
        self.exists_nodes = list(nodes)

        # 贝叶斯网络条件概率表建模
        for i in range(self.nums):
            
            cpt = self.cpts[i]
            variable = cpt.variable
            if variable not in nodes:
                continue
            print('为节点',variable,'构建条件概率表')
            parents = cpt.parents
            print(parents)
            evidence = [2 for i in range(len(parents))]
            temp1 = []
            temp2 = []
            temp = []
            values = cpt.values
            print(values)
            if len(values) != 2 ** len(parents):
                # 条件概率表的行数不正确
                self.error = 1
                print('条件概率表的行数不正确')
                return None
            for j in range(len(values)):
                if values[j][0] + values[j][1] != 1:
                    # 条件概率表的值不正确
                    print('条件概率表的值不正确')
                    self.error = 1
                    return None
                temp1.append(values[j][0])
                temp2.append(values[j][1])
            temp.append(temp2)
            temp.append(temp1)

            # re = temp2.copy()
            # re.reverse()
            # print(re)
            # res = '\n'.join(str(i) for i in re)
            # re_file = open('re.txt', 'w')
            # re_file.write(res)
            if len(parents) == 0:
                # 无父节点
                cpd = TabularCPD(variable, 2, temp)
                # print(variable)
                bayesian_network.add_cpds(cpd)
            else:
                # 有父节点
                cpd = TabularCPD(variable, 2, temp, parents, evidence)
                bayesian_network.add_cpds(cpd)

        return bayesian_network
    
    # 计算贝叶斯网络的边缘概率
    def marginal_prob(self, query, evidence):
        if self.error == 1:
            # 贝叶斯网络有错误
            return None

        #print(evidence)
        # 计算边缘概率
        if query == 'Restoration':
            print(query)
        
        new_evidence = {}
        for node, evi in evidence.items():
            if node in self.exists_nodes:
                new_evidence[node] = evi
        if query in self.exists_nodes:
            infer = VariableElimination(self.bayesian_network)
            marginal_prob_query = infer.query(variables=[query], evidence=new_evidence)
            marginal_prob_value = marginal_prob_query.values[1]
            #print(query, marginal_prob_value)
            return marginal_prob_value
        else:
            return 0
