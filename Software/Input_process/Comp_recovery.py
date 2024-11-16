# 组件图恢复
# 2023.11.08

# 构造每个函数的特征向量
'''
特征向量的内容
1、邻接矩阵, 每个数字表示依赖程度
2、返回类型
3、参数类型
4、所在文件
'''
import networkx as nx
import json
import os
os.environ['NLTK_DATA'] = os.path.abspath('Input_process/nltk_data/')
import math
import copy
import nltk

import Input_process.CodeInfoExtract
import Input_process.deal_plantUML

RESERVED_WORDS = [
    "int",
    "long",
    "short",
    "float",
    "double",
    "char",
    "unsigned",
    "signed",
    "const",
    "void",
    "volatile",
    "enum",
    "struct",
    "union",
    "if",
    "else",
    "goto",
    "switch",
    "case",
    "do",
    "while",
    "for",
    "continue",
    "break",
    "return",
    "default",
    "typedef",
    "auto",
    "register",
    "extern",
    "static",
    "return",
    "sizeof"
  ]
class func_information:
    def __init__(self, id, label, func_name, func_file, func_info):
        self.id = id
        self.label = label
        self.func_name = func_name
        self.func_file = func_file
        self.func_info = func_info
        self.Children = {}
        self.Parent = {}
        self.data_dependence = {}

        self.meraged_func = {}

        self.feature_vector = { }

def get_func_info(sdg: nx.multidigraph, funcInfo_dict: {}):
    Func_dict = {}

    for node in sdg.nodes:
        node_info = sdg.nodes[node]
        if 'label' in node_info and 'code_file_path' in node_info:
            id = node
            label = node_info['label'].replace('"','')
            func_name = label.split(':')[-1]
            func_file = node_info['code_file_path'].replace('"','')
            func_info = funcInfo_dict[label]
            new_func = func_information(id,label,func_name,func_file,func_info)
            Func_dict[label] = new_func
    sum_control_weight = 0
    sum_data_weight = 0
    for edge in sdg.edges()._viewer:
        start_node = edge[0]
        end_node = edge[1]
        edge_info = sdg.edges[edge]
        print(edge_info)
        data_dependence_weight = 0
        weight = 0
        if 'style' in edge_info:
            if edge_info['style'] == 'dotted':
                if "count" in edge_info.keys():
                    data_dependence_weight = int(edge_info["count"])
                    sum_data_weight += data_dependence_weight
                else:
                    data_dependence_weight = 1
                    sum_data_weight += data_dependence_weight
        else:
            if "count" in edge_info.keys():
                weight = int(edge_info["count"])
                sum_control_weight += weight
            else:
                weight = 1
                sum_control_weight += weight

        print(Func_dict)
        print(start_node)
        print(end_node)
        start_key = None
        end_key = None
        for func_key,func in Func_dict.items():
            if func.id == start_node:
                start_key = func_key
            
            if func.id == end_node:
                end_key = func_key

            if start_key != None and end_key != None:
                break
        
        if weight!=0:
            if end_key not in Func_dict[start_key].Children.keys():
                Func_dict[start_key].Children[end_key] = weight
            else:
                Func_dict[start_key].Children[end_key] += weight

            if start_key not in Func_dict[end_key].Parent.keys():
                Func_dict[end_key].Parent[start_key] = weight
            else:
                Func_dict[end_key].Parent[start_key] += weight

        if data_dependence_weight!=0:
            if end_key not in Func_dict[start_key].data_dependence.keys():
                Func_dict[start_key].data_dependence[end_key] = data_dependence_weight
            else:
                Func_dict[start_key].data_dependence[end_key] += data_dependence_weight

    return Func_dict, sum_control_weight, sum_data_weight

def cal_structural_dependencies(Func_dict, sum_control_weight, sum_data_weight):
    # 计算结构依赖矩阵
    # 1、初始化结构依赖矩阵
    # 2、遍历每个函数，根据公式计算结构依赖矩阵中对应位置的值
    # 3、返回结构依赖矩阵
    Structural_Dependencies = {}
    print(sum_control_weight)
    print(sum_data_weight)
    control_weight = sum_control_weight / (sum_control_weight + sum_data_weight)
    data_weight = sum_data_weight / (sum_control_weight + sum_data_weight)
    for func1, func_info1 in Func_dict.items():
        if func1 not in Structural_Dependencies.keys():
            Structural_Dependencies[func1] = {}
        for func2, func_info2 in Func_dict.items():
            if func2 not in Structural_Dependencies.keys():
                Structural_Dependencies[func2] = {}
            Structural_Dependencies[func2][func1] = 0
            if func1 == func2:
                continue
            control_freq = 0
            data_freq = 0
            if func2 in func_info1.Children.keys():
                control_freq = func_info1.Children[func2]
            if func2 in func_info1.data_dependence.keys():
                data_freq = func_info1.data_dependence[func2]

            Structural_Dependencies[func2][func1] = control_weight * control_freq + data_weight * data_freq

    # 归一化
    for func1, func_info1 in Func_dict.items():
        sum_ = 0
        for func2, func_info2 in Func_dict.items():
            sum_ += Structural_Dependencies[func1][func2]
        if sum_ == 0:
            continue
        for func2, func_info2 in Func_dict.items():
            Structural_Dependencies[func1][func2] /= sum_
            

    return Structural_Dependencies
            

