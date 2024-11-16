<template>
  <div style="height: 88vh">
    <iframe :src="g_url + url" style="width: 100%; height: 90%"></iframe>
  </div>
</template>

<script>
export default {
  name: "GraphView",
  data() {
    return {
      g_url: "project/" + this.$store.state.current_project.name,
      url: "",
    };
  },
  watch: {
    $route(to, from) {
      if (to.meta.params.title == "PLCG") {
        this.url = "/PLCG.dot.html";
      } else if (to.meta.params.title == "FLCG") {
        this.url = "/FLCG.dot.html";
      } else if (to.meta.params.title == "CFG") {
        this.url = "/FLCG.dot.html";
      } else if (to.meta.params.title == "PDG") {
        this.url = "/FLCG.dot.html";
      } else if (to.meta.params.title == "SDG") {
        this.url = "/FLCG.dot.html";
      } else if (to.meta.params.title == "架构依赖图") {
        this.url = "/clustered_sdg.dot_GNwithoutcomp.dot.html";
      } else if (to.meta.params.title == "管道过滤器风格架构图") {
        this.url = "/pipe_filter.html";
      } else if (to.meta.params.title == "调用返回风格架构图") {
        this.url = "/PLCG.dot.html";
      } else if (to.meta.params.title == "分层风格架构图") {
        this.url = "/FLCG.dot.html";
      }
    },
  },
  mounted() {
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
    });

    let params = this.$route.meta.params;
    // console.log("%%%%%%", params);
    if (params.title == "PLCG") {
      this.url = "/PLCG.dot.html";
    } else if (params.title == "FLCG") {
      this.url = "/FLCG.dot.html";
    } else if (params.title == "CFG") {
      this.url = "/FLCG.dot.html";
    } else if (params.title == "PDG") {
      this.url = "/FLCG.dot.html";
    } else if (params.title == "SDG") {
      this.url = "/FLCG.dot.html";
    } else if (params.title == "架构依赖图") {
      this.url = "/clustered_sdg.dot_GNwithoutcomp.dot.html";
    } else if (params.title == "管道过滤器风格架构图") {
      this.url = "/pipe_filter.html";
    } else if (params.title == "调用返回风格架构图") {
      this.url = "/PLCG.dot.html";
    } else if (params.title == "分层风格架构图") {
      this.url = "/FLCG.dot.html";
    }
  },
};
</script>

<style scoped></style>
