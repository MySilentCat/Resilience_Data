<template>
  <div>
    <el-row :gutter="20" style="margin-bottom: 30px">
      <el-col :span="24">
        <el-button
            type="success"
            style="float: right; margin-right: 40px; margin-bottom: 10px"
            @click="toUserManual"
        >用户手册
        </el-button>
        <el-button
            type="primary"
            style="float: right; margin-right: 40px; margin-bottom: 10px"
            @click="dialogVisible3 = true"
        >新建项目
        </el-button>
      </el-col>
    </el-row>
    <div class="box—wrapper">
      <el-card v-for="item in pagedData" :key="item.id" class="box-card">
        <div class="upload">
          <i class="el-icon-folder" style="font-size: 40px"></i>
          <div>{{ item.name }}</div>
          <el-button-group class="button-g" style="margin-top: 15px; width: 100px">
            <el-button
                type="primary"
                size="medium"
                round
                @click="toMain(item)"
                icon="el-icon-search"
            >查看
            </el-button>
            <el-button
                type="danger"
                size="medium"
                round
                icon="el-icon-delete"
                @click="remove(item.name, item.task_id)"
            >删除
            </el-button>
          </el-button-group>
        </div>
      </el-card>
      <el-card class="box-card">
        <a class="upload" @click="dialogVisible3 = true">
          <i class="el-icon-plus" style="font-size: 40px"></i>
          <div>新建项目</div>
        </a>
      </el-card>
    </div>
    <div class="pagination-container">
      <el-pagination
          :page-size="pageSize"
          :total="projects.length"
          layout="prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      >
      </el-pagination>
    </div>
    <el-dialog :visible.sync="dialogVisible1">
      <p>项目尚未加载完成，请稍后</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible1 = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible1 = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="dialogVisible2">
      <p>项目解析失败，请查看错误日志:app/data/{{ dialogParam }}/analyze_error.txt</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible2 = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible2 = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog width="50%" :visible.sync="dialogVisible3" title="新建须知">
      <div style="padding: 0 10%">
        <div class="des">
          &bull; 上传的项目依赖关系完整的，同时必须是<strong
            style="background-color: #f8f840"
        >ZIP</strong
        >压缩项目包
        </div>
        <div class="des">
          &bull; 上传项目中请不要包含中文目录，请不要使用中文命名<span class="code-style"
        >.c</span
        >和<span class="code-style">.h</span>文件
        </div>
        <div class="des">
          &bull; 如果项目编译依赖宏，请将宏添加到<span class="code-style"
        >macro_define.txt</span
        >中，每个宏占用一行
        </div>
        <div class="des">
          &bull;
          如果项目中存在依赖冲突，即：评估某模块时，应当依赖A库，而不应该依赖B库。请将排除的依赖库<strong
            style="background-color: #f8f840"
        >B所在目录</strong
        >以相对于项目根目录的相对路径形式添加到<span class="code-style"
        >excluded_path.txt</span
        >中，每个排除的目录占用一行
        </div>
        <div class="des">
          &bull; 如果需要使用到<span class="code-style">macro_define.txt</span>和<span
            class="code-style"
        >excluded_path.txt</span
        >，请将其与项目根目录同级进行压缩
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible3 = false">取 消</el-button>
        <el-button
            type="primary"
            @click="
            dialogVisible3 = false;
            dialogVisible4 = true;
          "
        >已知晓</el-button
        >
      </span>
    </el-dialog>
    <el-dialog width="50%" :visible.sync="dialogVisible4" title="项目名称">
      <div style="padding: 0 10%">
        <el-input
            v-model="newProjectName"
            placeholder="请输入项目名称"
            clearable=""
        ></el-input>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible4 = false">取 消</el-button>
        <el-button type="primary" @click="toNew">创 建</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import "../assets/js/jquery/dist/jquery.min.js";
import "bootstrap/dist/js/bootstrap.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/adminlte/skins/_all-skins.min.css";
import "../assets/css/adminlte/AdminLTE.min.css";
import "../assets/js/adminlte/adminlte.js";
import "font-awesome/css/font-awesome.css";
import "../assets/css/Ionicons/css/ionicons.min.css";
import config from "@/config";
import utils from "@/utils/utils";

