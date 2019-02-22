<template>
    <!--微学位-->
 <div>
    <h1>{{title}}</h1>
  </div>

</template>

<script>
    export default {
        name: "Micro",
      data(){
          return {
            title:null
          }
      },
      mounted(){
          this.initMicro()
      },
      methods:{
          initMicro(){  // 获取 微学位 信息
            var _this = this;
            this.$axios.request({
              url:_this.$store.state.apiList.micro,
              method:"GET",
              params:{  // 携带token   http://127.0.0.1:8000/api/v1/micro/?token=asdawasd464asd64
                token:_this.$store.state.token,
              }
            }).then(function (arg) {
              if(arg.data.code === 1000){
                _this.title = arg.data.title
              }
            }).catch(function (arg) {
              alert('请求失败')
            })
          },
      }
    }
</script>

<style scoped>

</style>
