# frontend

前端基于Vue2和element-ui开发，使用了Ruoyi为模板

demo演示[MOOC知识点标签管理系统](http://43.138.62.72:7878)

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
cd meta_info_system_frontend

# 安装依赖
npm install --force

# 如果上一步npm install 太慢可以试试下面这个代码，建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev
```

### 生产环境

#### 1.docker部署

```bash
#1.下载Dockerfile
#2.编译dockerfile
docker build -t meta_info:v1 .

#3.运行docker
docker run -itd \
	--name meta_info -p xxxx:80 \  #将外部端口绑定到80上
	-e MYSQL_HOST= <mysql服务器地址，默认为127.0.0.1> \
	-e MYSQL_PORT= <mysql服务器端口，默认为3306> \
	-e MYSQL_USER= <mysql服务器用户，默认为root> \
	-e MYSQL_PASSWORD= <mysql服务器密码，默认为123456> \
	-e MYSQL_DATABASE= <mysql服务器数据库，默认为meta_info_db> \
	meta_info:v1

```

#### 2.本地部署

```bash
echo "开始部署...\n"  echo "开始安装依赖...\n"  
apt update 
apt install -y unzip nginx  python3 python3-pip wget 
mkdir -p ~/.pip 
touch ~/.pip/pip.conf 
echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf 
cat ~/.pip/pip.conf  
pip install waitress 
echo "依赖安装成功\n"

echo "正在从gitee上下载并安装软件release最新版本...\n" 
mkdir -p /root/frontend 
mkdir -p /root/backend 
mkdir -p /root/backend/log 
cd /root/frontend 
wget  https://gitee.com/killuayz/meta_info_system/releases/download/v1.0/meta_info_frontend.tar.gz 
tar zxvf *.tar.gz 
cd /root/backend 
wget https://gitee.com/killuayz/meta_info_system/releases/download/v1.0/meta_info-1.0.0-py3-none-any.whl 
pip install *.whl 
echo "安装完成\n"

echo "正在进行部署配置..." 
#更改nginx配置文件，建议保存
echo "server {        listen 80 default_server;       listen [::]:80 default_server;  server_name localhost;  root /root/frontend;    index index.html; location / {try_files \$uri \$uri/ @router; } location @router { rewrite ^.*$ /index.html last; }  location /prod-api {            proxy_pass http://localhost:5000;               proxy_redirect off;     } }"  > /etc/nginx/sites-available/default   
rm  /usr/share/nginx/html/index.html 
sed -i '1d' /etc/nginx/nginx.conf 
echo "user root;" >> /etc/nginx/nginx.conf 

echo "正在启动服务..." 
export FLASK_APP=meta_info 
export LC_ALL=en_US.UTF-8 
service nginx restart 
nohup waitress-serve --listen=127.0.0.1:5000  --call 'meta_info:create_app' > /root/backend/log/flask_run.log & 
echo "启动完成~"

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
- Vue Cli
  - Vue脚手架，让我们可以方便地，组件式地开发。

- Vuex 
  - Vuex 是一个专为 Vue.js 应用程序开发的状态管理模式 + 库。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。我们借助它来储存网页中要用到的**所有的数据**。

- Babel
  - Babel是一个十分受欢迎的JS代码编译工具，以便我们在旧版和最新版的浏览器中使用新特性（如JSX、箭头函数、promise等）

- Scss
  - Scss是一个CSS预处理器，可以理解为是sass的升级版，相比sass，scss语言更兼容，不必使用严格的缩进。CSS预处理器定义了一种新的语言，其基本思想是，用一种专门的编程语言，为 CSS 增加了一些编程的特性，将 CSS作为目标生成文件，然后开发者就只要使用这种语言进行编码工作。让你的 CSS 更加简洁、适应性更强、可读性更佳，更易于代码的维护。我们借助它来编写CSS代码。

- Vue-router 
  - vue-router是Vue官方插件，我们借助它实现网页页面跳转。

- Axios
  - Axios 是一个基于 promise 网络请求库，是Vue.js团队推荐的优秀的，用于向服务器发送请求的库。

- json-server
  - json-server是一个简单的后端服务器，能够快速地创建简单的本地API，用于前端功能测试

- PostCSS
  - PostCSS可以自动为CSS代码添加前缀，使得代码能够兼容大部分浏览器

- Jest
  - Jest是Facebook设计的测试工具，它带有一个缓存系统，运行速度快，且由一个很好用的快照功能，可以帮助我们检测退化乃至更多问题。

- Mixin
  - mixin是可应用于其他定义对象的组件定义对象，它编写起来十分简单，就和普通的组件定义完全一样，它能很好地提高不同组件代码的重用性

- Vxe-table
  - Vxe-table是一个基于 [vue](https://www.npmjs.com/package/vue) 的 PC 端表格组件，支持增删改查、虚拟列表、虚拟树、懒加载、快捷菜单、数据校验、打印导出、表单渲染、数据分页、弹窗、自定义模板、渲染器、贼灵活的配置项等...

### 注意事项

- 各个组件之间需要共享的资源**一定要用vuex访存**，即使用store文件夹下的Index.js中定义的store来存储，写getter方法来读取，写actions方法来修改，不会用vuex的看一下[手把手教你使用Vuex，猴子都能看懂的教程 - 掘金 (juejin.cn)](https://juejin.cn/post/6928468842377117709)，各个组件内部使用的资源**建议**用vuex访存

- mixin非必须，鉴于项目很小，可以先忽略

- npm run serve开启的网页支持热重载，主要是通过以下几种方式，来显著加快开发速度：

  - 保留在完全重新加载页面期间丢失的应用程序状态。
  - 只更新变更内容，以节省宝贵的开发时间。
  - 在源代码中 CSS/JS 产生修改时，会立刻在浏览器中进行更新，这几乎相当于在浏览器 devtools 直接更改样式。