export default {
  data() {
    return {
      loading: [],
      projects: [],
      currentPage: 1,
      pageSize: 3,
      interval: null,
      dialogVisible1: false,
      dialogVisible2: false,
      dialogVisible3: false,
      dialogVisible4: false,
      newProjectName: null,
      dialogParam: ''
    };
  },
  mounted() {
    console.log(config.BASE_URL);
    let success = (response) => {
      if (response.status === 200) {
        this.projects = response.data.projects;
        this.taskProgress();
      }
    };
    utils.axiosMethod({
      method: "get",
      url: config.BASE_URL + "/getAllProject",
      callback: success,
    });
  },
  computed: {
    pagedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.projects.slice(start, end);
    },
  },
  beforeRouteLeave(to, from, next) {
    localStorage.removeItem("data");
    next();
  },
  methods: {
    toNew() {
      const _this = this;
      if (
          _this.newProjectName == null ||
          _this.newProjectName == "" ||
          _this.newProjectName.trim().length == 0
      ) {
        _this.$message.warning("项目名不能为空");
        return;
      }
      _this.newProjectName = this.newProjectName.trim();
      utils.axiosMethod({
        method: "GET",
        url: config.BASE_URL + "/queryProjectName/" + _this.newProjectName,
        callback: (res) => {
          const flag = parseInt(res.data.createFlag);
          if (flag === 0) {
            _this.$message.success("项目名可用");
            _this.dialogVisible3 = false;
            _this.$router.push({
              name: "create",
              params: {
                projectName: _this.newProjectName,
              },
            });
          } else {
            _this.$message.warning("项目名已存在，请重新输入");
          }
        },
        catch: (err) => {
          _this.$message.error("创建请求异常");
          _this.dialogVisible3 = false;
        },
      });
    },
    toMain(item) {

      let success = (response) => {
        console.log(response);
        if (response.data.progress === 1) {
          this.$store.commit("setCurrProject", item);
          this.$store.commit("refreshIndexList");
          this.$router.push({
            name: "main",
          });
        } else if (response.data.progress === -1) {
          this.dialogParam = item.name;
          this.dialogVisible2 = true;

        } else {
          this.dialogVisible1 = true;
        }
      };
      utils.axiosMethod({
        method: "get",
        url: config.BASE_URL + "/task_progress/" + item.task_id + "/" + item.name,
        callback: success,
      });

    },

    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    remove(item, task_id) {
      console.log("item: ", item);
      //if (item === "Demo-1" || item === "Demo-2" || item === "Demo-3") {
      //  console.log("item2: ", item);
      //  this.$message.warning("该项目用于演示，禁止删除！");
      //  return;
      //}
      const _this = this;
      this.$confirm("此操作将删除该项目, 是否继续？", "提示", {
        confirmButtonText: "确 定",
        cancelButtonText: "取 消",
        type: "warning",
      }).then(() => {
        let success = (response) => {
          _this.$message({
            type: "success",
            message: "删除成功!",
          });
          _this.$router.go(0);
        };
        utils.axiosMethod({
          method: "delete",
          url: config.BASE_URL + "/remove_project/" + item + "/" + task_id,
          callback: success,
          catch: (err) => {
            _this.$message.error("删除异常");
          },
        });
      });
    },
    taskProgress() {
      const _this = this;
      let flag = 0;
      for (let i = 0; i < _this.projects.length; i++) {
        let success = (response) => {
          if (response.data.progress === 1) {
            _this.projects[i].ready = true;
          } else if (response.data.progress === -1) {
            _this.projects[i].failed = true;
          }
          flag++;
        };
        if (!_this.projects[i].ready && !_this.projects[i].failed) {
          utils.axiosMethod({
            method: "get",
            url:
                config.BASE_URL +
                "/task_progress/" +
                _this.projects[i].task_id +
                "/" +
                _this.projects[i].name,
            callback: success,
          });
        } else {
          flag++;
        }
      }
    },
    toUserManual() {
      this.$router.push({name: "user_manual"});
    }
  },
};
</script>

<style scoped>
.nav-top {
  margin-left: 30px;
  margin-top: 10px;
  float: left;
}

.box—wrapper {
  height: 500px;
  display: flex;
  overflow: auto;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  align-content: center;
  flex-flow: row wrap;
  box-sizing: border-box;
}

.box-card {
  background-image: url(../assets/img/background.png);
  width: 30%;
  height: 200px;
  margin-top: 50px;
  /*margin-bottom: 50px;*/
  display: flex;
  justify-content: center;
  align-items: center;
  align-content: center;
}

.box-card:hover {
  background-color: cornsilk;
}

.upload {
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  align-content: center;
}

.des {
  margin-top: 5px;
}

.button-g {
  display: flex;
  justify-content: center;
  flex-direction: row;
  align-items: center;
  align-content: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.code-style {
  color: #ea5757;
  background-color: #ececea;
  border-radius: 2px;
  padding: 2px 4px;
}
</style>
