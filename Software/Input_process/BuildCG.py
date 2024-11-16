"""
构建CPP的CG
作者：刘梓轩
日期：2023年7月19日
"""
# 读取json文件
import json
import os
import networkx as nx
# from app import app
# import process_project
# import GetBadTaste
# import change_PLCG
# import call_back
# import layer_graph
import numpy as np
# import sdg
import subprocess


def run_cmd(cmd_str='', echo_print=1):
    """
    执行cmd命令，不显示执行过程中弹出的黑框
    备注：subprocess.run()函数会将本来打印到cmd上的内容打印到python执行界面上，所以避免了出现cmd弹出框的问题
    :param cmd_str: 执行的cmd命令
    :return: 
    """
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    # run(cmd_str, shell=True)
    subprocess.run(cmd_str, shell=True)


class funcInfo:
    def __init__(self, name, file, funIn, funOut, Function_identification):
        self.name = name
        self.file = file
        self.funIn = funIn
        self.funOut = funOut
        self.if_lib = 0
        self.Function_identification = Function_identification


def get_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_func_info(data):
    # data为项目信息的字典
    func_info = []
    funcInfo_dict = data
    for func, info in funcInfo_dict.items():
        func_name = info['name']
        func_file = info['locateFile']
        func_in = info['fanIn']
        func_out = info['fanOut']
        func_info.append(funcInfo(func_name, func_file, func_in, func_out, func))

    PLCG = {}
    # 根据路径和函数名生成调用关系
    for func in func_info:
        if func.Function_identification not in PLCG:
            PLCG[func.Function_identification] = []
        for fan in func.funOut:
            if fan not in PLCG[func.Function_identification]:
                PLCG[func.Function_identification].append(fan)

    # 根据PLCG构建FLCG
    FLCG = {}
    for key, value in PLCG.items():
        file_path = key.split(':')[0] + ":" + key.split(':')[1]
        if file_path not in FLCG:
            FLCG[file_path] = []
        for fan in value:
            called_file_path = fan.split(':')[0]+":" + fan.split(':')[1]
            if called_file_path not in FLCG[file_path] and called_file_path != file_path:
                FLCG[file_path].append(called_file_path)

    CG = {}
    CG['PLCG'] = PLCG
    CG['FLCG'] = FLCG

    return CG

def deal_path(path):
    # 处理路径，删掉../和./等
    if path == '<invalid loc>':
        return '<invalid loc>'
    fun_file = os.path.abspath(path).replace('\\', '/')
    return fun_file

