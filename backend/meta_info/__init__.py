from distutils.log import debug
from flask import Flask
from flask import request
from flask_cors import CORS # 跨域
# from dbtest.showdata10 import db # 引入其他蓝图
import os
import sys

from sqlalchemy import func
from apscheduler.schedulers.background import BackgroundScheduler

from meta_info.database.init_db import init_db
from meta_info.manage.tagManage import tag
from meta_info.manage.postManage import posts
from meta_info.mainpage.visualization import vis
from meta_info.auth.auth import auth
from meta_info.monitor.monitor import monitor
from meta_info.manage.userManage import user

from meta_info.manage.tagManage import tag as prod_tag
from meta_info.manage.postManage import posts as prod_posts
from meta_info.mainpage.visualization import vis as prod_vis
from meta_info.auth.auth import auth as prod_auth
from meta_info.monitor.monitor import monitor as prod_monitor
from meta_info.manage.userManage import user as prod_user

#创建flask app
def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #在应用中注册init_db
    @app.cli.command('init-db')
    def init_db_command():
        '''删除现有的所有数据，并新建关系表'''
        init_db()
        print("已初始化数据库")

   
    FLASK_ENV =  os.environ.get('FLASK_ENV')
    print('FLASK_ENV = ',FLASK_ENV)
    #在开发环境中注册蓝图
    if FLASK_ENV == 'development':
        print('当前服务器在开发环境下运行')
        app.register_blueprint(tag,url_prefix='/tag')
        app.register_blueprint(posts,url_prefix='/post')
        app.register_blueprint(vis,url_prefix='/vis')
        app.register_blueprint(auth,url_prefix='/auth')
        app.register_blueprint(monitor,url_prefix='/monitor')
        app.register_blueprint(user,url_prefix='/user')
    #生产环境蓝图注册
    elif FLASK_ENV is None or FLASK_ENV == 'production':
        print('当前服务器在生产环境下运行')
        app.register_blueprint(prod_tag,url_prefix='/prod-api/tag')
        app.register_blueprint(prod_posts,url_prefix='/prod-api/post')
        app.register_blueprint(prod_vis,url_prefix='/prod-api/vis')
        app.register_blueprint(prod_auth,url_prefix='/prod-api/auth')
        app.register_blueprint(prod_monitor,url_prefix='/prod-api/monitor')
        app.register_blueprint(prod_user,url_prefix='/prod-api/user')

    #配置定时任务
    from meta_info.manage.userManage import checkSessionsAvailability
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=checkSessionsAvailability,
                    id='checkSessionsAvailability',
                    trigger='interval',
                    seconds=1800,
                    replace_existing=True
    )
    #启动任务列表
    scheduler.start()
    return app
