import Index1 from "@/components/Index1.vue"
import Index2 from "@/components/Index2.vue"
import evaluate_result_show from "@/views/quality_evaluation/software/result_show.vue"
import evaluate_weight_set from "@/views/quality_evaluation/software/weight_set.vue"
import evaluate_index_select from "@/views/quality_evaluation/software/index_select.vue"
import evaluate_result_show1 from "@/views/quality_evaluation/design/result_show.vue"
import evaluate_expert_index from "@/views/quality_evaluation/design/expert_index.vue"

// 质量评估菜单
export default {
    path: "quality_evaluation",
    name: "quality_evaluation",
    hidden: false,
    meta: {
        title: "质量评估",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "software",
            name: "software",
            hidden: false,
            meta: {
            title: "软件质量评估",
            params: {}
            },
            component: Index2,
            children: [
            {
                path: "index_select",
                name: "index_select",
                hidden: false,
                meta: {
                title: "指标选择",
                params: {}
                },
                component: evaluate_index_select
            },
            {
                path: "weight_set",
                name: "weight_set",
                hidden: false,
                meta: {
                title: "权重设置",
                params: {}
                },
                component: evaluate_weight_set
            },
            {
                path: "result_show",
                name: "result_show",
                hidden: false,
                meta: {
                title: "结果展示",
                params: {}
                },
                component: evaluate_result_show
            },
            ]
        },
        {
            path: "design",
            name: "design",
            hidden: false,
            meta: {
            title: "设计质量评估",
            params: {}
            },
            component: Index2,
            children: [
            {
                path: "index_select1",
                name: "index_select1",
                hidden: false,
                meta: {
                title: "阈值设置",
                params: {}
                },
                component: evaluate_expert_index
            },
            {
                path: "result_show1",
                name: "result_show1",
                hidden: false,
                meta: {
                title: "结果展示",
                params: {}
                },
                component: evaluate_result_show1
            },
            ]
        }
    ]
}