# coding=gbk
import json
import os
import pickle

from sqlalchemy.orm import load_only

from app import app, db, redis


class Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(128))
    type = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    project_json = db.Column(db.BLOB(length=2**26-1))
    # bad_smell_json = db.Column(db.BLOB(length=2**26-1))
    function_info_json = db.Column(db.BLOB(length=2**26-1))
    # class_info_json = db.Column(db.BLOB(length=2**26-1))
    graph_info_json = db.Column(db.BLOB(length=2**26-1))
    index_info_json = db.Column(db.BLOB(length=2**26-1))
    # design_metrics_json = db.Column(db.BLOB(length=2**26-1))
    file_json = db.Column(db.BLOB(length=2**26-1))


# with app.app_context():
#     db.drop_all()
#
#     db.create_all()

def add_project(Project):
    # TODO ???????????????????
    with app.app_context():
        # 更新redis
        redis.delete("all_project")
        db.session.add(Project)
        db.session.commit()
        redis.set("all_project", pickle.dumps(get_project_from_mysql()))


def get_project_from_mysql():
    data = Project.query.options(load_only(Project.name, Project.path, Project.type, Project.task_id)).all()
    if data is not None:
        return [(item.name, item.path, item.type, item.task_id) for item in data]


def query1():
    # TODO ?????????????????????????????????????????????
    data = redis.get("all_project")
    if data is None:
        # print("redis is None")
        res = get_project_from_mysql()
        redis.set("all_project", pickle.dumps(res))
    else:
        # print("redis is not None")
        res = pickle.loads(data)
    return res


def query3(name):
    # TODO ?????????????????????????????????????????????
    with app.app_context():
        item = Project.query.filter(Project.name == name).first()
        return item


def query2(name):
    # TODO ??????????????????????????????,
    #  ????????????
    #   ??????JSON
    #   ???????JSON
    #   ???????JSON
    #   ?????JSON
    #   ????JSON
    #   ??????JSON
    #   ??????JSON
    with app.app_context():
        item = Project.query.filter(Project.name == name).first()
        if item is not None:
            a = json.loads(str(item.project_json, "UTF-8").replace("\'", '\"')) if item.project_json is not None else None
            b = json.loads(str(item.bad_smell_json, "UTF-8").replace("\'", '\"')) if item.bad_smell_json is not None else None
            c = json.loads(str(item.function_info_json, "UTF-8").replace("\'", '\"')) if item.function_info_json is not None else None
            # print(item.class_info_json)
            # print(item.class_info_json.decode())
            d = json.loads(str(item.class_info_json, "UTF-8").replace("\'", '\"').replace('False', 'false').replace('True', 'true')) if item.class_info_json is not None else None
            res = item.graph_info_json.decode()
            # print(res)
            # for k, v in res['cfg'].items():
            #     for k1,v1 in v.items():
            #         cfg = v1
            #         # ????????????string
            #         # cfg = cfg.decode()
            #         with open('test1.dot','w') as f:
            #             f.write(cfg)
            #         os.system("D:/Graphviz/bin/dot.exe -Tsvg test1.dot -o test1.svg")
            #         break
            # e = json.loads(str(item.graph_info_json, "UTF-8").replace("\'", "\"")) if item.graph_info_json is not None else None
            e = eval(res)
            f = json.loads(str(item.index_info_json, "UTF-8").replace("\'", '\"').replace("None", "null")) if item.index_info_json is not None else None
            g = json.loads(str(item.file_json, "UTF-8").replace("\'", '\"')) if item.file_json is not None else None
            h = json.loads(str(item.design_metrics_json, "UTF-8").replace("\'", '\"').replace("None", "null")) if item.design_metrics_json is not None else None
            # print(e)
            return a, b, c, d, e, f, g, h
        else:
            return None


def delete_project(name):
    # TODO ????????????????
    with app.app_context():
        p = Project.query.filter(Project.name == name).first()
        if p is not None:
            # 更新redis
            redis.delete("all_project")
            redis.delete("projectInfo:"+name)
            db.session.delete(p)
            db.session.commit()
            redis.set("all_project", pickle.dumps(get_project_from_mysql()))


# query2("CUnit")
