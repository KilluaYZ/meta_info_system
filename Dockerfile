FROM ubuntu
LABEL org.meta_info.version="1.0" org.meta_info.name="Meta Info Image" org.meta_info.vendor="ubuntu22.04" org.meta_info.license="MIT" org.meta_info.build-date="20221225"
RUN echo "开始部署...\n" && echo "开始安装依赖...\n" && apt update && apt install -y unzip nginx  python3 python3-pip wget && mkdir -p ~/.pip && touch ~/.pip/pip.conf && echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf && cat ~/.pip/pip.conf  && pip install waitress && echo "依赖安装成功\n"

RUN echo "正在从gitee上下载并安装软件release最新版本...\n" && mkdir -p /root/frontend && mkdir -p /root/backend && mkdir -p /root/backend/log && cd /root/frontend && wget  https://gitee.com/killuayz/meta_info_system/releases/download/v1.0/meta_info_frontend.tar.gz && tar zxvf *.tar.gz && chmod -R 777 /root/frontend && cd /root/backend && wget https://gitee.com/killuayz/meta_info_system/releases/download/v1.0/meta_info-1.0.0-py3-none-any.whl && pip install *.whl && echo "安装完成\n"

RUN  echo "正在进行部署配置..." && echo "server {        listen 80 default_server;       listen [::]:80 default_server;  server_name localhost;  root /root/frontend;    index index.html; location / {try_files \$uri \$uri/ @router; } location @router { rewrite ^.*$ /index.html last; }  location /prod-api {            proxy_pass http://localhost:5000;               proxy_redirect off;     } }"  > /etc/nginx/sites-available/default  && rm  /usr/share/nginx/html/index.html && sed -i '1d' /etc/nginx/nginx.conf && echo "user root;" >> /etc/nginx/nginx.conf 

CMD echo "正在启动服务..." && export FLASK_APP=meta_info && export LC_ALL=en_US.UTF-8 && service nginx restart && nohup waitress-serve --listen=127.0.0.1:5000  --call 'meta_info:create_app' > /root/backend/log/flask_run.log & && echo "启动完成~" && top