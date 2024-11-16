<template>
    <div>
        <el-tabs style="height: 6%;" type="border-card" v-model="activeName">
            <el-tab-pane label="评估概览" name="first"></el-tab-pane>
            <el-tab-pane label="评估详情" name="second"></el-tab-pane>
        </el-tabs>
        <div v-if="activeName == 'first'" class="container">
            <Overview class="container"></Overview>
        </div>
        <div v-if="activeName == 'second'" class="container">
            <Detail class="container"></Detail>
        </div>
    </div>
</template>

<script>
import Overview from './result_show/overview'
import Detail from './result_show/detail'
import Cache from '../../../utils/cache'
export default {
    name: "result_show",
    components: {
        Overview,
        Detail
    },
    data(){
        return {
            activeName: "first",
            result: null
        }
    },
    mounted(){
        // this.result = Cache.getCache("design_result")
    }
}
</script>

<style scoped>
.container{
    height: 94%;
    width: 100%;
}
</style>
