<template>
    <div class="app-container">
      <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
        <el-form-item label="图片类型" prop="imgtype">
          <el-select v-model="queryParams.imgtype" placeholder="请选择图片类型" clearable>
            <el-option
              v-for="imgtype in imagetype"
              :key="imgtype.value"
              :label="imgtype.label"
              :value="imgtype.value"
            />
          </el-select>
        </el-form-item>

				<el-form-item label="开始时间" prop="date">
					<el-date-picker
						v-model="queryParams.startdate"
						format="yyyy-MM-dd"
						value-format="yyyy-MM-dd"
						type="date"
						placeholder="开始日期"
						>
					</el-date-picker>
				</el-form-item>

				<el-form-item label="结束时间" prop="date">
					<el-date-picker
						v-model="queryParams.enddate"
						format="yyyy-MM-dd"
						value-format="yyyy-MM-dd"
						type="date"
						placeholder="结束日期"
						>
					</el-date-picker>
				</el-form-item>

        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        </el-form-item>
      </el-form>

      <div id='main' :style="{width:'100%',height:'400px'}"></div>
    </div>
  </template>
  
  <script>
  import { getData } from "@/api/manage/visualization";
  import * as echarts from 'echarts'
  
  export default {
    name: "Visualization",
    data() {
      return {
        // 遮罩层
        loading: true,

				showSearch: true,

        chartData: [],

        useAnalogData: true,

        AnalogData: [
          {tagName:"标签名1",frequency:20},
          {tagName:"标签名2",frequency:10},
          {tagName:"标签名3",frequency:50},
          {tagName:"标签名4",frequency:22},
          {tagName:"标签名5",frequency:35},
        ],
        //可选择图片类型
        imagetype : [
          {
            value: '条形图',
            label: '条形图'
          }
        ],
        // 查询参数
        queryParams: {
					startdate: "",
					enddate: "",
          imgtype: undefined
        },
        // 表单校验
        rules: {
          startdate: [
            { required: true, dateISO: true, message: "请选择正确的开始时间", trigger: "blur" }
          ],
          enddate: [
            { required: true, dateISO: true, message: "请选择正确的结束时间", trigger: "blur" }
          ],
          imgtype: [
            { required: true, message: "请选择生成的图片类型", trigger: "blur" }
          ]
        }
      };
    },
    mounted() {
		if(this.useAnalogData === true){
			if(document.readyState === "complete"){
				this.initChart();
			}
		}
	  },
    methods: {
      /** 生成图片按钮操作 */
      handleQuery() {
        this.loading = true;
        this.useAnalogData = false;
        getData(this.queryParams).then((res) => {
          this.chartData = res.data
          console.log('收到可视化数据')
          this.loading = false
        })
        
        this.initChart();
      },
      initChart() {
        const chart = echarts.init(document.getElementById('main'))
        var option = {
          title: {
            text: '热门标签频数条形图',
            subtext: '模拟数据',
            textAligh: 'auto',
            textVerticalAlign:'auto',
            left:'40%'
          },
          tooltip: {},
          grid: {
            top: "20%",
            left: "5%",
            right: "5%",
            bottom: "5%",
            // 把x轴和y轴纳入 grid
            containLabel: true
          },
          dataset: {
            source: this.AnalogData
          },
          xAxis: {
            name: '热度频数'
          },
          yAxis: {
            name: '标签名',
            type: 'category'
          },
          series: {
            name:'热度频数',
            type: 'bar',
            encode : {
              x: 'frequency',
              y: 'tagName'
            },
            label : {
              show: true,
              position: 'right'
            },
            itemStyle: {
              normal: {
                color: function(params){
                  var colorlist =  [
                    '#37A2DA',
                    '#32C5E9',
                    '#67E0E3',
                    '#9FE6B8',
                    '#FFDB5C',
                    '#ff9f7f',
                    '#fb7293',
                    '#E062AE',
                    '#E690D1',
                    '#e7bcf3',
                    '#9d96f5',
                    '#8378EA',
                    '#96BFFF'
                  ];
                  return colorlist[params.dataIndex]
                }
              }
            },

          },
          
        }
        if(this.useAnalogData === true){
          chart.setOption(option)
        }
        else{
          option.title = {
            text: '热门标签频数条形图',
            textAligh: 'auto',
            textVerticalAlign:'auto',
            left:'40%'
          }
          option.dataset.source = this.chartData
          chart.setOption(option)
        }
		  },
    }
  };
  </script>
  