def cal_Directory_Dependencies(Func_dict):
    # 计算目录依赖矩阵
    # 1、初始化目录依赖矩阵
    # 2、遍历每个函数，如果函数所在文件不同，则在目录依赖矩阵中对应位置+1
    # 3、返回目录依赖矩阵
    Directory_Dependencies = {}
    for func1, func_info1 in Func_dict.items():
        Directory_Dependencies[func1] = {}
        for func2, func_info2 in Func_dict.items():
            Directory_Dependencies[func1][func2] = 0
            if func1 == func2:
                continue
            file1 = func_info1.func_info['header']
            file2 = func_info2.func_info['header']
            dir_list1 = file1.split('/')
            dir_list2 = file2.split('/')
            # 找根目录
            root_dir = dir_list1[0]
            # 找最近公共目录，即最近公共祖先
            LCA = ''
            LCA_index = 0
            for i in range(min(len(dir_list1), len(dir_list2))):
                if dir_list1[i] == dir_list2[i]:
                    LCA = dir_list1[i]
                    LCA_index = i
                else:
                    break
            root_index = 0
            d_root_LCA = LCA_index - root_index
            d_file1_LCA = len(dir_list1) - LCA_index + 1
            d_file2_LCA = len(dir_list2) - LCA_index + 1
            d_file1_file2 = d_file1_LCA + d_file2_LCA
            Directory_Dependencies[func1][func2] = (1+ d_root_LCA) / (1 + d_file1_file2 + d_root_LCA)

    return Directory_Dependencies

def remove_camel_case(text: str) -> list:
    words = []
    word = ''
    for char in text:
        if char.isupper() and len(word) > 1:
            if word:
                words.append(word)
            word = char.lower()
        else:
            word += char
    if word:
        words.append(word)
    return " ".join(words)

def cal_Semantic_Dependencies(Func_dict, PLCG_nx):
    # 计算语义依赖矩阵
    # 1、获取语义相关信息
    Semantic_info = {}
    word_num = {}
    lib_node = {}
    for node in PLCG_nx.nodes:
        node_info = PLCG_nx.nodes[node]
        if node_info['file'].replace('"','') == 'Library function':
            lib_node[node] = node_info['Lib'].replace('"','').split('.')[0]

    call_lib = {}
    for edge in PLCG_nx.edges:
        source_node = edge[0]
        target_node = edge[1]
        if target_node in lib_node.keys():
            source_info = PLCG_nx.nodes[source_node]
            label = source_info['label'].replace('"','')
            if label not in call_lib.keys():
                call_lib[label] = []
            call_lib[label].append(lib_node[target_node])

    for func, func_info in Func_dict.items():
        temp_info = []
        # 获取函数名
        func_name = remove_camel_case(func_info.func_name).replace('_', ' ')
        temp_info.append(func_name)
        #获取参数名
        param_name = []
        for param in func_info.func_info['paramList']:
            temp_param_name = remove_camel_case(param['name']).replace('_', ' ')
            param_name.append(temp_param_name)
        temp_info.extend(param_name)
        # 获取返回值类型
        return_type = remove_camel_case(func_info.func_info['returnType']).replace('_', ' ')
        temp_info.append(return_type)
        # 获取函数体变量使用情况
        # var_name = []
        # for var in func_info.func_info['variables']:
        #     temp_var_name = remove_camel_case(var).replace('_', ' ')
        #     temp_info.append(temp_var_name)
        # temp_info.extend(var_name)
        # 注释信息
        temp_info.extend([remove_camel_case(aoon.replace('_', ' ')) for aoon in func_info.func_info['anno']])
        # 库函数使用信息
        if func in call_lib.keys():
            temp_info.extend([lib.replace('_', ' ') for lib in call_lib[func]])

        # 去除数字
        temp_info = [''.join([i for i in s if not i.isdigit()]) for s in temp_info]

        # 使用nltk进行tokenize
        temp_info = [nltk.word_tokenize(s) for s in temp_info]

        # 转为小写
        temp_info = [[s.lower() for s in l] for l in temp_info]

        # 去除标点
        temp_info = [[s for s in l if s.isalnum()] for l in temp_info]

        # 去除停用词
        stop_words = set(nltk.corpus.stopwords.words('english'))
        temp_info = [[s for s in l if s not in stop_words] for l in temp_info]

        # 使用nltk进行stemming
        stemmer = nltk.stem.PorterStemmer()
        temp_info = [[stemmer.stem(s) for s in l] for l in temp_info]

        # 去除保留字
        temp_info = [[s for s in l if s not in RESERVED_WORDS] for l in temp_info]

        words = [s for l in temp_info for s in l]
        for word in words:
            if word not in word_num.keys():
                word_num[word] = 0
            word_num[word] += 1
        Semantic_info[func] = words

    print(Semantic_info)
    # 2、计算每个函数tf-idf值
    tf_idf = {}
    for func, words in Semantic_info.items():
        tf_idf[func] = {}
        for word in words:
            if word in tf_idf[func].keys():
                continue
            tf = words.count(word) / len(words)
            tf_idf[func][word] = tf * (math.log((1+len(Func_dict)) / (1+word_num[word]))+1)
        
        sum_ = 0
        for value in tf_idf[func].values():
            sum_ += value ** 2
        sum_ = sum_ ** 0.5
        for word, value in tf_idf[func].items():
            tf_idf[func][word] = value / sum_
        
    print(tf_idf)

    # 3、计算每个函数之间的语义相似度, 采用余弦相似度
    Semantic_Dependencies = {}
    for func1, tf_idf1 in tf_idf.items():
        Semantic_Dependencies[func1] = {}
        for func2, tf_idf2 in tf_idf.items():
            Semantic_Dependencies[func1][func2] = 0
            if func1 == func2:
                continue
            for word, value in tf_idf1.items():
                if word in tf_idf2.keys():
                    Semantic_Dependencies[func1][func2] += value * tf_idf2[word]
            if (len(tf_idf1) * len(tf_idf2)) ** 0.5 != 0:
                Semantic_Dependencies[func1][func2] /= (len(tf_idf1) * len(tf_idf2)) ** 0.5

    print(Semantic_Dependencies)

    return Semantic_Dependencies

