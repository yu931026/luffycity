// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/store.js'


// axios 配置
import axios from 'axios'
Vue.prototype.$axios = axios;
// 在 vue 的全局变量中设置了 $axios = axios
// 以后每个组件使用时： this.$axios


Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});


// 拦截器，登录校验
router.beforeEach(function (to, from, next) {
  // to 是你要去哪，from 是从哪来，next是真正让你去跳转
  if(to.meta.requireLogin){
    // 如果 to.meta.requireLogin 为 true 是要去访问需要登录验证的url
    if (store.state.token){  // token不为空，已经登录，就去访问
      next()
    }else {  // 如果未登录，跳转到登录
      next({path:'/login', query:{backUrl:to.fullPath}})  // 等同于  next({name:'login'})。 query:{backUrl:to.fullPath} 是登录后跳转回之前的页面
    }
  }else {
    // 去访问不需要登录验证的 url
    next()
  }
});



