<template>
  <el-tabs
    v-if="Object.keys(file_list)[0]!='null'||Object.keys(file_list).length!=1"
    v-model="Object.keys(file_list)[0]"
    style="width: 95%; margin: auto; margin-top: 10px"
    @tab-click="handleClick"
  >
    <el-tab-pane
      v-for="(value, key) in file_list"
      v-if="key !='null'"
      :key="key"
      :label="key"
      :name="key"
    >
      <el-row type="flex" style="margin-top: 5px">
        <el-col :lg="12" :xs="24" style="font-size: 18px">
          <div class="div4">
            <span class="link-right" style="font-weight: bold">文档 </span>
            <span>&nbsp全部{{ key }}</span>
          </div>
        </el-col>
      </el-row>
      <div class="link-top"></div>
      <el-table
        ref="singleTable"
        :data="value.filter((v) => v.val!=null).slice((currentPage - 1) * 10, currentPage * 10)"
        tooltip-effect="dark"
        highlight-current-row
        height="calc(100vh - 300px)"
        width="100%"
        style="margin: auto; margin-top: 10px"
        :key="key1"
      >
        <el-table-column
          type="index"
          width="60"
          label="序号"
          align="center"
          :index="indexMethod"
        >
        </el-table-column>

        <el-table-column prop="des" label="描述" sortable min-width="50%">
          <template slot-scope="scope">
            <i class="el-icon-document"></i>
            &nbsp{{ scope.row.des }}
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" sortable min-width="10%"></el-table-column>
        <el-table-column prop="val" label="值" sortable min-width="10%"></el-table-column>
        <el-table-column prop="source" label="路径" sortable min-width="30%"> </el-table-column>
      </el-table>

      <el-pagination
        @current-change="handleCurrentPageChange"
        style="text-align: center; margin-top: 20px"
        :current-page="currentPage"
        :page-size="10"
        layout="total, prev, pager, next, jumper"
        :total="value.filter((v) => v.val!=null).length"
      >
      </el-pagination>
    </el-tab-pane>
  </el-tabs>
 
</template>
<script>
import MathJax from "@/utils/MathJax.js";
import utilsApi from "@/utils/utils.js";
import config from "../../config";
export default {
  data() {
    return {
      key1: 0,
      currentPage: 1,
      file_list: {},
      activeName: "second",
    };
  },
  mounted() {
    this.formatMath();
    const _this = this;
    utilsApi.axiosMethod({
      method: "get",
      url: config.BASE_URL + "/fileInfo/" + _this.$store.state.current_project.name,
      callback: (res)=>{
        //  console.log(res)
        _this.file_list = JSON.parse(JSON.stringify(res.data));
      }
    })
    },
  methods: {
    handleClick(tab, event) {
      //输出当前的tab-pane名称
      //   console.log(tab.name);
      this.currentPage = 1;
    },
    // 方法
    indexMethod(index) {
      return (this.currentPage - 1) * 10 + index + 1;
    },

    formatMath() {
      let that = this;

      that.$nextTick(function () {
        if (MathJax.isMathjaxConfig) {
          //判断是否初始配置，若无则配置。
          MathJax.initMathjaxConfig();
        }
        MathJax.MathQueue("1"); //传入组件id，让组件被MathJax渲染
      });
    },
    handleCurrentPageChange(val) {
      this.currentPage = val;
      this.key1 += 1;
      this.formatMath();
      //   console.log("当前页数为：", val);
    },
  },
};
</script>

<style scoped>
/*中间的过度的横线*/
.link-top {
  width: 98%;
  height: 1px;
  margin: 0 auto;
  margin-top: 15px;
  float: left;
  border-top: solid #acc0d8 1px;
}

/*画一条在右边的竖线*/
.link-right {
  width: 50px;
  height: 100%;
  border-right: solid #acc0d8 1px;
}

.div4 {
  width: 100%;
  height: 100%;
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: left;
  align-items: center;
  -webkit-justify-content: left;
  justify-content: left;
}
</style>