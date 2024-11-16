export default {
    data: [{
        "des": "这是设计指标的描述和公式",
        "metrics": [
            {
                "name": "可修改性",
                "des": "该指标用于描述对设计进行修改的难度，特指对设计改正和改进活动实施的难度，指标值越高，实施难度越低。",
                "formula": "\\begin{equation} \\begin{aligned} X = 1- \\frac{\\sum_{i=1}^N \\frac{OD_i + ID_i}{N}}{N} \\end{aligned} \\end{equation}",
                "factors": [
                    "`OD_i=函数i的出度`",
                    "`ID_i=函数i的入度`",
                    "`N=设计中函数的数量`"
                ]
            },
            {
                "name": "可扩展性",
                "des": "该指标度量的是对设计进行扩展的难度，指标值越高，扩展难度越低。",
                "formula": "\\begin{equation} \\begin{aligned} X = \\frac{N_{API}}{N} \\end{aligned} \\end{equation}",
                "factors": [
                    "`N_{API}=设计中API的数量`",
                    "`N=设计中函数的数量`"
                ]
            },
            {
                "name": "易测试性",
                "des": "该指标度量对该软件设计进行测试的难度，指标值越高，测试难度越小。",
                "formula": "\\begin{equation} \\begin{aligned} X = 1- \\frac{\\sum_{i=1}^N \\frac{OD_i}{N}}{N} \\end{aligned} \\end{equation}",
                "factors": [
                    "`OD_i=函数i的出度`",
                    "`N=设计中函数的数量`"
                ]
            },
            {
                "name": "可替换性",
                "des": "该指标度量设计中的函数被具有相似功能的函数替换的难度，以及删除特定功能函数的难度，指标值越高，替换/删除难度越小。",
                "formula": "\\begin{equation} \\begin{aligned} X &= \\frac{\\sum_{i=1}^N R_i}{N} \\\\ R_i &= \\frac{1}{1 + ID_i} \\end{aligned} \\end{equation}",
                "factors": [
                    "`R_i=函数i的可替换性`",
                    "`ID_i=函数i的入度`",
                    "`N=设计中函数的数量`"
                ]
            },
            {
                "name": "易理解性",
                "des": "该指标度量的是开发人员对于设计和现有工程文件理解的难易程度，指标值越高，设计和工程文件越易于理解，越利于开发人员开展演进活动。",
                "formula": "\\begin{equation} \\begin{aligned} X = \\frac{N_{comment}}{N} \\end{aligned} \\end{equation}",
                "factors": [
                    "`N_{comment}=包含注释的函数的数量`",
                    "`N=设计中函数的数量`"
                ]
            },
            {
                "name": "坏味道率",
                "des": "该指标度量的是设计和实现过程中出现坏味道的的频率，指标值越高，因设计缺陷或不良编码习惯而引入程序的、导致深层次质量问题越少。",
                "formula": "\\begin{equation} \\begin{aligned} X = 1 - \\frac{N_{bad}}{N} \\end{aligned} \\end{equation}",
                "factors": [
                    "`N_{bad}=存在坏味道的函数数量`",
                    "`N=设计中函数的数量`"
                ]
            }
        ]
    }]
}