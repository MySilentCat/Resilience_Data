import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

import Home from '@/components/Home.vue';
// import New from '@/components/New.vue';
import Create from '@/components/Create.vue';
import Main from "@/components/Main.vue"
import SelectDoc from "@/components/selectDoc";
import project_detail from "@/views/project_detail/project_detail.vue";
import file_info from"@/views/file_information/all_file_info.vue";
import user_manual from "@/views/user_manual/user_manual.vue"

import source_information from "./source_information";
import quality_evaluation from "./quality_evaluation"
// import file_information from "./file_information"
import designDiagram_information from './designDiagram_information';

import project_info from "@/views/project_detail/project_info.vue";

import UML from "./UML";
import DR from "./DR";



// 配置功能页路由，会同步到菜单栏
export const router_list = [
  {
    path: "project_info",
    name: "project_info",
    hidden: false,
    meta: {
        title: "项目信息提取",
        params: {}
    },
    component: project_info
  },
  UML,
  DR,
]

export const router = new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      hidden: true,
      meta: {
        title: "BNSA.Resilience Evaluator"
      },
      component:Home
    },
    // {
    //   path: '/new',
    //   name: 'new',
    //   hidden: true,
    //   meta: {
    //     title: "新建",
    //     keepAlive:true
    //   },
    //   component: New
    // },
    {
      path: '/create',
      name: 'create',
      hidden: true,
      meta: {
        title: "新建",
        keepAlive:true
      },
      component: Create
    },
    {
      path: '/selectDoc',
      name: 'selectDoc',
      hidden: true,
      meta: {
        title: "选择文档"
      },
      component: SelectDoc
    },
    {
      path: '/main',
      name: 'main',
      hidden: true,
      meta: {
        title: "项目"
      },
      component: Main,
      redirect: {
        name: "project_info"
      },
      children: router_list
    },
    {
      path: '/user_manual',
      name: 'user_manual',
      hidden: true,
      meta: {
        title: "用户手册"
      },
      component: user_manual
    },
    {
      path: '*',
      hidden: true,
      redirect: '/home'
    }
  ]
})
