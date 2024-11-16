<template>
  <div>
    <el-container style="height:88vh;border:1px solid #eee">
      <el-aside class="grid-content">
        <!--模块树-->
        <el-tree :data="fileTreeData" :props="fileProps" node-key="id" max-depth="1" highlight-current ref="tree"
          class="tree" default-expand-all @node-click="fileNodeClick">
        </el-tree>
      </el-aside>

      <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
        <!--文件级详细信息-->
        <el-row :gutter="15" style="height:98%" class="detailCards">
          <el-col :span="7" style="height:100%">
            <!--文件类型/名称/大小-->
            <el-card shadow="hover" style="height:32%; margin-bottom: 10px">
              <div class="fileLevelTitle" style="margin-bottom: 10px; font-size: 30px" v-if="fileId != ''">
                {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].type }}
              </div>
              <div>
                <div style="display:inline-block" class="fileitem">文件名:</div>
                <div style="display:inline-block " class="fileitem1" v-if="fileId != ''">{{ fileName }}</div>
              </div>
              <div>
                <div style="display:inline-block" class="fileitem">大小：</div>
                <div style="display:inline-block" v-if="fileId != ''" class="fileitem1">
                  {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].size }}
                </div>
              </div>
              <div>
                <div style="display:inline-block" class="filePath">路径：</div>
                <div style="display:inline-block" v-if="fileId != ''" class="filePath1" :title="this.fileLevel.moduleList[this.moduleName][this.fileId].codePath">
                  {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].codePath }}
                </div>
              </div>

            </el-card>

            <!--权限信息fileAuthority-->
            <el-card shadow="hover" class="authority-box-card" style="height:32%; margin-bottom: 10px">
              <div slot="header" class="clearfix">
                <span class="fileLevelTitle">权限</span>
              </div>

              <div v-for="(o, index) in fileAuthority" :key="index" class="text item">
                {{ o }}
              </div>
            </el-card>

            <!--if-else最大分支数&loopMaxDeep-->
            <el-card shadow="hover" style="height:32%; ">
              <div>
                <div style="display:inline-block" class="fileitem">if-else最大分支数:</div>
                <div style="display:inline-block; font-size: 16px" v-if="this.fileId != ''">
                  {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].ifelseMaxBranchNumber }}</div>
              </div>
              <div>
                <div style="display:inline-block" class="fileitem">最大循环深度：</div>
                <div style="display:inline-block; font-size: 16px" v-if="this.fileId != ''">
                  {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].loopMaxDeep.deep }}</div>
              </div>
              <div>
                <div style="display:inline-block" class="fileitem">最大循环深度函数：</div>
                <div v-if="this.fileId != ''"  style="display:inline-block; font-size: 16px">
                  <div v-if="this.fileLevel.moduleList[`${moduleName}`][`${fileId}`].loopMaxDeep.function.length !=0">
                  {{ fileLevel.moduleList[`${moduleName}`][`${fileId}`].loopMaxDeep.function }}
                  </div>
                  <div v-else >None</div>
                </div>

              </div>
            </el-card>
          </el-col>

          <el-col :span="17" style="height:100%">
            <!--双向柱状图展示代码信息-->
            <div class="grid-content1" ref="codeInfo" style="height:41%; margin-bottom: 20px">
            </div>
            <el-col :span="12" style="height:55%;padding-left: 0; ">
              <!--堆叠图展示变量数-->
              <div class="grid-content1" ref="variableInfo" style="height:100%">
              </div>
            </el-col>
            <el-col :span="12" style="height:55%; padding-right: 0;">
              <!--函数列表-->
              <div class="functionCard">
                <div class="fileLevelTitle" style="margin-top: 10px">函数列表</div>
                <el-table class="functionTable" :row-style="{ height: '20px' }" :cell-style="{ padding: '5px' }"
                  :data="functionList" style="width:100%; font-size: 16px" height="80%">
                  <el-table-column type="index" width="50">
                  </el-table-column>
                  <el-table-column property="name" label="函数名">
                  </el-table-column>
                </el-table>
              </div>
            </el-col>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import utils from "../../utils/utils";
import config from "../../config"

