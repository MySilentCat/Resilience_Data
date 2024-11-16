<template>
  <div>
    <el-container style="height: 88vh; border: 1px solid #eee">
      <el-aside class="module-tree">
        <!--模块树-->
        <el-tree :data="moduleTreeData" :props="moduleProps" node-key="id" max-depth="1" highlight-current
                  default-expand-all class="tree"
                  @node-click="moduleNodeClick">
        </el-tree>
      </el-aside>

      <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
        <!--模块级详细信息-->
        <el-row :gutter="15" style="height: 35% " class="detailCards">
          <el-col :span="16" style="height: 100% ">
            <div class="grid-content1" ref="codeInfo" style="height: 100% ">

            </div>
          </el-col>
          <el-col :span="8" style="height: 100% ">
            <el-card shadow="hover" style="height: 48%; margin-bottom: 3%">
              <div style="display: inline-block"><h3>圈复杂度：</h3></div>
              <div style="display: inline-block" v-if="moduleName!=''"><h2>
                {{ moduleLevel.moduleList[`${moduleName}`].cyclComplexity }}</h2></div>
            </el-card>

            <el-card shadow="hover" style="height: 48% ">
              <div style="display: inline-block"><h3>耦合度：</h3></div>
              <div style="display: inline-block" v-if="moduleName!=''"><h2>
                {{ moduleLevel.moduleList[`${moduleName}`].coupling }}</h2></div>
            </el-card>
          </el-col>

        </el-row>

        <!--文件列表& halstead复杂度-->
        <el-row :gutter="15" style="height: 60%; margin-top:20px" class="detailCards">
          <el-col :span="12" style="height: 100%">
            <div class='grid-content2' style="height: 100%">
              <div class="modelLevelTitle" style="margin-top: 5px">文件信息</div>
              <!-- 表格记录文件信息 -->
              <el-table
                  :data="moduleLevel.moduleList[`${moduleName}`].fileList"
                  height="80%"
                  style="width: 100%" v-if="moduleName!=''">
                <el-table-column
                    type="index"
                    width="50"
                    align="center">
                </el-table-column>
                <el-table-column
                    prop="name"
                    label="文件名称">
                </el-table-column>
                <el-table-column
                    prop="path"
                    label="文件路径">
                </el-table-column>
              </el-table>
            </div>
          </el-col>
          <el-col :span="12" style="height: 100%">
            <div class='grid-content2' style="height: 100%">
              <div class="modelLevelTitle" style="margin-top: 5px">halstead复杂度</div>
              <el-table
                  v-if="moduleName!=''"
                  :data="Halstead"
                  height="80%"
                  style="width: 100%">
                <el-table-column
                    prop="name"
                    label="指标名称">
                </el-table-column>
                <el-table-column
                    prop="value"
                    label="度量值">
                </el-table-column>

              </el-table>
            </div>

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
  name: "module_information",
  data() {
    return {
      myChart: null,
      codeInfoOption: {
        // title: {
        //   text: '模块信息展示',
        //   left:"center",
        //   subtext: '',
        //   textStyle:{
        //     color:"#000"
        //   }
        // },
        color: ['#60c4c4', '#fca268', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
        },
        legend: {
          left: "center",
          top: "10px",
          data: ['总代码行数', '总注释行数', '有效代码行数', '有效注释行数'],
          textStyle: {fontSize: 14}
        },
        toolbox: {
          show: false
        },
        Calculable: true,
        grid: [{left: "50%", top: "47px", bottom: "20%"}, {right: '50%', top: "47px", bottom: "20%"}],
        yAxis: [
          {
            type: 'category',
            axisLine: {show: true, onZero: false},
            axisTick: {show: false},
            axisLabel: {show: false},
            splitArea: {show: false},
            splitNumber: 20,
            splitLine: {show: false},
            data: ['有效行数'],
            position: "bottom",
            zlevel: 10,
            show: true,
            min: 0,
          },
          {
            type: 'category',
            show: false,
            axisLine: {show: true, onZero: false},
            axisTick: {show: false},
            axisLabel: {show: false},
            splitArea: {show: false},
            splitNumber: 20,
            splitLine: {show: false},
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
            nameTextStyle: {color: "#FFF"},
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
            nameTextStyle: {color: "#FFF"},
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
            nameTextStyle: {color: "#FFF"},
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
            nameTextStyle: {color: "#FFF"},
            max: 3000,
            min: 0
          },

        ],
        series: [
          {type: "bar", name: "有效代码行数", barMaxWidth: 30, label: {show: true, position: "right"}, data: []},
          {type: "bar", name: "总代码行数", barMaxWidth: 30, label: {show: true, position: "left"}, data: [], xAxisIndex: 1, yAxisIndex: 1},
          {type: "bar", name: "有效注释行数", barMaxWidth: 30, label: {show: true, position: "right"}, data: [], xAxisIndex: 2},
          {type: "bar", name: "总注释行数", barMaxWidth: 30, label: {show: true, position: "left"}, data: [], xAxisIndex: 3, yAxisIndex: 1}
        ]
      },

      // 当前模块
      moduleName: '',

      // 渲染时必要的中间变量
      Halstead: [],
      // Halstead 中英文对照
      HalsteadMap: {
        "diffOperators": "不同操作符个数",
        "diffOperands": "不同操作数个数",
        "totalOperators": "操作符总数",
        "totalOperands": "操作数总数",
        "programLength": "程序长度",
        "programVocabularyLength": "程序词汇表长度",
        "calculatedProgramLength": "预测程序长度",
        "calculatedProgramProportion": "预期程序占比",
        "volume": "程序体积",
        "difficulty": "编程难度",
        "level": "程序级别",
        "effort": "编程工作量",
        "languageLevel": "语言级别",
        "hours": "编程时间",
        "programErrorPrediction": "程序错误预测"
      },

      // 模块树
      moduleProps: {
        id: 'id',
        children: 'children',
        label: 'label'
      },
      moduleTreeData: [],
      moduleLevel: {
        "projectName": "CUnit",
        "moduleList": {
          "module1": {
            "fileList": [
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              },
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              }
            ],
            "codeInfo": {
              "codeLine": 2683, // 总代码行数
              "codeLineExp": 646, // 有效代码行数
              "commentLine": 1896, // 总注释行数
              "commentLineExp": 1546 // 有效注释行
            },
            "cyclComplexity": 0.0, // 圈复杂度
            "coupling": 12, // 耦合度
            "Halstead": { // Halstead复杂度
              "diffOperators": 191, // 不同操作符个数
              "diffOperands": 191, // 不同操作数个数
              "totalOperators": 191, // 操作符总数
              "totalOperands": 191, // 操作数总数
              "programLength": 191, // 程序长度
              "programVocabularyLength": 191, // 程序词汇表长度
              "calculatedProgramLength": 191, // 预测程序长度
              "calculatedProgramProportion": 191, // 预期程序占比
              "volume": 191, // 程序体积
              "difficulty": 191, // 编程难度
              "level": 191, // 程序级别
              "effort": 191, // 编程工作量
              "languageLevel": 191, // 语言级别
              "hours": 191, // 编程时间
              "programErrorPrediction": 191 // 程序错误预测
            }
          },
          "module2": {
            "fileList": [
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              },
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              }
            ],
            "codeInfo": {
              "codeLine": 268,
              "codeLineExp": 164,
              "commentLine": 189,
              "commentLineExp": 154
            },
            "cyclComplexity": 0.0,
            "coupling": 12,
            "Halstead": {
              "diffOperators": 191,
              "diffOperands": 191,
              "totalOperators": 191,
              "totalOperands": 191,
              "programLength": 191,
              "programVocabularyLength": 191,
              "calculatedProgramLength": 191,
              "calculatedProgramProportion": 191,
              "volume": 191,
              "difficulty": 191,
              "level": 191,
              "effort": 191,
              "languageLevel": 191,
              "hours": 191,
              "programErrorPrediction": 191
            }
          },
          "module3": {
            "fileList": [
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              },
              {
                "name": "xxx.c",
                "path": "xx/xx/xxx/c"
              }
            ],
            "codeInfo": {
              "codeLine": 2683,
              "codeLineExp": 646,
              "commentLine": 1896,
              "commentLineExp": 1546
            },
            "cyclComplexity": 0.0,
            "coupling": 12,
            "Halstead": {
              "diffOperators": 191,
              "diffOperands": 191,
              "totalOperators": 191,
              "totalOperands": 191,
              "programLength": 191,
              "programVocabularyLength": 191,
              "calculatedProgramLength": 191,
              "calculatedProgramProportion": 191,
              "volume": 191,
              "difficulty": 191,
              "level": 191,
              "effort": 191,
              "languageLevel": 191,
              "hours": 191,
              "programErrorPrediction": 191
            }
          }
        }
      },
    }
  },
  methods: {

    // 模块树过滤
    getModuleTreeData(data) {
      let obj = {};
      obj.label = data.projectName;
      obj.children = [];
      obj.id = 'a';
      let i = 0;
      for (const [key, value] of Object.entries(data.moduleList)) {
        // modelLevel 中的 moduleList 中的 key 为lable
        let obj1 = {};
        obj1.id = i;
        obj1.label = key;
        obj.children.push(obj1)
        i++
      }
      this.moduleTreeData.push(obj)
    },

    // 点击模块，加载模块级详细信息
    moduleNodeClick(data) {
      if (data.children != null) {
        return;
      }

      // 取出 data.label 模块名
      this.moduleName = data.label;

      // 1. 双向柱状图 codeInfo
      if (this.myChart != null) {
        this.myChart.dispose(); //销毁
      }
      // 根据模块名取对应的codeInfo信息
      this.codeInfoOption.series[0].data = [this.moduleLevel.moduleList[this.moduleName].codeInfo.codeLineExp];
      this.codeInfoOption.series[1].data = [this.moduleLevel.moduleList[this.moduleName].codeInfo.codeLine];
      this.codeInfoOption.series[2].data = [this.moduleLevel.moduleList[this.moduleName].codeInfo.commentLineExp];
      this.codeInfoOption.series[3].data = [this.moduleLevel.moduleList[this.moduleName].codeInfo.commentLine];

      // 双向柱状图最大值设置为 max{总代码行数，总注释行数} 向上取整
      let maxOne = Math.max(this.moduleLevel.moduleList[this.moduleName].codeInfo.codeLine, this.moduleLevel.moduleList[this.moduleName].codeInfo.commentLine)
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

      //渲染双向柱状图
      this.myChart = this.$echarts.init(this.$refs.codeInfo)
      this.myChart.setOption(this.codeInfoOption)
      let myChart = this.myChart
      //根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (myChart) {
          myChart.resize()
        }
      })

      // 2. Halstead复杂度 信息
      this.Halstead = [];
      // 遍历halstead字典取出key value
      for (const [key, value] of Object.entries(this.moduleLevel.moduleList[this.moduleName].Halstead)) {
        let obj = {};
        obj.name = this.HalsteadMap[key];
        obj.value = value;
        this.Halstead.push(obj)
      }
    }

  },
  mounted() {
    // 先将fileName置为空
    this.moduleName = "";

    const _this = this


    // 请求后台数据
    utils.axiosMethod({
      method: "get",
      url: config.BASE_URL + "/moduleInfo/" + _this.$store.state.current_project.name,
      callback: (res) => {
        _this.moduleLevel = JSON.parse(JSON.stringify(res.data));

        // 如果树结构是空的
        if (_this.moduleLevel.length === 0) {
          _this.$message({
            message: '该项目没有文件',
            type: 'warning'
          });
          return;
        }

        // 加载模块树数据
        _this.getModuleTreeData(_this.moduleLevel)

        // 进入页面时,树默认点击第一个二级节点
        _this.$nextTick(() => {
          //this.$refs.tree.setCurrentKey(this.fileTreeData[0].children[0].children[0].id);
          // 点击该节点
          document.querySelector('.el-tree-node__children .el-tree-node__content').click()
        })

        // 加载模块级代码信息echarts
        _this.myChart = _this.$echarts.init(_this.$refs.codeInfo)
        _this.myChart.setOption(_this.codeInfoOption)
        let myChart = _this.myChart
        // 根据窗口大小进行动态缩放
        window.addEventListener("resize", () => {
          if (myChart) {
            myChart.resize()
          }
        })

      }
    })


  }
}
</script>


