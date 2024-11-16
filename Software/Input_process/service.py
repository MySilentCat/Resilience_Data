# 执行总流程
import pythoncom
import threading
from CodeInfoExtract import *
from project import query3, Project
from taskModel import *
from app import *
import sdg_new
Threads = {}
def task(task_id, a):
    # 解决win32com包的并发错误
    pythoncom.CoInitialize()
    task_dict = {
        "done": 0,
        "backend_copy_test_project": None,
        "backend_CG": None,
        "backend_cfg": None,
        "backend_pdg": None,
        "backend_sdg": None,
        "backend_component_recovery": None,
        "backend_pipe_filter": None,
    }
    Threads[task_id] = (threading.current_thread().name,
                        threading.current_thread().ident)
    project = query3(a["projectName"])
    id = project.id
    # 设计恢复
    project_name = a["projectName"]
    # 获取代码文件列表
    fileTypes = a["fileTypes"]
    file_list = []
    file_list += a["codeFiles"]['header']
    file_list += a["codeFiles"]['source']
    # file_list, fileTypes = CI.getfilelist(a["codeRoot"])
    # 运行解析程序
    runParsing(file_list, a["codeRoot"])

    # # 此处的try except为测试用
    # try:

    # 获取信息
    print("源码解析完成，开始提取信息")
    codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list, input_locate, if_locate, matched_func_key = GetInfo(file_list, a["codeRoot"])
    # 保存为字典
    print("信息提取完成，开始保存信息")
    new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict = saveasdict(codeFileInfo_dict, funcInfo_dict, classInfo_dict, global_var_list)
    # 合并函数信息
    new_codeFileInfo_dict, new_funcInfo_dict = merge_funcInfo(new_codeFileInfo_dict, new_funcInfo_dict, matched_func_key)

    new_funcInfo_dict = get_func_anno(a["codeRoot"], new_funcInfo_dict, new_codeFileInfo_dict)
    new_classInfo_dict = get_class_anno(a["codeRoot"], new_classInfo_dict, new_codeFileInfo_dict)
    # 将plcg存到nx中
    PLCG_nx = build_plcg_dot(new_funcInfo_dict, a["codeRoot"], funcInfo_dict)
    print("合并函数信息完成")

    # 合并类信息 （戴政再添加）

    # 构造类图
    #new_classInfo_dict, class_js_data = Class_Diagram.CLASS_main(new_classInfo_dict, new_funcInfo_dict)
    projectInfo_dict = file2project(project_name, new_codeFileInfo_dict, a["codeRoot"], fileTypes)
    print("projectInfo_dict计算完成")
    print(a["codeRoot"])
    print2json(a["codeRoot"], new_codeFileInfo_dict, new_funcInfo_dict, new_classInfo_dict, projectInfo_dict)
    print("print2json完成")

    in_degree_0, func_header_source = get_info_from_func(new_funcInfo_dict)

    graph_json = {}
    print("get_info_from_func")
    # FOR C PROJECTS ONLY
    # TODO： CHECK if this is a C PROJECT
    # 构造调用返回和层次图
    # 构造组件依赖图
    # comp_data_csv_path = call_back_comp_cpp.main(new_funcInfo_dict, new_classInfo_dict, PLCG_nx)
    # call_back_json = call_back.comp2json(PLCG_nx, comp_data_csv_path)

    # if projectInfo_dict['projectType'] == 0:
    #     layer_graph_json = layer_graph.main(comp_data_csv_path, PLCG_nx)
    #     # 构造管道过滤器
    #     pipe_filter_svg = pipe_filter.main(file_list, PLCG_nx, a["codeRoot"])
    # 构造SDG
    sdg_svg, sdg_nx = sdg_new.main(file_list, PLCG_nx, a["codeRoot"])
    ml_PLCG_nx = nx.MultiDiGraph(PLCG_nx)
    # comp_js = Component_recovery.deal_sdg(ml_PLCG_nx, sdg_nx, func_header_source, a["projectName"])

    # # 构造CG
    # try:
    #     func_data, bad_smell, graph_json, CG, file_data, Component_redundancy, Standalone_components = BuildCG.BUILDCG_main(file_list, a["codeRoot"], a["projectName"], PLCG_nx, in_degree_0, func_header_source, call_back_json)
    # except Exception as e:
    #     print("BUILDCG ERROR", e)
    #     traceback.print_exc()

    # if projectInfo_dict['projectType'] == 0:
    #     graph_json['layer_js'] = layer_graph_json
    #     graph_json['pipe_filter_svg'] = pipe_filter_svg
    #     graph_json['sdg_svg'] = sdg_svg

    # graph_json['callback_js'] = call_back_json
    # graph_json['class_js'] = class_js_data
    # graph_json['comp_js'] = comp_js

    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
    # print(bad_smell)
    print("bad_smell计算完成")
    #design_metrics_data = getDesignMetric(func_data, new_classInfo_dict)
    # 获取缓冲区溢出信息
    buffer_overflow = get_Buffer_overflow(input_locate, if_locate)
    print("缓冲区溢出防止计算完成")
    # 圈复杂度的充分性从codeFileInfo_dict[key]['cyclComplexity']

    # 编码规则的符合性

    # 组件的冗余度

    # 组件间的耦合度

    # 资产的可重用性

    # path_LZX = path + f"/Design_recovery/project/{project_name}"
    # projectInfo = ProjectInfo(projectdata, filedata,
    #                           path_LZX, a["projectName"])
    # res = checkInfo(tmp, a["projectName"])
    # print(res)
    # print("ProjectInfo提取完成")
    # # 使用刘梓轩的func_num
    # with open(path + "/data/" + a["projectName"] + "/funcNumber.json", "r", encoding="utf-8") as f:
    #     content = json.load(f)
    # func_num = dict(content)
    # projectInfo["functionNumber"] = func_num["funcNumber"]
    # res["projectInfo"] = projectInfo
    # mainWindow = res
    # print("ProjectInfo修正完成")
    # # docInfo = docextract(a)
    #
    # if a["fileSelect"] or a['cddocs'] or a['pdocs']:
    #     docInfo = docextract(a)
    # else:
    #     docInfo = null25000.get25000()
        # Nonepath = path + "/data/25010None.json"
        # docInfo = dict()
        # with open(Nonepath, encoding='utf-8') as json_file:
        #     docInfo = json.load(json_file)
    print("docextract信息提取完成")
    # try:
    #     metric25010 = UpdataMetrix(docInfo, buffer_overflow, file_data, func_data, Component_redundancy, Standalone_components)
    #     print("metric25010信息更新完成")
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
    # 更新数据
    with app.app_context():
        project1 = Project.query.get(id)
        project1.function_info_json = str(func_data).encode()
        project1.class_info_json = str(new_classInfo_dict).encode()
        project1.project_json = str(projectInfo_dict).encode()
        project1.file_json = str(file_data).encode()
        #project1.bad_smell_json = str(bad_smell).encode()
        project1.type = projectInfo_dict['projectType']
        project1.graph_info_json = str(graph_json).encode()
        print(len(project1.graph_info_json))
        print(len(project1.function_info_json))
        #project1.index_info_json = str(metric25010).encode()
        #project1.design_metrics_json = str(design_metrics_data).encode()
        print(3)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
        print(4)

    print("finished")
    task_dict["done"] = 1
    update_task(task_id, task_dict)
    Threads.pop(task_id)