export default {
  name: "file_level",
  data() {
    return {
      myChart: null,//代码信息双向柱状图
      myChart1: null,//变量堆叠图

      //代码信息双向柱状图
      codeInfoOption: {
        title: {
          text: '代码信息',
          left: "left",
          subtext: '',
          textStyle: {
            color: "#000"
          }
        },
        color: ['#60c4c4', '#fca268', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
        },
        legend: {
          left: "center",
          top: "15%",
          data: ['总代码行数', '总注释行数', '有效代码行数', '有效注释行数'],
          textStyle: { fontSize: 12 }
        },
        toolbox: {
          show: false
        },
        Calculable: true,
        grid: [{ left: "50%", top: "40%", bottom: "20%" }, { right: '50%', top: "40%", bottom: "20%" }],
        yAxis: [
          {
            type: 'category',
            axisLine: { show: true, onZero: false },
            axisTick: { show: false },
            axisLabel: { show: false },
            splitArea: { show: false },
            splitNumber: 20,
            splitLine: { show: false },
            data: ['有效行数'],
            position: "bottom",
            zlevel: 10,
            show: true,
            min: 0,
          },
          {
            type: 'category',
            show: false,
            axisLine: { show: true, onZero: false },
            axisTick: { show: false },
            axisLabel: { show: false },
            splitArea: { show: false },
            splitNumber: 20,
            splitLine: { show: false },
            data: ['总行数'],
            gridIndex: 1,
            position: "bottom",
            zlevel: 10,
            min: 0,
          }
        ],
        xAxis: [
          {
            type: 'value',
            name: "有效代码行数",

            minInterval: 1,
            splitLine: false,
            nameTextStyle: { color: "#FFF" },
            max: 3000,
            min: 0
          },
          {
            type: 'value',
            name: "总代码行数",
            minInterval: 1,

            position: "left",
            splitLine: false,
            gridIndex: 1,
            nameGap: 30,
            inverse: true,
            nameTextStyle: { color: "#FFF" },
            max: 3000,
            min: 0

          },
          {
            type: 'value',
            name: "有效注释行数",
            show: false,
            minInterval: 1,
            splitLine: false,
            nameGap: 30,
            nameTextStyle: { color: "#FFF" },
            max: 3000,
            min: 0
          },
          {
            type: 'value',
            name: "总注释行数",
            show: false,
            minInterval: 1,
            position: "left",
            splitLine: false,
            gridIndex: 1,
            nameGap: 30,
            inverse: true,
            nameTextStyle: { color: "#FFF" },
            max: 3000,
            min: 0
          },

        ],
        series: [
          { type: "bar", name: "有效代码行数", barMaxWidth: 30, label: { show: true, position: "right" }, data: [] },
          { type: "bar", name: "总代码行数", barMaxWidth: 30, label: { show: true, position: "left" }, data: [], xAxisIndex: 1, yAxisIndex: 1 },
          { type: "bar", name: "有效注释行数", barMaxWidth: 30, label: { show: true, position: "right" }, data: [], xAxisIndex: 2 },
          { type: "bar", name: "总注释行数", barMaxWidth: 30, label: { show: true, position: "left" }, data: [], xAxisIndex: 3, yAxisIndex: 1 }
        ]
      },

      //变量堆叠图
      variableOption: {
        title: {
          text: '变量信息',
          left: "left",
          subtext: '',
          textStyle: {
            color: "#000"
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        color: ['#9FE080', '#FFDC60', '#5C7BD9'],
        legend: {
          left: "right",
          right: "20%",
          top: "40",
          textStyle: { fontSize: 12 }
        },
        grid: {
          left: '10%',
          bottom: '10%',
          top: '90',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: ['']
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: 'heap',
            type: 'bar',
            // stack: 'Ad',
            barMaxWidth: 30,
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true
            },
            data: []
          },
          {
            name: 'stack',
            type: 'bar',
            // stack: 'Ad',
            barMaxWidth: 30,
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true
            },
            data: []
          },

          {
            name: 'constant',
            type: 'bar',
            barMaxWidth: 30,
            label: {
              show: true
            },
            data: [],
            emphasis: {
              focus: 'series'
            },
          },
        ]
      },

      //文件树
      fileProps: {
        id: 'id',
        children: 'children',
        label: 'label'
      },
      fileTreeData: [],

      // 文件级信息
      fileLevel: {
        // "projectName": "CUnit",
        // "moduleList":
        // {
        //   "module1": {
        //     "file1": {
        //       "name": "filename", // 文件名
        //       "type": ".c", // 文件类型
        //       "codePath": "xx", // 文件路径
        //       "size": "10.2KB",
        //       "functionNumber": 25, // 文件定义的函数个数
        //       "globalVariable": 10, // 全局变量个数
        //       "variable": {
        //         "heap": 2,  // 堆区变量个数
        //         "stack": 2, // 栈区变量个数
        //         "constant": 5 // 常量区变量个数
        //       },
        //       "functionList": ["fun1()", "func2"], // 函数列表
        //       "ifelseMaxBranchNumber": 0, // 最大if-else分支数
        //       "loopMaxDeep": {
        //         "deep": 2, // 最大循环深度
        //         "function": "xxx" // 最大循环深度函数
        //       },
        //       "codeInfo": {
        //         "codeLine": 2683, // 总代码行数
        //         "codeLineExp": 646, // 有效代码行数
        //         "commentLine": 1896, // 总注释行数
        //         "commentLineExp": 1546 // 有效注释行数
        //       },
        //       "fileAuthority": {
        //         "read": 1, // 0为不可读，不可写，不可执行
        //         "write": 1,
        //         "execute": 1
        //       }
        //     },
        //     "file2": {
        //       "name": "filename", // 文件名
        //       "type": ".h", // 文件类型
        //       "codePath": "xx", // 文件路径
        //       "size": "9.2KB",
        //       "functionNumber": 25, // 文件定义的函数个数
        //       "globalVariable": 10, // 全局变量个数
        //       "variable": {
        //         "heap": 1,  // 堆区变量个数
        //         "stack": 3, // 栈区变量个数
        //         "constant": 5 // 常量区变量个数
        //       },
        //       "functionList": ["fun1()", "func2"], // 函数列表
        //       "ifelseMaxBranchNumber": 0, // 最大if-else分支数
        //       "loopMaxDeep": {
        //         "deep": 2, // 最大循环深度
        //         "function": "xxx" // 最大循环深度函数
        //       },
        //       "codeInfo": {
        //         "codeLine": 2683, // 总代码行数
        //         "codeLineExp": 646, // 有效代码行数
        //         "commentLine": 1896, // 总注释行数
        //         "commentLineExp": 1546 // 有效注释行数
        //       },
        //       "fileAuthority": {
        //         "read": 1, // 0为不可读，不可写，不可执行
        //         "write": 1,
        //         "execute": 1
        //       }
        //     }
        //   },
        //   "module2": {
        //     "file3": {
        //       "name": "main", // 文件名
        //       "type": ".c", // 文件类型
        //       "codePath": "xx", // 文件路径
        //       "size": "10.2KB",
        //       "functionNumber": 25, // 文件定义的函数个数
        //       "globalVariable": 10, // 全局变量个数
        //       "variable": {
        //         "heap": 0,  // 堆区变量个数
        //         "stack": 1, // 栈区变量个数
        //         "constant": 5 // 常量区变量个数
        //       },
        //       "functionList": ["fun1()", "func2"], // 函数列表
        //       "ifelseMaxBranchNumber": 0, // 最大if-else分支数
        //       "loopMaxDeep": {
        //         "deep": 2, // 最大循环深度
        //         "function": "xxx" // 最大循环深度函数
        //       },
        //       "codeInfo": {
        //         "codeLine": 2683, // 总代码行数
        //         "codeLineExp": 646, // 有效代码行数
        //         "commentLine": 1896, // 总注释行数
        //         "commentLineExp": 1546 // 有效注释行数
        //       },
        //       "fileAuthority": {
        //         "read": 1, // 0为不可读，不可写，不可执行
        //         "write": 1,
        //         "execute": 1
        //       }
        //     },
        //     "file4": {
        //       "name": "test", // 文件名
        //       "type": ".c", // 文件类型
        //       "codePath": "xx", // 文件路径
        //       "size": "10.2KB",
        //       "functionNumber": 25, // 文件定义的函数个数
        //       "globalVariable": 10, // 全局变量个数
        //       "variable": {
        //         "heap": 2,  // 堆区变量个数
        //         "stack": 2, // 栈区变量个数
        //         "constant": 5 // 常量区变量个数
        //       },
        //       "functionList": ["fun1()", "func2"], // 函数列表
        //       "ifelseMaxBranchNumber": 0, // 最大if-else分支数
        //       "loopMaxDeep": {
        //         "deep": 2, // 最大循环深度
        //         "function": "xxx" // 最大循环深度函数
        //       },
        //       "codeInfo": {
        //         "codeLine": 2683, // 总代码行数
        //         "codeLineExp": 646, // 有效代码行数
        //         "commentLine": 1896, // 总注释行数
        //         "commentLineExp": 1546 // 有效注释行数
        //       },
        //       "fileAuthority": {
        //         "read": 1, // 0为不可读，不可写，不可执行
        //         "write": 1,
        //         "execute": 1
        //       }
        //     }
        //   }
        // }
      },

      //展示信息,临时存储
      fileId: '',
      fileName: '',
      fileAuthority: [],
      functionList: [],
      moduleName: '',

    }
  },
  methods: {
    // 文件树过滤
    getFileTreeData(data) {
      this.fileTreeData = []
      let obj = {};
      obj.label = data.projectName;
      obj.children = [];
      obj.id = 0;
      let i = 1;
      let j = 0;
      for (const [key, value] of Object.entries(data.moduleList)) {
        let obj1 = {};
        obj1.id = i;
        obj1.label = key;
        obj1.children = [];
        for (const [key1, value1] of Object.entries(value)) {
          // fileLevel中的moduleList中的value为file
          let obj2 = {};
          obj2.id = key1; //key作为id eg file1
          obj2.label = value1.name; //value中的name属性作为label 是文件名
          obj2.type = value1.type
          obj1.children.push(obj2)
          j++
        }
        // 根据文件类型和文件名排序
        obj1.children.sort((a, b) => {
          const types = [".c", ".h"]
          if(a.type != b.type) {
            return types.indexOf(a.type) - types.indexOf(b.type)
          }
          return a.label.localeCompare(b.label)
        })
        obj.children.push(obj1)
        i++;
      }
      this.fileTreeData.push(obj)
    },

    // 点击文件名，加载文件级详细信息函数
    fileNodeClick(item, data) {
      if (data.children != null) {
        return;
      }
      this.moduleName = data.parent.data.label;
      this.fileId = item.id;
      this.fileName = item.label;

      // 1. 加载函数列表，变成字典格式
      this.functionList = [];
      for (let i = 0; i < this.fileLevel.moduleList[this.moduleName][this.fileId].functionList.length; i++) {
        let obj = {};
        obj.name = this.fileLevel.moduleList[this.moduleName][this.fileId].functionList[i];
        this.functionList.push(obj);
      }

      // 2. 加载权限信息
      this.fileAuthority = [];
      this.fileAuthority.push(this.fileLevel.moduleList[this.moduleName][this.fileId].fileAuthority.read === "1" ? "可读" : "不可读");
      this.fileAuthority.push(this.fileLevel.moduleList[this.moduleName][this.fileId].fileAuthority.write === "1" ? "可写" : "不可写");
      this.fileAuthority.push(this.fileLevel.moduleList[this.moduleName][this.fileId].fileAuthority.execute === "1" ? "可执行" : "不可执行");

      // 3.双向柱状图codeInfo
      // 根据file名取对应的codeInfo信息
      this.codeInfoOption.series[0].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.codeLineExp];
      this.codeInfoOption.series[1].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.codeLine];
      this.codeInfoOption.series[2].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.commentLineExp];
      this.codeInfoOption.series[3].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.commentLine];

      // 双向柱状图最大值设置为 max{总代码行数，总注释行数} 向上取整
      let maxOne = Math.max(this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.codeLine, this.fileLevel.moduleList[this.moduleName][this.fileId].codeInfo.commentLine)
      let max = 0;
      if (maxOne < 10) {
        max = maxOne + 3;
      } else if (maxOne <= 100) {
        max = Math.ceil(maxOne / 10) * 10 + 10;
      }
      max = Math.ceil(maxOne / 100) * 100 + 500;
      this.codeInfoOption.xAxis[0].max = max;
      this.codeInfoOption.xAxis[1].max = max;
      this.codeInfoOption.xAxis[2].max = max;
      this.codeInfoOption.xAxis[3].max = max;

      // 渲染双向柱状图
      if (this.myChart != null) {

        this.myChart.dispose(); //销毁

      }
      this.myChart = this.$echarts.init(this.$refs.codeInfo)
      this.myChart.setOption(this.codeInfoOption)
      let myChart = this.myChart
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (myChart) {
          myChart.resize()
        }
      })

      // 4.变量堆叠图variableOption
      // 根据file名取对应的cyclComplexity信息
      this.variableOption.series[0].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].variable.heap];
      this.variableOption.series[1].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].variable.stack];
      this.variableOption.series[2].data = [this.fileLevel.moduleList[this.moduleName][this.fileId].variable.constant];

      // 渲染堆叠图
      if (this.myChart1 != null) {

        this.myChart1.dispose(); //销毁

      }
      this.myChart1 = this.$echarts.init(this.$refs.variableInfo)
      this.myChart1.setOption(this.variableOption)
      let myChart1 = this.myChart1
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (myChart1) {
          myChart1.resize()
        }
      })

    }

  }
  ,
  mounted() {

    // 先将fileName置为空
    this.fileId = "";

    const _this = this
    utils.axiosMethod({
      method: "GET",
      url: config.BASE_URL + "/codeFileInfo/" + _this.$store.state.current_project.name,
      callback: (res)=>{
        _this.fileLevel = JSON.parse(JSON.stringify(res.data));

        // 如果树结构是空的
        if (_this.fileLevel.length === 0) {
          _this.$message({
            message: '该项目没有文件',
            type: 'warning'
          });
          return;
        }

        //加载模块树数据
        _this.getFileTreeData(_this.fileLevel)


        // 进入页面时,树默认点击第一个三级节点
        _this.$nextTick(() => {
          //this.$refs.tree.setCurrentKey(this.fileTreeData[0].children[0].children[0].id);
          // 点击该节点
          document.querySelector('.el-tree-node__children .el-tree-node__children .el-tree-node__content').click()
        })


        _this.myChart = _this.$echarts.init(_this.$refs.codeInfo)
        _this.myChart.setOption(_this.codeInfoOption)
        let myChart = _this.myChart
        //根据窗口大小进行动态缩放
        window.addEventListener("resize", () => {
          if (myChart) {
            myChart.resize()
          }
        })

        //加载变量堆叠图echarts
        _this.myChart1 = _this.$echarts.init(_this.$refs.variableInfo)
        _this.myChart1.setOption(_this.variableOption)
        let myChart1 = _this.myChart1
        //根据窗口大小进行动态缩放
        window.addEventListener("resize", () => {
          if (myChart1) {
            myChart1.resize()
          }
        })

      }
    })



  }
}
</script>