def CL_HAC(Func_dict, structural_Dependencies, Directory_Dependencies, Semantic_Dependencies, num):
    # 采用完全连锁层次聚类方法，逐渐将相似度最高的节点进行合并
    # 1、计算每两个节点之间的依赖度，为结构依赖度、目录依赖度、语义依赖度的加权和
    # 2、合并依赖度最高的两个节点
    # 3、重复2，直到聚类数目为num
    # 4、返回聚类结果

    cluster_result = {}
    for func, func_info in Func_dict.items():
        file = func_info.func_info['header']
        if file not in cluster_result.keys():
            cluster_result[file] = []
        cluster_result[file].append(func)
    id = 0
    new_cluster_result_ = {}
    for file, funcs in cluster_result.items():
        new_cluster_result_[id] = funcs
        id += 1
    best_cluster_result = new_cluster_result_
    print(best_cluster_result)

    #raise ValueError

    # 计算依赖度矩阵
    dependency_matrix = {}
    for func1, func_info1 in Func_dict.items():
        dependency_matrix[func1] = {}
        for func2, func_info2 in Func_dict.items():
            dependency_matrix[func1][func2] = 0
            if func1 == func2:
                continue
            # 依赖度为结构依赖度、目录依赖度、语义依赖度的均值
            dependency_matrix[func1][func2] = 0.1*structural_Dependencies[func1][func2] + 0.85*Directory_Dependencies[func1][func2] + 0.05*Semantic_Dependencies[func1][func2]

            #dependency_matrix[func1][func2] = (structural_Dependencies[func1][func2] + Directory_Dependencies[func1][func2] + Semantic_Dependencies[func1][func2]) / 3
    
    # 每个函数为一个聚类, 构建cluster之间的依赖度矩阵
    cluster_result = best_cluster_result
    cluster_dependency_matrix = {}
    for id1,funcs1 in cluster_result.items():
        cluster_dependency_matrix[id1] = {}
        for id2,funcs2 in cluster_result.items():
            if id1 == id2:
                cluster_dependency_matrix[id1][id2] = 0
            else:
                min_dep = 100000
                for func1 in funcs1:
                    for func2 in funcs2:
                        if dependency_matrix[func1][func2]<min_dep:
                            cluster_dependency_matrix[id1][id2] = min_dep

    # 采用完全连锁层次聚类方法，每次找到依赖度最高的两个cluster进行合并，更新依赖度矩阵时选择较小的依赖度作为新的依赖度
    max_silhouette_coefficient = 0
    #best_cluster_result = {}
    while len(cluster_result) > 5:
        max_dependency = 0
        max_cluster1 = None
        max_cluster2 = None
        for cluster1, funcs1 in cluster_result.items():
            for cluster2, funcs2 in cluster_result.items():
                if cluster1 != cluster2 and cluster_dependency_matrix[cluster1][cluster2] > max_dependency:
                    max_dependency = cluster_dependency_matrix[cluster1][cluster2]
                    max_cluster1 = cluster1
                    max_cluster2 = cluster2

        # 合并
        cluster_result[max_cluster1].extend(cluster_result[max_cluster2])
        cluster_result.pop(max_cluster2)

        # 更新依赖度矩阵,选择较小的依赖度作为新的依赖度
        cluster_dependency_matrix1 = cluster_dependency_matrix[max_cluster1]
        cluster_dependency_matrix2 = cluster_dependency_matrix[max_cluster2]
        cluster_dependency_matrix.pop(max_cluster2)
        # print(cluster_dependency_matrix1)
        # raise ValueError
        new_cluster_dependency_matrix = {}
        for cluster in cluster_dependency_matrix1.keys():
            new_cluster_dependency_matrix[cluster] = min(cluster_dependency_matrix1[cluster], cluster_dependency_matrix2[cluster])
        
        # 替换cluster1的依赖度矩阵
        cluster_dependency_matrix[max_cluster1] = new_cluster_dependency_matrix

        # 删除其他cluster对应的cluster2的依赖度矩阵
        for cluster in cluster_dependency_matrix.keys():
            cluster_dependency_matrix[cluster].pop(max_cluster2)

        # 计算轮廓系数
        if len(cluster_result) < 20:
            silhouette_coefficient = cal_silhouette_coefficient(Func_dict, cluster_result, dependency_matrix)
            if silhouette_coefficient > max_silhouette_coefficient:
                max_silhouette_coefficient = silhouette_coefficient
                best_cluster_result = {}
                best_cluster_result = copy.deepcopy(cluster_result)
        else:
            max_silhouette_coefficient = 0
            best_cluster_result = {}
            best_cluster_result = copy.deepcopy(cluster_result)

        print(cluster_result)
        
    return best_cluster_result, dependency_matrix

