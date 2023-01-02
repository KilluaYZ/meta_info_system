<template>
  <div class="app-container home">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" style="padding-left: 20px">
        <h2>知识点标签管理系统</h2>
        <p>迄今为止，中国大学MOOC平台上人大的数据库系统概论课程，自2016年起已经开课了13次，在课程讨论区的老师答疑区留下了学习者很多的提问问题。现已根据这些提问的问题，通过对其打上知识点标签形式，对问题分类，挖掘出高频疑难知识点和学生的关注点，用以对后续教学的指导参考。</p>
        <p style="padding-bottom: 50px;">
          <b>当前版本:</b><span>v{{ version }}</span>
        </p>
      </el-col>

      <!-- <el-col :xs="24" :sm="24" :md="12" :lg="4">
        <el-card class="info">
          <div>
            最近访问<i class="el-icon-timer"></i>
          </div>
          <div v-for="latestvisit in latestvisitlist">
            <span><i class="el-icon-caret-right"></i>{{ latestvisit }}</span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="4">
        <el-card class="info">
          <div>
            待办事项<i class="el-icon-warning"></i>
          </div>
          <div v-for="todo in todolist">
            <span><i class="el-icon-caret-right"></i>{{ todo }}</span>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="4">
        <el-card class="info">
          <div>
            通知公告<i class="el-icon-message-solid"></i>
          </div>
          <div v-for="notice in noticelist">
            <span><i class="el-icon-caret-right"></i>{{ notice }}</span>
          </div>
        </el-card>
      </el-col> -->

    </el-row>

    <el-divider></el-divider>

    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="12" :lg="10">
        <el-card class="update-log word-cloud-card">
          <div class="header">
            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false" href="http://localhost:5000/vis/getWordCloud">
              放大<i class="el-icon-view el-icon--right"></i>
            </el-link>
            <h3>词云图</h3>
            <!-- <el-image :src="img_url" :preview-src-list="img_url_list" :fit="cover" lazy></el-image> -->
          </div>  
          <!-- <iframe v-bind:src="img_url" id="wordcloud" scrolling="no" frameborder="0"></iframe> -->
          <el-image
            style="width: 100%; height: 100%"
            :src="img_url"
            fit="cover"
            :preview-src-list="img_url_list"
            ></el-image>
            <!-- <img  :src="img_url" /> -->
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="6">
        <el-card class="update-log">
          <div class="header">
            <el-link v-bind:style="HotTagSetting" :underline="false" @click="switchTagsTitle('Hot')">热门标签</el-link>
            <el-divider direction="vertical"></el-divider>
            <el-link v-bind:style="NewTagSetting" :underline="false" @click="switchTagsTitle('New')">最新标签</el-link>
            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false" @click="goTag(taghead)">
              更多<i class="el-icon-view el-icon--right"></i>
            </el-link>
          </div>
          <ul>
            <li v-for="Tag in displayTagsContent">
              <div class="col-item">
                <el-link v-loading="tagloading" type="primary" @click="showtagDetail(Tag)">{{ Tag.tagName }}</el-link>
              </div>
            </li>
          </ul>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="8">
        <el-card class="update-log">
          <div class="header">
            <el-link v-bind:style="HotPostSetting" :underline="false" @click="switchPostsTitle('Hot')">热门帖子</el-link>
            <el-divider style="color:black" direction="vertical"></el-divider>
            <el-link v-bind:style="NewPostSetting" :underline="false" @click="switchPostsTitle('New')">最新帖子</el-link>
            <el-link style="float:right; padding-bottom: 10px;" type="warning" el-link :underline="false" @click="goPost(posthead)">
              更多<i class="el-icon-view el-icon--right"></i>
            </el-link>
          </div>
          <ul>
            <li v-for="Post in displayPostsContent">
              <div class="col-item" >
                 <el-link v-loading="postloading" type="primary" @click="showpostDetail(Post)" >{{Post.postTitle}}</el-link>

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
        <el-form-item label="更新时间" prop="createTime">
          <el-input v-model="Tagform.createTime" readonly />
        </el-form-item>
        <el-form-item label="热度" prop="tagPopularity">
          <el-input v-model="Tagform.tagPopularity" readonly />
        </el-form-item>  
        <el-form-item label="备注" prop="remark">
          <el-input v-model="Tagform.remark" type="textarea" readonly :autosize="{ minRows: 5, maxRows: 15 }"></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>

    
    <el-dialog
      :title="title"
      :visible.sync="post_detail_open"
      width="600px"
      append-to-body
    >
      <el-form ref="form" :model="postform" label-width="100px">
        <el-form-item label="标题" prop="postTitle">
          <el-input v-model="postform.postTitle" readonly />
        </el-form-item>
        <!-- <el-form-item label="关键词" prop="postKeywords">
          <el-tag :key="keyword" type="primary" v-for="keyword in postform.postKeywords" >{{ keyword }}</el-tag>
        </el-form-item>
        <el-form-item label="标签" prop="postTag">
          <el-tag :key="tag.tagID" :type="tag.type" v-for="tag in postform.postTags" >{{ tag.tagName }}</el-tag>
        </el-form-item> -->
        <el-form-item label="发帖时间" prop="postTime">
          <el-input v-model="postform.postTime" readonly />
        </el-form-item>
        <el-form-item label="热度" prop="postPopularity">
          <el-input v-model="postform.postPopularity" readonly />
        </el-form-item>
        <el-form-item label="帖子内容" prop="postContent">
          <el-input
            v-model="postform.postContent"
            type="textarea"
            readonly
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
        <el-form-item label="帖子回答" prop="postAnswer">
          <el-input
            v-model="postform.postAnswer"
            type="textarea"
            readonly
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
    
  </div>
