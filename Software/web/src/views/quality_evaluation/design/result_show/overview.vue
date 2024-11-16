<template>
  <div style="height: 80vh">
    <div class="main">
      <div class="col1">
        <div ref="Chart1" class="col1-1"></div>
        <div ref="Chart2" class="col1-2"></div>
      </div>
      <div class="col2">
        <div ref="Chart3" class="col2-1"></div>
      </div>
      <div class="col3">
        <div ref="Chart4" class="col3-1"></div>
        <div ref="Chart5" class="col3-2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Cache from "@/utils/cache";
export default {
  data() {
    return {
      metrix: null,
      thresholds: null,
      Chart1: null,
      Chart2: null,
      Chart3: null,
      Chart4: null,
      Chart5: null,
      option1: null,
      option2: null,
      option3: null,
      option4: null,
      option5: null,
    };
  },
  mounted() {
    this.metrix = Cache.getCache("design_result");
    this.thresholds = Cache.getCache("design_thresholds");

    this.initChart1();
    this.initChart2();
    this.initChart3();
    this.initChart4();
    this.initChart5();
  },
  methods: {
    initChart1() {
      let data = [];
      let num1 = this.metrix.scalability.apiNum;
      let num = this.metrix.scalability.funcNum;

      data.push({
        name: "api数量",
        value: num1,
        rate: ((num1 / num) * 100).toFixed(2).toString(),
        itemStyle: {
          color: "rgb(16, 135, 240)",
        },
      });
      data.push({
        name: "非api数量",
        value: num - num1,
        rate: (((num - num1) / num) * 100).toFixed(2).toString(),
        itemStyle: {
          color: "rgb(251, 59, 136)",
        },
      });
      this.option1 = {
        title: {
          text: "API占比",
          left: "center",
          top: "1%",
        },
        tooltip: {
          trigger: "item",
          formatter: (param) => {
            let item = param.data;
            return `${item.name}:<br />${item.value}个<br />${item.rate}%`;
          },
        },
        legend: {
          top: "bottom",
          left: "left",
        },
        series: [
          {
            name: "数据",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: data,
            label: {
              show: true,
              position: "inside",
            },
          },
        ],
      };
      this.Chart1 = this.$echarts.init(this.$refs.Chart1);
      this.Chart1.setOption(this.option1);
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (this.Chart1) {
          this.Chart1.resize();
        }
      });
    },
    initChart2() {
      let map = {
        overInDegreeFunc: "过大入度坏味",
        overOutDegreeFunc: "过大出度坏味",
        overCyclComplexityFunc: "过大圈复杂度坏味",
        overLongFunc: "过长函数坏味",
        overLongParam: "过长参数坏味",
        funcCopy: "克隆函数坏味",
      };
      let map1 = {
        overInDegreeFunc: "funcInDegree",
        overOutDegreeFunc: "funcOutDegree",
        overCyclComplexityFunc: "funcCyclComplexity",
        overLongFunc: "funcLength",
        overLongParam: "funcParamLength",
        funcCopy: "funcCopyThreshold",
      };
      let map2 = {
        overInDegreeFunc: "purple",
        overOutDegreeFunc: "gray",
        overCyclComplexityFunc: "rgb(78, 236, 54)",
        overLongFunc: "pink",
        overLongParam: "orange",
        funcCopy: "blue",
      };
      let data1 = [];
      let data2 = [];
      for (let key in map) {
        data1.push(map[key]);
        data2.push({
          value: this.metrix.badSmellRatio[key].funcNum,
          threshold: this.thresholds[map1[key]],
          itemStyle: {
            color: map2[key],
          },
        });
      }
      this.option2 = {
        title: {
          text: "设计坏味函数数量",
          left: "center",
          top: "1%",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: (param) => {
            let item = param[0];
            return `${item.name}:${item.data.value}个<br />阈值:${item.data.threshold}`;
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "value",
          },
        ],
        yAxis: [
          {
            type: "category",
            data: data1,
            axisTick: {
              alignWithLabel: true,
            },
          },
        ],
        series: [
          {
            name: "数量",
            type: "bar",
            barWidth: "60%",
            data: data2,
            label: {
              show: true,
              position: "right",
            },
          },
        ],
      };

      this.Chart2 = this.$echarts.init(this.$refs.Chart2);
      this.Chart2.setOption(this.option2);
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (this.Chart2) {
          this.Chart2.resize();
        }
      });
    },
    initChart3() {
      const map = {
        comprehensibility: "易理解性",
        refundability: "可替换性",
        scalability: "可扩展性",
        modifiability: "可修改性",
        testability: "易测试性",
        badSmellRatio: "坏味道率",
      };
      let indicator = [];
      let values = [];
      let names = [];
      for (let key in this.metrix) {
        indicator.push({
          name: map[key],
          max: 1,
        });
        values.push(this.metrix[key].value.toFixed(3));
        names.push(map[key]);
      }
      this.option3 = {
        tooltip: {
          trigger: "axis",
        },
        title: {
          text: "设计质量评估概况",
          left: "center",
          top: "2%",
        },
        radar: {
          // shape: 'circle',
          indicator: indicator,
          axisName: {
            color: "black",
            fontSize: "16px",
          },
        },
        series: [
          {
            tooltip: {
              trigger: "item",
            },
            name: "指标",
            type: "radar",
            data: [
              {
                value: values,
                name: names,
              },
            ],
            color: "red",
          },
        ],
      };
      this.Chart3 = this.$echarts.init(this.$refs.Chart3);
      this.Chart3.setOption(this.option3);
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (this.Chart3) {
          this.Chart3.resize();
        }
      });
    },
    initChart4() {
      let data1 = {
        name: "文件数量",
        num: this.metrix.comprehensibility.fileNum,
        value: 100,
      };
      let data2 = {
        name: "包含注释的文件数量",
        num: this.metrix.comprehensibility.commentFile,
        value: (
          (this.metrix.comprehensibility.commentFile /
            this.metrix.comprehensibility.fileNum) *
          100
        ).toFixed(2),
      };
      let data3 = {
        name: "过多注释文件数量",
        num: this.metrix.badSmellRatio.overCommentLine.fileNum,
        value: (
          (this.metrix.badSmellRatio.overCommentLine.fileNum /
            this.metrix.comprehensibility.fileNum) *
          100
        ).toFixed(2),
      };
      let data4 = {
        name: "过少注释文件数量",
        num: this.metrix.badSmellRatio.limitCommentLine.fileNum,
        value: (
          (this.metrix.badSmellRatio.limitCommentLine.fileNum /
            this.metrix.comprehensibility.fileNum) *
          100
        ).toFixed(2),
      };
      const gaugeData = [
        {
          value: data2.value,
          num: data2.num,
          name: data2.name,
          title: {
            offsetCenter: ["0%", "-35%"],
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ["0%", "-20%"],
          },
        },
        {
          value: data3.value,
          num: data3.num,
          name: data3.name,
          title: {
            offsetCenter: ["0%", "-5%"],
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ["0%", "10%"],
          },
        },
        {
          value: data4.value,
          num: data4.num,
          name: data4.name,
          title: {
            offsetCenter: ["0%", "25%"],
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ["0%", "40%"],
          },
        },
      ];
      this.option4 = {
        title: {
          text: "带注释文件占比",
          subtext: "文件数量——" + data1.num + "个",
          left: "center",
        },
        tooltip: {
          formatter: (params) => {
            let { name, num } = params.data;
            return `${name}<br /> ${num}个`;
          },
        },
        series: [
          {
            type: "gauge",
            center: ["50%", "58%"],
            startAngle: 90,
            endAngle: -270,
            pointer: {
              show: false,
            },
            progress: {
              show: true,
              overlap: false,
              roundCap: true,
              clip: false,
              itemStyle: {
                borderWidth: 1,
                borderColor: "#464646",
              },
            },
            axisLine: {
              lineStyle: {
                width: 40,
              },
            },
            splitLine: {
              show: false,
              distance: 0,
              length: 10,
            },
            axisTick: {
              show: false,
            },
            axisLabel: {
              show: false,
              distance: 50,
            },
            data: gaugeData,
            title: {
              fontSize: 10,
            },
            detail: {
              width: 40,
              height: 12,
              fontSize: 10,
              color: "inherit",
              borderColor: "inherit",
              borderRadius: 20,
              borderWidth: 1,
              formatter: "{value}%",
            },
          },
        ],
      };
      this.Chart4 = this.$echarts.init(this.$refs.Chart4);
      this.Chart4.setOption(this.option4);
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (this.Chart4) {
          this.Chart4.resize();
        }
      });
    },
    initChart5() {
      let data = this.metrix.badSmellRatio.overCallDepthFunc;
      let data1 = [];
      let data2 = [];
      if (data.length > 0) {
        let map = {};
        let minLen = Number.MAX_SAFE_INTEGER;
        let maxLen = 1;
        for (let i in data) {
          let len = data[i];
          minLen = Math.min(minLen, len);
          maxLen = Math.max(maxLen, len);
          if (len in map) {
            map[len]++;
          } else {
            map[len] = 1;
          }
        }
        let left = (maxLen - minLen + 1) % 5;
        if (left != 0) {
          maxLen += 5 - left;
        }
        let step = (maxLen - minLen + 1) / 5;
        let start = minLen;
        let end = minLen - 1 + step;
        for (let i = 1; i <= 5; i++) {
          data1.push(start + "~" + end);
          let count = 0;
          for (let k = start; k <= end; k++) {
            if (k in map) {
              count += map[k];
            }
          }
          data2.push(count);
          start = end + 1;
          end = start - 1 + step;
        }
      } else {
        data2.push(0);
      }

      this.option5 = {
        title: {
          text: "过深函数调用的路径长度分布",
          left: "center",
          top: "1%",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            data: data1,
            axisTick: {
              alignWithLabel: true,
            },
          },
        ],
        yAxis: [
          {
            type: "value",
          },
        ],
        series: [
          {
            name: "数量",
            color: "green",
            type: "bar",
            barWidth: "60%",
            data: data2,
            label: {
              show: true,
              position: "inside",
            },
            color: "orange",
          },
        ],
      };
      this.Chart5 = this.$echarts.init(this.$refs.Chart5);
      this.Chart5.setOption(this.option5);
      // 根据窗口大小进行动态缩放
      window.addEventListener("resize", () => {
        if (this.Chart5) {
          this.Chart5.resize();
        }
      });
    },
  },
};
</script>

<style scoped>
.main {
  height: 95%;
  width: 100%;
  display: flex;
  flex-direction: row;
  margin-top: 3%;
}
.col1 {
  height: 100%;
  width: 25%;
}
.col1-1 {
  height: 44%;
  width: 100%;
  margin-bottom: 2%;
  box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
.col1-2 {
  height: 44%;
  width: 100%;
  box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
.col2 {
  height: 90%;
  width: 48%;
  margin: 0 auto;
}
.col2-1 {
  height: 100%;
  width: 100%;
  box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
.col3 {
  height: 100%;
  width: 25%;
}
.col3-1 {
  height: 44%;
  width: 100%;
  margin-bottom: 2%;
  box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
.col3-2 {
  height: 44%;
  width: 100%;
  box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
</style>
