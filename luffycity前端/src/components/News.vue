<template>
    <!--深科技-->
  <div>
    <h1>深科技</h1>
    <h2>咨询文章列表</h2>
    <div v-for="(item,index) in newsList">
      <div style="width: 350px;float: left">
          <img src="" alt="">

          <h3><router-link :to="{name: 'newscontent', params:{id:item.id},}">{{item.title}}</router-link></h3>
          <!--根据 路由的name 找到对应的路径，params:{id:item.id} 要传值的键值对-->
          <div><router-link :to="{name: 'newscontent', params:{id:item.id},}">{{item.article_type}}</router-link></div>
          <div>评论数（{{item.comment_num}}）</div>
        <div>点赞数（{{item.agree_num}}）</div>
        <div>观看数（{{item.view_num}}）</div>
        <div>收藏数（{{item.collect_num}}）</div>
        </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "News",
      data(){
          return {
            newsList:[]
          }
      },
      mounted(){
          this.initNews()
      },
      methods:{
          initNews(){
            var _this = this;
            this.$axios({
              url:_this.$store.state.apiList.news,
              method:'GET',
            }).then(function (arg) {
              if(arg.data.code === 1000){
                _this.newsList = arg.data.data
              }else {
                console.log(arg.data.error)
              }
            }).catch(function (arg) {
              console.log("发送请求失败")
            })
          }
      }
    }
</script>

<style scoped>

</style>
