from Dynamic_Bayesian_network.Build_Dynamic_Bayesian_network import Dynamic_Bayesian_network_MAIN
from Input_process.deal_plantUML import comp_wsd_to_txt
from Input_process.Comp_recovery import comp_main
from Input_process.CodeInfoExtract import getfilelist
import numpy as np
#from my_utils import copy_code_file
import os
import json
import shutil
import chardet
WEB_PATH = "./web/public/project"
pwd = os.getcwd()
# 基于UML图的软件架构韧性评估
def UML_Resilience_Assessment(UML_file, static_bayesian_network_path, dynamic_Bayesian_network_path):
    information_txt = '/'.join(UML_file.split('/')[:-1])+'/information.txt'
    main = ''
    sub = []
    if os.path.exists(information_txt):
        f = open(information_txt, 'rb')
        data = f.read()
        encoding = chardet.detect(data)['encoding']
        f.close()
        f=open(information_txt,'r',encoding=encoding)
        with f:
            data=f.read()
            data_list=data.split("\n")
            main = data_list[0]
            sub = data_list[1].split(' ')
    print('main',main)
    print('sub',sub)
    #raise ValueError
    comp = comp_wsd_to_txt(UML_file,main,sub)
    static_js_data, Dynamic_js_data=Dynamic_Bayesian_network_MAIN(comp, static_bayesian_network_path, dynamic_Bayesian_network_path,[],'',main = main,sub=sub)
    with open(static_bayesian_network_path, 'w') as f:
        f.write('var graph = ')
        json.dump(static_js_data, f, indent=4)
    with open(dynamic_Bayesian_network_path, 'w') as f:
        f.write('var graph = ')
        json.dump(Dynamic_js_data, f, indent=4)

# 基于源代码设计恢复的软件架构韧性评估
def Code_Resilience_Assessment(file_list, fileTypes, project_path, static_bayesian_network_path, dynamic_Bayesian_network_path):
    comps, Attacked_nodes = comp_main(file_list, fileTypes, project_path)
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
    static_json_data = {}
    static_json_data["data"] = []
    static_json_data["categories"] = categories
    static_json_data["links"] = []
    static_json_data["resilience"] = []
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
    Dynamic_json_data = {}
    Dynamic_json_data["data"] = []
    Dynamic_json_data["categories"] = categories
    Dynamic_json_data["links"] = []
    Dynamic_json_data["resilience"] = []
    print(len(comps))
    for i in range(len(comps)):
        print('第',i,'个组件图...')
        comp = comps[i]
        comp_id = i
        Attacked_node = Attacked_nodes[i]
        static_js_data, Dynamic_js_data = Dynamic_Bayesian_network_MAIN(comp, static_bayesian_network_path, dynamic_Bayesian_network_path, Attacked_node, comp_id)
        print(static_js_data)
        static_json_data["data"].extend(static_js_data["data"])
        static_json_data["links"].extend(static_js_data["links"])
        static_json_data["resilience"].append(static_js_data["resilience"])
        Dynamic_json_data["data"].extend(Dynamic_js_data["data"])
        Dynamic_json_data["links"].extend(Dynamic_js_data["links"])
        Dynamic_json_data["resilience"].append(Dynamic_js_data["resilience"])

    static_json_data["resilience"] = round(np.mean(static_json_data["resilience"]),5)
    Dynamic_json_data["resilience"] = round(np.mean(Dynamic_json_data["resilience"]),5)

    with open(static_bayesian_network_path, 'w') as f:
        f.write('var graph = ')
        json.dump(static_json_data, f, indent=4)
    with open(dynamic_Bayesian_network_path, 'w') as f:
        f.write('var graph = ')
        json.dump(Dynamic_json_data, f, indent=4)

# def copy_test_project(project_name, code_path, task_id):
#     """
#     将给定项目复制到指定文件夹下以便进行架构恢复
#     """
#     avalue = 0
#     if not os.path.exists(f"Design_recovery/project/{project_name}"):
#         os.makedirs(f"Design_recovery/project/{project_name}")
#     now_root = pwd + f"/Design_recovery/project/{project_name}/code"
#     copy_code_file(code_path, now_root)
#     # 读取json
#     with open(f"{pwd}/data/{project_name}/analyze_files.json", 'r', encoding='utf-8') as load_f:
#         load_dict = dict(json.load(load_f))
#     avalue = 1
#     file_list = []
#     code_file_match_dict = {}
#     for key, value in load_dict.items():
#         for file_path in value:
#             now_path = file_path.replace(code_path, now_root)
#             file_list.append(now_path)
#             code_file_match_dict[now_path] = file_path
#     with open(f"Design_recovery/project/{project_name}/code_file_match.txt", 'w') as f:
#         for key, value in code_file_match_dict.items():
#             info = key+":: "+value+"\n"
#             f.write(info)

#     print("finish copy")
#     # 读取json
#     with open("./data/task.json", 'r', encoding='utf-8') as load_f:
#         load_dict = dict(json.load(load_f))
#     # 修改json
#     load_dict[str(task_id)]["backend_copy_test_project"] = avalue

#     with open("./data/task.json", 'w', encoding='utf-8') as load_f:
#         json.dump(load_dict, load_f)
#     print("write json")
#     # 返回project_name文件夹的绝对路径
#     return file_list, pwd + f"/Design_recovery/project/{project_name}"
#     # return f"{os.getcwd()}/Design_recovery/project/{project_name}"

if __name__ == '__main__':
    UML_file = r'\temp_grad\Input_process\网上商城系统.wsd'.replace("\\","/")
    static_bayesian_network_path = r'UML_Static_Bayesian_network.js'
    dynamic_Bayesian_network_path = r'UML_Dynamic_Bayesian_network.js'
    UML_Resilience_Assessment(UML_file, static_bayesian_network_path, dynamic_Bayesian_network_path)

    project_path = r'\temp_grad\uploads\grpc'.replace("\\","/")
    file_list, fileTypes = getfilelist(project_path)
    #comp_num = get_comp_num(file_list, project_path)
    static_bayesian_network_path = r'Code_Static_Bayesian_network.js'
    dynamic_Bayesian_network_path = r'Code_Dynamic_Bayesian_network.js'
    Code_Resilience_Assessment(file_list, fileTypes, project_path,static_bayesian_network_path, dynamic_Bayesian_network_path)
    shutil.copy(static_bayesian_network_path, WEB_PATH + "/" + 'test')