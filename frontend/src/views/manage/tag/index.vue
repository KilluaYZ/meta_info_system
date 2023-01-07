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
      <el-form-item label="标签名称" prop="tagName">
        <el-input
          v-model="queryParams.tagName"
          placeholder="请输入标签名称"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="级别" prop="tagClass">
        <el-select
          v-model="queryParams.tagClass"
          placeholder="标签级别"
          clearable
          style="width: 240px;padding-right: 25px;"
        >
          <el-option label="1" value="1">1</el-option>
          <el-option label="2" value="2">2</el-option>
          <el-option label="3" value="3">3</el-option>
        </el-select>
      </el-form-item>
      
      

      <el-form-item label="排序方式" prop="sortMode">
        <el-select
          v-model="queryParams.sortMode"
          placeholder="按序号排序"
          clearable
          style="width: 240px;"
        >
          <el-option label="默认排序" value="Default"></el-option>
          <el-option label="按热度排序" value="Hot"></el-option>
          <el-option label="按时间排序" value="New"></el-option>

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
      :data="tagTableData"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column
        label="名称"
        align="center"
        prop="tagName"
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          <el-button  type="text" @click="showDetials({data:scope.row,row:'selftag'})">
            <span>{{ scope.row.tagName }}</span>
          </el-button>
        </template>      
      </el-table-column>
      <el-table-column
        label="父标签"
        align="center"
        :show-overflow-tooltip="true"
        prop="tagParentName"
      >
        <template slot-scope="scope">
          <el-button size="mini" type="text" @click="showDetials({data:scope.row,row:'parent'})">
            <span>{{ scope.row.tagParentName }}</span>
          </el-button>
        </template>
      </el-table-column>

      <el-table-column label="级别" align="center" prop="tagClass">
        <!--<template slot-scope="scope">
          <dict-tag :options="dict.type.sys_normal_disable" :value="scope.row.status" />
          <span>{{scope.row.tagClass}}</span>
        </template>-->
      </el-table-column>
      <el-table-column label="热度" align="center" prop="tagPopularity">
      </el-table-column>


      <el-table-column label="创建时间" align="center" prop="createTime"></el-table-column>
  
      <el-table-column
        label="备注"
        align="center"
        prop="remark"
        :show-overflow-tooltip="true"
      />
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
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
      width="500px"
      append-to-body
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标签名" prop="tagName">
          <el-input v-model="form.tagName" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="父标签名" prop="tagParentName">
          <!-- <el-input v-model="form.tagParentName" placeholder="请输入父标签名称" /> -->
          <el-select
            v-model="form.tagParentName"
            filterable
            placeholder="父标签名"
            :disabled="configPageParentTagDisabled"
          >
            <el-option
              v-for="item in configPageParentTags"
              :key="item.tagName"
              :value="item.tagName"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签级别" prop="tagClass" v-if="!form.tagID">
          <el-radio-group
            v-model="form.tagClass"
            size="small"
            @change="handleConfigPageParentTagNameSelectChanged(form.tagClass)"
          >
            <el-radio-button label="1" value="1">级别1</el-radio-button>
            <el-radio-button label="2" value="2">级别2</el-radio-button>
            <el-radio-button label="3" value="3">级别3</el-radio-button>
          </el-radio-group>
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

    <!-- 显示详情对话框 -->
    <el-dialog
      :title="title"
      :visible.sync="detail_open"
      width="500px"
      append-to-body
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标签名称" prop="tagName">
          <el-input v-model="form.tagName" readonly />
        </el-form-item>
        <el-form-item label="父标签名" prop="tagParentName">
          <el-input v-model="form.tagParentName" readonly />
        </el-form-item>
        <el-form-item label="标签级别" prop="tagClass">
          <el-input v-model="form.tagClass" readonly />
        </el-form-item>
        <el-form-item label="创建时间" prop="createTime">
          <el-input v-model="form.createTime" readonly />
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
  </div>
</template>

