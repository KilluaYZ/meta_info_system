# frontend

前端基于Vue2和element-ui开发，使用了Ruoyi为模板

## 部署方式

### 开发环境

```bash
# 安装npm node gitbash
node版本最好选15

# 安装vue脚手架
npm install -g @vue/cli

# 克隆项目
git clone https://gitee.com/killuayz/meta_info_system_frontend.git

# 进入项目目录
cd meta_info_system/frontend

# 安装依赖
npm install --force

# 如果上一步npm install 太慢可以试试下面这个代码，建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev
```



### 模板

[介绍 | RuoYi](http://doc.ruoyi.vip/ruoyi/)

### 目录

重点需要关注的文件及文件夹

- dist  编译（npm run build）后生成的编译文件存放的地方

- node_modules  node基础的依赖包以及我们拓展安装的插件等

- public

  - index.html 入口页面
  - favicon.ico 图标

- src 源码目录

  - api    axios网络请求定义，定义一系列axios与服务器通信的方法，供前端页面调用

  - assets   存放一些资源文件，如图片，图标，css，json等

    - icons   图标
    - img    图片
    - json    需要用到的静态数据

  - components  组件目录，储存网页中可复用的所有组件

    - NavMenu.vue    导航栏组件

  - views 存放页面视图

  - layout 存放页面布局

  - router    vue-router路由配置，用于加载各个组件，管理路由和导航

  - store    vuex状态管理目录，用于存放页面所需**所有**信息

    - index.js    储存了页面所需所有信息，getter， setter方法

  - styles   全局css样式文件，用scss写

  - utils   工具页面，存放开发中要用到的工具代码文件

  - main.js    程序入口文件，用于创建vue实例，加载各种资源、组件

  - permission.js 管理页面权限

  - settings.js 配置文件

      

- package.json : 项目基本信息，包依赖信息等

- vue.config.js : vue配置信息

  ​    

### 技术栈

- Vue

  - Vue是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套声明式的、组件化的编程模型，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。

- Vuex 
  - Vuex 是一个专为 Vue.js 应用程序开发的状态管理模式 + 库。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。我们借助它来储存网页中要用到的数据。

- Babel
  - Babel 是一个工具链，主要用于在当前和旧的浏览器或环境中，将 ECMAScript 2015+ 代码转换为 JavaScript 向后兼容版本的代码。以便我们在旧版和最新版的浏览器中使用新特性（如JSX、箭头函数、promise等）

- Scss
  - Scss是一个CSS预处理器，可以理解为是sass的升级版，相比sass，scss语言更兼容，不必使用严格的缩进。CSS预处理器定义了一种新的语言，其基本思想是，用一种专门的编程语言，为 CSS 增加了一些编程的特性，将 CSS作为目标生成文件，然后开发者就只要使用这种语言进行编码工作。让你的 CSS 更加简洁、适应性更强、可读性更佳，更易于代码的维护。我们借助它来编写CSS代码。

- Vue-router 
  - vue-router是Vue官方插件，我们借助它实现网页页面跳转。

- Axios
  - Axios 是一个基于 promise 网络请求库，是Vue.js团队推荐的优秀的，用于向服务器发送请求的库。

  
