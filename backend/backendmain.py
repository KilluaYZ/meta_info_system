# Filename : backendmain.py
# Author by : Qinliang Xue
# Date : 2022-11-14

from flask import Flask
from flask import request
from flask_cors import CORS # 跨域

from bptest.view import bp # 引入其他蓝图
from dbtest.showdata10 import db # 引入其他蓝图
import os
import sys

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.model_test import modelfunction

app = Flask(__name__)
CORS(app)
# 注册路由
app.register_blueprint(bp,url_prefix='/bp')
app.register_blueprint(db,url_prefix='/db')

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/req', methods=['GET', 'POST'])
def req():
    if request.method == 'POST':
        return 'POST'
    else:
        return 'GET'

@app.route('/testmodel', methods=['GET'])
def testmodel():
    return modelfunction()

if __name__ == '__main__':
    app.run(debug = True)