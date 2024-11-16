import copy
import ctypes
import inspect
import json
from math import floor
import multiprocessing
import shelve
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from Input_process.charset import SaveAsUTF8
from Input_process.CodeInfoExtract import getfilelist
import zipfile
import pandas as pd
import random
import os
import time
import shutil
from Input_process.InfoExtract import InfoExtract

from Resilience_Assessment import UML_Resilience_Assessment, Code_Resilience_Assessment

# from app.charset import SaveAsUTF8
#from design_recovery_main import *

#import pythoncom
from flask import Flask, jsonify, render_template, session, send_from_directory
from flask import request
# from DocExtract import docextract, UpdataMetrix, get_None_25000
# from DocInf import get_doc_info
# from CodeExtract import *
# from ExpertMetric import Get_expert_metric
# import metricCheck
# import AHP
from my_utils import add_micro_define, get_pro_files, rewrite_file, walk_floder
# from run_ast_creator import generate_codeAnalyze_exe
from flask_cors import CORS
from gevent import pywsgi

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)
app.permanent_session_lifetime = timedelta(minutes=30)
app.secret_key = 'your_secret_key_here'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
path = os.getcwd()
path = path.replace("\\", "/")
print("app path:", path)
# 用于监控任务进度
# tasks = {}
Threads = {}
# filedata = None
with open(path + "/Input_process/config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
UPLOADS_DEFAULT_DEST = content["UPLOADS_DEFAULT_DEST"].replace("\\", "/")
app.config["UPLOADS_DEFAULT_DEST"] = content["UPLOADS_DEFAULT_DEST"].replace("\\", "/")
WEB_PATH = content["WEB_PATH"].replace("\\", "/")
SERVER_HOST = content["SERVER_HOST"]
SERVER_PORT = content["SERVER_PORT"]


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(pid):
    # 停止运行
    _async_raise(pid, SystemExit)


def task(task_id, a):
    """
    分析文档以及源码任务
    :param task_id:
    :param a:
    :return:
    """
    # 解决win32com包的并发错误
    # pythoncom.CoInitialize()
    with open(path + "/data/task.json", "r", encoding="utf-8") as f:
        tasks = dict(json.load(f))
    Threads[task_id] = (threading.current_thread().name,
                        threading.current_thread().ident)
    pdir = path + "/data/" + a["projectName"]
    # 设计恢复
    project_name = a["projectName"]
    time_begin = time.time()
    try:
        if not os.path.exists(f"Design_recovery/project/{project_name}/graphs"):
            # a["codeRoot"] = str(a["codeRoot"]).replace("\\", '/')
            # project_path = copy_test_project(
            # file_list, project_path = copy_test_project(
            #     a["projectName"], a["codeRoot"], task_id)
            # project_path = project_path.replace("\\", "/")

            # 基于UML的软件架构韧性评估
            project_path = '/'.join(a['codeRoot'].split('/')[:-1])
            if a['cddocs'] != []:
                # 将该文件复制到uplpads文件夹下
                #shutil.copy(a['cddocs'][0], UPLOADS_DEFAULT_DEST + "/" + project_name + "/docs")
                static_bayesian_network_path = project_path + "/UML_static_bayesian_network.js"
                dynamic_Bayesian_network_path = project_path + "/UML_dynamic_Bayesian_network.js"
                UML_file = a['cddocs'][0]
                UML_Resilience_Assessment(UML_file, static_bayesian_network_path, dynamic_Bayesian_network_path)
            else:
                json_data = {}
                data_list = {}
                categories = {}
                link_list = {}
                json_data["data"] = data_list
                json_data["categories"] = categories
                json_data["links"] = link_list

                with open(project_path + "/UML_static_bayesian_network.js", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                
                json_data = {}
                json_data["data"] = data_list
                json_data["categories"] = categories
                json_data["links"] = link_list
                json_data["resilience"] = None
                
                with open(project_path + "/UML_dynamic_Bayesian_network.js", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

            if a['selectCodeFiles'] != []:
                
                file_list, fileTypes = getfilelist(project_path)
                #comp_num = get_comp_num(file_list, project_path)
                static_bayesian_network_path = project_path + "/Code_static_bayesian_network.js"
                dynamic_Bayesian_network_path = project_path + "/Code_dynamic_Bayesian_network.js"
                Code_Resilience_Assessment(file_list, fileTypes, project_path, static_bayesian_network_path, dynamic_Bayesian_network_path)
            else:
                json_data = {}
                data_list = {}
                categories = {}
                link_list = {}
                json_data["data"] = data_list
                json_data["categories"] = categories
                json_data["links"] = link_list

                with open(project_path + "/Code_static_bayesian_network.js", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                
                json_data = {}
                json_data["data"] = data_list
                json_data["categories"] = categories
                json_data["links"] = link_list
                json_data["resilience"] = None
                
                with open(project_path + "/Code_dynamic_Bayesian_network.js", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

            print('评估结束')
            # 如果WEB_PATH + "/" + project_name文件夹不存在，则新建
            if not os.path.exists(WEB_PATH + "/" + project_name):
                print('新建项目路径：', WEB_PATH + "/" + project_name)
                os.mkdir(WEB_PATH + "/" + project_name)
            print(0)
            shutil.copy(project_path + "/UML_static_bayesian_network.js", WEB_PATH + "/" + project_name)
            shutil.copy(project_path + "/UML_dynamic_Bayesian_network.js", WEB_PATH + "/" + project_name)
            shutil.copy(project_path + "/Code_static_bayesian_network.js", WEB_PATH + "/" + project_name)
            shutil.copy(project_path + "/Code_dynamic_Bayesian_network.js", WEB_PATH + "/" + project_name)
            print(1)

            # 将./html下的文件复制到project_path下
            for item in os.scandir(path + "/html"):
                if item.is_file():
                    shutil.copy(item.path, WEB_PATH + "/" + project_name)
            print(2)
    except Exception as e:
        traceback.print_exc()

        # 项目代码复制完成
       # process_result = design_recovery(file_list, project_path, task_id, a["projectName"])
        
    refresh(task_id, 1)
    print("finished")
    Threads.pop(task_id)


# 线程池,处理耗时任务，防止阻塞主线程
executor = ThreadPoolExecutor(max_workers=5)


def refresh(task_id, val):
    task_id = str(task_id)
    with open(path + "/data/task.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
    file.close()
    tasks = dict(tasks)
    if task_id not in tasks.keys():
        tasks[task_id] = {}
    tasks[task_id]["done"] = val
    with open(path + "/data/task.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)
    file.close()


# 现在已由uploadProjectFile/<projectName>代替
@app.route('/createProject', methods=['POST'])
def create_task():
    with open(path + "/data/task.json", "r", encoding="utf-8") as f:
        tasks = dict(json.load(f))
    a = dict(request.get_json())
    a["codeRoot"] = UPLOADS_DEFAULT_DEST + "/" + a["projectName"] + "/code"
    a["codeRoot"] = a["codeRoot"].replace("//", "/")
    a["codeFiles"] = {"header": [], "source": []}
    upload_path = UPLOADS_DEFAULT_DEST + "/" + a["projectName"] + "/code"
    upload_path = upload_path.replace("//", "/")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx", ".y")
    for file_path in a["selectCodeFiles"]:
        if file_path.endswith(sourcetypelist):
            a["codeFiles"]["source"].append(file_path.replace("\\", "/").replace("./", upload_path+"/"))
        elif file_path.endswith(headertypelist):
            a["codeFiles"]["header"].append(file_path.replace("\\", "/").replace("./", upload_path+"/"))
    if a["fileSelect"]:
        for i in a["fileSelect"]:
            i["path"] = UPLOADS_DEFAULT_DEST + "/" + \
                a["projectName"] + "/docs/" + i["path"]
            i["path"] = i["path"].replace("\\", "/").replace("//", "/")
    else:
        tmp = []
        for i in a['cddocs']:
            i = UPLOADS_DEFAULT_DEST + "/" + a["projectName"] + "/docs/" + i
            i = i.replace("\\", "/").replace("//", "/")
            tmp.append(i)
        a["cddocs"] = tmp
    pdir = path + "/data/" + a["projectName"]
    if os.path.exists(pdir):
        tmp_cmd = "rm -r " + pdir
        rst = subprocess.Popen(["Powershell.exe", tmp_cmd])
        if rst.returncode != 0:
            raise Exception("删除旧项目失败")
    os.mkdir(pdir)
    task_id = len(tasks)
    for t in tasks.keys():
        if int(t) >= task_id:
            task_id = int(t) + 1
    refresh(task_id, 0)
    a["task_id"] = str(task_id)
    session[a["projectName"]] = a
    with open(pdir + "/" + a["projectName"] + ".json", "w", encoding="utf-8") as file:
        json.dump(a, file, ensure_ascii=False, indent=4)
    file.close()
    with open(pdir + "/analyze_files.json", 'w', encoding='utf-8') as file:
        json.dump(a["codeFiles"], file,
                  ensure_ascii=False, indent=4)
    with open('/'.join(a['codeRoot'].split('/')[:-1]) + "/analyze_files.json", "w", encoding="utf-8") as file:
        json.dump(a["codeFiles"], file,
                  ensure_ascii=False, indent=4)
    # 执行解析任务
    executor.submit(task, task_id, a)
    return jsonify({"createFlag": 0, "msg": a["projectName"] + "项目创建成功!"}), 201


@app.route('/CFG/<projectname>', methods=['GET'])
def cfg_json(projectname):
    with open(path + "/Design_recovery/project/" + projectname + "/graphs/cfg.json", "r", encoding="utf-8") as f:
        res = json.load(f)
    f.close()
    return jsonify(res)


@app.route('/PDG/<projectname>', methods=['GET'])
def pdg_json(projectname):
    with open(path + "/Design_recovery/project/" + projectname + "/graphs/pdg.json", "r", encoding="utf-8") as f:
        res = json.load(f)
    f.close()
    return jsonify(res)


@app.route('/task_progress/<int:task_id>/<projectname>', methods=['GET'])
def progress(task_id, projectname):
    """
    用于轮询任务进度
    :param task_id:
    :return:
    """
    with open(path + "/data/task.json", "r", encoding="utf-8") as f:
        res = dict(json.load(f))
    f.close()
    progress = res.get(str(task_id))
    done = res.get(str(task_id))["done"]
    for k in progress.keys():
        if k != "done" and progress[k] == 0:
            done = -1
    if progress is not None:
        if done == -1:
            with shelve.open(path + "/data/" + projectname + "/expect_filelist") as db:
                expect_filelist = db["expect_filelist"]
            jsonify({"task_id": task_id, "progress": done, "fileList": expect_filelist})
        return jsonify({"task_id": task_id, "progress": done})
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route("/queryProjectName/<projectName>", methods=['POST', "GET"])
def queryProjectName(projectName):
    if os.path.exists(UPLOADS_DEFAULT_DEST + "/" + projectName):
        if os.path.exists(path + "/data/" + projectName) and os.path.exists(path + "/Design_recovery/project/" + projectName):
            return jsonify({"createFlag": 1, "msg": "项目已存在"}), 200
        else:
            shutil.rmtree(UPLOADS_DEFAULT_DEST + "/" + projectName)
            # tmp = f"rm -r {UPLOADS_DEFAULT_DEST + '/' + projectName}"
            # rst = subprocess.Popen(["Powershell.exe", tmp])
            # if rst.returncode != 0:
            #     raise Exception("删除UPLOADS_DEFAULT_DEST文件失败")
            if os.path.exists(path + "/data/" + projectName):
                shutil.rmtree(path + "/data/" + projectName)
                # tmp = f"rm -r {path + '/data/' + projectName}"
                # rst = subprocess.Popen(["Powershell.exe", tmp])
                # if rst.returncode != 0:
                #     raise Exception("删除data文件失败")
            if os.path.exists(path + "/Design_recovery/project/" + projectName):
                shutil.rmtree(path + "/Design_recovery/project/" + projectName)
                # tmp = f"rm -r {path + '/Design_recovery/project/' + projectName}"
                # rst = subprocess.Popen(["Powershell.exe", tmp])
                # if rst.returncode != 0:
                #     raise Exception("删除Design_recovery文件失败")
            return jsonify({"createFlag": 0, "msg": "旧项目创建失败，已清理"}), 200
    else:
        return jsonify({"createFlag": 0, "msg": "新项目创建成功"}), 200


@app.route("/uploadProjectZip/<projectName>", methods=['POST'])
def uploadProjectZip(projectName):
    zip_file = request.files.get("projectZip")
    project_path = UPLOADS_DEFAULT_DEST + "/" + projectName
    project_path = project_path.replace("\\", "/").replace("//", "/")
    if os.path.exists(project_path):
        # tmp = f"rm -r {project_path}"
        # rs = subprocess.Popen(["Powershell.exe", tmp])
        # if rs.returncode != 0:
        #     raise Exception("删除旧项目失败")
        shutil.rmtree(project_path)
    zip_file_name = zip_file.filename
    os.mkdir(project_path)
    zip_file_path = project_path + "/" + zip_file_name
    zip_file.save(zip_file_path)
    code_path = project_path + "/code"
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压后如果是文件直接在code目录，如果是文件夹则在code目录下一个文件夹展开
        zip_ref.extractall(code_path)
    includes_list = set()
    if os.path.exists(code_path+"/excluded_path.txt"):
        replace_dir = []
        for item in os.scandir(code_path):
            if item.is_dir():
                replace_dir.append(item.name)
        if len(replace_dir) > 1:
            raise Exception("压缩包中存在多个项目文件夹，不符合要求！")
        with open(code_path+"/excluded_path.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().strip("\n")
                if line != "":
                    if len(replace_dir) == 1:
                        line = line.replace("\\", "/")
                        line = line.replace(".", "./" + replace_dir[0])
                    else:
                        line = line.replace("\\", "/")
                    if line[-1] == "/":
                        line = line[:-1]
                    # 直接删除该文件夹下所有的文件
                    del_path = os.path.abspath(os.path.join(code_path, line))
                    if os.path.exists(del_path):
                        shutil.rmtree(del_path)
                    # includes_list.add(line)
                    # tmp_line = os.path.abspath(os.path.join(code_path, line)).replace("\\", "/")
                    # for root, dirs, files in os.walk(tmp_line):
                    #     for dir_name in dirs:
                    #         tmp_dir = os.path.join(root, dir_name).replace("\\", "/")
                    #         tmp_rp = os.path.abspath(code_path).replace("\\", "/")
                    #         includes_list.add(tmp_dir.replace(tmp_rp, "."))
    # 解析文件夹目录树并返回，如果是一个一个文件则返回"."
    uvprojx_path = []
    pro_files = []
    floder_tree = walk_floder(code_path, code_path, uvprojx_path)
    code_dict = rewrite_file(code_path, project_path, includes_list)
    add_micro_define(code_path, project_path)
    if uvprojx_path != []:
        pro_files = get_pro_files(uvprojx_path[0], code_path, code_dict)
    return jsonify({"floder_tree": [{"id": 0, "path": "/", "label": "/", "children": floder_tree}], "uvprojx": pro_files}), 200
    # return jsonify([{"id": 0, "path": "/", "label": "/", "children": floder_tree}]), 200

@app.route("/uploadProjectFile/<projectName>", methods=['POST'])
def uploadProjectFile(projectName):
    docs = request.files.getlist("docs")
    for doc in docs:
        print('DOC:',doc)
        #raise ValueError
        file_name = doc.filename.split("/")
        file_path = UPLOADS_DEFAULT_DEST + "/" + projectName
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path += "/docs/"
        # print(file_path)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for i in range(len(file_name) - 1):
            file_path += file_name[i] + "/"
            # print(file_path)
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        file_path += file_name[-1]
        if os.path.exists(file_path):
            continue
        else:
            doc.save(file_path)
    return jsonify({"createFlag": 0, "msg": "success"}), 200


# @app.route('/upload', methods=['POST', 'GET'])
# def uploadcode():
#     projectname = request.form.get("project")
#     code = request.files.getlist("files")
#     if os.path.exists(UPLOADS_DEFAULT_DEST + "/" + projectname):
#         return jsonify({"msg": "error"}), 400
#     for file in code:
#         file_name = file.filename.split("/")
#         # file_path = UPLOADS_DEFAULT_DEST + "/" + projectname
#         project_path = UPLOADS_DEFAULT_DEST + "/" + projectname

#         if not os.path.exists(project_path):
#             os.mkdir(project_path)
#         code_path = project_path + "/code/"
#         if not os.path.exists(code_path):
#             os.mkdir(code_path)
#         file.save(project_path+"/"+file_name[-1])
#         with zipfile.ZipFile(project_path+"/"+file_name[-1], 'r') as zip_ref:
#             zip_ref.extractall(code_path)
#         # # print(file_path)
#         # if not os.path.exists(file_path):
#         #     os.mkdir(file_path)
#         # for i in range(len(file_name) - 1):
#         #     file_path += file_name[i] + "/"
#         #     # print(file_path)
#         #     if not os.path.exists(file_path):
#         #         os.mkdir(file_path)
#         # if os.path.exists(file_path+file_name[-1]):
#         #     continue
#         # else:
#         #     file.save(file_path+file_name[-1])
#         #     with zipfile.ZipFile(file_path+file_name[-1], 'r') as zip_ref:
#         #         zip_ref.extractall(file_path+file_name[-1].split(".")[0])

#     # 上传完后重新以utf-8编码保存
#     SaveAsUTF8(UPLOADS_DEFAULT_DEST + "/" + projectname + "/code/")
#     docs = request.files.getlist("docs")
#     for doc in docs:
#         file_name = doc.filename.split("/")
#         file_path = UPLOADS_DEFAULT_DEST + "/" + projectname
#         if not os.path.exists(file_path):
#             os.mkdir(file_path)
#         file_path += "/docs/"
#         # print(file_path)
#         if not os.path.exists(file_path):
#             os.mkdir(file_path)
#         for i in range(len(file_name) - 1):
#             file_path += file_name[i] + "/"
#             # print(file_path)
#             if not os.path.exists(file_path):
#                 os.mkdir(file_path)
#         file_path += file_name[-1]
#         if os.path.exists(file_path):
#             continue
#         else:
#             doc.save(file_path)
#         # SaveAsUTF8(UPLOADS_DEFAULT_DEST + "/" + projectname+"/code/")
#     return jsonify({"msg": "success"}), 200


@app.route('/session-data', methods=['get'])
def session_data():
    return jsonify(session), 200


@app.route('/remove_project/<projectname>/<task_id>', methods=['delete'])
def remove_project(projectname, task_id):
    if (task_id in Threads.keys()):
        stop_thread(Threads[task_id][1])
    pdir = path + "/data/" + projectname
    ddir = "Design_recovery/project/" + projectname
    updir = UPLOADS_DEFAULT_DEST + "/" + projectname
    if os.path.exists(pdir):
        shutil.rmtree(pdir)
    # shutil.rmtree(pdir)
    if os.path.exists(ddir):
        shutil.rmtree(ddir)
    # shutil.rmtree(ddir)
    if os.path.exists(updir):
        shutil.rmtree(updir)
    cpath = WEB_PATH + "/" + projectname
    tmp = f"rm -r {cpath}"
    if os.path.exists(cpath):
        subprocess.Popen(["Powershell.exe", tmp])
    # subprocess.Popen(["Powershell.exe", tmp])
    # subprocess.Popen(["Powershell.exe", 'rm ./data/tmp/'+projectname+'*'])
    return "ok"


@app.route('/badSmell/<smellType>/<projectName>/<page>', methods=['get'])
def send_badsmell(smellType, projectName, page):
    db = shelve.open(path + "/data/" + projectName + "/badSmell")
    page = int(page)
    totalNum = db[smellType + "_num"]
    rst = []
    for i in range((page - 1) * 20, min(page * 20, totalNum)):
        rst.append(db[smellType][i])
    db.close()
    return jsonify({smellType: rst, "totalNum": totalNum}), 200


# @app.route('/setExpertThreshold/<projectname>', methods=['post'])
# def setExpertThreshold(projectname):
    a = dict(request.get_json())
    # 判断是否已经有阈值并且阈值相同，就直接返回保存的数据，不再评估
    # 默认不重新评估
    new_eval_flag = False
    pdir = path + "/data/" + projectname
    if os.path.exists(pdir + "/" + projectname + "setExpertThreshold.json"):
        # 比较阈值是否相同，相同阈值new_eval_flag = False
        with open(pdir + "/" + projectname + "setExpertThreshold.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        threshold = dict(content)
        for key in threshold.keys():
            if threshold[key] != a[key]:
                new_eval_flag = True
                break
            else:
                continue
    else:
        # 本地不存在阈值，则需要进行评估
        new_eval_flag = True
    if new_eval_flag:
        with open(pdir + "/" + projectname + "setExpertThreshold.json", "w", encoding="utf-8") as file:
            json.dump(a, file, ensure_ascii=False, indent=4)
        with open(path + "/data/" + projectname + "/" + projectname + ".json", "r", encoding="utf-8") as f:
            content = json.load(f)
        path_CC = dict(content)["codeRoot"]
        print("path_CC", path_CC)
        path_LZX = path+f"/Design_recovery/project/{projectname}"
        print("path_LZX", path_LZX)
        db = shelve.open(path + "/data/" + projectname + "/filedata")
        filedata = db["filedata"]
        db.close()
        # print(filedata.code_info)
        with open(path + "/data/" + projectname + "/analyze_files.json", "r", encoding="utf-8") as f:
            file_dict = dict(json.load(f))
        expertMetric = Get_expert_metric(path_CC, path_LZX, filedata, a['funcInDegree'],
                                         a['funcOutDegree'], a['funcCallDeep'], a['funcCyclComplexity'], a['funcLength'], a['funcParamLength'], a['fileComment'], a['shortComment'], file_dict, a['funcCopyThreshold'])
        db = shelve.open(path + "/data/" + projectname + "/filedata")
        fun_comment = db["fun_comment"]
        db.close()
        # expertMetric["metrix"]["comprehensibility"]['commentFunc'] = fun_comment
        with open(path + "/data/" + projectname + "/funcNumber.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        func_num = dict(content)["funcNumber"]
        expertMetric["metrix"]["comprehensibility"]['value'] = fun_comment / func_num  # 评估值改为函数级，但是其他数据用于渲染文件级坏味
        # expertMetric["metrix"]["comprehensibility"]['fileNum'] = func_num
        print('回到app')
        tmp = {"metrix": {}}
        tmp["metrix"]['comprehensibility'] = expertMetric["metrix"]['comprehensibility']
        tmp["metrix"]['modifiability'] = expertMetric["metrix"]['modifiability']
        tmp["metrix"]['scalability'] = expertMetric["metrix"]['scalability']
        tmp["metrix"]['testability'] = expertMetric["metrix"]['testability']
        tmp["metrix"]["refundability"] = expertMetric["metrix"]["refundability"]
        overCyclComplexityFunc_num = len(expertMetric["metrix"]["badSmellRatio"]["overCyclComplexityFunc"])
        overOutDegreeFunc_num = len(expertMetric["metrix"]["badSmellRatio"]["overOutDegreeFunc"])
        overInDegreeFunc_num = len(expertMetric["metrix"]["badSmellRatio"]["overInDegreeFunc"])
        overCallDepthFunc_num = len(expertMetric["metrix"]["badSmellRatio"]["overCallDepthFunc"])
        funcCopy_num = len(expertMetric["metrix"]["badSmellRatio"]["funcCopy"])
        overLongFunc_num = len(expertMetric["metrix"]["badSmellRatio"]["overLongFunc"])
        overLongParam_num = len(expertMetric["metrix"]["badSmellRatio"]["overLongParam"])
        overCommentLine_num = len(expertMetric["metrix"]["badSmellRatio"]["overCommentLine"])
        limitCommentLine_num = len(expertMetric["metrix"]["badSmellRatio"]["limitCommentLine"])
        tmp["metrix"]["badSmellRatio"] = {
            "overCyclComplexityFunc": {
                "funcNum": overCyclComplexityFunc_num
            },
            "overOutDegreeFunc": {
                "funcNum": overOutDegreeFunc_num
            },
            "overInDegreeFunc": {
                "funcNum": overInDegreeFunc_num
            },
            "overCallDepthFunc": [
                len(i) for i in expertMetric["metrix"]["badSmellRatio"]["overCallDepthFunc"]
            ],
            "funcCopy": {
                "funcNum": funcCopy_num
            },
            "overLongFunc": {
                "funcNum": overLongFunc_num
            },
            "overLongParam": {
                "funcNum": overLongParam_num
            },
            "overCommentLine": {
                "fileNum": overCommentLine_num
            },
            "limitCommentLine": {
                "fileNum": limitCommentLine_num
            },
            "value": expertMetric["metrix"]["badSmellRatio"]["value"]
        }
        # 保存评估结果
        with open(pdir + "/" + projectname + "expertMetric.json", "w", encoding="utf-8") as file:
            json.dump(tmp, file, ensure_ascii=False, indent=4)
        db = shelve.open(pdir + "/badSmell")
        db["overCyclComplexityFunc"] = expertMetric["metrix"]["badSmellRatio"]["overCyclComplexityFunc"]
        db["overCyclComplexityFunc_num"] = overCyclComplexityFunc_num
        db['overOutDegreeFunc'] = expertMetric["metrix"]["badSmellRatio"]["overOutDegreeFunc"]
        db['overOutDegreeFunc_num'] = overOutDegreeFunc_num
        db['overInDegreeFunc'] = expertMetric["metrix"]["badSmellRatio"]["overInDegreeFunc"]
        db['overInDegreeFunc_num'] = overInDegreeFunc_num
        db['overCallDepthFunc'] = expertMetric["metrix"]["badSmellRatio"]["overCallDepthFunc"]
        db['overCallDepthFunc_num'] = overCallDepthFunc_num
        db['funcCopy'] = expertMetric["metrix"]["badSmellRatio"]["funcCopy"]
        db['funcCopy_num'] = funcCopy_num
        db['overLongFunc'] = expertMetric["metrix"]["badSmellRatio"]["overLongFunc"]
        db['overLongFunc_num'] = overLongFunc_num
        db['overLongParam'] = expertMetric["metrix"]["badSmellRatio"]["overLongParam"]
        db['overLongParam_num'] = overLongParam_num
        db['overCommentLine'] = expertMetric["metrix"]["badSmellRatio"]["overCommentLine"]
        db['overCommentLine_num'] = overCommentLine_num
        db['limitCommentLine'] = expertMetric["metrix"]["badSmellRatio"]["limitCommentLine"]
        db['limitCommentLine_num'] = limitCommentLine_num
        db.close()
        return jsonify(tmp), 200
    else:
        # 读取数据返回
        with open(pdir + "/" + projectname + "expertMetric.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        expertMetric = dict(content)
        return jsonify(expertMetric), 200


# @app.route('/fileInfo/<projectname>', methods=['get'])
# def fileInfo(projectname):
#     with open(path + "/data/" + projectname + "/" + projectname + "25010.json", "r", encoding="utf-8") as f:
#         content = json.load(f)
#     matrix = dict(content)

#     a = get_doc_info(matrix)
#     with open(path + "/data/" + projectname + "/" + projectname + "FileInfo.json", "w", encoding="utf-8") as file:
#         json.dump(a, file, ensure_ascii=False, indent=4)
#     # return jsonify(a), 200
#     return json.dumps(a), 200


@app.route('/mainWindow/<projectname>', methods=['get'])
def mainWindow(projectname):
    with open(path + "/data/" + projectname + "/" + projectname + "MainWindow.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    res = dict(content)
    return jsonify(res), 200

# 项目信息提取
def ProjectInfoExtract(projectname):
    print(projectname)
    info_path = path + '/uploads'+"/"+projectname
    Info = {}
    # 加载projectInfo.json
    if os.path.exists(info_path + "/projectinfo.json"):
        Info["projectInfo"] = json.load(open(info_path + "/projectinfo.json", "r", encoding="utf-8"))
    else:
        Info["projectInfo"] = {}
    # 加载moduleInfo.json
    if os.path.exists(info_path + "/codeFileInfo.json"):
        Info["codeFileInfo"] = json.load(open(info_path + "/codeFileInfo.json", "r", encoding="utf-8"))
    else:
        Info["codeFileInfo"] = {}
    # 加载codeFileInfo.json
    if os.path.exists(info_path + "/moduleInfo.json"):
        Info["moduleInfo"] = json.load(open(info_path + "/moduleInfo.json", "r", encoding="utf-8"))
    else:
        Info["moduleInfo"] = {}
    # 加载funcInfo.json
    if os.path.exists(info_path + "/funcInfo.json"):
        Info["funcInfo"] = json.load(open(info_path + "/funcInfo.json", "r", encoding="utf-8"))
    else:
        Info["funcInfo"] = {}
    res = InfoExtract(Info)

    return res

@app.route("/GetprojectInfo/<projectname>", methods=['get'])
def projectInfo(projectname):
    print(projectname)
    if os.path.exists(path + '/uploads'+"/"+projectname + "/projectinfo.json"):
        data = ProjectInfoExtract(projectname)
        # 获取uploads/项目名/docs下的文件
        docs_path = path + '/uploads'+"/"+projectname + "/docs"
        if os.path.exists(docs_path):
            data["docs"] = os.listdir(docs_path)[0]

    else:
        data = {}
        # 获取uploads/项目名/docs下的文件
        docs_path = path + '/uploads'+"/"+projectname + "/docs"
        if os.path.exists(docs_path):
            data["docs"] = os.listdir(docs_path)[0]
    return jsonify(data)


# @app.route('/projectInfo/<projectname>', methods=['get'])
# def projectInfo(projectname):
#     with open(path + "/data/" + projectname + "/" + projectname + "ProjectInfo.json", "r", encoding="utf-8") as f:
#         content = json.load(f)
#     res = dict(content)
#     return jsonify(res), 200


@app.route('/moduleInfo/<projectname>', methods=['get'])
def moduleInfo(projectname):
    with open(path + "/data/" + projectname + "/" + projectname + "ModuleInfo.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    res = dict(content)
    return jsonify(res), 200


@app.route('/codeFileInfo/<projectname>', methods=['get'])
def codeFileInfo(projectname):
    with open(path + "/data/" + projectname + "/" + projectname + "CodeFileInfo.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    res = dict(content)
    return jsonify(res), 200


@app.route('/metricSelected/<projectname>', methods=['post'])
def metricSelected(projectname):
    a = dict(request.get_json())
    pdir = path + "/data/" + projectname
    with open(pdir + "/" + projectname + "metricSelected.json", "w", encoding="utf-8") as file:
        json.dump(a['metricTree'], file, ensure_ascii=False, indent=4)
    return jsonify({"msg": "success"}), 200


# @app.route('/metricWeight/<projectname>', methods=['get'])
# def metricWeight(projectname):
#     pdir = path + "/data/" + projectname
#     responseDict = {}
#     if os.path.exists(pdir + "/" + projectname + "metricSelected.json"):
#         with open(path + "/data/" + projectname + "/" + projectname + "25010.json", "r",
#                   encoding="utf-8") as f:
#             content = json.load(f)
#         res = dict(content)
#         temp_res = {}
#         for key1 in res.keys():
#             temp_res[key1] = {}
#             for key2 in res[key1].keys():
#                 temp_res[key1][key2] = {}
#                 for key3 in res[key1][key2].keys():
#                     # print(key1, key2,key3)
#                     temp_res[key1][key2][key3] = res[key1][key2][key3]['val']
#         with open(path + "/data/" + projectname + "/" + projectname + "metricSelected.json", "r",
#                   encoding="utf-8") as f:
#             content = json.load(f)
#         mat = dict(content)
#         ret = metricCheck.get_metric_checked(temp_res, mat)
#         if len(ret) == 0:
#             responseDict["metricSelected"] = 0
#         else:
#             responseDict["metricSelected"] = 1
#         responseDict["metricTree"] = ret
#     else:
#         responseDict["metricSelected"] = -1
#         responseDict["metricTree"] = {}
#     return jsonify(responseDict), 200


# @app.route('/weightCheck/<projectname>', methods=['post'])
# def weightCheck(projectname):
#     a = dict(request.get_json())
#     responseDict = {}
#     metricWeight = a["metricWeight"]
#     # print(metricWeight)
#     errorMetric = []
#     rstMetricWeight = {}
#     for key in metricWeight.keys():
#         strData = metricWeight[key]["data"]
#         # numData = eval(strData)
#         numData = strData
#         weightRst = AHP.cal_weight(numData)
#         if weightRst is None:
#             errorMetric.append(key)
#         else:
#             rstMetricWeight[key] = {}
#             for idx in range(len(weightRst)):
#                 rstMetricWeight[key][metricWeight[key]
#                                      ["index"][idx]] = float(weightRst[idx])
#     if len(errorMetric) == 0:
#         responseDict["weightFlag"] = 1
#         responseDict["data"] = {}
#         with open(path + "/data/" + projectname + "/" + projectname + "metricWeight.json", "w",
#                   encoding="utf-8") as file:
#             json.dump(rstMetricWeight, file, ensure_ascii=False, indent=4)
#     else:
#         responseDict["weightFlag"] = 0
#         levelOne = ['功能适应性', '性能效率', '兼容性',
#                     '易用性', '可靠性', '信息安全性', '维护性', '可移植性']
#         responseDict["data"] = {"levelOne": [i for i in errorMetric if i in levelOne], "levelTwo": [
#             i for i in errorMetric if i not in levelOne]}
#     return jsonify(responseDict), 200


@app.route('/getSelectedMetrics/<projectname>', methods=['get'])
def getSelectedMetrics(projectname):
    responseDict = {}
    # if os.path.exists(path + "/data/" + projectname + "/" + projectname + "metricSelected.json"):
    # if os.path.exists(path + "/data/" + projectname + "/" + projectname + "metricResult.json"):
    #     responseDict["metricCalculated"] = 1
    #     with open(path + "/data/" + projectname + "/" + projectname + "metricResult.json", "r",
    #               encoding="utf-8") as f:
    #         content = json.load(f)
    #     responseDict["data"] = content["data"]
    #     return jsonify(responseDict), 200
    # else:
    # 读选择的指标
    with open(path + "/data/" + projectname + "/" + projectname + "metricSelected.json", "r",
              encoding="utf-8") as f:
        content = json.load(f)
    mat = dict(content)
    # 读25010计算的指标
    with open(path + "/data/" + projectname + "/" + projectname + "25010.json", "r",
              encoding="utf-8") as f:
        content = json.load(f)
    res = dict(content)
    for key1 in mat.keys():
        for key2 in mat[key1].keys():
            for key3 in mat[key1][key2].keys():

                mat[key1][key2][key3] = res[key1][key2][key3]['val']
    # 读取权重计算二级指标
    with open(path + "/data/" + projectname + "/" + projectname + "metricWeight.json", "r",
              encoding="utf-8") as f:
        content = json.load(f)
    metricWeight = dict(content)
    levelOne = ['功能适应性', '性能效率', '兼容性', '易用性', '可靠性', '信息安全性', '维护性', '可移植性']
    parentMetric = list(metricWeight.keys())
    parentLevelOne = [i for i in parentMetric if i in levelOne]
    parentLevelTwo = [i for i in parentMetric if i not in levelOne]

    temp_mat = {}
    for key1 in mat.keys():
        temp_mat[key1] = {
            "name": key1,
            "sub": {}
        }
        # 计算一级指标
        tmp_val_one = 0.0
        if key1 in parentLevelOne:
            for key2 in mat[key1].keys():
                if key2 in parentLevelTwo:
                    # 有三级指标的权重
                    temp_mat[key1]["sub"][key2] = {
                        "name": key2,
                        "sub": {}
                    }
                    # 计算二级指标
                    tmp_val = 0.0
                    for key3 in mat[key1][key2].keys():
                        wm = list(metricWeight[key2].keys())
                        if key3 in wm:
                            temp_mat[key1]["sub"][key2]["sub"][key3] = {
                                "name": key3,
                                "val": mat[key1][key2][key3],
                                "weight": metricWeight[key2][key3]
                            }
                            if mat[key1][key2][key3] is None:
                                tmp_val += 0.0 * metricWeight[key2][key3]
                            else:
                                tmp_val += mat[key1][key2][key3] * \
                                    metricWeight[key2][key3]
                        else:
                            temp_mat[key1]["sub"][key2]["sub"][key3] = {
                                "name": key3,
                                "val": mat[key1][key2][key3],
                                "weight": 0.0
                            }
                    temp_mat[key1]["sub"][key2]['val'] = tmp_val
                else:
                    # 无三级指标的权重
                    temp_mat[key1]["sub"][key2] = {
                        "name": key2,
                        "sub": {},
                        "val": 0.0
                    }
                wm_one = list(metricWeight[key1].keys())
                if key2 in wm_one:
                    temp_mat[key1]["sub"][key2]['weight'] = metricWeight[key1][key2]
                    tmp_val_one += temp_mat[key1]["sub"][key2]['val'] * \
                        metricWeight[key1][key2]
                else:
                    temp_mat[key1]["sub"][key2]['weight'] = 0.0
            temp_mat[key1]['val'] = tmp_val_one
        else:
            # 无二级指标的权重
            temp_mat[key1]['val'] = 0.0

    # metricWeight 的格式是{父级指标：{子级：权重}}
    # 构建回复
    responseDict["metricCalculated"] = 1
    responseDict["data"] = []
    # print("temp_mat", temp_mat)
    for key1 in temp_mat.keys():
        responseDict["data"].append({
            "name": key1,
            "val": temp_mat[key1]['val'],
            "sub": [],
            "subMetric": []
        })
        for key2 in temp_mat[key1]["sub"].keys():
            # print(key1,key2)
            responseDict["data"][-1]["sub"].append({
                "id": key2,
                "value": temp_mat[key1]["sub"][key2]['val'],
                "weight": temp_mat[key1]["sub"][key2]['weight']
            })
            responseDict["data"][-1]["subMetric"].append({
                "name": key2,
                "val": temp_mat[key1]["sub"][key2]['val'],
                "sub": [],
                "subMetric": []
            })
            for key3 in mat[key1][key2].keys():
                if key3 in temp_mat[key1]["sub"][key2]["sub"].keys():
                    tmp_weight = temp_mat[key1]["sub"][key2]["sub"][key3]['weight']
                else:
                    tmp_weight = 0.0
                responseDict["data"][-1]["subMetric"][-1]["sub"].append({
                    "id": key3,
                    "value": res[key1][key2][key3]['val'],
                    "weight": tmp_weight
                })
                responseDict["data"][-1]["subMetric"][-1]["subMetric"].append({
                    "name": key3,
                    "val": res[key1][key2][key3]['val'],
                    "sub": res[key1][key2][key3]['sub']
                })
    with open(path + "/data/" + projectname + "/" + projectname + "metricResult.json", "w",
              encoding="utf-8") as file:
        json.dump({"data": responseDict["data"]},
                  file, ensure_ascii=False, indent=4)

    # else:
    #     responseDict["metricCalculated"] = 0
    return jsonify(responseDict), 200


@app.route('/getAllProject')
def getALLproject():
    subdirectories = [d for d in os.listdir(
        path + "/data/") if "." not in d and d != 'tmp']
    with open(path + "/data/task.json", "r", encoding="utf-8") as f:
        tasks = dict(json.load(f))
    f.close()
    res = {"projects": []}
    for d in subdirectories:
        project = {"name": d, "path": path + "/data/" + d}
        with open(path + "/data/" + d + "/" + d + ".json", "r", encoding="utf-8") as f:
            content = json.load(f)
        project["task_id"] = content["task_id"]
        project["ready"] = tasks[content["task_id"]]["done"] == 1
        project["failed"] = tasks[content["task_id"]]['done'] == -1
        res["projects"].append(project)
    return jsonify(res), 200


def extract_comp_info_from_csv(csv_file_path: str):
    csv_data = pd.read_csv(csv_file_path)
    comp_datas = {}
    time_str = "None"
    for index, row in csv_data.iterrows():
        if not pd.isna(row["topic"]):
            if row["topic"] not in comp_datas:
                comp_datas[row["topic"]] = []
            comp_datas[row["topic"]].append({row["name"]: row["headerfile"]})
            time_str = row["time"]
    return comp_datas, time_str


def save_comp_info_to_csv(csv_file_path: str, comp_data: dict):
    csv_data = pd.read_csv(csv_file_path)
    cur_time_str = time.strftime("%Y%m%d%H%M%S") + str(random.randint(0, 100))
    for comp, comp_funcs in comp_data.items():
        for func_dict in comp_funcs:
            func = list(func_dict.keys())[0]
            header_file = list(func_dict.values())[0]
            # find func with header file
            result = csv_data[(csv_data["name"] == func) & (csv_data["headerfile"] == header_file)]
            if len(result.index) > 1:
                return False
            elif len(result.index) < 1:
                pass
            else:
                if result.loc[result.index[0], "topic"] != comp:
                    # update the element
                    csv_data.loc[(csv_data["name"] == func) & (csv_data["headerfile"] == header_file), "topic"] = comp
                    # print(csv_data.loc[(csv_data["name"]==func) & (csv_data["headerfile"]==header_file)])
    for index, row in csv_data.iterrows():
        if not pd.isna(row["topic"]):
            csv_data.loc[index, "time"] = cur_time_str
    csv_data.to_csv(csv_file_path, index=False)
    return True


@app.route('/getCallBackGraphInfo/<projectname>', methods=['get'])
def getCallBackGraphInfo(projectname):
    dr_path = f"{path}/Design_recovery/project/{projectname}/graphs"
    comp_csv_path = f"{dr_path}/{projectname}_42.csv"
    res, time_str = extract_comp_info_from_csv(comp_csv_path)
    return jsonify({"data": res, "time": time_str}), 200


# @app.route('/updateCallBackGraph/<projectname>', methods=['post'])
# def updateCallBackGraph(projectname):
#     updated_info = dict(request.get_json())
#     # updated_info = a["func_comp_info"]
#     dr_path = f"{path}/Design_recovery/project/{projectname}/graphs"
#     plcg_path = f"{dr_path}/PLCG.dot"
#     comp_csv_path = f"{dr_path}/{projectname}_42.csv"
#     # 更新新的组件信息
#     if save_comp_info_to_csv(comp_csv_path, updated_info):
#         graph_to_json.comp2json(plcg_path, comp_csv_path)
#         newhtmlpath = update_call_back(projectname)
#         return jsonify({"updated": "success", "path": newhtmlpath}), 200
#     else:
#         return jsonify({"updated": "failed"}), 200

# @app.route('/updateCallBackGraph/<projectname>', methods=['post'])
# def updateCallBackGraph(projectname):
#     a = dict(request.get_json())
#     funcpath = a["path"]
#     funcname = a["funcname"]
#     comp = a["comp"]
#     dr_path = f"{path}/Design_recovery/project/{projectname}/graphs"
#     funcpath = f"{path}/Design_recovery/project/{projectname}/code/{funcpath}"
#     # open project's plcg
#     plcg_path = f"{dr_path}/PLCG.dot"
#     # open comp csv file
#     comp_csv_path = f"{dr_path}/{projectname}_42.csv"
#     comp_df = pd.read_csv(comp_csv_path)
#     findex = -1
#     for index, row in comp_df.iterrows():
#         if row["name"] == funcname and os.path.samefile(row["headerfile"],funcpath):
#             # row["topic"] = comp
#             findex = index
#             break
#     if findex == -1:
#         return jsonify({}), 200
#     comp_df.loc[findex, "topic"] = comp
#     comp_df.to_csv(comp_csv_path)
#     # re-generate call back graph js
#     graph_to_json.comp2json(plcg_path, comp_csv_path)
#     copy_js(projectname)
#     return jsonify({}), 200


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    with open(path + "/data/task.json", "r", encoding="utf-8") as f:
        tasks = dict(json.load(f))
    if not os.path.exists(path + "/data/task.json"):
        f = open(path + "/data/task.json", "w", encoding="utf-8")
        f.close()
    # app.run(port=9090, debug=False, threaded=True)
    server = pywsgi.WSGIServer((str(SERVER_HOST), int(SERVER_PORT)), app)
    server.serve_forever()
