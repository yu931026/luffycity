import Vue from 'vue'

// 引入 cookies
import Cookie from 'vue-cookies'

// 定义创建store
import Vuex from 'vuex'  // 引入 vuex
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    // 这里面的状态 跟每个组件的 数据属性有关系
    username:Cookie.get('username'),  //  取cookie里面的值
    token:Cookie.get('token'),
    apiList:{  // 存放所有的接口
      course:'http://127.0.0.1:8000/api/v1/course/',
      courseinfo:'http://127.0.0.1:8000/api/v1/course/',
      login:'http://127.0.0.1:8000/api/v1/login/',
      micro:'http://127.0.0.1:8000/api/v1/micro/',
      news:'http://127.0.0.1:8000/api/v1/news/',
      newsinfo:'http://127.0.0.1:8000/api/v1/news/',
      agree:'http://127.0.0.1:8000/api/v1/news/agree/',
      collect:'http://127.0.0.1:8000/api/v1/news/collect/',
    }
  },
  mutations: {  // 声明一些方法，来修改 state中的值。
    saveToken(state,userToken){  // 保存 token到cookie中
      state.username = userToken.username;
      state.token = userToken.token;

    //  保存设置cookie  Cookie.set(key,value,超时时间);
      Cookie.set('username',userToken.username,'20min');
      Cookie.set('token',userToken.token,'20min');
    },
    clearToken(state){  // 清除cookie
      state.username = null;
      state.token = null;
      Cookie.remove("username");
      Cookie.remove("token");
    },
  }
});










