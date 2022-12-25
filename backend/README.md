# Backend
基于flask框架搭建的后端服务器

demo演示[MOOC知识点标签管理系统](http://43.138.62.72:7878)

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
export FLASK_APP=meta_info
export FLASK_ENV=development
export MYSQL_HOST= <mysql服务器地址，默认为127.0.0.1>
export MYSQL_PORT= <mysql服务器端口，默认为3306>
export MYSQL_USER= <mysql服务器用户，默认为root>
export MYSQL_PASSWORD= <mysql服务器密码，默认为123456>
export MYSQL_DATABASE= <mysql服务器数据库，默认为meta_info_db>
cd .../backend/ #转到backend目录下
flask run
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

