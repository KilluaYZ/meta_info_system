from distutils.log import debug
from flask import Flask
from flask import request
from flask_cors import CORS # 跨域
# from dbtest.showdata10 import db # 引入其他蓝图
import os
import sys


# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# sys.path.append(".")
# sys.path.append("..")

from database.init_db import init_db
from manage.tagManage import tag
from manage.postManage import posts
from mainpage.visualization import vis
from auth.auth import auth
from monitor.monitor import monitor


#创建flask app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_HOST='127.0.0.1',
        DATABASE_PORT='3306',
        DATABASE_USER='root',
        DATABASE_PASSWD='123456'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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

    #在应用中注册蓝图
    # app.register_blueprint(db,url_prefix='/db')
    app.register_blueprint(tag,url_prefix='/tag')
    app.register_blueprint(posts,url_prefix='/post')
    app.register_blueprint(vis,url_prefix='/vis')
    app.register_blueprint(auth,url_prefix='/auth')
    app.register_blueprint(monitor,url_prefix='/monitor')

    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)
