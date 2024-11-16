<template>
  <el-container v-loading="loading">
    <el-header style="margin-top: 20px; height: 40px">
      <el-row type="flex">
        <el-col :span="20" style="font-size: 22px; text-align: center; margin-top: 5px">
          <span style="font-weight: bold">设计质量评估指标</span>
        </el-col>
        <el-col :span="4" style="font-size: 18px; text-align: left">
          <!--          <el-button type="primary" @click="goResultShow" style="margin-left: 30px">下一步</el-button>-->
          <el-button
            type="primary"
            @click="dialogFormVisible = true"
            style="margin-left: 30px"
            >下一步</el-button
          >
          <el-dialog title="指标阈值设置" :visible.sync="dialogFormVisible">
            <el-form :model="threshold">
              <el-form-item label="函数长度阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcLength"
                  :placeholder="threshold.funcLength.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="文件过多注释行数阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.fileComment"
                  :placeholder="threshold.fileComment.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="文件过少注释行数阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.shortComment"
                  :placeholder="threshold.shortComment.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="函数参数个数阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcParamLength"
                  :placeholder="threshold.funcParamLength.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="函数圈复杂度阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcCyclComplexity"
                  :placeholder="threshold.funcCyclComplexity.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="函数入度阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcInDegree"
                  :placeholder="threshold.funcInDegree.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="函数出度阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcOutDegree"
                  :placeholder="threshold.funcOutDegree.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="函数调用深度阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcCallDeep"
                  :placeholder="threshold.funcCallDeep.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
              <el-form-item label="克隆函数CFG节点阈值" label-width="40%">
                <el-input-number
                  v-model="threshold.funcCopyThreshold"
                  :placeholder="threshold.funcCopyThreshold.toString()"
                  controls-position="right"
                  @change="handleChange"
                  :min="1"
                ></el-input-number>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="goResultShow">确 定</el-button>
            </div>
          </el-dialog>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-table
        :data="this.expert_list[0].metrics"
        ref="singleTable"
        highlight-current-row
        border
        style="width: 100%"
      >
        <el-table-column
          type="index"
          width="50"
          align="center"
          label="序号"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column prop="name" align="center" label="名称" min-width="10%">
        </el-table-column>
        <el-table-column prop="des" align="center" label="描述" min-width="20%">
        </el-table-column>
        <el-table-column prop="formula" align="center" label="公式" min-width="30%">
        </el-table-column>
        <el-table-column prop="factors" align="center" label="公式因子" min-width="35%">
          <template slot-scope="scope">
            <li v-for="(value, index) in scope.row.factors" :key="index">
              {{ value }}
            </li>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
import expertMetric from "@/utils/expertMetric.js";
import MathJax from "@/utils/MathJax.js";
import Cache from "@/utils/cache.js";
import utils from "../../../utils/utils";
import config from "../../../config";
export default {
  data() {
    return {
      dialogFormVisible: false,
      expert_list: this.copyList(expertMetric.data),
      threshold: {
        funcLength: 100, // 函数长度阈值
        fileComment: 100, // 文件过多注释行数阈值
        shortComment: 10, // 文件过少注释行数阈值
        funcParamLength: 10, // 函数参数个数阈值
        funcCyclComplexity: 10, // 函数圈复杂度阈值
        funcInDegree: 10, // 函数入度阈值
        funcOutDegree: 10, // 函数出度阈值
        funcCallDeep: 10, // 函数调用深度阈值
        funcCopyThreshold: 10, // 函数克隆的CFG节点阈值
      },
      // name: {
      //   "funcLength": "函数长度", // 函数长度阈值
      //   "fileComment": "文件过多注释行数", // 文件过多注释行数阈值
      //   "shortComment": "文件过少注释行数", // 文件过少注释行数阈值
      //   "funcParamLength": "函数参数列表长度", // 函数参数个数阈值
      //   "funcCyclComplexity": "函数圈复杂度", // 函数圈复杂度阈值
      //   "funcInDegree": "函数入度", // 函数入度阈值
      //   "funcOutDegree": "函数出度", // 函数出度阈值
      //   "funcCallDeep": "函数调用深度", // 函数调用深度阈值
      // },
      num: 0,
      loading: false,
    };
  },
  mounted() {
    this.formatMath();
    // console.log(this.expert_list[0].metrics);
  },
  methods: {
    handleChange() {
      this.$forceUpdate();
    },
    goResultShow() {
      this.loading = true;
      this.dialogFormVisible = false;
      // 需要将设置的阈值存入缓存，结果展示页面需要
      Cache.setCache("design_thresholds", this.threshold);
      const _this = this;

      utils.axiosMethod({
        method: "POST",
        url:
          config.BASE_URL +
          "/setExpertThreshold/" +
          _this.$store.state.current_project.name,
        data: _this.threshold,
        callback: (res) => {
          let result = res.data.metrix;
          // 将返回的评估结果存入缓存，跳转后的页面从缓存中取出这个结果
          Cache.setCache("design_result", result);
          _this.loading = false;
          _this.$router.push({ name: "result_show1" });
        },
        catch: (err) => {
          _this.$message.error("设置阈值异常");
          _this.loading = false;
        },
      });
    },
    copyList(objList) {
      let newList = [];
      for (var i = 0; i < objList.length; i++) {
        newList.push(JSON.parse(JSON.stringify(objList[i])));
      }
      return newList;
    },
    formatMath() {
      let that = this;
      setTimeout(function () {
        that.$nextTick(function () {
          if (MathJax.isMathjaxConfig) {
            //判断是否初始配置，若无则配置。
            MathJax.initMathjaxConfig();
          }
          MathJax.MathQueue("MathJax"); //传入组件id，让组件被MathJax渲染
        });
      }, 500);
    },
  },
};
</script>
