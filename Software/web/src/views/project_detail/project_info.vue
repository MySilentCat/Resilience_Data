<template>
    <div class="main">
        <div ref="myChart" class="main-left"></div>

        <div class="main-right">
            <div class="tables">
                <div class="table1">
                    <el-table :data="tableData1" border
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                        <!-- <el-table-column
                            prop="dirNumber"
                            label="文件夹"
                            align="center">
                        </el-table-column> -->
                        <el-table-column prop="fileNumber" label="文件" align="center">
                        </el-table-column>
                        <el-table-column prop="functionNumber" label="函数" align="center">
                        </el-table-column>
                    </el-table>
                </div>
                <div class="table2">
                    <el-table :data="tableData2" border
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
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

                <div class="table3">
                    <el-table :data="tableData3" border
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                        <el-table-column prop="codeLineExpProp" label="有效代码行占比" align="center">
                        </el-table-column>
                        <el-table-column prop="emptyLineProp" label="空行占比" align="center">
                        </el-table-column>
                        <el-table-column prop="commentLineExpProp" label="有效注释行占比" align="center">
                        </el-table-column>
                    </el-table>
                </div>

                <div class="table4">
                    <el-table :data="tableData4" border
                        :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}">
                        <el-table-column prop="UML_name" label="UML文件" align="center">
                        </el-table-column>
                        <el-table-column prop="UML_status" label="状态" align="center">
                        </el-table-column>
                    </el-table>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import utils from "../../utils/utils"
import config from "../../config"
export default {
    data(){
        return {
            project: {
                name: "项目XXX"
            },
            projectInfo: null,
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
                            { value: 1048, name: 'header' },
                            { value: 735, name: 'c_source' },
                            { value: 580, name: 'c++_source' },
                            { value: 484, name: 'other_file' }
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
            tableData3: [],
            tableData4: []
        }
    },
    mounted(){
        console.log(this.$store.state.current_project.name)
        this.getData()
    },
    methods: {
        chartInit(){
            this.myChart = this.$echarts.init(this.$refs.myChart)
            this.myChart.setOption(this.option)
            let myChart = this.myChart
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if(myChart){
                    myChart.resize()
                }
            })
        },
        getData() {
            console.log(config.BASE_URL)
            console.log("获取项目信息")
            const _this = this
            utils.axiosMethod({
                method: "GET",
                url: config.BASE_URL + "/GetprojectInfo/" + this.$store.state.current_project.name,
                callback: (response)=>{
                    console.log(response)
                    // 启用菜单栏
                    _this.$store.commit("setMenuDisabled", false)
                    let data = response.data
                    this.option = {
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
                                data: data.fileProp,
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
                    this.chartInit()

                    this.tableData1 = [{
                        dirNumber: data.dirNumber + "个",
                        fileNumber: data.fileNumber + "个",
                        functionNumber: data.functionNumber + "个"
                    }]
                    this.tableData2 = [{
                        codeLine: data.codeLine + "行",
                        codeLineExp: data.codeLineExp + "行",
                        commentLine: data.commentLine + "行",
                        commentLineExp: data.commentLineExp + "行"
                    }]
                    this.tableData3 = [{
                        codeLineExpProp: data.codeLineExpProp,
                        emptyLineProp: data.emptyLineProp,
                        commentLineExpProp: data.commentLineExpProp
                    }]

                    this.tableData4 = [{
                        UML_name: data.docs,
                        UML_status: "解析成功"
                    }]

                }
            })

            // let data = {
            //     // 文件分布
            //     "fileProp": [
            //         {
            //             "name": ".h",  // 文件类型
            //             "value": 156  // 数量
            //         },
            //         {
            //             "name": ".c",
            //             "value": 230
            //         },
            //         {
            //             "name": ".cpp",
            //             "value": 42
            //         },
            //         {
            //             "name": "other_file",
            //             "value": 60
            //         }
            //     ],
            //     "fileNumber": 130,  // 文件数
            //     "functionNumber": 2000,  // 函数数
            //     "codeLine": 2683,  // 代码行数
            //     "codeLineExp": 646,  // 有效代码行数
            //     "commentLine": 1896,  // 注释行数
            //     "commentLineExp": 1546,  // 有效注释行数
            //     "codeLineExpProp": "86.3%",  // 有效代码行占比
            //     "emptyLineProp": "3.2%",  // 空行占比
            //     "commentLineExpProp": "10.5%"  //有效注释行占比
            // }
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
    height: 89vh;
    width: 50vw;
    padding-left: 3%;
}

.main-right {
    height: 89vh;
    width: 50%;
    padding: 3% 3% 3% 3%;
}

.tables {
    height: 100%;
    width: 100%;
    padding-top: 5%;
}

.table1 {
    width: 90%;
    margin-bottom: 10%;
}

.table2 {
    width: 90%;
    margin-bottom: 10%;
}

.table3 {
    width: 90%;
    margin-bottom: 10%;
}

.table4 {
    width: 90%;
    margin-bottom: 10%;
}
</style>