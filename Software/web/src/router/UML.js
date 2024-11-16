import Index1 from "@/components/Index1.vue"

import UML_StaticView from "@/views/UML_Diagram/UML_Static"
import UML_DynamicView from "@/views/UML_Diagram/UML_Dynamic"

// 设计图信息
export default {
    path: "UML_Diagram",
    name: "UML_Diagram",
    hidden: false,
    meta: {
        title: "基于4+1架构模型的软件架构韧性评估",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "UML_StaticView",
            name: "UML_StaticView",
            hidden: false,
            meta: {
                title: "基于静态贝叶斯网络的软件架构韧性评估",
                params: {
                    title: "UML_StaticView",
                }
            },
            component: UML_StaticView
        },
        {
            path: "UML_DynamicView",
            name: "UML_DynamicView",
            hidden: false,
            meta: {
                title: "基于动态贝叶斯网络的软件架构韧性评估",
                params: {
                    title: "UML_DynamicView",
                }
            },
            component: UML_DynamicView
        }
    ]
}
