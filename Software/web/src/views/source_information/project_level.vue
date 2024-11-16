<template>
    <div class="main">
        <div class="main-left">
            <div ref="myChart" class="my-chart"></div>
            <div class="tables">
                <div class="table1">
                    <el-table :data="tableData1" border
                        :header-cell-style="() => { return 'background: antiquewhite;color:black;' }">
                        <el-table-column prop="dirNumber" label="文件夹" align="center">
                        </el-table-column>
                        <el-table-column prop="fileNumber" label="文件" align="center">
                        </el-table-column>
                        <el-table-column prop="functionNumber" label="函数" align="center">
                        </el-table-column>
                    </el-table>
                </div>
                <div class="table2">
                    <el-table :data="tableData2" border
                        :header-cell-style="() => { return 'background: antiquewhite;color:black;' }">
                        <el-table-column prop="codeLine" label="代码行" align="center">
                        </el-table-column>
                        <el-table-column prop="codeLineExp" label="有效代码行" align="center">
                        </el-table-column>
                        <el-table-column prop="commentLine" label="注释行" align="center">
                        </el-table-column>
                        <el-table-column prop="commentLineExp" label="有效注释行" align="center">
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </div>

        <div class="main-right">
            <div class="cards">
                <el-card class="card" shadow="hover" v-for="(card, index) in cardInfo" :key="index">
                    <div slot="header" style="font-weight: bolder;font-size:calc(100vw * 16 / 1920);">
                        <span>{{ card.title }}</span>
                    </div>
                    <div class="card-item">
                        <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.key1 }}</div>
                            </el-col>
                            <!--    <el-col :span="12">
                                <div style="text-align: right;">{{ card.val1 }}</div>
                            </el-col> -->
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row style="font-size:calc(100vw * 13 / 1920); color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.msg }}</div>
                            </el-col>
                            <div style="text-align: right;">{{ card.val1 }}</div>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row style="font-size:calc(100vw * 13 / 1920);">
                            <el-col :span="12">
                                <div>{{ card.key2 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val2 }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item" style="font-size:calc(100vw * 13 / 1920);">
                        <el-row>
                            <el-col :span="12">
                                <div>{{ card.key3 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val3 }}</div>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </div>
            <div class="table3">
                <el-table height="33vh" :data="tableData3" border
                    :header-cell-style="() => { return 'background: rgb(182, 254, 230);color:black;' }">
                    <el-table-column prop="name" label="源码文件" align="center">
                    </el-table-column>
                    <el-table-column prop="type" label="类型" align="center">
                        <template slot-scope="scope">
                            <span v-if="scope.row.type === 0">头文件</span>
                            <span v-else>源文件</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="path" label="路径" align="center">
                    </el-table-column>
                    <el-table-column prop="status" label="状态2" align="center">
                        <template slot-scope="scope">
                            <span v-if="scope.row.status == '0'" style="color: red;">解析失败</span>
                            <span v-if="scope.row.status == '1'" style="color: rgb(29, 232, 32);">解析成功</span>
                            <span v-if="scope.row.status == '-1'" style="color: rgb(147, 110, 46);">未解析</span>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script>
import utils from "../../utils/utils"
import config from "../../config"
export default {
    data() {
        return {
            project: {
                name: "项目XXX"
            },
            projectInfo: null,
            cardInfo: [
                // {
                //     title: null,
                //     key1: null,
                //     val1: null,
                //     key2: null,
                //     val2: null,
                //     key3: null,
                //     val3: null
                // }
            ],
            myChart: null,
            option: {
                title: {
                    text: this.$store.state.current_project.name + '文件种类',
                    left: 'center',
                    top: '5%'
                },
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    top: '5%'
                },
                series: [
                    {
                        // name: 'Access From',
                        type: 'pie',
                        radius: '50%',
                        data: [
                            { value: 1048, name: 'c' },
                            { value: 735, name: 'h' },
                            { value: 580, name: 'sh' },
                            { value: 484, name: 'README' },
                            { value: 300, name: 'disabled' }
                        ],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            },
            tableData1: [],
            tableData2: [],
            tableData3: []
        }
    },
    mounted() {
        this.project = this.$store.state.current_project
        this.getProjectInfo()
    },
    methods: {
        chartInit() {
            this.myChart = this.$echarts.init(this.$refs.myChart)
            this.myChart.setOption(this.option)
            let myChart = this.myChart
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart) {
                    myChart.resize()
                }
            })
        },
        getProjectInfo() {
            const _this = this
            utils.axiosMethod({
                method: "GET",
                url: config.BASE_URL + "/projectInfo/" + _this.project.name,
                callback: (res) => {
                    let projectInfo = res.data
                    let fileTypes = projectInfo.fileTypes
                    let typeList = []
                    for (let key in fileTypes) {
                        typeList.push({
                            name: key,
                            value: fileTypes[key].length
                        })
                    }

                    _this.option = {
                        title: {
                            text: _this.$store.state.current_project.name + '文件种类',
                            left: 'center',
                            top: '5%'
                        },
                        tooltip: {
                            trigger: 'item'
                        },
                        legend: {
                            orient: 'vertical',
                            left: 'left',
                            top: '5%'
                        },
                        series: [
                            {
                                // name: 'Access From',
                                type: 'pie',
                                radius: '50%',
                                data: typeList,
                                emphasis: {
                                    itemStyle: {
                                        shadowBlur: 10,
                                        shadowOffsetX: 0,
                                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                                    }
                                }
                            }
                        ]
                    }
                    _this.chartInit()

                    _this.cardInfo.push({
                        title: "最大行数函数",
                        key1: projectInfo.functionLine.maxLineFunc,
                        msg: "行数",
                        val1: projectInfo.functionLine.maxLine + "行",
                        key2: "平均行数",
                        val2: projectInfo.functionLine.avgLine.toFixed(2) + "行",
                        key3: "最小行数",
                        val3: projectInfo.functionLine.minLine + "行"
                    })
                    _this.cardInfo.push({
                        title: "最大行数文件",
                        key1: projectInfo.fileLine.maxLineFunc,
                        msg: "行数",
                        val1: projectInfo.fileLine.maxLine + "行",
                        key2: "平均行数",
                        val2: projectInfo.fileLine.avgLine.toFixed(2) + "行",
                        key3: "最小行数",
                        val3: projectInfo.fileLine.minLine + "行"
                    })
                    _this.cardInfo.push({
                        title: "包含函数最多的文件",
                        key1: projectInfo.defineFuncFile.maxFuncFile,
                        msg: "包含函数",
                        val1: projectInfo.defineFuncFile.maxFunc + "个",
                        key2: "平均包含函数",
                        val2: projectInfo.defineFuncFile.avgFunc.toFixed(2) + "个",
                        key3: "最小包含函数",
                        val3: projectInfo.defineFuncFile.minFunc + "个"
                    })
                    _this.cardInfo.push({
                        title: "最大出度函数",
                        key1: projectInfo.outDegreeFunc.maxOutFunc,
                        msg: "出度值",
                        val1: projectInfo.outDegreeFunc.maxOut,
                        key2: "平均出度",
                        val2: projectInfo.outDegreeFunc.avgOut.toFixed(2),
                        key3: "最小出度",
                        val3: projectInfo.outDegreeFunc.minOut
                    })
                    _this.cardInfo.push({
                        title: "最大入度函数",
                        key1: projectInfo.inDegreeFunc.maxInFunc,
                        msg: "入度值",
                        val1: projectInfo.inDegreeFunc.maxIn,
                        key2: "平均入度",
                        val2: projectInfo.inDegreeFunc.avgIn.toFixed(2),
                        key3: "最小入度",
                        val3: projectInfo.inDegreeFunc.minIn
                    })
                    _this.cardInfo.push({
                        title: "最大圈复杂度的函数",
                        key1: projectInfo.cyclComplexityFile.maxComplexFunc,
                        msg: "圈复杂度值",
                        val1: projectInfo.cyclComplexityFile.maxComplex,
                        key2: "平均圈复杂度",
                        val2: projectInfo.cyclComplexityFile.avgComplex.toFixed(2),
                        key3: "最小圈复杂度",
                        val3: projectInfo.cyclComplexityFile.minComplex
                    })

                    _this.tableData1 = [{
                        dirNumber: projectInfo.dirNumber + "个",
                        fileNumber: projectInfo.fileNumber + "个",
                        functionNumber: projectInfo.functionNumber + "个"
                    }]
                    _this.tableData2 = [{
                        codeLine: projectInfo.codeInfo.codeLine + "行",
                        codeLineExp: projectInfo.codeInfo.codeLineExp + "行",
                        commentLine: projectInfo.codeInfo.commentLine + "行",
                        commentLineExp: projectInfo.codeInfo.commentLineExp + "行"
                    }]
                    _this.tableData3 = projectInfo.fileList
                }
            })
        }
    }
}
</script>

<style scoped>
.main {
    display: flex;
    flex-direction: row;
}

.main-left {
    height: 100%;
    width: 50%;
    padding-left: 3%;
}

.my-chart {
    height: 60vh;
    width: 50vw;
}

.tables {
    height: 35%;
    width: 100%;
}

.table1 {
    /* height: 15%; */
    width: 90%;
    margin-bottom: 5%;
}

.table2 {
    /* height: 15%; */
    width: 90%;
}

.main-right {
    height: 100%;
    width: 50%;
    padding: 3% 3% 3% 3%;
}

.cards {
    height: 40%;
    width: 100%;
    display: flex;
    flex-flow: wrap;
}

.card {
    /* height: 40%; */
    width: 32%;
    margin-right: 1%;
    margin-bottom: 1%;
}

.card-item {
    font-size: calc(100vw * 15 / 1920);
    margin-bottom: 2%;
}

.table3 {
    height: 50%;
    width: 100%;
}
</style>