</template>


<script>

import { getHotTags, getNewTags, getHotPosts, getNewPosts } from "@/api/manage/mainpage.js";
import { getTag } from "@/api/manage/tag.js"
import { getWordCloud } from "@/api/manage/visualization.js"
import { getPost } from "@/api/manage/post.js"


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
      //
      post_detail_open: false,
      //标签表单
      Tagform: {},

      postform: {},
      //标题字体样式设置
      HotTagSetting: { color: 'red', fontSize: '16px' },

      NewTagSetting: { fontSize: '16px' },

      HotPostSetting: { color: 'red', fontSize: '16px' },

      NewPostSetting: { fontSize: '16px' },

      img_url_list: [],
      
      // img_url:"localhost:5000/static/img/wordcloud_img.jpg",
      img_url:"",
      // img_url:"http://localhost:5000/vis/getWordCloud",

      taghead: 'Hot',

      posthead: 'Hot',

      queryHotTagsParams: {
        HotTagsNum: 5,
      },
      queryNewTagsParams: {
        NewTagsNum: 5,
      },
      queryHotPostsParams: {
        HotPostsNum: 5,
      },
      queryNewPostsParams: {
        NewPostsNum: 5,
      },

      latestvisitlist: ["暂无"],

      todolist: ["暂无"],

      noticelist: ["快点写,不然就做不完了"]
    };
  },
  created() {
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
        console.log(res.data)
        this.HotPostsContent = res.data;
        this.displayPostsContent = res.data
      })
      getNewPosts(this.queryNewPostsParams).then((res) => {
        console.log("成功取得NewPosts数据")
        this.NewPostsContent = res.data;
      })
      getWordCloud().then((res) => {
        console.log('接收到词云图')
        console.log(res)
        
        this.img_url = res.data.img_url;
        this.img_url_list.push(this.img_url)
      })
    },
    goTag(sortForm) {
      sessionStorage.setItem("tagpresetParam",sortForm)
      sessionStorage.setItem("tagneedRunPreset","ok")
      this.$router.push('/system/tag')
    },
    goPost(sortForm) {
      sessionStorage.setItem("postpresetParam",sortForm)
      sessionStorage.setItem("postneedRunPreset","ok")
      this.$router.push('/system/post')
    },
    switchTagsTitle(title) {
      this.tagloading = true;
      this.settagTitletheme(title)
      setTimeout(() => {
        if (title === 'Hot') {
          this.displayTagsContent = this.HotTagsContent;
          this.taghead = 'Hot';
        }
        else {
          this.displayTagsContent = this.NewTagsContent;
          this.taghead = 'New';
        }
        this.tagloading = false
      }, 200);
      //console.log(HotTagsContent[0].tagName)
    },
    switchPostsTitle(title) {
      this.postloading = true;
      this.setpostTitletheme(title);
      setTimeout(() => {
        if(title === 'Hot'){
          this.displayPostsContent = this.HotPostsContent;
          this.posthead = 'Hot'
        }
        else{
          this.displayPostsContent = this.NewPostsContent;
          this.posthead = 'New'
        }
        this.postloading = false
      }, 200);
    },
    showtagDetail(row) {
      const tagName = row.tagName;
      getTag({ tagName: tagName }).then((res) => {
        console.log('点开详情页面，收到数据')
        console.log(res)
        this.Tagform = res.data[0];
        this.Tag_detail_open = true;
        this.title = "标签详情";
      })
    },
    showpostDetail(row) {
      const postIDData = row.postID;
      getPost({ postID: postIDData}).then((res) => {
        console.log('点开详情界面，收到数据')
        console.log(res)
        this.postform = res.data[0];
        this.post_detail_open = true;
        this.title = "帖子详情";
      })
    },
    //根据标签主题设置字符样式
    settagTitletheme(title) {
      if (title === 'Hot') {
        this.HotTagSetting = { color: 'red', fontSize: '16px' };
        this.NewTagSetting = { fontSize: '16px' };
      }
      else {
        this.HotTagSetting = { fontSize: '16px' };
        this.NewTagSetting = { color: 'red', fontSize: '16px' };
      }
    },
    setpostTitletheme(title) {
      if (title === 'Hot') {
        this.HotPostSetting = { color: 'red', fontSize: '16px' };
        this.NewPostSetting = { fontSize: '16px' };
      }
      else {
        this.HotPostSetting = { fontSize: '16px' };
        this.NewPostSetting = { color: 'red', fontSize: '16px' };
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

  font-family: "open sans",
  "Helvetica Neue",
  Helvetica,
  Arial,
  sans-serif;
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

  .info {
    background-color: #ece0db;
    //background-color: #c9dbef;
    font-size: 15px;
    color: #01847f;
    height: 200px;

    ol {
      display: block;
      list-style-type: decimal;
      margin-block-start: 10px;
      margin-block-end: 10px;
      margin-inline-start: 0;
      margin-inline-end: 0;
      padding-inline-start: 40px;

    }

    span {
      line-height: 30px;
    }
  }
}

#wordcloud{
  width: 100%;
  height: 100%;
  min-width: 700px;
  min-height: 600px;
}

#wordcloud img{
  width:100%;
  height: auto;
}

.word-cloud-card .el-card__body{
  width: 100%;
  height: 100%;
  margin: 0;
  object-fit: cover;
}


</style>

