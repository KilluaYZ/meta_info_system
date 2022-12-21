<template>
  <div class="app-container">
    <el-form
      :model="queryParams"
      ref="queryForm"
      size="small"
      :inline="true"
      v-show="showSearch"
      label-width="68px"
    >
      <el-form-item label="帖子标题" prop="postTitle">
        <el-input
          v-model="queryParams.postTitle"
          placeholder="请输入帖子标题"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="帖子ID" prop="postID">
        <el-input
          v-model="queryParams.postID"
          placeholder="请输入帖子ID"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="关键词" prop="postKeywords">
        <el-input
          v-model="queryParams.postKeywords"
          placeholder="请输入关键词"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>

      <el-form-item label="标签" prop="postTag">
        <el-input
          v-model="queryParams.postTag"
          placeholder="请输入标签"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>

      <el-form-item label="时间" prop="postTime">
        <el-date-picker
          v-model="queryParams.postTime"
          value-format="yyyy-MM-dd"
          type="daterange"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        >
        </el-date-picker>
      </el-form-item>

      <el-form-item label="排序方式" prop="sort">
        <el-select
          v-model="queryParams.sortMode"
          placeholder="默认排序"
          clearable
          style="width: 240px;"
        >
          <el-option label="默认排序" value="Default">默认排序</el-option>
          <el-option label="按热度排序" value="Hot">按热度排序</el-option>
          <el-option label="按时间排序" value="New">按时间排序</el-option>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          icon="el-icon-search"
          size="mini"
          @click="handleQuery"
          >搜索</el-button
        >
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery"
          >重置</el-button
        >
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          >新增</el-button
        >
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          >删除</el-button
        >
      </el-col>
      <!-- <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          >导出</el-button
        >
      </el-col> -->
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-refresh"
          size="mini"
          @click="handleRefreshCache"
          >刷新缓存</el-button
        >
      </el-col>
      <right-toolbar
        :showSearch.sync="showSearch"
        @queryTable="getList"
      ></right-toolbar>
    </el-row>

    <el-table
      v-loading="loading"
      :data="TableData"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="55"
        align="center"
        fixed="left"
      />
      <el-table-column label="ID" align="center" prop="postID" fixed="left" />
      <el-table-column
        label="标题"
        align="center"
        prop="postTitle"
        :show-overflow-tooltip="true"
        width="250"
      >
        <template slot-scope="scope" class="postpage-warp-column">
          <el-button type="text"
            @click="showpostDetails(scope.row)"
          >
            <span>{{ scope.row.postTitle }}</span>
          </el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="关键词"
        align="center"
        prop="postKeywords"
        width="300"
      >
        <template slot-scope="scope" class="postpage-warp-column">
          <el-tag v-for="keyword in scope.row.postKeywords" :key="keyword.id">
            {{ keyword }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column
        label="标签"
        align="center"
        :show-overflow-tooltip="true"
        prop="postTag"
        width="400"
      >
        <template slot-scope="scope" class="postpage-warp-column">
          <el-button
            size="mini"
            v-for="item in scope.row.postTag"
            :key="item"
            :type="item.type"
            @click="showtagDetails(item)"
          >
            <span>{{ item.tagName }}</span>
          </el-button>
        </template>
      </el-table-column>

      <el-table-column
        label="热度"
        align="center"
        prop="postPopularity"
        :show-overflow-tooltip="true"
      />

      <el-table-column
        label="发帖时间"
        align="center"
        prop="postTime"
        width="150"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.postTime }}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="备注"
        align="center"
        prop="remark"
        :show-overflow-tooltip="true"
        width="300"
      />
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
        fixed="right"
        width="200"
      >
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            >修改</el-button
          >
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            style="color: crimson;"
            @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog
      :title="title"
      :visible.sync="config_open"
      width="80vw"
      append-to-body
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="帖子标题" prop="postTitle">
          <el-input v-model="form.postTitle" placeholder="请输入帖子标题" />
        </el-form-item>

        <el-form-item label="关键词" prop="postKeywords">
          <el-tag
            :key="keyword"
            v-for="keyword in form.postKeywords"
            closable
            @close="handleConfigPageKeywordClose(keyword)"
          >
            {{ keyword }}
          </el-tag>
          <el-input
            v-if="configPageKeywordInputVisiable"
            v-model="configPageKeywordInputValue"
            ref="saveConfigPageKeywordInput"
            class="input-new-tag"
            size="small"
            @keyup.enter.native="handleConfigPageKeywordInput"
            @blur="handleConfigPageKeywordInput"
          >
          </el-input>
          <el-button
            v-else
            class="button-new-tag"
            size="small"
            @click="showConfigPageKeywordInput"
          >
            + 新关键词
          </el-button>
        </el-form-item>

        <el-form-item label="标签" prop="postTag">
          <el-tag
            :key="tag.tagName"
            closable
            v-for="tag in form.postTag"
            :type="tag.type"
            @close="handleConfigPageTagClose(tag)"
          >
            {{ tag.tagName }}
          </el-tag>

          <template v-if="configPageTagAddVisiable">
            <el-select
              v-model="configPageFirstTagValue"
              filterable
              clearable
              placeholder="一级标签"
              :loading="firstTagSelectLoading"
              @change="handleTagAddSelectChanged(1)"
              @clear="handleTagAddSelectClear(1)"
            >
              <el-option
                v-for="item in firstTags"
                :key="item.tagName"
                :value="item.tagName"
                :label="item.tagName"
              >
              </el-option>
            </el-select>
            <el-select
              v-model="configPageSecondTagValue"
              filterable
              clearable
              :loading="secondTagSelectLoading"
              placeholder="二级标签"
              @change="handleTagAddSelectChanged(2)"
              @clear="handleTagAddSelectClear(2)"
            >
              <el-option
                v-for="item in secondTags"
                :key="item.tagName"
                :value="item.tagName"
              >
              </el-option>
            </el-select>
            <el-select
              v-model="configPageThirdTagValue"
              filterable
              clearable
              :loading="thirdTagSelectLoading"
              placeholder="三级标签"
              @change="handleTagAddSelectChanged(3)"
              @clear="handleTagAddSelectClear(3)"
            >
              <el-option
                v-for="item in thirdTags"
                :key="item.tagName"
                :value="item.tagName"
              >
              </el-option>
            </el-select>
            <el-button
              size="small"
              type="success"
              class="configPageAddTagBtn"
              @click="handlerConfigPageTagAdd"
            >
              确认
            </el-button>
            <el-button
              size="small"
              type="danger"
              class="configPageAddTagBtn"
              @click="unshowConfigPageTagAdd"
            >
              取消
            </el-button>
          </template>

          <el-button
            v-else
            size="small"
            @click="showConfigPageTagAdd"
            class="button-new-tag"
          >
            + 新标签
          </el-button>
        </el-form-item>

        <el-form-item label="发帖日期" prop="postTime">
          <el-date-picker
            v-model="form.postTime"
            type="date"
            placeholder="选择发帖日期"
            value-format="yyyy-MM-dd"
          >
          </el-date-picker>
        </el-form-item>

        <el-form-item label="热度" prop="postPopularity">
          <el-input
            v-model="form.postPopularity"
            placeholder="请输入帖子热度"
          />
        </el-form-item>

        <el-form-item label="内容" prop="postContent">
          <el-input
            v-model="form.postContent"
            type="textarea"
            placeholder="请输入内容"
            :autosize="{ minRows: 15, maxRows: 20 }"
          ></el-input>
        </el-form-item>

        <el-form-item label="回答" prop="postAnswer">
          <el-input
            v-model="form.postAnswer"
            type="textarea"
            placeholder="请输入内容"
            :autosize="{ minRows: 10, maxRows: 15 }"
          ></el-input>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            placeholder="请输入内容"
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 显示标签详情对话框 -->
    <el-dialog
      :title="title"
      :visible.sync="tag_detail_open"
      width="600px"
      append-to-body
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标签名称" prop="tagName">
          <el-input v-model="form.tagName" readonly />
        </el-form-item>
        <el-form-item label="父标签名" prop="tagParentName">
          <el-input v-model="form.tagParentName" readonly />
        </el-form-item>
        <el-form-item label="标签级别" prop="tagClass">
          <el-input v-model="form.tagClass" readonly />
        </el-form-item>
        <el-form-item label="标签继承关系" prop="frontTagTree">
          <el-tag
            :key="tag.tagName"
            v-for="tag in form.frontTagTree"
            :type="tag.type"
            :disable-transitions="false"
          >
            {{ tag.tagName }}
          </el-tag>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            readonly
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog
      :title="title"
      :visible.sync="post_detail_open"
      width="600px"
      append-to-body
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="postTitle">
          <el-input v-model="form.postTitle" readonly />
        </el-form-item>
        <el-form-item label="帖子内容" prop="postContent">
          <el-input
            v-model="form.postContent"
            type="textarea"
            readonly
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
        <el-form-item label="帖子回答" prop="postAnswer">
          <el-input
            v-model="form.postAnswer"
            type="textarea"
            readonly
            :autosize="{ minRows: 5, maxRows: 15 }"
          ></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<style lang="scss">
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
.configPageAddTagBtn{
  margin-left: 10px;
}

