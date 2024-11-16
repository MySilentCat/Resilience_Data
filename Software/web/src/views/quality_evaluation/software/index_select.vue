<template>
  <div>
    <el-container>
      <el-header style="margin-top: 20px; height: 120px">
        <el-row type="flex">
          <el-col :span="20" style="
              font-size: 22px;
              text-align: center;
              margin-top: 5px;
              margin-left:10%
            ">
            <span style="font-weight: bold">软件质量评估指标</span>
          </el-col>
          <el-col :span="4" style="font-size: 18px; text-align: left; margin-right:2.5%">
            <el-button type="primary" @click="goWeightSet">分配权重</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col style="text-align: left; font-size: 14px; margin-top: 10px">
            <li>
              <span style="color: red">红色指标</span>代表 [高度推荐使用] ，表示经常使用这个质量测度;
            </li>
            <li>
              <span style="color: green">绿色指标</span>代表 [推荐使用] ，表示在合适的时候使用这个质量测度;
            </li>
            <li>
              <span style="color: orange">橘色指标</span>代表 [用户自行判断使用] ，表示开发一个新的质量测度时将这个质量测度作为参考,因为新的质量测度具有未知的可靠性。
            </li>

            <li>树形列表对应指标名称、描述、测量函数</li>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="
          font-size: 18px;
          height: calc(100vh - 250px);
          text-align: center;
          margin-top: 20px;
          padding-top: 0;
        ">
        <div>
          <el-card class="box-card" shadow="never" style="margin-bottom: 20px">
            <el-tree
              :data="this.index_list"
              show-checkbox
              default-expand-all
              ref="tree"
              node-key="id"
              highlight-current
              :props="defaultProps"
              style="width: 95%; margin: auto"
            >
              <div
                class="custom-tree-node"
                slot-scope="{ node, data }"
                :style="changeFontColor(data.type)"
              >
                <div style="width: 100px; text-align: left">
                  {{ data.label }}
                </div>
                <div style="
                    float: right;
                    width: calc(100vw - 550px);
                    text-align: left;
                    margin-left: auto;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    font-size: 14px;
                    white-space: nowrap;
                  " :title="data.des">
                  {{ data.des }}
                </div>
                <div style="width: 100px; float: right">
                  <el-popover placement="top-start" :title="data.equation" width="100%" trigger="hover">
                    <li v-for="(item, index) in data.factors" :key="index">
                      {{ data.factors[index] }}
                    </li>
                    <el-button slot="reference" v-if="data.equation" style="
                        height: 10px;
                        float: right;
                        width: 100px;
                        position: relative;
                      "><span style="
                          position: absolute;
                          top: 50%;
                          left: 50%;
                          transform: translate(-50%, -50%);
                        ">计算公式</span></el-button>
                  </el-popover>
                </div>
              </div>
            </el-tree>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import indexList from "@/utils/index_list.js";
import MathJax from "@/utils/MathJax.js";
export default {
  data() {
    return {
      defaultProps: {
        children: "children",
        label: "label",
      },
      index_list: [],
    };
  },
  mounted() {
    this.formatMath();
    this.index_list = this.$store.state.index_list;

    if (this.$store.state.index_selected.length != 0) {
      let selected_list = [];
      for (let i = 0; i < this.$store.state.index_selected.length; i++) {
        selected_list.push(this.$store.state.index_selected[i].id);
      }
      this.$refs.tree.setCheckedKeys(selected_list);
    }
  },

  methods: {
    changeFontColor(type) {
      if (type == -1) {
        return "color: red";
      } else if (type == 0) {
        return "color: green";
      } else if (type == 1) {
        return "color: orange";
      } else {
        return " ";
      }
    },
    formatMath() {
      let that = this;
      setTimeout(function () {
        that.$nextTick(function () {
          if (MathJax.isMathjaxConfig) {
            //判断是否初始配置，若无则配置。
            MathJax.initMathjaxConfig();
          }
          MathJax.MathQueue("hello"); //传入组件id，让组件被MathJax渲染
        });
      }, 500);
    },
    goWeightSet() {
      //如果没有选择指标，就不跳转
      if (this.$refs.tree.getCheckedNodes(true, false).length == 0) {
        this.$message({
          message: "请先选择指标",
          type: "warning",
        });
        return;
      }

      //选择上的节点，只记录三级节点
      let select_nodes = this.$refs.tree.getCheckedNodes(true);
      //所有节点列表
      if (this.$store.state.index_selected.length != 0) {
        this.$store.commit("refreshIndexList");
        // this.$store.state.index_selected = [];
      }
      this.$store.commit("setIndexSelected", select_nodes);
      //  this.$store.state.index_selected = select_nodes;
      let node_list = this.$store.state.index_list;

      select_nodes.forEach((node) => {
        // console.log(node.id);
        //node.id =="1234"
        //node.id[0]无意义 node.id[1]-1代表是第某个一级指标
        //node.id[2]-1代表第某个二级指标 node.id[3]-1代表第某个三级指标
        var index_node =
          node_list[(parseInt(node.id / 100) % 10) - 1].children[
            (parseInt(node.id / 10) % 10) - 1
          ].children[(node.id % 10) - 1];

        //修改三级指标的selected属性
        index_node.selected = true;
        //判断二级和一级指标的selected属性是否修改了
        var second_node =
          node_list[(parseInt(node.id / 100) % 10) - 1].children[
          (parseInt(node.id / 10) % 10) - 1
          ];
        var first_node = node_list[(parseInt(node.id / 100) % 10) - 1];
        if (second_node.selected == false) {
          second_node.selected = true;
          if (first_node.selected == false) {
            first_node.selected = true;
          }
        }
      });
      //跳转到权重分配页面
      this.$router.push({ name: "weight_set" });
    },

  },
};
</script>
<style scoped>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>