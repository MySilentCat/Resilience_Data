<template>
  <div style="height: 88vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">控制流图</span>
            <el-popover placement="right" trigger="click" style="margin-left: 5px">
              <div>&bull; 节点表示语句，边表示控制流</div>
              <div>&bull; 使用shift+滚轮向下进行放大，shift+滚轮向上进行缩小</div>
              <el-button
                slot="reference"
                icon="el-icon-question"
                type="text"
                circle
                style="padding: 0; font-size: 17px"
              ></el-button>
            </el-popover>
          </div>
          <p id="intro_text">
            控制流图(Control Flow Graph， CFG)是一个有向图G = (V,E)，其中V是顶点的集合，
            E是有向边的集合。在CFG中，每个顶点代表一个基本块，该基本块是具有一个入口点（执行的第一条指令）和一个出口点（执行最后一条指令）的程序指令的线性序列，有向边显示控制流路径。
            CFG用图的形式表示一个过程内所有基本块执行的可能流向，能反映一个过程的实时执行过程。从CFG中可以提取过程中顺序结构、选择结构和循环结构，观察过程内各个基本块之间的关系，有助于帮助分析程序代码执行的流程和可能的控制流路径，可以作为静态分析工具的基础。
          </p>
        </el-card></el-col
      >
    </el-row>
    <el-row style="height: 1%; width: 100%"> </el-row>
    <el-row style="height: 80%; width: 100%">
      <el-col :span="6" style="height: 100%">
        <!--模块树-->
        <el-tree
          :data="fileTreeData"
          :props="fileProps"
          node-key="id"
          max-depth="1"
          highlight-current
          ref="tree"
          class="tree"
          accordion
          @node-click="fileNodeClick"
        >
        </el-tree>
      </el-col>
      <el-col :span="12" style="height: 100%">
        <div style="width: 98%; height: 100%">
          <!-- <webview :src="g_url+url" style="width:99%;height: 99%;"></webview> -->
          <iframe
            ref="htmlwebview"
            :src="g_url + url"
            style="width: 100%; height: 100%; border: none"
          ></iframe>
        </div>
      </el-col>
      <el-col :span="6" style="height: 100%">
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>图信息</span>
            </div>
          </template>
          <div ref="number_of_nodes" class="text item">节点个数：</div>
          <div ref="number_of_edges" class="text item">边个数：</div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点语句：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import utilsApi from "@/utils/utils.js";
import config from "../../config";
export default {
  name: "GraphView",
  data() {
    return {
      g_url: "project/" + this.$store.state.current_project.name,
      url: "/graphs/cfg_graph.html",
      fileProps: {
        id: "id",
        children: "children",
        label: "label",
        path: "path",
      },
      fileTreeData: null,
    };
  },
  methods: {
    fileNodeClick(item, data) {
    if (data.data.type == "func") {
      console.log(data.data.path);
      this.$refs.htmlwebview.contentWindow.postMessage(
        { path: data.data.path, flag: "update" },
        "*"
      );
      console.log("向iframe发送信息", { path: data.data.path, flag: "update" });
      }
    },
  },
  mounted() {
    let _this = this;
    utilsApi.axiosMethod({
      method: "get",
      url: config.BASE_URL + "/CFG/" + _this.$store.state.current_project.name,
      callback: (res) => {
        //  console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
      },
    });
    let projectName = this.$store.state.current_project.name;
    // let treeData = (`./${projectName}/graphs/cfg.js`).treeData
    // import(`../../../public/project/${projectName}/graphs/cfg.js`).then((treeData) => {
    //     console.log("$$$", projectName, treeData)
    //     this.fileTreeData = treeData.treeData
    // })
    // import(`../../../public/project/${projectName}/graphs/cfg.js`).then((treeData) => {
    //     console.log("$$$", projectName, treeData)
    //     this.fileTreeData = treeData.treeData
    // })

    // let treeData = require(`../../../public/project/${projectName}/graphs/cfg.js`).treeData
    // console.log("$$$", projectName, treeData)
    // this.fileTreeData = treeData

    this.url = "/graphs/cfg_graph.html";

    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_nodes) {
          this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数："];
          this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数："];
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "节点语句：" + e.data.data["节点语句："];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
        }
      }
    });
  },
};
</script>

<style scoped>
/*标题样式*/
.fileLevelTitle {
  /*二级标题*/
  font-size: 20px;
  font-weight: 600;
}

.textitem {
  font-size: 20px;
  font-weight: 600;
}
</style>
