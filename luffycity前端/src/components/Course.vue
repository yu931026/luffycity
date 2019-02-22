<template>
    <!--课程-->

    <div>
      <h1>课程列表</h1>
      <!--<ul v-for="(item,index) in courseList">-->
        <!--<li><router-link :to="{name: 'courseinfo', params:{id:item.id},}">{{item.title}}</router-link></li>-->
        <!--根据 路由的name 找到对应的路径，params:{id:item.id} 要传值的键值对-->
      <!--</ul>-->
      <div v-for="(item,index) in courseList">
        <div style="width: 350px;float: left">
          <!--<img src="/static/Python.jpg" alt="">-->
          <img :src="`/static/${item.course_img}`">

          <h3><router-link :to="{name: 'courseinfo', params:{id:item.id},}">{{item.title}}</router-link></h3>
          <!--根据 路由的name 找到对应的路径，params:{id:item.id} 要传值的键值对-->
          <div><router-link :to="{name: 'courseinfo', params:{id:item.id},}">{{item.level}}</router-link></div>
        </div>
      </div>

    </div>
</template>

<script>
    export default {
        name: "Course",
        data(){
          return {
            courseList:[],
          }
        },
        mounted(){
          this.initCourse()
        },
        methods:{
          initCourse(){
            // 通过ajax 发送请求，获取课程列表
            var _this = this;
            this.$axios.request({
              url:_this.$store.state.apiList.course,
              method:'GET'
            }).then(function (ret) {   // 成功后的回调函数
              if(ret.data.code === 1000){  //  通过 ret.data 是后端传来的数据 ret
                _this.courseList = ret.data.data;
              }else{
                alert('获取数据失败')
              }
            }).catch(function (error) {  // 如果上面的发生异常（返回400或500系列状态码）了，就自动执行
              console.log("请求失败")
            })
          },
        },
    }
</script>

<style scoped>

</style>
