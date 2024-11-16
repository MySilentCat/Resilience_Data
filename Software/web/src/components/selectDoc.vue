<template>
  <div>
    <el-main class="main—wrapper">
      <el-card class="box-card">
        <el-form ref="form" label-position="left" label-width="400px">
          <el-form-item v-for="(item,index) in docname" :key="item.id" :label="item">
            <el-select v-model="type[index]" placeholder="please select your zone">
              <el-option label="组件图" :value="1"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </el-card>

      <el-form ref="form" class="form" style="margin-top: 40px;">
        <el-form-item>
          <el-button type="primary" @click="onSubmit">选择完成</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="back">返回</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import NaviBar from "./NaviBar";

export default {
  name: "selectDoc",
  components: {NaviBar},
  data() {
    return {
      fileSelect: [],
      type: [],
      doclist: [],
      docname: []
    }
  },
  mounted() {
    this.doclist = this.$route.params.wd
    this.doclist.forEach((self, index) => {
      this.$set(this.docname, index, self)
      this.$set(this.type, index, 1)
    })
  },
  beforeRouteLeave(to, from, next) {
    //设置下一个路由的meta,让列表页面缓存,即不刷新
    to.meta.keepAlive = true;
    next();
  },
  methods: {
    onSubmit: function () {
      // console.log("msg", this.doclist)
      // console.log(this.docname)
      // console.log(this.type)
      this.doclist.forEach((self, index) => {
        switch (this.type[index]) {
          case 1:
            this.fileSelect.push({path: self, type: "组件图"});
            break
        }
      })
      console.log(this.fileSelect)
      this.$router.push({
        name: "create",
        // 传参给页面
        params: {
          projectName: this.$route.params.projectName,
          typeList: this.fileSelect
        }
      })
    },
    back() {
      // window.history.back()
      this.doclist = []
      this.$router.push({
        name: "create",
        params: {
          projectName: this.$route.params.projectName
        }
      })
    }
  }
}
</script>

<style scoped>

.main—wrapper {
  height: 900px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  /*align-items: center;*/
  align-content: center;
  flex-flow: row wrap
}

.box-card {
  width: 70%;
  height: 600px;
  overflow: auto;
  margin-top: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  align-content: center;


}


.form {
  margin-top: 40px;
  width: 40%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  align-content: center;
}
</style>

<style scoped>

</style>