<style scoped>

/*标题样式*/
.modelLevelTitle {
  font-size: 20px;
  font-weight: 600;
  margin-top: 0px;
}

/*codeInfo 框样式*/
.grid-content1 {
  border: 1px solid #EBEEF5;
  border-radius: 5px;
  /*内边距设置*/
  padding-top: 10px;
  height: 200px;
}

.grid-content1:hover {
  /* 悬浮显示阴影*/
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}

/*文件信息& halstead复杂度信息 框样式*/
.grid-content2 {
  border: 1px solid #EBEEF5;
  /*圆角框*/
  border-radius: 5px;
  /*内边距设置*/
  padding-top: 10px;
  padding-left: 20px;
  padding-right: 10px;
}

.grid-content2:hover {
  /* 悬浮显示阴影*/
  transition: .3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
}

.detailCards {
  /*外边距*/
  margin-top: 10px;
}

/*自定义树节点样式*/
.module-tree {
  padding-top: 10px;
  border: 1px solid #dcdfe6;
  width: 20vw;
  overflow-x: scroll;
  /*自适应高度*/
  height: 100%;
}

.tree /deep/ .el-tree-node{
    width: max-content;
}

/* 点击节点*/
.tree /deep/ .el-tree-node:focus > .el-tree-node__content {
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
.tree /deep/ .el-tree-node.is-current > .el-tree-node__content {
  color: #409eff;
  font-weight: bold;
}


</style>