.postpage-warp-column{
  // display: flex;
  // flex-direction: column;
  // justify-content: center;
  // align-items: center;
}
</style>


<script>
import {
  addTag,
  delTag,
  updateTag,
  getTag,
  getFrontTagTree,
} from "@/api/manage/tag.js";
import { addPost, delPost, updatePost, getPost } from "@/api/manage/post.js";
export default {
  name: "Post",
  // dicts: ["sys_normal_disable"],
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 标签表格数据
      TableData: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      config_open: false,
      // 是否显示标签详情页面
      tag_detail_open: false,
      // 是否显示帖子详情页面
      post_detail_open: false,
      // 日期范围
      dateRange: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        postTitle: undefined,
        postID: undefined,
        postKeywords: undefined,
        postTag: undefined,
        postTime: undefined,
        sortMode: "Default"
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        postTitle: [
          { required: true, message: "帖子标题不能为空", trigger: "blur" },
        ],
        postContent: [
          { required: true, message: "帖子内容不能为空", trigger: "blur" },
        ],
        postTime: [
          { required: true, message: "发帖时间不能为空", trigger: "blur" },
        ],
      },
      configPageKeywordInputVisiable: false,
      configPageKeywordInputValue: "",
      configPageTagAddVisiable: false,
      configPageFirstTagValue: "", //储存选中的一级标签的tagName
      configPageSecondTagValue: "",
      configPageThirdTagValue: "",
      firstTags: [],
      secondTags: [],
      thirdTags: [],
      firstTagSelectLoading: false,
      secondTagSelectLoading: false,
      thirdTagSelectLoading: false,
    };
  },
  created() {
    this.getList();
    this.firstTagSelectLoading = true
    getTag({ tagClass: "1" }).then((res) => {
      this.firstTags = res.data;
      this.firstTagSelectLoading = false
    });
    console.log("创建post页面ing");
  },
  methods: {
    /** 查询标签类型列表 */
    getList() {
      this.loading = true;
      // listType(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
      //     this.typeList = response.rows;
      //     this.total = response.total;
      //     this.loading = false;
      //   }
      // );
      // getTag(this.queryParams).then((res) => {
      //   console.log("成功取得getTag mock数据");
      //   this.tagTableData = res.data;
      //   this.total = res.data.length;
      //   this.loading = false;
      // });
      getPost(this.queryParams).then((res) => {
        console.log("成功取得getPost mock数据");
        console.log(res);
        this.TableData = res.data;
        this.total = res.length;
        this.loading = false;
      });
    },

    // 取消按钮
    cancel() {
      this.config_open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        postID: undefined,
        postTitle: undefined,
        postKeywords: [],
        postTag: [],
        postContent: undefined,
        postTime: undefined,
        postAnswer: undefined,
        postPopularity: undefined,
        remark: undefined,
      };
      this.resetForm("form");
      this.configPageFirstTagValue = "";
      this.configPageSecondTagValue = "";
      this.configPageThirdTagValue = "";
      this.configPageKeywordInputVisiable = "";
      this.secondTags = []
      this.thirdTags = []
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.config_open = true;
      this.title = "添加标签类型";
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map((item) => item.postID);
      this.single = selection.length != 1;
      this.multiple = !selection.length;
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const postIDData = row.postID;
      getPost({ postID: postIDData }).then((response) => {
        this.form = response.data[0];
        this.config_open = true;
        this.title = "帖子详情&修改";
      });
    },

    showtagDetails(row) {
      this.reset();
      const tagName = row.tagName;
      getTag({ tagName: tagName }).then((res) => {
        console.log("点开详情页面，收到数据");
        console.log(res);
        this.form = res.data[0];
        getFrontTagTree({tagName:tagName}).then((res) => {
          this.form.frontTagTree = res.data;
          this.tag_detail_open = true;
          this.title = "标签详情";
        });
      });
    },

    showpostDetails(row) {
      this.reset();
      const postIDData = row.postID;
      getPost({ postID: postIDData }).then((response) =>{
        console.log("点开详情页面，收到数据")
        this.form = response.data[0];
        console.log(this.form);
        this.post_detail_open = true;
        this.title = "帖子详情";
      })
    },

    /** 提交按钮 */
    submitForm: function () {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          if (this.form.postID != undefined) {
            updatePost(this.form).then((response) => {
              this.$modal.msgSuccess("修改成功");
              this.config_open = false;
              this.getList();
            });
          } else {
            addPost(this.form).then((response) => {
              this.$modal.msgSuccess("新增成功");
              this.config_open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const postIDList = row.postID ? [row.postID+""] : this.ids;
      this.$modal
        .confirm('是否确认删除ID为"' + postIDList.toString() + '"的数据项？')
        .then(() => {
          // return delPost(postID);
          postIDList.forEach((item,index) => {
            delPost({postID:item}).then(()=>{
              this.$modal.msgSuccess("删除"+item+"成功");
            }).catch(()=>{
              this.$modal.msgError('删除'+item+'失败');
            })
          })
        })
        .then(() => {
          this.getList();
        })
        .catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      // this.download(
      //   "system/dict/type/export",
      //   {
      //     ...this.queryParams,
      //   },
      //   `type_${new Date().getTime()}.xlsx`
      // );
      alert("暂不支持该功能");
    },
    /** 刷新缓存按钮操作 */
    handleRefreshCache() {
      refreshCache().then(() => {
        this.$modal.msgSuccess("刷新成功");
        this.$store.dispatch("dict/cleanDict");
      });
    },
    //处理配置页面添加新的关键词
    handleConfigPageKeywordInput() {
      let inputValue = this.configPageKeywordInputValue;
      if (inputValue) {
        //输入不为空
        if (this.form.postKeywords.indexOf(inputValue) == -1) {
          //不重复
          this.form.postKeywords.push(inputValue);
        } else {
          //发出错误提示
          this.$modal.msgError("相同关键词不能重复添加");
        }
      }
      this.configPageKeywordInputVisiable = false;
      this.configPageKeywordInputValue = "";
    },
    //展示input框
    showConfigPageKeywordInput() {
      this.configPageKeywordInputVisiable = true;
      this.$nextTick((_) => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    //删除已有关键词
    handleConfigPageKeywordClose(keyword) {
      this.form.postKeywords.splice(this.form.postKeywords.indexOf(keyword), 1);
    },
    //添加标签
    handlerConfigPageTagAdd() {
      if (this.configPageThirdTagValue) {
        if (
          this.configPageFirstTagValue == "" ||
          this.configPageSecondTagValue == ""
        ) {
          this.$modal.msgError("请确保一级二级标签不为空！");
        } else {
          getTag({ tagName: this.configPageThirdTagValue }).then((res) => {
            let tag = res.data[0];
            this.form.postTag.push(tag);
          });
        }
      } else if (this.configPageSecondTagValue) {
        if (this.configPageFirstTagValue == "") {
          this.$modal.msgError("请确保一级标签不为空！");
        } else {
          getTag({ tagName: this.configPageSecondTagValue }).then((res) => {
            let tag = res.data[0];
            this.form.postTag.push(tag);
          });
        }
      } else if (this.configPageFirstTagValue) {
        getTag({ tagName: this.configPageFirstTagValue }).then((res) => {
          let tag = res.data[0];
          this.form.postTag.push(tag);
        });
      }
      this.configPageTagAddVisiable = false;
    },
    //删除标签
    handleConfigPageTagClose(tag) {
      this.form.postTag.splice(this.form.postTag.indexOf(tag),1);
    },
    //显示添加标签选项
    showConfigPageTagAdd() {
      this.configPageTagAddVisiable = true;
    },
    unshowConfigPageTagAdd() {
      this.configPageTagAddVisiable = false;
      this.configPageFirstTagValue = "";
      this.configPageSecondTagValue = "";
      this.configPageThirdTagValue = "";
    },
    //处理tagAdd选择改变
    handleTagAddSelectChanged(tagClass) {
      
      if (tagClass == 1 && this.configPageFirstTagValue) {
        this.secondTagSelectLoading = true
        this.thirdTagSelectLoading = true
        getTag({ tagParentName: this.configPageFirstTagValue }).then((res) => {
          this.secondTags = res.data;
          this.thirdTags = [];
          this.configPageSecondTagValue = ""
          this.configPageThirdTagValue = ""
          this.secondTagSelectLoading = false
          this.thirdTagSelectLoading = false
        });
      } else if (tagClass == 2 && this.configPageSecondTagValue) {
        this.thirdTagSelectLoading = true
        getTag({ tagParentName: this.configPageSecondTagValue }).then((res) => {
          this.thirdTags = res.data;
          this.configPageThirdTagValue = ""
          this.thirdTagSelectLoading = false
        });
      }
    },

    //处理用户点击标签添加的clear
    handleTagAddSelectClear(tagClass){
      if(tagClass == 1){
        //如果clear了第一个，则将2、3都删掉
        this.configPageFirstTagValue = ""
        this.configPageSecondTagValue = ""
        this.configPageThirdTagValue = ""
        this.secondTags = []
        this.thirdTags = []
      }else if(tagClass == 2){
        this.configPageSecondTagValue = ""
        this.configPageThirdTagValue = ""
        this.thirdTags = []
      }else if(tagClass == 3){
        this.configPageThirdTagValue = ""
      }
    },
  },
  watch: {
    queryParams: {
      handler(newQuery, oldQuery) {
        console.log("newQuery");
        console.log(newQuery);
      },
      immediate: true,
      deep: true,
    },
  },
};
</script>
