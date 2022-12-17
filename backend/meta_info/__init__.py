from flask import Flask
from flask import request
from flask_cors import CORS # 跨域
# from dbtest.showdata10 import db # 引入其他蓝图
import os
import sys

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
    from . import db
    db.init_app(app)

    #在应用中注册蓝图
    # app.register_blueprint(db,url_prefix='/db')
    
    return app