def cal_silhouette_coefficient(Func_dict, cluster_result, dependency_matrix):
    # 计算聚类结果的轮廓系数
    silhouette_coefficient = 0
    distance_matrix = {} # 函数之间的距离，即为依赖度的倒数
    for func1, func_info1 in Func_dict.items():
        distance_matrix[func1] = {}
        for func2, func_info2 in Func_dict.items():
            distance_matrix[func1][func2] = 0
            if func1 == func2:
                continue
            if dependency_matrix[func1][func2] == 0:
                distance_matrix[func1][func2] = 100000000
            else:
                distance_matrix[func1][func2] = 1 / dependency_matrix[func1][func2]

    for cluster, funcs in cluster_result.items():
        if len(funcs) == 1:
            continue
        for func1 in funcs:
            a = 0
            b = 0
            for func2 in funcs:
                if func1 == func2:
                    continue
                a += distance_matrix[func1][func2]
            a /= len(funcs) - 1
            min_b = 100000000
            for cluster2, funcs2 in cluster_result.items():
                if cluster2 == cluster:
                    continue
                b = 0
                for func2 in funcs2:
                    b += distance_matrix[func1][func2]
                b /= len(funcs2)
                if b < min_b:
                    min_b = b
            silhouette_coefficient += (min_b - a) / max(a, min_b)
    silhouette_coefficient /= len(Func_dict)
    print('轮廓系数为：', silhouette_coefficient)
    return silhouette_coefficient

def set_feature_vector(Func_dict):
    # 设置每个函数的特征向量
    feature_vector = {}
    file_dict = {}
    param_dict = {}
    return_type_dict = {}
    for func, func_info in Func_dict.items():
        feature_vector[func] = 0
        header = func_info.func_info['header']
        source = func_info.func_info['source']
        if header not in file_dict.keys():
            file_dict[header] = 0
        if source not in file_dict.keys():
            file_dict[source] = 0
        for param in func_info.func_info['paramList']:
            if param['type'] not in param_dict.keys():
                param_dict[param['type']] = 0
        return_type = func_info.func_info['returnType']
        if 'returnType: ' + return_type not in return_type_dict.keys():
            return_type_dict['returnType: ' + return_type] = 0
        
    feature_vector.update(file_dict)
    feature_vector.update(param_dict)
    feature_vector.update(return_type_dict)
    
    for func, func_info in Func_dict.items():
        func_info.feature_vector = feature_vector.copy()
        for child, count in func_info.Children.items():
            func_info.feature_vector[child] = count
        header = func_info.func_info['header']
        source = func_info.func_info['source']
        func_info.feature_vector[header] = 1
        func_info.feature_vector[source] = 1
        for param in func_info.func_info['paramList']:
            func_info.feature_vector[param['type']] +=1
        return_type = func_info.func_info['returnType']
        func_info.feature_vector['returnType: ' + return_type] = 1
        
        print(func_info.feature_vector)

    return Func_dict

