from flask import request
from flask import Blueprint
import os
import sys
import inspect
import hashlib

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# sys.path.append("..")
from werkzeug.security import check_password_hash, generate_password_hash

from utils.buildResponse import *
from utils.check import is_number
from database.connect import Conndb
from manage.tagManage import query_sql,update_sql
from static.data import routerData

# conndb = Conndb(cursor_mode='dict')
auth = Blueprint('auth', __name__)

import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb
# tokenList = []

def build_token():
    while True:
        token = hashlib.sha1(os.urandom(24)).hexdigest()
        # rows = pooldb.read('select * from user_token where token="%s"' % token)
        # if rows and len(rows) <= 0:
        #     #找到一个不重复的token
        #     return token
        return token
            
def build_session(uid):
    try:
        token = build_token()
        print('[DEBUG] build token success, token=',token)
        conn,cursor = pooldb.get_conn()
        cursor.execute('insert into user_token(uid, token) values(%s, %s)',(uid,token))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        return token
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        print(e)
        raise Exception('创建会话失败')

def get_user_by_token(token):
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute('select * from user, user_token where token=%s and user_token.uid=user.uid',(token))
        row = cursor.fetchone()
        if row is None or len(row) <= 0:
            raise Exception('会话不存在')
        
        pooldb.close_conn(conn,cursor)
        return row
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        print(e)
        raise Exception('会话不存在')

@auth.route('/getRouters', methods=['GET'])
def getRouters():
    return build_success_response(routerData)

#收到用户名密码，返回会话对应的toKen
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if('username' not in data or 'password' not in data):
            raise Exception('前端数据不正确，无用户名或密码')
        username = data['username']
        
        password = data['password']
        conn,cursor = pooldb.get_conn()
        cursor.execute('select * from user where username=%s',(username))
        user = cursor.fetchone()
        pooldb.close_conn(conn,cursor)
        if user is None:
            raise Exception('用户名不正确')
        
        if not check_password_hash(user['password'],password):
            raise Exception('密码不正确')
        #都正确了，开始创建会话
        print('验证成功')
        token = build_session(user['uid'])
        print('[DEBUG] get token, token = ',token)
        # tokenList.append(token)
        return build_raw_response({"msg":'操作成功',"token":token})
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        return build_error_response(msg='登录失败')    
    

#获取用户的详细信息
@auth.route('/getInfo', methods=['GET'])
def getInfo():
    try:
        token = request.headers.get('Authorization')
        if token is None:
            raise Exception('token不存在，无法查询')
        print(1)
        user = get_user_by_token(token)
        print(2)
        response = {
            "msg": "操作成功",
            "roles": [user['roles']],
            "user":{
                "userId": user['uid'],
                "userName": user['username'],
                "nickName": user['nickname'],
                "email": user['email'],
                "phonenumber": user['phonenumber'],
                "avator":user['avator']
            }
        }
        print(3)
        if user['roles'] == 'admin':
            response['user']['admin']=True
        else:
            response['user']['admin']=False
        print(4)
        return build_raw_response(response)
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
        
#退出登录，本质上就是删除与用户建立的对话
@auth.route('/logout', methods=['POST','GET'])
def logout():
    try:
        token = request.headers.get('Authorization')
        if token is None:
            return build_success_response()
        conn,cursor = pooldb.get_conn()
        cursor.execute('delete from user_token where token=%s',(token))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        return build_success_response()
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        return build_error_response()

@auth.route('/captchaImage', methods=['POST','GET'])
def captchaImage():
    return build_success_response()
