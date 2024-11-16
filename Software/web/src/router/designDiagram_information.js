import Index1 from "@/components/Index1.vue"
import Index2 from "@/components/Index2.vue"

import GraphView from "@/views/designDiagram_information/GraphView"
import PLCGView from "@/views/designDiagram_information/PLCGView"
import FLCGView from "@/views/designDiagram_information/FLCGView"
import SDGView from "@/views/designDiagram_information/SDGView"
import ArchitectureDependencyGraphView from "@/views/designDiagram_information/ArchitectureDependencyGraphView"
import PipeFilterGraphView from "@/views/designDiagram_information/PipeFilterGraphView"
import PDGView from "@/views/designDiagram_information/PDGView"
import CFGView from "@/views/designDiagram_information/CFGView"
import CGView from "@/views/designDiagram_information/CGView"
import LevelView from "@/views/designDiagram_information/LevelView"
import CallBackView from "@/views/designDiagram_information/CallBackView"
// 设计图信息
export default {
    path: "GraphView",
    name: "GraphView",
    hidden: false,
    meta: {
        title: "设计图信息",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "CG",
            name: "CG",
            hidden: false,
            meta: {
                title: "调用图",
                params: {
                    title: "CG",
                }
            },
            component: Index2,
            children:[
                {
                    path: "PLCG",
                    name: "PLCG",
                    hidden: false,
                    meta: {
                        title: "过程级调用图",
                        params: {
                            title: "PLCG",
                        }
                    },
                    component: PLCGView
                },
                {
                    path: "FLCG",
                    name: "FLCG",
                    hidden: false,
                    meta: {
                        title: "文件级调用图",
                        params: {
                            title: "FLCG",
                        }
                    },
                    component: CGView
                },
            ]
        },
        {
            path: "CFG",
            name: "CFG",
            hidden: false,
            meta: {
                title: "控制流图",
                params: {
                    title: "CFG",
                }
            },
            component: CFGView
        },
        {
            path: "PDG",
            name: "PDG",
            hidden: false,
            meta: {
                title: "过程依赖图",
                params: {
                    title: "PDG",
                }
            },
            component: PDGView
        },
        {
            path: "SDG",
            name: "SDG",
            hidden: false,
            meta: {
                title: "系统依赖图",
                params: {
                    title: "SDG",
                }
            },
            component: SDGView,
        },
        {
            path: "架构视图",
            name: "架构视图",
            hidden: false,
            meta: {
                title: "架构视图",
                params: {
                    title: "架构视图",
                }
            },
            component: Index2,
            children: [
                {
                    path: "架构依赖图",
                    name: "架构依赖图",
                    hidden: false,
                    meta: {
                        title: "架构依赖图",
                        params: {
                            title: "架构依赖图",
                        }
                    },
                    component: ArchitectureDependencyGraphView
                },
                {
                    path: "管道过滤器风格架构图",
                    name: "管道过滤器风格架构图",
                    hidden: false,
                    meta: {
                        title: "管道过滤器风格架构图",
                        params: {
                            title: "管道过滤器风格架构图",
                        }
                    },
                    component: PipeFilterGraphView
                },
                {
                    path: "调用返回风格架构图",
                    name: "调用返回风格架构图",
                    hidden: false,
                    meta: {
                        title: "调用返回风格架构图",
                        params: {
                            title: "调用返回风格架构图",
                        }
                    },
                    component: CallBackView
                },
                {
                    path: "分层风格架构图",
                    name: "分层风格架构图",
                    hidden: false,
                    meta: {
                        title: "分层风格架构图",
                        params: {
                            title: "分层风格架构图",
                        }
                    },
                    component: LevelView
                },    
            ]
        },    
    ]
}
