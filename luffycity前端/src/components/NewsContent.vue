<template>
    <div>
      <h2>咨询文章详情</h2>
      <div>
        <p>{{newsContent.title}}</p>
        <p>{{newsContent.content}}</p>
        <p>评论数（{{newsContent.comment_num}}）</p>
        <p >点赞数（{{newsContent.agree_num}}）<button v-if="agreeStatus">已赞</button>
        <button @click="agree" v-else>点赞</button></p>
        <p>观看数（{{newsContent.view_num}}）</p>
        <p>收藏数（{{newsContent.collect_num}}）<button v-if="collectStatus" >已收藏</button>
          <button v-else @click="collect(newsContent.id)">收藏</button>
        </p>
      </div>


    </div>
</template>

<script>
    export default {
        name: "ArticleContent",
      data(){
          return {
            newsContent:{
              id:null,
              title:'',
              content:'',
              comment_num: 0,  // 评论数
              agree_num: 0,  // 点赞数
              view_num:0,  // 观看数
              collect_num:0 // 收藏数
            },
            agreeStatus:false,
            collectStatus:false,
          }
      },
      mounted(){
          var nid = this.$route.params.id;
          this.initNewsContent(nid)
      },
      methods:{
          initNewsContent(nid){
            var _this = this;
            this.$axios({
              url:_this.$store.state.apiList.newsinfo +nid+ '/',
              method:'GET',
            }).then(function (arg) {
              if(arg.data.code === 1000){
                _this.newsContent = arg.data.data
              }else {
                console.log(arg.data.error)
              }
            }).catch(function (arg) {
              console.log('发送请求失败')
            })
          },
          agree(){
            // 点赞
            var _this = this;
            this.$axios({
              url:_this.$store.state.apiList.agree,
              method:'POST',
              data:{
                id:_this.newsContent.id,
                token:_this.$store.state.token,
              },

            }).then(function (arg) {
              if(arg.data.code === 1000){
                _this.newsContent.agree_num += 1;
                _this.status = arg.data.agreeStatus
              }else {
                console.log(arg.data.error)
              }
            }).catch(function (arg) {
              console.log("发送请求失败");
              _this.$router.push({name:'login' })
            })
          },
          collect(nid){
            // 收藏
            var _this = this;
            this.$axios.request({
              url:_this.$store.state.apiList.collect +nid +'/',
              method:'POST',
              data:{token: _this.$store.state.token},
              params:{
                token: _this.$store.state.token
              }
            }).then(function (arg) {
              console.log(arg.data);
              if(arg.data.code === 1000){
                _this.collectStatus = arg.data.status;
                _this.newsContent.collect_num += 1;
              }else {
                console.log("收藏失败");
                // _this.collectStatus = arg.data.status;
              }
            }).catch(function (arg) {
              console.log("收藏请求失败")
            })
          }
      },

    }
</script>

<style scoped>

</style>
