import Index1 from "@/components/Index1.vue"

import DR_StaticView from "@/views/DesignRecovery_Diagram/DR_Static"
import DR_DynamicView from "@/views/DesignRecovery_Diagram/DR_Dynamic"

// 设计图信息
export default {
    path: "DesignRecovery_Diagram",
    name: "DesignRecovery_Diagram",
    hidden: false,
    meta: {
        title: "基于源代码设计恢复的软件架构韧性评估",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "DR_StaticView",
            name: "DR_StaticView",
            hidden: false,
            meta: {
                title: "基于静态贝叶斯网络的软件架构韧性评估",
                params: {
                    title: "DR_StaticView",
                }
            },
            component: DR_StaticView
        },
        {
            path: "DR_DynamicView",
            name: "DR_DynamicView",
            hidden: false,
            meta: {
                title: "基于动态贝叶斯网络的软件架构韧性评估",
                params: {
                    title: "DR_DynamicView",
                }
            },
            component: DR_DynamicView
        }
    ]
}
