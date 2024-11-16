<template>
<!-- 
  <div>
  <h1 class="link-right">需求</h1>
  </div> -->
<div>
<!-- 
  <div>
  <h1 class="link-right">需求</h1>
  </div> -->
<el-container>
    <el-header style="margin-top:20px;margin-bottom:-30px">
      <el-row type="flex" >                
      <el-col :lg="12" :xs="24" style="font-size:18px;" >
        <div class="div4">
          <span class="link-right" style="font-weight: bold;">{{this.title}} </span>
          <span>&nbsp全部{{this.title1}} · </span>
          <span> {{this.total}}</span>
        </div>        
      </el-col> 

      <el-col :lg="12" :xs="24" style="text-align:right">
      <!-- <el-dropdown @command="handleCommand" style="margin-right:15px">
      <span class="el-dropdown-link">
         <i class="el-icon-setting"></i>
        批量操作<i class="el-icon-arrow-down el-icon--right" ></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="a">导出所选</el-dropdown-item>
        <el-dropdown-item command="b">导出所有</el-dropdown-item>
        <el-dropdown-item command="c">修改11</el-dropdown-item>
        <el-dropdown-item command="d">删除所选</el-dropdown-item>
        <el-dropdown-item command="e">修改22</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>  -->
    <!-- <el-input
    placeholder="请输入内容"
    v-model="search_input"
    style="width: 200px;"
    clearable>
    </el-input> -->
    <!-- <el-button icon="el-icon-search"  @click="search"></el-button> -->
      </el-col>
      </el-row>
    </el-header>

  <el-main style="margin-bottom:10px;height:calc(100vh - 300px)">
  <div class="link-top"></div>
    <!-- max-height="400"    -->
    <el-table
    ref="singleTable"
    :data="tableData"
    tooltip-effect="dark"
    highlight-current-row
    height="500"
    @current-change="handleCurrentChange"
    style="width:95%;margin:auto">

    <el-table-column
      type="index"
      width="55">
    </el-table-column>
   
    <el-table-column
      prop="file_name"
      label="文档名称"
      sortable
      width="320"
      >
      <template slot-scope="scope">
            <i class="el-icon-document"></i>
            &nbsp{{scope.row.file_name}}
      </template>
    </el-table-column>

    <el-table-column
      prop="description"
      label="描述"
      sortable   
     >
    </el-table-column>
    
  </el-table>
  </el-main>
  <el-footer >  
  <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentPageChange"
      style="text-align: center;"
      :current-page="currentPage4"
      :page-sizes="[10, 20]"
      :page-size="10"
      layout="total, sizes, prev, pager, next, jumper"
      :total=this.total>
    </el-pagination>
    
    </el-footer>

  </el-container>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        search_input: '',
        total:20,
        title: '',
        title1:'',
        tableData: [{
          description: '里程碑管理主要应用在“经典项目管理”模式，在这种项目管理模式下，会有明确的项目目标和时间点要求，因此会预先规划几个月甚至更长时间阶段的项目目标，以里程碑的形式进行管理；Projex的里程碑管理会以数据列表和时间轴两种方式展示里程碑，在时间轴模式下，按照里程碑的计划完成时间从左到右进行展示，里程碑的不同状态也会有不同的展示方式，帮助项目成员了解目前的项目进展；',
          file_name: '通过里程碑和风险管理保证项目按期完成'
        }, {
          description: '王小虎3',
          file_name: '文档2'
        }, {
          description: '王小虎5',
          file_name: '文档3'
        }, {
          description: '王小虎2',
          file_name: '文档4'
        }, {
          description: '王小虎6',
          file_name: '文档8'
        }, {
          description: '王小虎8',
          file_name: '文档6'
        }, {
          description: '王小虎',
          file_name: '文档5'
        }, {
          description: '王小虎',
          file_name: '文档5'
        }, {
          description: '王小虎',
          file_name: '文档5'
        }, {
          description: '王小虎',
          file_name: '文档5'
        }],
        multipleSelection: []
      }
    },
    mounted(){     
      this.title = this.$route.meta.params.title;
      this.title1 = this.$route.meta.params.title1;
      console.log("该文档名称为"+this.title);  
    },
    watch: {
      '$route'(to, from) {
        this.title = to.meta.params.title;
        this.title1 = to.meta.params.title1;
        console.log("该文档名称为"+this.title);  
      }
    },
    methods: {     
      setCurrent(row) {
        this.$refs.singleTable.setCurrentRow(row);
      },
      handleCurrentChange(val) {
        this.currentRow = val;
      },
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentPageChange(val) {
        console.log(`当前页: ${val}`);
      }
    
    }
  }
</script>

<style scoped>
        /*中间的过度的横线*/
        .link-top {
            width: 100%;
            height: 1px;
            margin: 0 auto;
            border-top: solid #ACC0D8 1px;
        }
 
        /*画一条在右边的竖线*/
        .link-right {
            width: 50px;
            height: 100%;
            border-right: solid #ACC0D8 1px;
            
        }

         .div4 {
				width: 100%;
				height: 100%;			
				display: -webkit-flex;
				display: flex;
				-webkit-align-items: left;
				align-items: center;
				-webkit-justify-content: left;
				justify-content: left;
			}
</style>