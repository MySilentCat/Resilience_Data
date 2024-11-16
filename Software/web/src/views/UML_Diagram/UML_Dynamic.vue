<template>
    <div style="height: 88vh">
      <!-- <div>
              <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
            </div> -->
      <el-row style="height: 20%; width: 100%">
        <el-col :span="24"
          ><el-card class="box-card" style="height: 100%">
            <div slot="header" class="clearfix">
              <span class="fileLevelTitle">基于动态贝叶斯网络的软件架构韧性评估</span>
              <el-popover placement="right" trigger="click" style="margin-left: 5px">
                <div>&bull; 圆形节点表示贝叶斯网络节点，边表示影响关系</div>
                <div>&bull; 使用滚轮向上进行放大，滚轮向下进行缩小</div>
                <el-button
                  slot="reference"
                  icon="el-icon-question"
                  type="text"
                  circle
                  style="padding: 0; font-size: 17px"
                ></el-button>
              </el-popover>
            </div>
          </el-card></el-col
        >
      </el-row>
      <el-row style="height: 1%; width: 100%"> </el-row>
      <el-row style="height: 80%; width: 100%">
        <el-col :span="18" style="height: 100%">
          <div style="width: 98%; height: 100%">
            <!-- <webview :src="g_url+url" style="width:99%;height: 99%;"></webview> -->
            <iframe
              :src="g_url + url"
              style="height: 100%; width: 100%; border: none"
            ></iframe>
          </div>
        </el-col>
        <el-col :span="6" style="height: 100%">
          <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>评估结果</span>
              </div>
            </template>
            <div ref="comp_nodes" class="text item">组件节点个数：</div>
            <div ref="path_nodes" class="text item">路径节点个数：</div>
            <div ref="re" class="text item">韧性评估结果：</div>
          </el-card>
          <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>当前节点信息</span>
              </div>
            </template>
            <div ref="node_name" class="text item">节点名称：</div>
            <div ref="node_type" class="text item">节点类型：</div>
            <div ref="CGBR" class="text item">重要程度：</div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script>
  export default {
    name: "GraphView",
    data() {
      return {
        g_url: "project/" + this.$store.state.current_project.name,
        url: "/Dynamic_UML.html",
      };
    },
    mounted() {
      // 接受iframe组件传过来的数据
      window.addEventListener("message", (e) => {
        console.log("接受html页面的数据", e.data);
        console.log(e.data.data);
        if (e.data.flag == "graph") {
          if (this.$refs.comp_nodes) {
            this.$refs.comp_nodes.innerHTML = "组件节点个数：" + e.data.data["Comp_nums"];
            this.$refs.path_nodes.innerHTML = "路径节点个数：" + e.data.data["Path_nums"];
            this.$refs.re.innerHTML = "韧性评估结果：" + e.data.data["Resilience"];
          }
        }
        if (e.data.flag == "node") {
          if (this.$refs.node_name) {
            this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["name"];
            this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["type"];
            this.$refs.CGBR.innerHTML = "重要程度：" + e.data.data["CGBR"];
          }
        }
      });
  
      let params = this.$route.meta.params;
      // console.log("%%%%%%", params);
      if (params.title == "UML_DynamicView") {
        this.url = "/Dynamic_UML.html";
      } else {
        this.url = "/radar/radar.html";
      }
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
  