def func_cluster(Func_dict, num):
    # 采用层次聚类方法，逐渐将相似度最高的节点进行合并
    # 1、计算每个节点的相似度，采用余弦相似度
    # 2、合并相似度最高的两个节点, 更新特征向量，更新相似度矩阵
    # 3、重复2，直到聚类数目为num
    # 4、返回聚类结果

    # 计算相似度矩阵
    similarity_matrix = {}
    for func1, func_info1 in Func_dict.items():
        similarity_matrix[func1] = {}
        for func2, func_info2 in Func_dict.items():
            similarity_matrix[func1][func2] = 0
            for key, value in func_info1.feature_vector.items():
                if key in func_info2.feature_vector.keys():
                    similarity_matrix[func1][func2] += value * func_info2.feature_vector[key]
            similarity_matrix[func1][func2] /= (len(func_info1.feature_vector) * len(func_info2.feature_vector)) ** 0.5

    # 合并相似度最高的两个节点
    while len(Func_dict) > num:
        max_similarity = 0
        max_func1 = None
        max_func2 = None
        for func1, func_info1 in Func_dict.items():
            for func2, func_info2 in Func_dict.items():
                if func1 != func2 and similarity_matrix[func1][func2] > max_similarity:
                    max_similarity = similarity_matrix[func1][func2]
                    max_func1 = func1
                    max_func2 = func2
        
        # 合并
        # 更新特征向量，对应key的value相加
        Func_dict[max_func1].feature_vector.update(Func_dict[max_func2].feature_vector)
        Func_dict[max_func1].meraged_func[max_func2] = Func_dict[max_func2]
        # 更新Children和Parent，对应key的value相加
        Func_dict[max_func1].Children.update(Func_dict[max_func2].Children)
        Func_dict[max_func1].Parent.update(Func_dict[max_func2].Parent)
        # Func_dict.pop(max_func2)

        # 将max_func2的Children和Parent中的max_func2替换为max_func1
        for child, count in Func_dict[max_func2].Children.items():
            # Func_dict[max_func1].Children[child] += count
            Func_dict[child].Parent.pop(max_func2)
            Func_dict[child].Parent[max_func1] = Func_dict[max_func1].Children[child]
        for parent, count in Func_dict[max_func2].Parent.items():
            # Func_dict[max_func1].Parent[parent] += count
            Func_dict[parent].Children.pop(max_func2)
            Func_dict[parent].Children[max_func1] = Func_dict[max_func1].Parent[parent]

        Func_dict.pop(max_func2)


        # 更新相似度矩阵
        similarity_matrix.pop(max_func2)
        for func1, func_info1 in Func_dict.items():
            similarity_matrix[func1].pop(max_func2)
            similarity_matrix[func1][max_func1] = 0
            for key, value in func_info1.feature_vector.items():
                if key in Func_dict[max_func1].feature_vector.keys():
                    similarity_matrix[func1][max_func1] += value * Func_dict[max_func1].feature_vector[key]
            similarity_matrix[func1][max_func1] /= (len(func_info1.feature_vector) * len(Func_dict[max_func1].feature_vector)) ** 0.5

    return Func_dict

def get_Attacked_Func(PLCG_nx):
    # 所有涉及输入输出的函数，均为易受攻击函数
    # 存储所有流输出/输入标准库
    input_output_lib = ['iostream', 'iomanip', 'ios', 'istream', 'ostream', 'sstream', 'fstream', 'iosfwd', 'streambuf', 'cstdio', 'cwchar', 'stdio', 'stdlib', 'conio', 'cstdlib', 'string', # 输入输出
                        'socket', 'curl', 'in', 'inet', 'asio', 'winnet', 'netdb', 'unistd', 'windows', 'winsock2' # 网络
                        'sql', 'sqlext', 'mysql', 'sqlite3', 'libpq-fe', 'oci', 'frontend', 'soci', 'database', 'QtSql', 'Session'] # 数据库
    
    lib_node = {}
    for node in PLCG_nx.nodes:
        node_info = PLCG_nx.nodes[node]
        if node_info['file'].replace('"','') == 'Library function':
            lib_node[node] = node_info['Lib'].replace('"','').split('.')[0]

    call_lib = {}
    for edge in PLCG_nx.edges:
        source_node = edge[0]
        target_node = edge[1]
        if target_node in lib_node.keys():
            source_info = PLCG_nx.nodes[source_node]
            label = source_info['label'].replace('"','')
            if label not in call_lib.keys():
                call_lib[label] = []
            call_lib[label].append(lib_node[target_node])

    print("call_lib:", call_lib)
    Attacked_func = []
    for func, libs in call_lib.items():
        print(libs)
        for lib in libs:
            print(lib)
            if lib in input_output_lib:
                Attacked_func.append(func)
                break

    print("Attacked_func:", Attacked_func)
    #raise ValueError
    return Attacked_func

# 构建组件图
def build_component_graph(Func_dict, cluster_result, project_path):
    print('构建组件图')
    print(cluster_result)
    comp = Input_process.deal_plantUML.Component_diagram(len(cluster_result))
    func_cluster = {}
    for cluster, funcs in cluster_result.items():
        node_name = 'cluster' + str(cluster)
        comp.names.append(node_name)
        for func in funcs:
            func_cluster[func] = node_name
    
    for func, func_info in Func_dict.items():
        if func not in func_cluster.keys():
            continue
        parent_cluster = func_cluster[func]
        if parent_cluster not in comp.children.keys():
            comp.children[parent_cluster] = []
        for child, count in func_info.Children.items():
            child_cluster = func_cluster[child]
            if parent_cluster != child_cluster:
                if child_cluster not in comp.children[parent_cluster]:
                    print('zujiantubian')
                    comp.children[parent_cluster].append(child_cluster)

    print(comp.children)
    
    comp.set_index()
    comp.build_adjacency_matrix()
    comp.build_parents_children()
    comp.build_adjacency_matrix()

    # # 将组件图存到networkx
    # comp_nx = nx.DiGraph()
    # for node in comp.names:
    #     comp_nx.add_node(node)
    # for i in range(len(comp.adjacency_matrix)):
    #     for j in range(len(comp.adjacency_matrix)):
    #         if comp.adjacency_matrix[i][j] == 1:
    #             print(i,j)
    #             comp_nx.add_edge(comp.names[i], comp.names[j])
    # # 将组件图存到dot
    # comp_dot = nx.nx_pydot.to_pydot(comp_nx)
    # comp_dot.write(project_path + '/comp1.dot')
    #Attacked_node = list(set(Attacked_node))
    return comp

