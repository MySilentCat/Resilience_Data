<template>
    <div style="height: 88vh;">
        <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
        <el-row style="height:20%;width:100%">
          <el-col :span="24"><el-card class="box-card" style="height:100%">
                    <div slot="header" class="clearfix">
                      <span class="fileLevelTitle">调用返回风格架构图</span>
                      <el-popover placement="right" trigger="click" style="margin-left: 5px">
                        <div>&bull; 节点表示组件，边表示调用关系</div>
                        <div>&bull; 使用滚轮向上进行放大，滚轮向下进行缩小</div>
                        <el-button slot="reference" icon="el-icon-question"  type="text" circle style="padding: 0; font-size: 17px"></el-button>
                      </el-popover>
                      <el-button type="success" size="medium" class="node-btn" @click="toUpdate">更新组件</el-button>
                    </div>
                    <p id="intro_text">调用返回风格顾名思义，就是指在系统中采用了调用与返回机制。利用调用返回实际上是一种分而治之的策略，其主要思想是将一个复杂的大系统分解为一些子系统，以便降低复杂度，并且增加可修改性。图中每个节点都是一个组件，组件是由一组功能相似的函数组成，节点之间的边表示组件之间的调用关系。</p>
                  </el-card></el-col>
        </el-row>
        <el-row style="height:1%;width:100%">
        </el-row>
        <el-row style="height:80%;width:100%">
          <el-col :span="18" style="height:100%">
          <div style="width:98%;height: 100%;">
            <!-- <webview :src="g_url+url" style="width:99%;height: 99%;"></webview> -->
            <iframe :key="fresh" :src="g_url+url" style="width:100%;height: 100%;border:none"></iframe>
        </div>
            </el-col>
          <el-col :span="6" style="height:100%">
                <el-card class="box-card" style="width:99%;height:50%" shadow="hover">
                    <template #header>
                    <div class="card-header">
                        <span>图信息</span>
                    </div>
                    </template>
                    <div ref="number_of_comps" class="text item">组件个数：</div>
                    <div ref="number_of_funcs" class="text item">总函数个数：</div>
                    <div ref="max_in_degree" class="text item">最大入度：</div>
                    <div ref="max_out_degree" class="text item">最大出度：</div>
                </el-card>
                <el-card class="box-card" style="width:99%; height:50%; overflow-y: scroll;" shadow="hover">
                    <template #header>
                    <div class="card-header">
                        <span>当前节点信息</span>
                    </div>
                    </template>
                    <div ref="node_name" class="text item">组件内函数：</div>
                    <div ref="node_type" class="text item">节点类型：</div>
                    <div ref="node_call_num" class="text item">出度：</div>
                    <div ref="node_called_num" class="text item">入度：</div>
                    <div ref="node_func_num" class="text item">包含函数个数：</div>
                </el-card>
            </el-col>
        </el-row>

        <el-dialog
        title="更新组件"
        :visible.sync="dialogVisible"
        width="40%">
            <div style="display: flex;">
                <el-transfer
                style="margin: 0 auto;"
                :data="selectList"
                v-model="selectRightList"
                :titles="[updateCompFrom.left, updateCompFrom.right]">
                    <div class="transfer-footer" slot="left-footer">
                        <el-select v-model="updateCompFrom.left" placeholder="请选择" @change="changeLeft">
                            <el-option
                                v-for="item in Object.keys(componentData)"
                                :disabled="item == updateCompFrom.right"
                                :key="item"
                                :label="item"
                                :value="item">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="transfer-footer" slot="right-footer">
                        <el-select v-model="updateCompFrom.right" placeholder="请选择" @change="changeRight">
                            <el-option
                                v-for="item in Object.keys(componentData)"
                                :disabled="item == updateCompFrom.left"
                                :key="item"
                                :label="item"
                                :value="item">
                            </el-option>
                        </el-select>
                    </div>
                </el-transfer>
            </div>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="sumbitUpdate">确 定</el-button>
        </span>
        </el-dialog>
      
      </div>
</template>

