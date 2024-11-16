<template>
    <div class="container">
        <div class="tree">
            <el-tree ref="menuTree" :data="treeNodes" :props="defaultProps" default-expand-all highlight-current
                node-key="id" :expand-on-click-node="false" @node-click="handleNodeClick" :indent="50" class="el-tree">
                <span class="tree-node" slot-scope="{ node }">
                    <span>{{ node.label }}</span>
                </span>
            </el-tree>
        </div>

        <div class="main">
            <div class="title">{{ selectedNode.label }}</div>
            <div v-if="isLeaf" style="text-align: center;font-size: large;">{{this.result.des}}</div>
            <div class="cards" style="overflow:auto">
                <el-card v-if="isLeaf && card.val != null" class="card" shadow="hover"
                    v-for="(card, index) in selectedNode.sub" :key="index">
                    <div slot="header" class="card-header">
                        <el-col :span="12">
                            <div>{{ card.id }}</div>
                        </el-col>
                        <el-col :span="12">
                            <div style="text-align: right;">{{ card.val.toFixed(2) }}</div>
                        </el-col>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>描述</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.des }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>来源</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.source }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>来源类型</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.type }}</div>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>

                <el-card v-if="!isLeaf && card.value != null" class="card" shadow="hover"
                    v-for="(card, index) in selectedNode.sub" :key="index">
                    <div slot="header" class="card-header">
                        <el-col :span="12">
                            <div>{{ card.id }}</div>
                        </el-col>
                        <el-col :span="12">
                            <div style="text-align: right;">{{ card.val }}</div>
                        </el-col>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>值</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.value.toFixed(2) }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>权重</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.weight.toFixed(2) }}</div>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import utils from "../../../utils/utils"
import config from "../../../config"
import indexScope from "@/utils/index_scope.js";
export default {
    data() {
        return {
            treeNodes: [],
            defaultProps: {
                label: 'label',
                children: 'subMetric'
            },
            selectedNode: {
                label: "请选择指标",
                sub: []
            },
            isLeaf: false,
            index_scope: this.copyList(indexScope.data),
            result:''
        }
    },
    mounted() {
        this.getIndexSubInfo()
    },
    methods: {
        getIndexSubInfo() {
            const _this = this
            utils.axiosMethod({
                method: "GET",
                url: config.BASE_URL + "/getSelectedMetrics/" + _this.$store.state.current_project.name,
                callback: (res) => {
                    if (parseInt(res.data.metricCalculated) == -1) {
                        _this.$message({
                            message: '计算未完毕',
                            type: 'warning'
                        })
                        return
                    }

                    // 将返回的数据转换为嵌套树形嵌套列表
                    let data = res.data.data
                    // console.log("data", data)
                    let treeNodes = []
                    let flag = 1
                    for (let k in data) {
                        let data1 = data[k]
                        if (data1.val == null || data1.sub.length == 0)
                            continue
                        let treeNodes1 = []
                        for (let k1 in data1.subMetric) {
                            let data2 = data1.subMetric[k1]
                            if (data2.val == null || data2.sub.length == 0)
                                continue
                            let treeNodes2 = []
                            for (let k2 in data2.subMetric) {
                                let data3 = data2.subMetric[k2]
                                if (data3.val == null || data3.sub.length == 0)
                                    continue
                                treeNodes2.push({
                                    id: flag,
                                    label: data3.val != null ? data3.name + " — " + data3.val.toFixed(2) : data3.name,
                                    isLeaf: true,
                                    sub: data3.sub
                                })
                                flag++
                            }
                            treeNodes1.push({
                                id: flag,
                                label: data2.val != null ? data2.name + " — " + data2.val.toFixed(2) : data2.name,
                                isLeaf: false,
                                sub: data2.sub,
                                subMetric: treeNodes2
                            })
                            flag++
                        }
                        treeNodes.push({
                            id: flag,
                            label: data1.val != null ? data1.name + " — " + data1.val.toFixed(2) : data1.name,
                            isLeaf: false,
                            sub: data1.sub,
                            subMetric: treeNodes1
                        })
                        flag++
                    }
                    _this.treeNodes = treeNodes
                }
            })
        },
        handleNodeClick(e) {
            this.selectedNode = e
            console.log("selectedNode", this.selectedNode)
            this.isLeaf = e.isLeaf
            var nstr = this.selectedNode.label.split(' ');
            this.result = this.index_scope.find((item) => item.label === nstr[0]);  
        },
        copyList(objList) {
            let newList = [];
            for (var i = 0; i < objList.length; i++) {
                newList.push(JSON.parse(JSON.stringify(objList[i])));
            }
            return newList;
        }
    }
}
</script>

<style scoped>
.container {
    height: 89vh;
    width: 100%;
    display: flex;
}

.tree {
    height: 100%;
    width: 50%;
    overflow: auto;
    padding-left: 5%;
}

.el-tree {
    width: 100%;
    margin-top: 2%;
}

.tree-node {
    margin-left: 1%;
}

.main {
    height: 100%;
    width: 50%;
    display: flex;
    flex-direction: column;
}

.title {
    height: 10%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: x-large;
}

.cards {
    height: 85%;
    overflow: auto;
}

.card {
    height: auto;
    width: 60%;
    margin: 2% auto;
}

.card-header {
    font-weight: bolder;
    padding-bottom: 10%;
    font-size: medium;
    color: rgb(244, 70, 163);
}

.card-item {
    margin-bottom: 2%;
    font-size: small;
}
</style>
