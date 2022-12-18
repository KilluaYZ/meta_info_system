<template>
  <div class="app-container home">
    <el-row :gutter="20">
      <el-col :sm="24" :lg="12" style="padding-left: 20px">
        <h2>知识点标签管理系统</h2>
        <p>一段话</p>
        <p style="padding-bottom: 50px;">
          <b>当前版本:</b><span>v{{version}}</span>
        </p>
      </el-col>
    </el-row>

    <el-divider></el-divider>

    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12" :lg="10">
        <el-card class="update-log">
          <div>
            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false">
              更多<i class="el-icon-view el-icon--right"></i>
            </el-link>
            <h3>可视化</h3>
          </div>
          <div style="margin:0 auto;">
            <el-carousel :interval="4000" type="card" height="300px"  >
              <el-carousel-item v-for="item in imgList" :key="item.id">
                <img :src="item.idView" width="450px" height="275px">
              </el-carousel-item>
            </el-carousel>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="5">
        <el-card class="update-log">
          <div class="header">
            <el-link v-bind:style="HotTagSetting" :underline="false" @click="switchTagsTitle('Hot')">热门标签</el-link>
            <el-divider direction="vertical"></el-divider>
            <el-link v-bind:style="NewTagSetting" :underline="false" @click="switchTagsTitle('New')">最新标签</el-link>

            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false" @click="goTag({sort:'Hot'})">
              更多<i class="el-icon-view el-icon--right"></i>
            </el-link>
          </div>
          <ul>
            <li v-for="Tag in displayTagsContent">
              <div class="col-item">
                 <el-link v-loading="tagloading" type="primary" @click="showtagDetail(Tag)" >{{Tag.tagName}}</el-link>
              </div>
            </li>
          </ul>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="9" >
        <el-card class="update-log">
          <div class="header">
            <el-link v-bind:style="HotPostSetting" :underline="false" @click="switchPostsTitle('Hot')">热门帖子</el-link>
            <el-divider style="color:black" direction="vertical"></el-divider>
            <el-link v-bind:style="NewPostSetting" :underline="false" @click="switchPostsTitle('New')">最新帖子</el-link>

            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false" @click="goTag({sort:'New'})">
              更多<i class="el-icon-view el-icon--right"></i>
            </el-link>
          </div>
          <ul>
            <li v-for="Post in displayPostsContent">
              <div class="col-item" >
                 <el-link v-loading="postloading" type="primary" >{{Post.postContent}}</el-link>
              </div>
            </li>
          </ul>
        </el-card>
      </el-col>
  
    </el-row>

    <!-- 显示标签详情对话框 -->
    <el-dialog :title="title" :visible.sync="Tag_detail_open" width="500px" append-to-body>
      <el-form ref="form" :model="Tagform" label-width="80px">
        <el-form-item label="标签名称" prop="tagName">
          <el-input v-model="Tagform.tagName" readonly />
        </el-form-item>
        <el-form-item label="父标签名" prop="tagParentName">
          <el-input v-model="Tagform.tagParentName" readonly />
        </el-form-item>
        <el-form-item label="标签级别" prop="tagClass">
          <el-input v-model="Tagform.tagClass" readonly />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="Tagform.remark" type="textarea" readonly :autosize="{ minRows: 5, maxRows: 15}" ></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>


<script>

import { getHotTags, getNewTags, getHotPosts, getNewPosts} from "@/api/manage/mainpage.js";
import { getTag } from "@/api/manage/tag.js"

