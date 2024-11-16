"""
合并函数信息
作者：刘梓轩
日期：2023年7月19日
"""
# 读取json文件
import json
import os

from Input_process.utils import get_param_list


def get_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


class fileInfo:
    def __init__(self, path, functionList, fanIn):
        self.path = path
        self.functionList = functionList
        self.fanIn = fanIn


class funcInfo:
    def __init__(self, name, file, Function_identification, info):
        self.name = name
        self.file = file
        self.info = info

        self.Function_identification = Function_identification
ctypelist = (".c")
cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx", '.y')

def merge_funcInfo(file_data, func_data, matched_func_key):
    # data为项目信息的字典
    fileInfo_dict = file_data
    funcInfo_dict = func_data
    matched_func = {}
    # 遍历fileInfo_dict，将函数列表中重复的函数进行合并
    print("合并前funcInfo数量：", len(funcInfo_dict))
    # same_func = {}
    # for file, info in fileInfo_dict.items():
    #     file_path = file
    #     function_list = info['functionList']
    #     for i in range(len(function_list)):
    #         for j in range(i + 1, len(function_list)):
    #             func_name_i = funcInfo_dict[function_list[i][-2]]['name']
    #             func_name_j = funcInfo_dict[function_list[j][-2]]['name']
    #             if func_name_i == func_name_j:
    #                 # print(function_list[i][-2], funcInfo_dict[function_list[i][-2]]['paramList'])
    #                 func_param_i = get_param_list(funcInfo_dict[function_list[i][-2]]['codeText'], funcInfo_dict[function_list[i][-2]]['paramList'])
    #                 # print(function_list[j][-2], funcInfo_dict[function_list[j][-2]]['paramList'])
    #                 func_param_j = get_param_list(funcInfo_dict[function_list[j][-2]]['codeText'], funcInfo_dict[function_list[j][-2]]['paramList'])
    #                 if func_param_i == func_param_j:
    #                     if file_path not in same_func.keys():
    #                         if function_list[i][1] == function_list[j][1]:
    #                             # continue
    #                             same_func[file_path] = [[function_list[i], function_list[j]]]
    #                             continue
    #                     if file_path not in same_func.keys():
    #                         continue

    #                     flag_tmp = 1
    #                     for s in same_func[file_path]:
    #                         if function_list[i][-2] in s:
    #                             flag_tmp = 0
    #                             s.append(function_list[j])
    #                             break
    #                     if flag_tmp == 1:
    #                         if function_list[i][1] == function_list[j][1]:
    #                             # continue
    #                             same_func[file_path].append([function_list[i], function_list[j]])
    #                         # same_func[file_path].append([function_list[i], function_list[j]])

    # file1: [func1_key, func2_key, func3_key]
    # same_func = {"file": [[fun1, func2, fun3],[]]}
    # matched_func_key = {} key:实现的，value：声明的
    # for file in same_func.keys():
    #     for sf in same_func[file]:
    #         df = ""
    #         tmp = None
    #         tmp_index = [(int(sf[i][2]), i) for i in range(len(sf))]
    #         tmp_index.sort(key=lambda x: x[0])
    #         df = sf[tmp_index[0][1]][-2]
    #         tmp = sf[tmp_index[0][1]]
    #         if 'refresh_options_window' in df:
    #             print()
    #         for func in sf:
    #             if func[-2] != df:
    #                 matched_func_key[func[-2]] = df
    #                 matched_func[func[-2]] = tmp.copy()
    #                 infoo = funcInfo_dict[func[-2]]
    #                 funcInfo_dict[df] = funcInfo_dict[func[-2]]
    #                 del funcInfo_dict[func[-2]]

    # for file in fileInfo_dict.keys():
    #     tmp_func_list = []
    #     for func in fileInfo_dict[file]['functionList']:
    #         if func[-2] not in matched_func_key.keys():
    #             tmp_func_list.append(func)
    #         else:
    #             tmp_func_list.append(matched_func[func[-2]])
    #     rst = []
    #     for func in tmp_func_list:
    #         if func not in rst:
    #             rst.append(func)
    #     fileInfo_dict[file]['functionList'] = rst

    # 生成fileInfo
    file_info = []
    for file, info in fileInfo_dict.items():
        file_path = file
        function_list = info['functionList']
        fan_in = info['fanOut']
        file_info.append(fileInfo(file_path, function_list, fan_in))

    # 生成funcInfo
    func_info = []
    for func, info in funcInfo_dict.items():
        func_name = info['name']
        func_file = info['locateFile']
        func_info.append(funcInfo(func_name, func_file, func, info))

    matched_func = []
    for file in file_info:
        file_path = file.path
        print('merge_func', file_path)
        # 如果文件结尾为.h则跳过
        if file_path.endswith(headertypelist):
            continue
        # 先同一个文件 再include
        for fun_info in file.functionList:
            temp_file_list = file.fanIn+[file_path]
            for include_file in temp_file_list:

                for file1 in file_info:
                    if include_file == file1.path:
                        for fun_info1 in file1.functionList:
                            if fun_info[-2] == fun_info1[-2]:
                                continue
                            fun_name = funcInfo_dict[fun_info[-2]]['name']
                            fun1_name = funcInfo_dict[fun_info1[-2]]['name']
                            print(fun_info)
                            print(fun_info1)

                            fun_param = get_param_list(funcInfo_dict[fun_info[-2]]['codeText'], funcInfo_dict[fun_info[-2]]['paramList'])
                            print('fun_prame ', fun_param)

                            fun1_param = get_param_list(funcInfo_dict[fun_info1[-2]]['codeText'], funcInfo_dict[fun_info1[-2]]['paramList'])
                            print('fun1_param ',fun1_param)
                            # if fun_name == 'automated_test_complete_message_handler' and fun1_name == 'automated_test_complete_message_handler':
                            #     raise ValueError
                            if fun_name == fun1_name and fun_param == fun1_param and fun_info[1] == fun_info1[1]:
                                if file1.path.endswith(headertypelist):
                                    matched_func.append([fun_info, fun_info1])
                                else:
                                    if [fun_info1, fun_info] not in matched_func and [fun_info, fun_info1] not in matched_func:
                                        matched_func.append([fun_info1, fun_info])
                                break
                        break
    # 将源文件中的信息添加到目标文件中
    print(matched_func)
    remove_func = []
    for func in matched_func:
        func1 = func[0][3]
        func2 = func[1][3]
        func_info1 = None
        func_info2 = None
        # 将func1的信息添加到func2中
        for info in func_info:
            if func1 == info.Function_identification:
                func_info1 = info
            if func2 == info.Function_identification:
                func_info2 = info
            if func_info1 != None and func_info2 != None:
                break

        # 判断func2的函数体是否为空,如果为空，则将信息添加到func2中
        if func_info2.info['ifbody'] == "0" or func1.split(':')[0] == func2.split(':')[0]:
            anno = func_info2.info['anno']
            func_info2.info = func_info1.info.copy()
            func_info2.info['anno'].extend(anno)
            func_info2.info['locateFile'] = func_info2.file
            func_info2.info['header'] = ":".join(func_info2.file.split(":")[:-1])
            func_info2.info['source'] = ":".join(func_info1.file.split(":")[:-1])
            func_info2.info['source_key'] = func_info1.Function_identification
            # 修改fileInfo中的函数列表
            for file, info in fileInfo_dict.items():
                func_file = ":".join(func_info1.file.split(":")[:-1])
                if func_file == file:
                    tmp_list = []
                    for fun in info['functionList']:

                        if func1 == fun[3]:
                            tmp_list.append(func[1])
                        else:
                            tmp_list.append(fun)
                    info['functionList'] = tmp_list
                    break

            # 删除func_info1
            remove_func.append(func1)
        if func_info2.info['name'] == 'automated_test_complete_message_handler':
            print(func1)
            print(func2)
            print(func_info2.info)
            #raise ValueError
        # 将所有的func1替换为func2
        for func in func_info:
            if func1 in func.info['fanOut']:
                func.info['fanOut'].remove(func1)
                if func2 not in func.info['fanOut']:
                    func.info['fanOut'].append(func2)

    # print(remove_func)
    # with open('remove_func.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(remove_func))
    funcInfo_dict = {}
    for func in func_info:
        if func.Function_identification not in remove_func:
            funcInfo_dict[func.Function_identification] = func.info
    # with open('func_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(funcInfo_dict, f, indent=4)
    # raise ValueError
    # funOut 修改fanIn
    for key, value in funcInfo_dict.items():
        for fun in value['fanOut']:
            if '184:show_detail_window_message' in fun:
                print()
            if fun not in funcInfo_dict.keys():
                continue
            funcInfo_dict[fun]['fanIn'].append(key)

    # 如果funcinfo没有source和header，则添加
    for key, value in funcInfo_dict.items():
        if 'source' not in value.keys():
            value['source'] = ":".join(value['locateFile'].split(":")[:-1])
        if 'header' not in value.keys():
            value['header'] = ":".join(value['locateFile'].split(":")[:-1])
    print("合并后funcInfo数量：", len(funcInfo_dict))
    # raise ValueError
    func_name_num = {}
    for func,info in funcInfo_dict.items():
        if info['name'] not in func_name_num.keys():
            func_name_num[info['name']] = {}
            func_name_num[info['name']]['num'] = 1
            #func_name_num[info['name']]['info'] = info
        else:
            func_name_num[info['name']]['num']+=1
            #func_name_num[info['name']]['info'] = info
    with open('func_info.json', 'w', encoding='utf-8') as f:
        json.dump(func_name_num, f, indent=4)
    return fileInfo_dict, funcInfo_dict


if __name__ == "__main__":
    # 读取json文件
    json_file = r"E:\CPP_master\dev0815\codeFileInfo.json"
    file_data = get_json_data(json_file)
    json_file = r"E:\CPP_master\dev0815\funcInfo.json"
    func_data = get_json_data(json_file)
    fileInfo_dict, funcInfo_dict = merge_funcInfo(file_data, func_data, {})
    # with open(r"D:\Code\VScode\CPP_Support\codeFileInfo1.json", 'w', encoding='utf-8') as f:
    #     json.dump(fileInfo_dict, f, indent=4)
    # with open(r"D:\Code\VScode\CPP_Support\funcInfo1.json", 'w', encoding='utf-8') as f:
    #     json.dump(funcInfo_dict, f, indent=4)
