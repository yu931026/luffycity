<template>
  <div>
    <h1>用户登录</h1>
    <div>
      <p>
        <input type="text" placeholder="请输入用户名" v-model="username">
      </p>
      <p>
        <input type="password" placeholder="请输入密码" v-model="password">
      </p>
      <p>
        <input type="button" value="登录" @click="doLogin">
      </p>
    </div>
  </div>

</template>

<script>
    export default {
        name: "Login",
      data(){
          return {
            username:'',
            password:'',
          }
      },
      methods:{
        doLogin(){  // 点击登录
          var _this = this;
          this.$axios.request({
            url:_this.$store.state.apiList.login,
            method:'POST',
            data:{
              user:this.username,
              pwd:this.password
            },
            headers:{
              'Content-Type':'application/json'  // 设置请求头，是复杂请求。发送的数据是 json格式
            }
          }).then(function (arg) {
            if(arg.data.code === 1000){
              // alert('登录成功');  // 保存 token值
              _this.$store.commit('saveToken',{token:arg.data.token, username:_this.username});
              // 登录后跳转
              var url = _this.$route.query.backUrl;  // 获取跳转的url
              if(url){
                _this.$router.push({path:url})  // 跳转到来的 页面
              }else {
                _this.$router.push({name:'index'})  // 没有跳转的url 就登录后跳转首页
              }
            }else {
              alert(arg.data.error)
            }
          }).catch(function (arg) {
            alert('发生错误')
          })
        }
      },
    }
</script>

<style scoped>

</style>
