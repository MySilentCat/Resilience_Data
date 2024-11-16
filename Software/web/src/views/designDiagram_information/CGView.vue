<template>
  <div style="height: 88vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">调用图</span>
            <el-popover placement="right" trigger="click" style="margin-left: 5px">
              <div>&bull; 圆角矩形节点表示文件，圆形节点表示函数，边表示调用关系</div>
              <div>&bull; 双击文件节点可将该文件展开成函数，双击函数节点可恢复到文件节点</div>
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
            文件级调用图(FLCG)中，每个节点表示C语言项目中的一个文件，边表示两个文件之间存在的调用关系。
          </p>
        </el-card></el-col
      >
    </el-row>
    <el-row style="height: 1%; width: 100%"> </el-row>
    <el-row style="height: 69%; width: 100%">
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
          <div ref="number_of_nodes_file" class="text item">文件个数：</div>
          <div ref="number_of_edges_file" class="text item">文件调用边个数：</div>
          <div ref="number_of_nodes_func" class="text item">函数个数：</div>
          <div ref="number_of_edges_func" class="text item">函数调用边个数：</div>
          <div ref="number_of_custom_files" class="text item">用户定义文件个数：</div>
          <div ref="number_of_unrecognized_files" class="text item">未识别文件个数：</div>
          <div ref="number_of_custom_functions" class="text item">用户定义函数个数：</div>
          <div ref="number_of_unrecognized_functions" class="text item">
            未识别函数个数：
          </div>
          <div ref="max_in_degree_file" class="text item">文件最大入度：</div>
          <div ref="max_out_degree_file" class="text item">文件最大出度：</div>
          <div ref="max_call_depth_file" class="text item">文件最大调用深度：</div>
          <div ref="min_call_depth_file" class="text item">文件最小调用深度：</div>
          <div ref="max_in_degree_func" class="text item">函数最大入度：</div>
          <div ref="max_out_degree_func" class="text item">函数最大出度：</div>
          <div ref="max_call_depth_func" class="text item">函数最大调用深度：</div>
          <div ref="min_call_depth_func" class="text item">函数最小调用深度：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点名称：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
          <div ref="node_path" class="text item">文件路径：</div>
          <div ref="func_num" class="text item">包含函数个数：</div>
          <div ref="category" class="text item">节点类别：</div>
          <div ref="type" class="text item">节点类型：</div>
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
      url: "/graphs/CG.html",
    };
  },
  mounted() {
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      console.log(e.data.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_nodes_file) {
          this.$refs.number_of_nodes_file.innerHTML =
            "文件个数：" + e.data.data["文件个数："];
          this.$refs.number_of_edges_file.innerHTML =
            "文件调用边个数：" + e.data.data["文件调用边个数："];
          this.$refs.number_of_nodes_func.innerHTML =
            "函数个数：" + e.data.data["函数个数："];
          this.$refs.number_of_edges_func.innerHTML =
            "函数调用边个数：" + e.data.data["函数调用边个数："];
          this.$refs.number_of_custom_files.innerHTML =
            "用户定义文件个数：" + e.data.data["用户定义文件个数: "];
          this.$refs.number_of_unrecognized_files.innerHTML =
            "未识别文件个数：" + e.data.data["未识别文件个数: "];
          this.$refs.number_of_custom_functions.innerHTML =
            "用户定义函数个数：" + e.data.data["用户定义函数个数: "];
          this.$refs.number_of_unrecognized_functions.innerHTML =
            "未识别函数个数：" + e.data.data["未识别函数个数: "];
          this.$refs.max_in_degree_file.innerHTML =
            "文件最大入度：" + e.data.data["最大入度文件: "];
          this.$refs.max_out_degree_file.innerHTML =
            "文件最大出度：" + e.data.data["最大出度文件: "];
          this.$refs.max_call_depth_file.innerHTML =
            "文件最大调用深度：" + e.data.data["文件最大调用深度: "];
          this.$refs.min_call_depth_file.innerHTML =
            "文件最小调用深度：" + e.data.data["文件最小调用深度: "];
          this.$refs.max_in_degree_func.innerHTML =
            "函数最大入度：" + e.data.data["最大入度函数: "];
          this.$refs.max_out_degree_func.innerHTML =
            "函数最大出度：" + e.data.data["最大出度函数: "];
          this.$refs.max_call_depth_func.innerHTML =
            "函数最大调用深度：" + e.data.data["函数最大调用深度: "];
          this.$refs.min_call_depth_func.innerHTML =
            "函数最小调用深度：" + e.data.data["函数最小调用深度: "];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "文件名称：" + e.data.data["节点名称"];
          this.$refs.node_path.innerHTML = "文件路径：" + e.data.data["节点文件路径"];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度"];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度"];
          this.$refs.func_num.innerHTML = "包含函数个数：" + e.data.data["包含函数个数"];

          this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["节点名称："];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
          this.$refs.node_path.innerHTML = "文件路径：" + e.data.data["文件路径："];
          this.$refs.func_num.innerHTML =
            "包含函数个数：" + e.data.data["包含函数个数："];
          this.$refs.category.innerHTML = "节点类别：" + e.data.data["节点类别："];
          this.$refs.type.innerHTML = "节点类型：" + e.data.data["节点类型："];
        }
      }
    });

    let params = this.$route.meta.params;
    // console.log("%%%%%%", params);
    if (params.title == "FLCG") {
      this.url = "/graphs/CG.html";
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