<script>
import utils from "@/utils/utils";
import config from "@/config"
export default {
    name: "GraphView",
    data() {
        return {
            g_url: "project/" + this.$store.state.current_project.name,
            url: "/graphs/level_comp.html",
            fresh: true,
            dialogVisible: false,
            componentData: {
                // "component1": [
                //     {"func1": "aaa.c"},
                //     {"func2": "bbb.c"},
                //     {"func3": "ccc.c"},
                //     {"func4": "ddd.c"},
                // ],
                // "component2": [
                //     {"func1": "eee.c"},
                //     {"func2": "fff.c"},
                // ],
                // "component3": [
                //     {"func11": "aaa.c"},
                //     {"func22": "bbb.c"},
                //     {"func33": "ccc.c"},
                //     {"func44": "ddd.c"},
                // ],
                // "component4": [
                //     {"func55": "eee.c"},
                //     {"func66": "fff.c"},
                // ],
            },
            updateCompFrom: {
                left: null,
                right: null
            },
            selectList: [],
            selectRightList: []
        }
    },
    mounted() {
        const _this = this
        // 接受iframe组件传过来的数据
        window.addEventListener('message', (e)=>{
            console.log("接受html页面的数据", e.data);
            if(e.data.flag == "graph"){
            if(this.$refs.number_of_comps){this.$refs.number_of_comps.innerHTML = "组件个数：" + e.data.data["组件个数："]
            this.$refs.number_of_funcs.innerHTML = "总函数个数：" + e.data.data["总函数个数："]
            this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："]
            this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："]}
            
            }
            if(e.data.flag == "node"){
                if(this.$refs.node_name){
                    this.$refs.node_name.innerHTML = e.data.data["节点名称："]
                this.$refs.node_func_num.innerHTML = "包含函数个数：" + e.data.data["包含函数个数："]
                this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["节点类型："]
                this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："]
                this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："]
                }
                
            }
            if(e.data.flag == "update"){
                utils.axiosMethod({
                    method: "POST",
                    url:
                        config.BASE_URL +
                        "/updateCallBackGraph/" +
                        _this.$store.state.current_project.name,

                    data: {
                        path: e.data.data["path"],
                        funcname: e.data.data["func"],
                        comp: e.data.data["comp"],
                        // "file_path": null,
                    },
                    callback: (res) => {
                        // _this.fresh = !_this.fresh
                        // _this.$router.push("home")
                    },
                    })
            }
        })
        let params = this.$route.meta.params
        // console.log("%%%%%%", params);
        utils.axiosMethod({
                method: "GET",
                url: config.BASE_URL + "/getCallBackGraphInfo/" + this.$store.state.current_project.name,
                callback: (res) => {
                    this.url = "/graphs/level_comp_" + res.data.time + ".html"
                },
                catch: (err) => {
                    _this.$message.error("获取数据异常")
                }
            })
    },
    methods: {
        toUpdate() {
            const _this = this
            utils.axiosMethod({
                method: "GET",
                url: config.BASE_URL + "/getCallBackGraphInfo/" + this.$store.state.current_project.name,
                callback: (res) => {
                    _this.componentData = res.data.data
                    _this.dialogVisible = true
                },
                catch: (err) => {
                    _this.$message.error("获取数据异常")
                }
            })
        },
        changeLeft(val) {
            let right = this.updateCompFrom.right
            this.selectList = []
            this.selectRightList = []
            for(let item of this.componentData[val]) {
                let key = Object.keys(item)[0]
                let value = item[key]
                this.selectList.push({
                    key: key + "@" + value,
                    label: key,
                    data: item
                })
            }
            if(right != null) {
                for(let item of this.componentData[right]) {
                    let key = Object.keys(item)[0]
                    let value = item[key]
                    this.selectRightList.push(key + "@" + value)
                    this.selectList.push({
                        key: key + "@" + value,
                        label: key,
                        data: item
                    })
                }
            }
        },
        changeRight(val) {
            let left = this.updateCompFrom.left
            this.selectList = []
            this.selectRightList = []
            for(let item of this.componentData[val]) {
                let key = Object.keys(item)[0]
                let value = item[key]
                this.selectRightList.push(key + "@" + value)
                this.selectList.push({
                    key: key + "@" + value,
                    label: key,
                    data: item
                })
            }
            if(left != null) {
                for(let item of this.componentData[left]) {
                    let key = Object.keys(item)[0]
                    let value = item[key]
                    this.selectList.push({
                        key: key + "@" + value,
                        label: key,
                        data: item
                    })
                }
            }
        },
        sumbitUpdate() {
            const _this = this
            let left = this.updateCompFrom.left
            let right = this.updateCompFrom.right
            this.componentData[left] = []
            this.componentData[right] = []
            for(let item of this.selectList) {
                if(this.selectRightList.indexOf(item.key) == -1) {
                    this.componentData[left].push(item.data)
                } else {
                    this.componentData[right].push(item.data)
                }
            }
            // console.log("$%$%$%$%$%", this.componentData)
            utils.axiosMethod({
                method: "POST",
                url: config.BASE_URL + "/updateCallBackGraph/" + this.$store.state.current_project.name,
                data: _this.componentData,
                callback: (res) => {
                    _this.url = res.data.path
                    // _this.fresh = !_this.fresh
                    // _this.$router.push("/main/GraphView/架构视图/调用返回风格架构图")
                },
                catch: (err) => {
                    _this.$message.error("修改请求发生异常")
                }
            })
            
            this.updateCompFrom.left = null
            this.updateCompFrom.right = null
            this.selectList = []
            this.selectRightList = []
            this.dialogVisible = false
        }
    }
}
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

.node-btn{
    float: right;
}

</style>