def get_comp_num(file_list, project_path):
    # 获取project_path+'/code'下的所有直接子文件夹和文件
    dir_list = [project_path+'/code']
    
    while len(dir_list) <= 1:
        last_path = dir_list[0].replace('\\', '/')
        if os.path.isdir(dir_list[0]) == False:
            return 1
        dir_list = os.listdir(dir_list[0])
        for i in range(len(dir_list)):
            dir_list[i] = last_path + '/' + dir_list[i]
            dir_list[i] = dir_list[i].replace('\\', '/')
        

        # 删除不在file_list中的文件
        remove_list = []
        for dir in dir_list:
            # dir_path = project_path+'/code/'+dir
            # dir_path = dir_path.replace('\\', '/')
            find = False
            for file in file_list:
                if file.startswith(dir):
                    find = True
                    break
            if not find:
                remove_list.append(dir)
        for dir in remove_list:
            dir_list.remove(dir)
    print(dir_list)
    return len(file_list)

def merge_comp(comp, cluster_result, dependency_matrix, Func_dict, project_path):
    # 将不同连通子图中相似度最高的两个cluster进行合并
    # 存到networkx
    print('合并组件图')
    print(cluster_result)
    #raise ValueError
    comp_nx = nx.DiGraph()
    for node in comp.names:
        comp_nx.add_node(node)
    for i in range(len(comp.adjacency_matrix)):
        for j in range(len(comp.adjacency_matrix)):
            if comp.adjacency_matrix[i][j] == 1:
                comp_nx.add_edge(comp.names[i], comp.names[j])
    #求所有连通子图
    sub_graphs = list(nx.weakly_connected_components(comp_nx))
    new_cluster_result = cluster_result.copy()
    # 按节点数目从小到大排序
    sub_graphs.sort(key=lambda x:len(x))
    print(len(sub_graphs))
    # 将依赖度最高的两个cluster进行合并
    while len(sub_graphs)>1:
        max_dependency = 0
        max_cluster1 = None
        max_cluster2 = None
        max_comp1 = None
        max_comp2 = None
        for i in range(len(sub_graphs)):
            for j in range(i+1, len(sub_graphs)):
                comp1 = sub_graphs[i]
                comp2 = sub_graphs[j]
                dependency = 0
                count = 0
                for cluster1 in comp1:
                    cluster1 = int(cluster1.replace('cluster', ''))
                    for cluster2 in comp2:
                        cluster2 = int(cluster2.replace('cluster', ''))
                        cluster1_funcs = cluster_result[cluster1]
                        cluster2_funcs = cluster_result[cluster2]
                        for func1 in cluster1_funcs:
                            for func2 in cluster2_funcs:
                                dependency += dependency_matrix[func1][func2]
                                count += 1
                        dependency /= count
                        if dependency > max_dependency:
                            max_dependency = dependency
                            max_cluster1 = cluster1
                            max_cluster2 = cluster2
                            max_comp1 = comp1
                            max_comp2 = comp2
        # 合并
        print('相似度最高的两个组件为：')
        print(max_cluster1)
        print(max_cluster2)
        new_cluster_result[max_cluster1].extend(new_cluster_result[max_cluster2])
        new_cluster_result.pop(max_cluster2)
        print(new_cluster_result.keys())
        print(sub_graphs)
        max_comp2.remove('cluster'+str(max_cluster2))
        sub_graphs.remove(max_comp2)
        sub_graphs.remove(max_comp1)
        sub_graphs.append(max_comp1.union(max_comp2))
        print(sub_graphs)
        #raise ValueError
    #raise ValueError
    comp = build_component_graph(Func_dict, new_cluster_result, project_path)

    # # 将组件图存到networkx
    # comp_nx = nx.DiGraph()
    # for node in comp.names:
    #     comp_nx.add_node(node)
    # for i in range(len(comp.adjacency_matrix)):
    #     for j in range(len(comp.adjacency_matrix)):
    #         if comp.adjacency_matrix[i][j] == 1:
    #             comp_nx.add_edge(comp.names[i], comp.names[j])
    # # 将组件图存到dot
    # comp_dot = nx.nx_pydot.to_pydot(comp_nx)
    # comp_dot.write(project_path + '/comp.dot')

    return comp, new_cluster_result

