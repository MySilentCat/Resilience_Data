import Vue from 'vue';
import Vuex from 'vuex';
import indexList from '@/utils/index_list'
import Cache from "@/utils/cache"

Vue.use(Vuex)
function copyList(objList){
  let newList = []
  for (var i = 0; i < objList.length; i++) {
    newList.push(JSON.parse(JSON.stringify(objList[i])))
  }
  return newList;
}

const state = {
    // 当前操作的项目
    current_project: Cache.getCache("current_project") || {
        name: "项目XXX"
    },
    // 选中的指标
    index_selected: [],
    //指标列表
    index_list: copyList(indexList.data),
    // 菜单栏是否禁用
    menuDisabled: true,
    // navibar数据
    naviList: Cache.getCache("naviList") || []
}

var mutations={
    setCurrProject(state, project){
        Cache.setCache("current_project", project)
        state.current_project = project
    },
    refreshIndexList(state){
      state.index_list = copyList(indexList.data)
      state.index_selected = []
    },
    setIndexSelected(state, index){
      state.index_selected = index
    },
    setMenuDisabled(state, flag){
      state.menuDisabled = flag
    },
    setNaviList(state, naviList){
      Cache.setCache("naviList", naviList)
      state.naviList = naviList
    },
}
var getters={
    getIndexValue (state) {
        return state.index_list
    }
}
export default new Vuex.Store({
    getters,
    state,
    mutations
})