<script>
// import {
//   listType,
//   getType,
//   delType,
//   addType,
//   updateType,
//   refreshCache,
// } from "@/api/system/dict/type";

import { addTag, delTag, updateTag, getTag } from "@/api/manage/tag.js";

export default {
  name: "Tag",
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
      tagTableData: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      config_open: false,
      // 是否显示详情页面
      detail_open: false,
      // 日期范围
      dateRange: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        tagName: undefined,
        tagClass: undefined,
        tagDate: undefined,
        sortMode: "Default",
        nameQueryMode: "blur"
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        tagName: [
          { required: true, message: "标签名称不能为空", trigger: "blur" },
        ],
        tagClass: [
          { required: true, message: "标签级别不能为空", trigger: "blur" },
        ],
      },
      configPageParentTags: [],
      configPageParentTagDisabled: false,
    };
  },
  created() {
    console.log(sessionStorage.getItem("tagneedRunPreset"))
    if(sessionStorage.getItem("tagneedRunPreset") === "ok"){
      console.log("使用初始化配置")
      if(sessionStorage.getItem("tagpresetParam") === 'Hot')
        this.queryParams.sortMode = "Hot"
      if(sessionStorage.getItem("tagpresetParam") === 'New')
        this.queryParams.sortMode = "New"
    }
    console.log(this.queryParams.sortMode)
    this.getList();
    //if(this.$store.state.tagneedRunPreset === true)
    //  console.log("使用配置")
    console.log(sessionStorage.getItem("tagneedRunPreset"))
    console.log("创建tag页面ing");
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
      getTag(this.queryParams).then((res) => {
        console.log("成功取得getTag mock数据");
        this.tagTableData = res.data;
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
        tagName: undefined,
        tagClass: undefined,
        tagParentName: undefined,
        tagDate: undefined,
        remark: undefined,
      };
      this.resetForm("form");
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
      this.ids = selection.map((item) => item.tagName);
      this.single = selection.length != 1;
      this.multiple = !selection.length;
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const tagNameData = row.tagName;
      getTag({ tagName: tagNameData }).then((response) => {
        console.log("点开修改页面，收到数据");
        console.log(response)
        this.form = response.data[0];
        this.handleConfigPageParentTagNameSelectChanged(this.form.tagClass)
        console.log("this.form");
        console.log(this.form);
        this.config_open = true;
        this.title = "修改标签类型";
      });
    },
    showDetials(param) {
      this.reset();
      const tagName = param.row === 'parent' ? param.data.tagParentName : param.data.tagName;
      getTag({ tagName: tagName }).then((res) => {
        console.log("点开详情页面，收到数据");
        console.log(res);
        this.form = res.data[0];
        console.log(res.data[0])
        this.detail_open = true;
        this.title = "标签详情";
      });
    },

    /** 提交按钮 */
    submitForm: function () {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          if (this.form.tagID != undefined) {
            updateTag(this.form).then((response) => {
              this.$modal.msgSuccess("修改成功");
              this.config_open = false;
              this.getList();
            });
          } else {
            addTag(this.form).then((response) => {
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
      const tagName = row.tagName ? [row.tagName + ""] : this.ids;
      console.log("tagName:");
      console.log(tagName);
      console.log("ids:");
      console.log(this.ids);
      this.$modal
        .confirm('是否确认删除标签名称为"' + tagName.toString() + '"的数据项？')
        .then(() => {
          tagName.forEach((item) => {
            delTag({ tagName: item })
              .then(() => {
                this.$modal.msgSuccess('成功删除标签"' + item + '"');
              })
              .catch(() => {
                this.$modal.msgError('删除标签"' + item + '"失败');
              });
          });
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
    handleConfigPageParentTagNameSelectChanged(selectedTagClass) {
      if (selectedTagClass == 1) {
        //选了级别1时，让父标签失效
        this.configPageParentTagDisabled = true;
      } else {
        this.configPageParentTagDisabled = false;
        getTag({ tagClass: selectedTagClass - 1 }).then((res) => {
          this.configPageParentTags = res.data;
        });
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
