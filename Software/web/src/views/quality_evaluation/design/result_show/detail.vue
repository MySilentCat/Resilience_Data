<template>
  <div class="container">
    <div class="list">
      <el-menu
        style="height: 100%"
        :default-active="this.listNodes[0].key"
        class="el-menu-vertical-demo"
        @select="handleSelect"
      >
        <el-menu-item v-for="item in listNodes" :index="item.key" :key="item.key">
          <i class="el-icon-document"></i>
          <span slot="title">{{ item.name }}</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="main">
      <div type="flex" style="margin-top: 15px; margin-left: 35px; height: 4%">
        <el-col :lg="12" :xs="24" style="font-size: 18px">
          <div class="div4">
            <span class="link-right" style="font-weight: bold">阈值 </span>
            <span>&nbsp{{ value }}</span>
          </div>
        </el-col>
      </div>
      <el-table
        :data="selectedData"
        stripe
        style="margin-left: 30px; width: auto; height: 96%"
        height="96%"
      >
        <el-table-column
          v-for="(item, index) in selectedTableHeader"
          :prop="item.prop"
          :label="item.label"
          :width="item.width"
          :key="index"
        >
        </el-table-column>
      </el-table>
      <el-pagination
        :key="keyPag"
        background
        layout="prev, pager, next"
        :current-page.sync="currentPage"
        :page-size="20"
        :total="totalNum"
        @current-change="getData"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import utils from "@/utils/utils";
import Cache from "@/utils/cache";
import config from "@/config";
export default {
  data() {
    return {
      currentPage: 1,
      totalNum: 0,
      keyPag: true,
      active: null,
      design_thresholds: null,
      listNodes: [
        {
          key: "overLongFunc",
          name: "长函数",
        },
        {
          key: "overLongParam",
          name: "长参数函数",
        },
        {
          key: "overCommentLine",
          name: "过多注释文件列表",
        },
        {
          key: "limitCommentLine",
          name: "过少注释文件列表",
        },
        {
          key: "overCyclComplexityFunc",
          name: "大圈复杂度函数",
        },
        {
          key: "overOutDegreeFunc",
          name: "大出度函数",
        },
        {
          key: "overInDegreeFunc",
          name: "大入度函数",
        },
        {
          key: "overCallDepthFunc",
          name: "过深调用函数",
        },
        {
          key: "funcCopy",
          name: "代码克隆函数",
        },
      ],
      selectedData: [],
      value: "",
      selectedTableHeader: [],
      tableHeaders: {
        overLongFunc: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "函数行数",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overLongParam: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "参数个数",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overCommentLine: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "文件名称",
            width: "160px",
          },
          {
            prop: "name3",
            label: "注释行数",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        limitCommentLine: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "文件名称",
            width: "160px",
          },
          {
            prop: "name3",
            label: "注释行数",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overCyclComplexityFunc: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "圈复杂度",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overOutDegreeFunc: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "出度值",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overInDegreeFunc: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "入度值",
            width: "160px",
          },
          {
            prop: "name4",
            label: "路径",
          },
        ],
        overCallDepthFunc: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数名",
            width: "200px",
          },
          {
            prop: "name3",
            label: "调用链",
          },
          {
            prop: "name4",
            label: "调用深度",
            width: "160px",
          },
          {
            prop: "name5",
            label: "路径",
          },
        ],
        funcCopy: [
          {
            prop: "name1",
            label: "序号",
            width: "160px",
          },
          {
            prop: "name2",
            label: "函数1",
            width: "200px",
          },
          {
            prop: "name3",
            label: "路径1",
          },
          {
            prop: "name4",
            label: "函数2",
            width: "200px",
          },
          {
            prop: "name5",
            label: "路径2",
          },
          {
            prop: "name6",
            label: "控制流图节点数",
          },
        ],
      },
    };
  },
  mounted() {
    this.active = this.listNodes[0].key;
    this.design_thresholds = Cache.getCache("design_thresholds");
    this.handleSelect(this.listNodes[0].key);
  },
  methods: {
    processData(res) {
      let key = this.active;
      let data = res.data;
      this.totalNum = data.totalNum;
      if (key != "value" && key != "overCallDepthFunc" && key != "funcCopy") {
        let list1 = data[key];
        let data1 = [];
        for (let i in list1) {
          let tmp = list1[i].name.split("/");
          data1.push({
            name1: parseInt(i) + 1,
            name2: tmp[tmp.length - 1],
            name3: list1[i].val,
            name4: tmp.join("/"),
          });
        }
        this.selectedData = data1;
      } else if (key === "overCallDepthFunc") {
        let list1 = data[key];
        let data1 = [];
        for (let i in list1) {
          let list2 = list1[i];
          let tmp = list2[0];
          let tmp1 = tmp.split("/");
          data1.push({
            name1: parseInt(i) + 1,
            name2: tmp1[tmp1.length - 1],
            name3: list2.toString(),
            name4: list2.length,
            name5: tmp,
          });
        }
        this.selectedData = data1;
      } else if (key === "funcCopy") {
        let list1 = data[key];
        let data1 = [];
        for (let i in list1) {
          let tmp = list1[i][0].split("/");
          let tmp_ = list1[i][0].split("/");
          tmp_.pop();
          let tmp1 = list1[i][1].split("/");
          let tmp1_ = list1[i][1].split("/");
          tmp1_.pop();
          data1.push({
            name1: parseInt(i) + 1,
            name2: tmp[tmp.length - 1],
            name3: tmp_.join("/"),
            name4: tmp1[tmp1.length - 1],
            name5: tmp1_.join("/"),
            name6: list1[i][2],
          });
        }
        this.selectedData = data1;
      }
    },
    getData() {
      const _this = this;
      let key = this.active;
      const map = {
        overLongFunc: "funcLength",
        overLongParam: "funcParamLength",
        overCommentLine: "fileComment",
        limitCommentLine: "shortComment",
        overCyclComplexityFunc: "funcCyclComplexity",
        overOutDegreeFunc: "funcOutDegree",
        overInDegreeFunc: "funcInDegree",
        overCallDepthFunc: "funcCallDeep",
        funcCopy: "funcCopyThreshold",
      };

      utils.axiosMethod({
        url:
          config.BASE_URL +
          "/badSmell/" +
          key +
          "/" +
          _this.$store.state.current_project.name +
          "/" +
          _this.currentPage,
        method: "GET",
        callback: (res) => {
          _this.value = _this.design_thresholds[map[key]];
          _this.selectedTableHeader = _this.tableHeaders[key];
          _this.processData(res);
        },
        catch: (err) => {
          _this.$message.error("获取数据异常");
        },
      });
    },
    handleSelect(key) {
      this.active = key;
      this.currentPage = 1;
      this.keyPag = !this.keyPag;
      this.getData();
    },
  },
};
</script>

<style scoped>
.container {
  height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: row;
}

.list {
  height: 90%;
  width: 20%;
  margin-top: 2%;
}

/*画一条在右边的竖线*/
.link-right {
  width: 50px;
  height: 100%;
  border-right: solid #acc0d8 1px;
}

.el-tree {
  width: 100%;
  margin-top: 2%;
}

.tree-node {
  margin-left: 1%;
}

.main {
  width: 80%;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.title {
  height: 15%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: xx-large;
}

.tables {
  width: 60%;
  height: 80%;
  margin: 0 auto;
}

.tables1 {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
  flex-flow: wrap;
  align-content: flex-start;
}

.table1 {
  width: 45%;
  height: 18%;
  margin: 2% auto;
}
</style>