<style scoped>
.fileLevelTitle {
  /*二级标题*/
  font-size: 20px;
  font-weight: 600;

}

.grid-content {
  padding-top: 10px;
  border: 1px solid #EBEEF5;
  /*自适应高度*/
  height: 100%;
  width: 20vw;
  overflow-x: scroll;
}

/*两个echarts图的框的样式*/
.grid-content1 {
  border: 1px solid #EBEEF5;
  /*圆角框*/
  border-radius: 5px;
  /*内边距设置*/
  padding-top: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

.grid-content1:hover {
  /* 悬浮显示阴影*/
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}

/*函数列表card样式*/
.functionCard {
  border: 1px solid #EBEEF5;
  /*圆角框*/
  border-radius: 5px;
  /*内边距设置*/
  padding-top: 5px;
  padding-left: 10px;
  padding-right: 10px;
  height: 100%;
}

.functionCard:hover {
  /* 悬浮显示阴影*/
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}

/*函数列表样式*/
.functionTable {
  /*内边距设置*/
  padding-left: 15px;
  padding-right: 15px;
}

.detailCards {
  /*外边距*/
  margin-top: 10px;

}

/*card样式*/
.text {
  font-size: 14px;
}

/*权限列表样式*/
.item {
  padding: 3px;
  font-size: 16px;
}

.authority-box-card /deep/ .el-card__body {
  padding-top: 10px;
}

.authority-box-card /deep/ .el-card__header {
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 20px;
}

/*文件信息样式*/
.fileitem {
  font-size: 16px;
  margin-top: 10px;
}

.fileitem1 {
  padding-left: 15%;
  width: 80%;
  font-size: 16px;
  /* 自动换行 */
  word-wrap: break-word;
}

.filePath {
  font-size: 16px;
  margin-top: 10px;
  /* 靠上 */
  vertical-align: top;
}

.filePath1{
  font-size: 16px;
  padding-left: 15%;
  /* 自动换行 */
  word-wrap: break-word;
  width: 80%;
  padding-top: 10px;

}

/*树形结构样式*/
.tree /deep/ .el-tree-node{
    width: max-content;
}

/* 点击节点*/
.tree /deep/ .el-tree-node:focus>.el-tree-node__content {
  color: #409eff; 
  font-weight: bold;
}

.tree /deep/ .el-tree-node__content {
  height: 30px;
}

/* 鼠标悬浮节点*/
.tree /deep/ .el-tree-node__content:hover {
  color: #409eff; 
  font-weight: bold;
}

/*当前已选中节点样式*/
.tree /deep/ .el-tree-node.is-current>.el-tree-node__content {
  color: #409eff;
  font-weight: bold;
}
</style>