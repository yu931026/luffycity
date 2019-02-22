import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Index from '@/components/Index'
import Course from '@/components/Course'
import Micro from '@/components/Micro'
import News from '@/components/News'
import CourseInfo from '@/components/CourseInfo'
import Login from '@/components/Login'
import NewsContent from '@/components/NewsContent'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,

    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/index',
      name: 'index',
      component: Index
    },
    {
      path: '/course',
      name: 'course',
      component: Course,
      meta:{
        requireLogin:true,  // 表示必须要登录校验
      }
    },
    {
      path: '/courseinfo/:id',
      name: 'courseinfo',
      component: CourseInfo
    },
    {
      path: '/micro',
      name: 'micro',
      component: Micro,
      meta:{
        requireLogin:true,  // 表示必须要登录
      }
    },
    {
      path: '/news',
      name: 'news',
      component: News,

    },
    {
      path: '/news/:id',
      name: 'newscontent',
      component: NewsContent,
      meta:{
        requireLogin:true,  // 表示必须要登录
      }
    },
  ]
})
