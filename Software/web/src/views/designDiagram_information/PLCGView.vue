<template>
  <div style="height: 88vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">过程级调用图</span>

            <el-popover placement="right" trigger="click" style="margin-left: 5px">
              <div>&bull; 节点表示函数，边表示调用关系</div>
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

          <p id="intro_text">
            在过程级调用图(PLCG)中，每个节点表示C程序中的一个函数，边表示函数之间的调用关系。
          </p>
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
          <div ref="number_of_custom_functions" class="text item">用户定义函数个数：</div>
          <div ref="number_of_lib_functions" class="text item">库函数个数：</div>
          <div ref="number_of_unrecognized_functions" class="text item">
            未识别函数个数：
          </div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
          <div ref="max_call_depth" class="text item">最大调用深度：</div>
          <div ref="min_call_depth" class="text item">最小调用深度：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">函数名称：</div>
          <div ref="node_type" class="text item">函数类型：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
          <div ref="node_path" class="text item">函数声明文件：</div>
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
      url: "/graphs/PLCG.dot.html",
    };
  },
  mounted() {
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      console.log(e.data.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_nodes) {
          this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数"];
          this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数"];
          this.$refs.number_of_custom_functions.innerHTML =
            "用户定义函数个数：" + e.data.data["用户定义函数个数"];
          this.$refs.number_of_lib_functions.innerHTML =
            "库函数个数：" + e.data.data["库函数个数"];
          this.$refs.number_of_unrecognized_functions.innerHTML =
            "未识别函数个数：" + e.data.data["未识别函数个数"];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度"];
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度"];
          this.$refs.max_call_depth.innerHTML =
            "最大调用深度：" + e.data.data["最大调用深度"];
          this.$refs.min_call_depth.innerHTML =
            "最小调用深度：" + e.data.data["最小调用深度"];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "函数名称：" + e.data.data["节点名称"];
          this.$refs.node_path.innerHTML = "函数声明文件：" + e.data.data["函数位置"];
          this.$refs.node_type.innerHTML = "函数类型：" + e.data.data["节点类型"];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度"];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度"];
        }
      }
    });

    let params = this.$route.meta.params;
    // console.log("%%%%%%", params);
    if (params.title == "PLCG") {
      this.url = "/graphs/PLCG.dot.html";
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