def deal_pointer_func(func_data, project_path):
    # 处理函数指针问题
    # 按行读取.var_using文件
    var_using_files = []
    var_define_files = []
    parameter_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith("var_using"):
                var_using_files.append(os.path.join(root, file).replace("\\", "/").replace("//", "/"))
            if file.endswith("var_define1"):
                var_define_files.append(os.path.join(root, file).replace("\\", "/").replace("//", "/"))
            if file.endswith("parameter"):
                parameter_files.append(os.path.join(root, file).replace("\\", "/").replace("//", "/"))
    
    var_using = {}
    for var_using_file in var_using_files:
        with open(var_using_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line != "":
                line = line.split(";;")
                var_using[line[-2]] = line[-1]+"$$"+line[0]

    var_define = []
    for var_define_file in var_define_files:
        with open(var_define_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line != "":
                line = line.split(";;")
                var_define.append(line[-1]+"$$"+line[0])

    # 获取project_path下的所有结尾为pf的文件
    pf_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith("pf"):
                pf_files.append(os.path.join(root, file).replace("\\", "/").replace("//", "/"))

    # 按行读取pf文件
    pf_list = []
    pointer_func_matched_func = {}
    for pf_file in pf_files:
        # 按行读取pf文件
        lines = []
        with open(pf_file, 'r') as f:
            lines = f.readlines()

        remove_pf_list = []
        for line in lines:
            # 如果不为空行，则去掉首尾的花括号
            if line != "\n":
                line = line.strip()
                line = line[1:-2]
                # 如果line不为空，则添加到pf_list中
                if line != "":
                    # 按], 分割
                    func_list = line.split("], ")
                    pointer_func_info = func_list[0].replace("[", "").split(" ;; ")
                    pointer_func_name = pointer_func_info[1]  # 函数指针名称
                    pointer_func_file = pointer_func_info[0].split(' <Spelling=')[0]  # 函数指针声明文件
                    pointer_func_file = deal_path(pointer_func_file)
                    line = int(pointer_func_file.split(':')[1])
                    pointer_func_file = pointer_func_file.split(':')[0] #+':'+pointer_func_file.split(':')[1]
                    pointer_func_key = pointer_func_file + ':' + str(line) + ':' + pointer_func_name
                    # 获取函数指针指向的函数
                    matched_func_list = []
                    for func in func_list[1:]:
                        func_info = func.replace("[", "").replace("]", "").replace(",", "").split(" ;; ")
                        func_name = func_info[1]
                        func_file = func_info[0]
                        func_file = deal_path(func_file)
                        func_file = ':'.join(func_file.split(':')[:-1])
                        for func, info in func_data.items():
                            if func_name == info['name'] and func_file == info['locateFile']:
                                matched_func_list.append(func)
                                break
                    
                    pointer_func_matched_func[pointer_func_name] = matched_func_list

                    # 如果matched_func_list不为空，则遍历函数节点，找到调用pointer_func的节点
                    # 将matched_func_list中的节点添加到调用pointer_func的节点的fanOut中
                    if len(matched_func_list) != 0:
                        for func, info in func_data.items():
                            # remove_pf_list = []
                            for called_fun in info['fanOut']:
                                if called_fun == pointer_func_key:
                                    info['fanOut'].extend(matched_func_list)
                                    info['fanOut'] = list(set(info['fanOut']))
                                    info['fanOut'].remove(called_fun)
                                    break
    
    # 构建fanIn
    for func, info in func_data.items():
        info['fanIn'] = []
    for func, info in func_data.items():
        for called_fun in info['fanOut']:
            if called_fun in func_data.keys():
                func_data[called_fun]['fanIn'].append(func)
    # # 遍历函数的fanOut，如果fanOut中仍然有函数指针，则将函数指针指向的函数添加到fanOut中
    # for func, info in func_data.items():
    #     remove_pf_list = []
    #     matched_func_list = {}
    #     for called_fun in info['fanOut']:
    #         if '$$' in called_fun and '->' in called_fun:
    #             matched_func_list[called_fun] = []
    #         # 仍然为函数指针，也就是这个函数指针为这个函数的参数，遍历父节点，找到这个函数被调用时的实参
    #             if len(info['fanIn']) != 0:
    #                 for fanIn in info['fanIn']:
    #                     parent_parent_info = func_data[fanIn]
    #                     for fan_O, call_lines in parent_parent_info['fanout_callLine'].items():
    #                         if fan_O == func:
    #                             for call_line in call_lines:
    #                                 for key, value in var_using.items():
    #                                     if key.find(call_line) != -1:
    #                                         # 找到实参
    #                                         pointer_name = value+'->'+called_fun.split('->')[-1]
    #                                         print(pointer_name)
    #                                         temp_matched_func_list = get_matched_func(fanIn, pointer_func_matched_func, pointer_name, var_using, called_fun.split('->')[-1],[fanIn],func_data)
    #                                         matched_func_list[called_fun].extend(temp_matched_func_list)
    #             else:
    #                 # 找到实参
    #                 pointer_name = ':'.join(called_fun.split(':')[3:])
    #                 temp_matched_func_list = get_matched_func(func, pointer_func_matched_func, pointer_name, var_using, called_fun.split('->')[-1],[func],func_data)
    #                 matched_func_list[called_fun].extend(temp_matched_func_list)
    #     for key, value in matched_func_list.items():
    #         if len(value) != 0:
    #             info['fanOut'].extend(value)
    #             info['fanOut'] = list(set(info['fanOut']))
    #             info['fanOut'].remove(key)

    # 构建fanIn
    for func, info in func_data.items():
        info['fanIn'] = []
    for func, info in func_data.items():
        for called_fun in info['fanOut']:
            if called_fun in func_data.keys():
                func_data[called_fun]['fanIn'].append(func)

    return func_data

def get_matched_func(node, pointer_func_matched_func, pointer_name, var_using, p_name, dealed_node,func_data):
    if pointer_name in pointer_func_matched_func.keys():
        matched_func_list = pointer_func_matched_func[pointer_name]
        return matched_func_list
    else:
        matched_func_list = []
        for parent in func_data[node]['fanIn']:
            for call_fun, code_list in func_data[parent]['fanout_callLine'].items():
                if call_fun == node:
                    for code in code_list:
                        loc = code
                        for key, value in var_using.items():
                            if key.find(loc) != -1:
                                # 找到实参
                                pointer_name = value+'->'+p_name
                                if parent not in dealed_node:
                                    dealed_node.append(parent)
                                    matched_func_list.extend(get_matched_func(parent, pointer_func_matched_func, pointer_name, var_using,p_name,dealed_node,func_data))
                #if pointer_name.find(loc) != -1:
                # 找到实参
        find = 0
        for child in func_data[node]['fanOut']:
            if child not in func_data.keys():
                continue
            child_info = func_data[child]
            start_line = int(child_info['start_line'])
            end_line = int(child_info['end_line'])
            for pf, matched_func in pointer_func_matched_func.items():
                line = int(pf.split(':')[1])
                if line >= start_line and line <= end_line:
                    if pf.split('->')[-1] == pointer_name.split('->')[-1]:
                        matched_func_list.extend(matched_func)
                        find = 1
                        break
            if find == 0:
                if child not in dealed_node:
                    dealed_node.append(child)
                    
                    temp_matched_func_list = get_matched_func(child, pointer_func_matched_func, pointer_name, var_using, p_name,dealed_node,func_data)
                    matched_func_list.extend(temp_matched_func_list)
        return matched_func_list

    
    return []

# 根据PLCG和FLCG获取js
def get_js_from_PLCG(PLCG, data, js_path):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "C"
        },
        {
            "name": "C++"
        }
    ]
    func_id = 0
    for func, info in data.items():
        temp_dict = {}
        name = info["name"]
        temp_dict["name"] = name
        temp_dict["id"] = func
        temp_dict["file"] = info["locateFile"].split('/')[-1]
        if info['type'] == 'Method':
            temp_dict["name"] = info['locateClass'] + ": " + name
        func_id += 1
        source_file = info['source']
        if source_file[-2:] == ".c" or source_file[-2:] == ".h":
            temp_dict["category"] = 0
        else:
            temp_dict["category"] = 1

        temp_dict["symbolSize"] = 45
        temp_dict["fixed"] = False
        temp_dict["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        temp_dict["outDegree"] = len(info["fanOut"])
        # 入度
        temp_dict["inDegree"] = len(info["fanIn"])
        data_list.append(temp_dict)

    for key, value in PLCG.items():
        for fan in value:
            temp_dict = {}
            temp_dict["source"] = key
            temp_dict["target"] = fan
            temp_dict["symbol"] = [
                "none",
                "arrow"
            ]
            temp_dict["lineStyle"] = {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                            "opacity": 1
                }
            }
            link_list.append(temp_dict)

    PLCG_G = nx.DiGraph()
    for key, value in PLCG.items():
        PLCG_G.add_node(key)
        for value1 in value:
            if value1 not in PLCG_G.nodes:
                PLCG_G.add_node(value1)
        for fan in value:
            PLCG_G.add_edge(key, fan)

    # 最大出度
    max_out_degree = max(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
    max_out_degree_val = max(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 最小出度
    min_out_degree = min(PLCG_G.out_degree, key=lambda x: x[1])[0]+'()'
    min_out_degree_val = min(PLCG_G.out_degree, key=lambda x: x[1])[1]
    # 平均出度
    avg_out_degree = sum([d[1] for d in PLCG_G.out_degree])/len(PLCG_G.out_degree)
    # 最大入度
    max_in_degree = max(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
    max_in_degree_val = max(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 最小入度
    min_in_degree = min(PLCG_G.in_degree, key=lambda x: x[1])[0]+'()'
    min_in_degree_val = min(PLCG_G.in_degree, key=lambda x: x[1])[1]
    # 平均入度
    avg_in_degree = sum([d[1] for d in PLCG_G.in_degree])/len(PLCG_G.in_degree)

    in_degree_0 = []
    out_degree_0 = []
    for key, value in PLCG_G.out_degree:
        if value == 0:
            out_degree_0.append(key)
    for key, value in PLCG_G.in_degree:
        if value == 0:
            in_degree_0.append(key)
    # 获取所有简单路径，起点为入度为0的节点，终点为出度为0的节点
    simple_path = []
    for in_degree_node in in_degree_0:
        for out_degree_node in out_degree_0:
            simple_path.extend(nx.all_simple_paths(PLCG_G, in_degree_node, out_degree_node))
    # 最长调用路径
    if len(simple_path) == 0:
        max_call_path = []
    else:
        max_call_path = max(simple_path, key=lambda x: len(x))
    # 最短调用路径
    if len(simple_path) == 0:
        min_call_path = []
    else:
        min_call_path = min(simple_path, key=lambda x: len(x))
    # 平均调用路径
    if len(simple_path) == 0:
        avg_call_path = 0
    else:
        avg_call_path = sum([len(x) for x in simple_path])/len(simple_path)

    js_data = {}
    js_data["data"] = data_list
    js_data["links"] = link_list
    js_data["categories"] = categories
    js_data["maxOutFunc"] = max_out_degree.split('/')[-1] + '(' + str(max_out_degree_val) + ')'
    js_data["minOutFunc"] = min_out_degree.split('/')[-1] + '(' + str(min_out_degree_val) + ')'
    js_data["avgOut"] = avg_out_degree
    js_data["maxInFunc"] = max_in_degree.split('/')[-1] + '(' + str(max_in_degree_val) + ')'
    js_data["minInFunc"] = min_in_degree.split('/')[-1] + '(' + str(min_in_degree_val) + ')'
    js_data["avgIn"] = avg_in_degree
    js_data["maxCallPath"] = max_call_path
    js_data["minCallPath"] = min_call_path
    js_data["avgCallPath"] = avg_call_path

    # 写入到js文件中
    return js_data

def get_js_from_FLCG(FLCG, data, js_path):
    data_list = []
    link_list = []
    categories = [
        {
            "name": "Header file"
        },
        {
            "name": "C Source file"
        },
        {
            "name": "C++ Source file"
        }
    ]
    file_id = 0

    for file, info in data.items():
        temp_dict = {}
        temp_dict["name"] = info["name"]
        temp_dict["id"] = file
        file_id += 1
        if file.endswith((".h", ".H", ".hh", ".hpp", ".hxx", '.y')):
            temp_dict["category"] = 0
        elif file.endswith((".c")):
            temp_dict["category"] = 1
        else:
            temp_dict["category"] = 2
        temp_dict["symbolSize"] = 45
        temp_dict["fixed"] = False
        temp_dict["itemStyle"] = {
            "normal": {
                "opacity": 1
            }
        }
        # 出度
        temp_dict["outDegree"] = len(info["fanOut"])
        # 入度
        temp_dict["inDegree"] = len(info["fanIn"])
        # 包含函数个数
        temp_dict["funcNum"] = len(info["functionList"])
        data_list.append(temp_dict)

    for key, value in FLCG.items():
        for fan in value:
            temp_dict = {}
            temp_dict["source"] = key
            temp_dict["target"] = fan
            temp_dict["symbol"] = [
                "none",
                "arrow"
            ]
            temp_dict["lineStyle"] = {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                            "opacity": 1
                }
            }
            link_list.append(temp_dict)

    FLCG_G = nx.DiGraph()
    for key, value in FLCG.items():
        FLCG_G.add_node(key)
        for value1 in value:
            if value1 not in FLCG_G.nodes:
                FLCG_G.add_node(value1)
        for fan in value:
            FLCG_G.add_edge(key, fan)

    # 最大出度
    max_out_degree = max(FLCG_G.out_degree, key=lambda x: x[1])[0]
    max_out_degree_val = max(FLCG_G.out_degree, key=lambda x: x[1])[1]
    # 最小出度
    min_out_degree = min(FLCG_G.out_degree, key=lambda x: x[1])[0]
    min_out_degree_val = min(FLCG_G.out_degree, key=lambda x: x[1])[1]
    # 平均出度
    avg_out_degree = sum([d[1] for d in FLCG_G.out_degree])/len(FLCG_G.out_degree)
    # 最大入度
    max_in_degree = max(FLCG_G.in_degree, key=lambda x: x[1])[0]
    max_in_degree_val = max(FLCG_G.in_degree, key=lambda x: x[1])[1]
    # 最小入度
    min_in_degree = min(FLCG_G.in_degree, key=lambda x: x[1])[0]
    min_in_degree_val = min(FLCG_G.in_degree, key=lambda x: x[1])[1]
    # 平均入度
    avg_in_degree = sum([d[1] for d in FLCG_G.in_degree])/len(FLCG_G.in_degree)

    in_degree_0 = []
    out_degree_0 = []
    for key, value in FLCG_G.out_degree:
        if value == 0:
            out_degree_0.append(key)
    for key, value in FLCG_G.in_degree:
        if value == 0:
            in_degree_0.append(key)
    # 获取所有简单路径，起点为入度为0的节点，终点为出度为0的节点
    simple_path = []
    for in_degree_node in in_degree_0:
        for out_degree_node in out_degree_0:
            simple_path.extend(nx.all_simple_paths(FLCG_G, in_degree_node, out_degree_node))
    # 最长调用路径
    if len(simple_path) == 0:
        max_call_path = []
    else:
        max_call_path = max(simple_path, key=lambda x: len(x))
    # 最短调用路径
    if len(simple_path) == 0:
        min_call_path = []
    else:
        min_call_path = min(simple_path, key=lambda x: len(x))
    # 平均调用路径
    if len(simple_path) == 0:
        avg_call_path = 0
    else:
        avg_call_path = sum([len(x) for x in simple_path])/len(simple_path)

    js_data = {}
    js_data["data"] = data_list
    js_data["links"] = link_list
    js_data["categories"] = categories
    js_data["maxOutFunc"] = max_out_degree.split('/')[-1] + '(' + str(max_out_degree_val) + ')'
    js_data["minOutFunc"] = min_out_degree.split('/')[-1] + '(' + str(min_out_degree_val) + ')'
    js_data["avgOut"] = avg_out_degree
    js_data["maxInFunc"] = max_in_degree.split('/')[-1] + '(' + str(max_in_degree_val) + ')'
    js_data["minInFunc"] = min_in_degree.split('/')[-1] + '(' + str(min_in_degree_val) + ')'
    js_data["avgIn"] = avg_in_degree
    js_data["maxCallPath"] = max_call_path
    js_data["minCallPath"] = min_call_path
    js_data["avgCallPath"] = avg_call_path

    return js_data


# 根据PLCG和FLCG计算信息


def build_CG_tree(project_path, project_name, file_list, id_num):
    root = {}
    root["id"] = id_num
    root["label"] = project_name
    root["path"] = project_path.replace('\\', '/')
    root["children"] = []
    # 判断project_path是文件还是目录
    if os.path.isfile(project_path):
        root["type"] = "source"
    else:
        root["type"] = "folder"
        # 获取peoject_path的直接子目录和文件
        for file in os.listdir(project_path):
            file = os.path.join(project_path, file)
            file = file.replace('\\', '/')
            # 判断file是文件还是目录
            if os.path.isdir(file):
                file_name = file.split('/')[-1]
                id_num += 1
                node = build_CG_tree(file, file_name, file_list, id_num)
                if node != None:
                    root["children"].append(node)
            else:
                if file in file_list:
                    file_name = file.split('/')[-1]
                    node = build_CG_tree(file, file_name, file_list, id_num)
                    if node != None:
                        root["children"].append(node)
    return root


def get_info_from_func(func_data):
    # 获取所有入度为0的函数和所有函数的头文件和源文件
    in_degree_0 = []
    func_header_source = {}
    for key, value in func_data.items():
        if len(value['fanIn']) == 0:
            in_degree_0.append(key)
        func_header_source[key] = [value['source'], value['header']]

    return in_degree_0, func_header_source


def BUILDCG_main(file_list, project_path, project_name, nxplcg: nx.DiGraph, in_degree_0, func_header_source, comp_data):
    print("BUILDCG_main", project_path, project_name)
    # 读取json文件
    func_json_file = project_path + r"\funcInfo.json"
    func_data = get_json_data(func_json_file)
    CG = get_func_info(func_data)
    print("BUILDCG_main, 1")
    # 根据PLCG和FLCG计算指标
    # cal_metric_from_CG(data['PLCG'], data['FLCG'])
    # 根据PLCG和FLCG生成js
    js_path = os.path.join(os.path.dirname(__file__), 'PLCG.js')
    PLCG = get_js_from_PLCG(CG['PLCG'], func_data, 'PLCG.js')
    file_json_file = project_path + r"\codeFileInfo.json"
    file_data = get_json_data(file_json_file)
    js_path = os.path.join(os.path.dirname(__file__), 'FLCG.js')
    FLCG = get_js_from_FLCG(CG['FLCG'], file_data, 'FLCG.js')
    print("BUILDCG_main, 2")
    # 计算信息和坏味
    # 获取CFG信息
    data = {}
    data['funcInfo'] = func_data
    # cfg_data, pdg_data, graph_json, dominate_matrixes = process_project.process_project_to_json(file_list, project_path)
    # graph_json['PLCG'] = PLCG
    # # change_PLCG.change_PLCG(func_data,'E:/CPP_master/dev0807/CPP_support/uploads/saoleiqqq/code/code')
    # graph_json['FLCG'] = FLCG
    # file_tree = []
    # root = build_CG_tree(project_path, project_name, file_data.keys(), 1)
    # file_tree.append(root)
    # graph_json['CG_js'] = str(file_tree)

    print("BUILDCG_main, 2.5")
    # construct sdg and function level sdg

    # print("BUILDCG_main, 3")
    # func_data, bad_smell_data, file_data, Component_redundancy, Standalone_components = cal_metric_from_CG(dominate_matrixes, cfg_data, func_data, file_data, {}, comp_data)
    # print("BUILDCG_main, 4")
    # # 输出到json文件中
    # with open(func_json_file, 'w', encoding='utf-8') as f:
    #     json.dump(func_data, f, indent=4)
    # with open(file_json_file, 'w', encoding='utf-8') as f:
    #     json.dump(file_data, f, indent=4)
    #     bad_smell = GetBadTaste.Bad_smell_from_function(data)
    # bad_smell["funcCopy"]['cfg_copy'] = bad_smell_data['cfg_copy']
    # bad_smell_json_file = project_path + r"\badSmell_fromfunc.json"
    # with open(bad_smell_json_file, 'w', encoding='utf-8') as f:
    #     json.dump(bad_smell, f, indent=4)
    print("BUILDCG_main, 5")
    # with open(app.config.get("EXE_PATH") + "/static/PLCG.js", 'w') as f:
    #     f.write("var graph = ")
    #     json.dump(PLCG, f, indent=4)

    # with open(app.config.get("EXE_PATH") + "/static/FLCG.js", 'w') as f:
    #     f.write("var graph = ")
    #     json.dump(FLCG, f, indent=4)
    if not os.path.exists("temp/" + project_name):
        os.makedirs("temp/" + project_name)
    with open("temp/" + project_name + "/PLCG.json", 'w') as f:
        json.dump(CG["PLCG"], f, indent=4)
    print("BuildCG finished")
    return func_data


if __name__ == "__main__":

    project_path = r"E:\CPP_master\dev0815\CPP_support\back_end\project\c-cpp"
    # load json str from
    comp_data = r"static\callback.js"
    # with open(comp_data, 'r', encoding='utf-8') as f:
    #     comp_data = f.read()
    BUILDCG_main(project_path, 'CUnit', None, None, None, comp_data)