def comp_main1(file_list, fileTypes, project_path, comp_num):
    # file_list, fileTypes = Input_process.CodeInfoExtract.getfilelist(project_path)
    PLCG_DOT = project_path+ '/PLCG.dot'
    SDG_DOT = project_path+ '/sdg.dot'
    func_info_path = project_path+ '/funcinfo.json'
    plcg_nx = None
    sdg_nx = None
    if os.path.exists(PLCG_DOT) and os.path.exists(SDG_DOT) and os.path.exists(func_info_path):
        plcg_nx = nx.DiGraph(nx.nx_pydot.read_dot(PLCG_DOT))
        sdg_nx = nx.MultiDiGraph(nx.nx_pydot.read_dot(SDG_DOT))
        with open(func_info_path, 'r', encoding='utf-8') as f:
            func_info = json.load(f)
    else:
        func_info, PLCG_nx, sdg_nx = Input_process.CodeInfoExtract.main(file_list, fileTypes, project_path)
    Func_dict, sum_control_weight, sum_data_weight = get_func_info(sdg_nx, func_info)
    structural_Dependencies = cal_structural_dependencies(Func_dict, sum_control_weight, sum_data_weight)
    Directory_Dependencies = cal_Directory_Dependencies(Func_dict)
    Semantic_Dependencies = cal_Semantic_Dependencies(Func_dict, PLCG_nx)
     
    cluster_result, dependency_matrix  = CL_HAC(Func_dict, structural_Dependencies, Directory_Dependencies, Semantic_Dependencies, comp_num)
    Func_dict = set_feature_vector(Func_dict)
    #Func_dict = func_cluster(Func_dict, 5)

    comp = build_component_graph(Func_dict, cluster_result)
    comp = merge_comp(comp, cluster_result, dependency_matrix, Func_dict)

    Attacked_func = get_Attacked_Func(PLCG_nx)
    Attacked_node = []
    for func in Attacked_func:
        for cluster, funcs in cluster_result.items():
            if func in funcs:
                Attacked_node.append('cluster' + str(cluster))
                break
    # 将组件图存到networkx
    comp_nx = nx.DiGraph()
    for node in comp.names:
        comp_nx.add_node(node)
    for i in range(len(comp.adjacency_matrix)):
        for j in range(len(comp.adjacency_matrix)):
            if comp.adjacency_matrix[i][j] == 1:
                comp_nx.add_edge(comp.names[i], comp.names[j])
    # 将组件图存到dot
    comp_dot = nx.nx_pydot.to_pydot(comp_nx)
    comp_dot.write(project_path + '/comp.dot')
    Attacked_node = list(set(Attacked_node))

    print("Attacked_node:", Attacked_node)

    return comp, Attacked_node

