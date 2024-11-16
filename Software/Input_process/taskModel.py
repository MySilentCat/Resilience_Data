from sqlalchemy.orm import sessionmaker

from app import app, db, redis
import pickle
import warnings

warnings.filterwarnings('ignore')
class Task(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Integer)
    backend_copy_test_project = db.Column(db.Integer)
    backend_CG = db.Column(db.Integer)
    backend_cfg = db.Column(db.Integer)
    backend_pdg = db.Column(db.Integer)
    backend_sdg = db.Column(db.Integer)
    backend_component_recovery = db.Column(db.Integer)
    backend_pipe_filter = db.Column(db.Integer)


def add_task():
    newTask = Task(
        done=0,
    )
    with app.app_context():
        db.session.add(newTask)
        db.session.commit()

        db.session.refresh(newTask)
        db.session.expunge(newTask)
        db.session.close()
    return newTask.id


# def queryTasks():
#     # TODO 读取全部的TASK
#     with app.app_context():
#         t = Task.query.all()
#     res = {}
#     for item in t:
#         res[str(item.id)] = {
#             "done": item.done,
#             "backend_copy_test_project": item.backend_copy_test_project,
#             "backend_CG": item.backend_CG,
#             "backend_cfg": item.backend_cfg,
#             "backend_pdg": item.backend_pdg,
#             "backend_sdg": item.backend_sdg,
#             "backend_component_recovery": item.backend_component_recovery,
#             "backend_pipe_filter": item.backend_pipe_filter,
#             "backend_ast": item.backend_ast,
#             "backend_input_analyze": item.backend_input_analyze,
#             "backend_myCodeAnalyze": item.backend_myCodeAnalyze,
#             "backend_CMakeProject": item.backend_CMakeProject
#         }
#     return res


def get_task_from_mysql(task_id):
    with app.app_context():
        item = Task.query.get(task_id)
    if item:
        res = {
            "done": item.done,
            "backend_copy_test_project": item.backend_copy_test_project,
            "backend_CG": item.backend_CG,
            "backend_cfg": item.backend_cfg,
            "backend_pdg": item.backend_pdg,
            "backend_sdg": item.backend_sdg,
            "backend_component_recovery": item.backend_component_recovery,
            "backend_pipe_filter": item.backend_pipe_filter,
        }
        data = pickle.dumps(res)
        redis.set("task_id:"+str(task_id),data)
        return res
    else:
        print("Task not found")
        return {}

def get_task(task_id):
    data = redis.get("task_id:"+str(task_id))
    if data is None:
        res = get_task_from_mysql(task_id)
    else:
        res = pickle.loads(data)
    return res



def update_task(task_id, task_data):
    with app.app_context():
        t = Task.query.get(task_id)
        t.backend_copy_test_project = task_data["backend_copy_test_project"]
        t.backend_CG = task_data["backend_CG"]
        t.backend_cfg = task_data["backend_cfg"]
        t.backend_pdg = task_data["backend_pdg"]
        t.backend_sdg = task_data["backend_sdg"]
        t.backend_component_recovery = task_data["backend_component_recovery"]
        t.backend_pipe_filter = task_data["backend_pipe_filter"]
        t.done = task_data["done"]
        db.session.commit()
        redis.delete("task_id:"+str(task_id))

# id = add_task()
# print(get_task(id))
# task_dict = {
#             "done": 1,
#             "backend_copy_test_project": None,
#             "backend_CG": None,
#             "backend_cfg": None,
#             "backend_pdg": None,
#             "backend_sdg": None,
#             "backend_component_recovery": None,
#             "backend_pipe_filter": None,
# }
# update_task(6, task_dict)
# get_task(6)