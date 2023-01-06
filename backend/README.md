# Backend
基于flask框架搭建的后端服务器

## 依赖

```
install_requires=[
        'flask',
        'PyMySql',
        'flask_cors',
        'sqlalchemy',
        'DButils',
        'wordcloud',
        'psutil',
        'flask_apscheduler'
    ]
```

## 部署方式

### 开发环境

```bash
#pip安装相应依赖
#clone项目
git clone https://gitee.com/killuayz/meta_info_system_frontend.git
#进入backend目录
cd meta_info_system/backend
#运行
export FLASK_APP=meta_info
export FLASK_ENV=development
export MYSQL_HOST= <mysql服务器地址，默认为127.0.0.1>
export MYSQL_PORT= <mysql服务器端口，默认为3306>
export MYSQL_USER= <mysql服务器用户，默认为root>
export MYSQL_PASSWORD= <mysql服务器密码，默认为123456>
export MYSQL_DATABASE= <mysql服务器数据库，默认为meta_info_db>
export SERVER_IP= <后端服务器ip用于显示词云图，默认为127.0.0.1:5000>

#如果是第一次运行，还需要运行以下命令，初始化数据库，可能需要开启mysql数据库的local_infile,具体见MySQL ERROR 3948
flask init-db

flask run
```



## 目录结构

- meta_info
  - auth
    - auth.py	用户登录注册，权限管理
    - routerdata.py   不同类型用户的菜单栏数据
  - database
    - connectPool.py	与MySQL数据库交互
    - data1.txt    初始化帖子数据
    - init.sql       初始化sql语句，定义了关系，触发器，进行了插入等操作
    - init_db.py   flask自定义语句，用于初始化数据库
  - mainpage
    - visualization.py    可视化
  - manage
    - postManage.py    帖子管理
    - tagManage.py    标签管理
    - userManage.py    用户管理
  - monitor
    - monitor.py    服务器监控
  - static   图片、css等
  - utils
  - \_\_init\_\_.py    生成flask app