def comp_main(file_list, fileTypes, project_path):
    print('组件恢复')
    # file_list, fileTypes = Input_process.CodeInfoExtract.getfilelist(project_path)
    PLCG_DOT = project_path+ '/PLCG.dot'
    SDG_DOT = project_path+ '/sdg.dot'
    func_info_path = project_path+ '/funcinfo.json'
    cluster_result_json = project_path+ '/cluster_result1.json'
    if os.path.exists(cluster_result_json):
        cluster_result = {}
        with open(cluster_result_json, 'r', encoding='utf-8') as f:
            cluster_result = json.load(f)
        
        PLCG_nx = nx.DiGraph(nx.nx_pydot.read_dot(PLCG_DOT))
        PLCG_nx = None
        sdg_nx = None
        func_info = None
        if os.path.exists(PLCG_DOT) and os.path.exists(SDG_DOT) and os.path.exists(func_info_path):
            PLCG_nx = nx.DiGraph(nx.nx_pydot.read_dot(PLCG_DOT))
            sdg_nx = nx.MultiDiGraph(nx.nx_pydot.read_dot(SDG_DOT))
            with open(func_info_path, 'r', encoding='utf-8') as f:
                func_info = json.load(f)
        Func_dict, sum_control_weight, sum_data_weight = get_func_info(sdg_nx, func_info)
        comp = build_component_graph(Func_dict, cluster_result, project_path)
        
        #comp, new_cluster_result = merge_comp(comp, cluster_result, dependency_matrix, Func_dict,project_path)
        new_cluster_result= cluster_result
        print(new_cluster_result)
        #raise ValueError
        Attacked_func = get_Attacked_Func(PLCG_nx)
        Attacked_node = []
        for func in Attacked_func:
            for cluster, funcs in cluster_result.items():
                if func in funcs:
                    Attacked_node.append('cluster' + str(cluster))
                    break
        print(Attacked_node)
        #raise ValueError
        # 将组件图存到networkx
        comp_nx = nx.DiGraph()
        for node in comp.names:
            comp_nx.add_node(node)
        for i in range(len(comp.adjacency_matrix)):
            for j in range(len(comp.adjacency_matrix)):
                if comp.adjacency_matrix[i][j] == 1:
                    comp_nx.add_edge(comp.names[i], comp.names[j])
        # 将组件图存到dot
        comp_dot = nx.nx_pydot.to_pydot(comp_nx)
        comp_dot.write(project_path + '/comp1'+'.dot')

        cluster_result_json = project_path + '/cluster_result1'+'.json'
        with open(cluster_result_json, 'w') as f:
            json.dump(new_cluster_result, f, indent=4)

        Attacked_node = list(set(Attacked_node))
        comps = [comp]
        return comps, [Attacked_node]

        
    PLCG_nx = None
    sdg_nx = None
    func_info = None
    if os.path.exists(PLCG_DOT) and os.path.exists(SDG_DOT) and os.path.exists(func_info_path):
        PLCG_nx = nx.DiGraph(nx.nx_pydot.read_dot(PLCG_DOT))
        sdg_nx = nx.MultiDiGraph(nx.nx_pydot.read_dot(SDG_DOT))
        with open(func_info_path, 'r', encoding='utf-8') as f:
            func_info = json.load(f)
    else:
        print('执行代码解析')
        func_info, PLCG_nx, sdg_nx = Input_process.CodeInfoExtract.main(file_list, fileTypes, project_path)

    # 获取sdg_nx的连通子图
    sdg_nxs = list(nx.weakly_connected_components(sdg_nx))
    sdg_nxs = [list(sdg_nx.nodes())]
    print('子图有',len(sdg_nxs),'个')
    comps = []
    Attacked_nodes = []
    count = 1
    for sdg in sdg_nxs:
        if len(sdg) <=1 :
            continue
        print(sdg)
        file_list = set()
        new_sdg_nx = nx.MultiDiGraph()
        for node in sdg:
            node_info = sdg_nx.nodes[node]
            label = node_info['label'].replace('"','')
            source_file = func_info[label]['source']
            if not source_file.endswith((".h", ".H", ".hh", ".hpp", ".hxx", ".y")):
                file_list.add(source_file)
            new_sdg_nx.add_node(node, **node_info)
        for edge in sdg_nx.edges:
            edge_info = sdg_nx.edges[edge]
            print(edge_info)
            if edge[0] in sdg and edge[1] in sdg:
                new_sdg_nx.add_edge(edge[0], edge[1], **edge_info)
        Func_dict, sum_control_weight, sum_data_weight = get_func_info(new_sdg_nx, func_info)
        structural_Dependencies = cal_structural_dependencies(Func_dict, sum_control_weight, sum_data_weight)
        Directory_Dependencies = cal_Directory_Dependencies(Func_dict)
        Semantic_Dependencies = cal_Semantic_Dependencies(Func_dict, PLCG_nx)
        print(file_list)
        comp_num = get_comp_num(list(file_list), project_path)
        
        print('组件数量',comp_num)
        #raise ValueError
        cluster_result, dependency_matrix = CL_HAC(Func_dict, structural_Dependencies, Directory_Dependencies, Semantic_Dependencies, comp_num)
        print(cluster_result)
        #raise ValueError
        #raise ValueError
        #Func_dict = set_feature_vector(Func_dict)
        #Func_dict = func_cluster(Func_dict, 5)
        #raise ValueError
        comp = build_component_graph(Func_dict, cluster_result, project_path)
        
        comp, new_cluster_result = merge_comp(comp, cluster_result, dependency_matrix, Func_dict,project_path)
        print(new_cluster_result)
        #raise ValueError
        Attacked_func = get_Attacked_Func(PLCG_nx)
        Attacked_node = []
        for func in Attacked_func:
            for cluster, funcs in cluster_result.items():
                if func in funcs:
                    Attacked_node.append('cluster' + str(cluster))
                    break
        print(Attacked_node)
        #raise ValueError
        # 将组件图存到networkx
        comp_nx = nx.DiGraph()
        for node in comp.names:
            comp_nx.add_node(node)
        for i in range(len(comp.adjacency_matrix)):
            for j in range(len(comp.adjacency_matrix)):
                if comp.adjacency_matrix[i][j] == 1:
                    comp_nx.add_edge(comp.names[i], comp.names[j])
        # 将组件图存到dot
        comp_dot = nx.nx_pydot.to_pydot(comp_nx)
        comp_dot.write(project_path + '/comp'+str(count)+'.dot')

        cluster_result_json = project_path + '/cluster_result'+str(count)+'.json'
        with open(cluster_result_json, 'w') as f:
            json.dump(new_cluster_result, f, indent=4)

        Attacked_node = list(set(Attacked_node))
        #raise ValueError
        if len(comp.names)<=1:
            continue

        comps.append(comp)
        Attacked_nodes.append(Attacked_node)
        print("Attacked_node:", Attacked_node)

    print('设计恢复完成')
    print(comps)
    
    return comps, Attacked_nodes
if __name__ == "__main__":
    # func_info_dict_path = r'E:\Graduation_Design\Input_process\test\saolei\funcInfo.json'
    # # 读取json
    # with open(func_info_dict_path, 'r', encoding='utf-8') as f:
    #     func_info = json.load(f)
    # sdg_dot_path = r'E:\Graduation_Design\Input_process\test\saolei\code\sdg.dot'
    # sdg = nx.MultiDiGraph(nx.nx_pydot.read_dot(sdg_dot_path))

    project_path = r"uploads\saolei".replace("\\","/")
    file_list, fileTypes = Input_process.CodeInfoExtract.getfilelist(project_path)
    comp, Attacked_node = comp_main(file_list, fileTypes,project_path,5)





            


