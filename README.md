# Meta Data Management

## Environment
node.js 16.13.1<br>
npm 8.1.2<br>
python 3.9.12<br>
pip 21.9.4<br>
if the environment is prepared, you must:<br>
```
cd frontend
npm run build
cd ..
cd backend
pip install -r requirements.txt
```
to start frontend, it listens the port 8080:
```
cd frontend
npm run serve
```
to start backend, it listens the port 5000:
```
cd backend
python backendmain.py
```

## Frontend Tutorial
🌟 **最重要的技术：Vue3.0，可以不求甚解，先能上手开始写，之后用到哪个功能再详细去学（API风格咱们用组合式，不用选项式，语言用Javascript，不用Typescript）**<br>
**https://cn.vuejs.org/guide/introduction.html**<br>
**选项式和组合式的对比**（选项式风格也能看懂就更好了）<br>
https://www.cnblogs.com/dingshaohua/p/15661255.html<br>
**Element-UI**，适配Vue的UI库，简单看一下，知道有哪些组建哪些功能即可，用到再去看代码<br>
https://element.eleme.cn/#/zh-CN/component/installation<br>

✨ **技术基础和支撑，Vue中会用到的基本语言，可以快速过一遍语法**<br>
Javascript学习：<br>
https://www.runoob.com/js/js-tutorial.html<br>
HTML5学习：<br>
https://www.runoob.com/html/html-tutorial.html<br>
CSS学习：<br>
https://www.runoob.com/css/css-tutorial.html<br>

🪐 **项目构建有关知识**<br>
NVM类似于python中的Anaconda，是一个环境管理工具，<br>
node.js就类似于python，有不同版本，<br>
npm类似于pip，是一个包管理工具<br>

Windows通过NVM安装node.js<br>
https://blog.csdn.net/z17864151193/article/details/123843412<br>
MacOS通过NVM安装node.js<br>
https://baijiahao.baidu.com/s?id=1676054080568599126&wfr=spider&for=pc<br>
npm换cnpm:<br>
https://blog.csdn.net/weixin_42402845/article/details/107630921<br>
Vue脚手架介绍：<br>
https://blog.csdn.net/m0_67495466/article/details/124133275<br>
Vue脚手架教程：<br>
https://cli.vuejs.org/zh/guide/<br>

⭐️ **前端如何向后端发送数据**<br>
vue axios包介绍：<br>
https://blog.csdn.net/qq_41809113/article/details/121705383<br>
HTTP状态消息入门：<br>
https://www.runoob.com/tags/html-httpmessages.html<br>
HTTP几种请求方式入门：<br>
https://www.runoob.com/tags/html-httpmethods.html<br>

## Backend Tutorial

可以先了解一下前端相关框架，后端要与前端持续沟通对齐接口<br>

**Flask 框架简介**<br>
https://dormousehole.readthedocs.io/en/latest/<br>

**Flask：从第一个小项目做起**<br>
https://blog.csdn.net/Littleflowers/article/details/113926184<br>

**Flask：项目架构介绍——蓝图的使用**<br>
https://zhuanlan.zhihu.com/p/356740061<br>

**学点SQL，一点点就好**<br>
https://www.runoob.com/sql/sql-tutorial.html<br>

**后端如何与SQL交互：一个最简单的cursor教程**<br>
https://cloud.tencent.com/developer/article/1575066<br>

