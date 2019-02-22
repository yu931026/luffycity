<template>
  <div id="app">

    <router-link to="/index">首页</router-link>
    <router-link to="/course">课程</router-link>
    <router-link to="/micro">微职位</router-link>
    <router-link to="/news">深科技</router-link>
    <div v-if="this.$store.state.token">
      <!--登录后-->
      <a>{{this.$store.state.username}}</a>
      <a @click="logout">注销</a>
    </div>
    <div v-else>
      <router-link to="/login">登录</router-link>
    </div>
    <!--<img src="./assets/logo.png" alt="">-->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods:{
    logout(){  // 注销
      this.$store.commit('clearToken');
      this.$router.push({name:'index'})
    }
  }
}
</script>

<style>

</style>
