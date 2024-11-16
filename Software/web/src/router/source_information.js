import Index1 from "@/components/Index1.vue"

import project_level from "@/views/source_information/project_level.vue"
import module_level from "@/views/source_information/module_level.vue"
import file_level from "@/views/source_information/file_level.vue";


export default {
    path: "source_information",
    name: "source_information",
    hidden: false,
    meta: {
        title: "源码信息",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "project_level",
            name: "project_level",
            hidden: false,
            meta: {
                title: "项目级信息",
                params: {}
            },
            component: project_level
        },
        {
            path: "module_level",
            name: "module_level",
            hidden: false,
            meta: {
                title: "模块级信息",
                params: {}
            },
            component: module_level
        },
        {
            path: "file_level",
            name: "file_level",
            hidden: false,
            meta: {
                title: "文件级信息",
                params: {}
            },
            component: file_level
        }
    ]
}