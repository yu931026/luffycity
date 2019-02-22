<template>
    <div>
      <h1>{{courseInfo.title}}课程详细页面</h1>
      <p>{{courseInfo.img}}</p>
      <p>{{courseInfo.level}}</p>
      <p>{{courseInfo.slogon}}</p>
      <p>{{courseInfo.why_study}}</p>
      <p>推荐课程</p>
      <ul v-for="(item,index) in courseInfo.rec_courses">
          <li @click="changeInfo(item.id)">{{item.title}}</li>
      </ul>
      <p>章节信息</p>
      <ul v-for="(item,index) in courseInfo.chapter">
            <li>第{{item.num}}章：{{item.name}}</li>
      </ul>
    </div>
</template>

<script>
    export default {
        name: "CourseInfo",
        data(){
          return {
            courseInfo:{
              course:null,
              title:null,
              img:null,
              level:null,
              slogon:null,
              why_study:null,
              rec_courses:[],
              chapter:[],
            },
          }
        },
      mounted(){
        // console.log(this.$route.params.id);
        var nid = this.$route.params.id;
        this.initCourseInfo(nid);
      },
      methods:{
        initCourseInfo(nid){
          // 获取课程详情
          var _this = this;
          this.$axios.request({
            url:_this.$store.state.apiList.courseinfo+nid+'/',
            method:'GET'
          }).then(function (ret) {
            if(ret.data.code === 1000){
              _this.courseInfo = ret.data.data;
              console.log(ret.data.data)
            }else{
              console.log(ret.data.error)
            }
          }).catch(function (err) {
            console.log('请求失败')
          })
        },
        changeInfo(id){
          // 跳转推荐课程详情
          this.initCourseInfo(id);  // 点击推荐课程 数据重新获取
          this.$router.push({name:'courseinfo',params:{id:id}});  // 主动重定向。点击推荐课程跳转是url变化
        },
      },
    }
</script>

<style scoped>

</style>