export default {
  name: "Index",
  data() {
    return {
      // 版本号
      version: "1.0.0",
      
      tagloading: false,

      postloading: false,

      HotTagsContent: [],

      NewTagsContent: [],

      HotPostsContent: [],

      NewPostsContent: [],
      //现在显示的标签内容
      displayTagsContent: [],
      //现在显示的帖子内容
      displayPostsContent: [],
      //打开详情界面的标题
      title: "",
      //是否打开标签详情界面
      Tag_detail_open: false,
      //标签表单
      Tagform: {},
      //标题字体样式设置
      HotTagSetting: {color:'red',fontSize:'16px'},
        
      NewTagSetting: {fontSize:'16px'},

      HotPostSetting: {color:'red',fontSize:'16px'},

      NewPostSetting: {fontSize:'16px'},

      imgList : [
        // {id:1,idView:require('../assets/mainpage/1.png')},
        // {id:2,idView:require('../assets/mainpage/2.png')},
        // {id:3,idView:require('../assets/mainpage/3.png')}
      ],

      queryHotTagsParams: {
        HotTagsNum: 5,
        tagName: undefined,
        tagClass: undefined,
        tagID: undefined,
      },
      queryNewTagsParams: {
        NewTagsNum: 5,
      },
      queryHotPostsParams: {
        HotPostsNum: 5,
      },
      queryNewPostsParams: {
        NewPostsNum: 5,
      }
    };  
  },
  created() 
  {
    console.log("获取数据");
    this.getList();
  },
  methods: {
    goTarget(href) {
      window.open(href, "_blank");
    },
    getList() {
      getHotTags(this.queryHotTagsParams).then((res) => {
        console.log("成功取得HotTags数据")
        this.HotTagsContent = res.data;
        this.displayTagsContent = res.data;
      })
      getNewTags(this.queryNewTagsParams).then((res) => {
        console.log("成功取得NewTags数据")
        this.NewTagsContent = res.data;
      })
      getHotPosts(this.queryHotPostsParams).then((res) => {
        console.log("成功取得HotPosts数据")
        this.HotPostsContent = res.data;
        this.displayPostsContent = res.data
      })
      getNewPosts(this.queryNewPostsParams).then((res) => {
        console.log("成功取得NewPosts数据")
        this.NewPostsContent = res.data;
      })   
    },
    goTag(sortForm) {
      this.$store.commit('tag/setpresetParam',sortForm)
      this.$router.push('/system/tag')
    },
    switchTagsTitle(title) {
      this.tagloading = true;
      this.settagTitletheme(title)
      setTimeout(() => {
        if(title === 'Hot')
          this.displayTagsContent = this.HotTagsContent;
        else
          this.displayTagsContent = this.NewTagsContent;
        this.tagloading = false
      }, 200);
      //console.log(HotTagsContent[0].tagName)
    },
    switchPostsTitle(title) {
      this.postloading = true;
      this.setpostTitletheme(title);
      setTimeout(() => {
        if(title === 'Hot')
          this.displayPostsContent = this.HotPostsContent;
        else
          this.displayPostsContent = this.NewPostsContent;
        this.postloading = false
      }, 200);   
    },
    showtagDetail(row) {
      const tagName = row.tagName;
      getTag({tagName: tagName}).then((res)=>{
        console.log('点开详情页面，收到数据')
        console.log(res)
        this.Tagform = res.data[0];
        this.Tag_detail_open = true;
        this.title = "标签详情";
      })
    },
    //根据标签主题设置字符样式
    settagTitletheme(title) {
      if(title === 'Hot'){
        this.HotTagSetting = {color:'red',fontSize:'16px'};
        this.NewTagSetting = {fontSize:'16px'};
      }
      else{
        this.HotTagSetting = {fontSize:'16px'};
        this.NewTagSetting = {color:'red',fontSize:'16px'};    
      }
    },
    setpostTitletheme(title) {
      if(title === 'Hot'){
        this.HotPostSetting = {color:'red',fontSize:'16px'};
        this.NewPostSetting = {fontSize:'16px'};
      }
      else{
        this.HotPostSetting = {fontSize:'16px'}; 
        this.NewPostSetting = {color:'red',fontSize:'16px'}; 
      }
    }
  },
};
</script>

<style scoped lang="scss">
.home {
  blockquote {
    padding: 10px 20px;
    margin: 0 0 20px;
    font-size: 17.5px;
    border-left: 5px solid #eee;
  }
  hr {
    margin-top: 20px;
    margin-bottom: 20px;
    border: 0;
  }
  h3 {
    margin-top: 10px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgb(200, 200, 200);
    font-size: 16px;
  }
  .col-item {
    width: 100%;
    margin-top: 20px;
    margin-bottom: 20px;
    padding-top: 0px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgb(200, 200, 200);
    white-space: nowrap;
    overflow: hidden;
    word-break: break-all;
  }
  .header {
    padding-top: 8px;
    padding-bottom: 9px;
    border-bottom: 1px solid rgb(200, 200, 200);
  }

  ul {
    padding: 0;
    margin: 0;
  }

  font-family: "open sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 13px;
  color: #676a6c;
  overflow-x: hidden;

  ul {
    list-style-type: none;
  }

  h4 {
    margin-top: 0px;
  }

  h2 {
    margin-top: 10px;
    font-size: 26px;
    font-weight: 100;
  }

  p {
    margin-top: 10px;

    b {
      font-weight: 700;
    }
  }

  .update-log {
    ol {
      display: block;
      list-style-type: decimal;
      margin-block-start: 1em;
      margin-block-end: 1em;
      margin-inline-start: 0;
      margin-inline-end: 0;
      padding-inline-start: 40px;
    }
    margin-bottom: 20px;
    height: 350px;
  }

}
</style>

