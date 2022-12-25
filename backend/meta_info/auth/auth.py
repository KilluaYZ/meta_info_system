from flask import request
from flask import Blueprint
import os
import sys
import inspect

from werkzeug.security import check_password_hash, generate_password_hash

from meta_info.utils.buildResponse import *
from meta_info.utils.check import is_number
from meta_info.manage.tagManage import query_sql,update_sql
from meta_info.auth.routerdata import *
from meta_info.utils.auth import build_token,get_user_by_token,build_session,update_token_visit_time,checkTokens
# conndb = Conndb(cursor_mode='dict')
auth = Blueprint('auth', __name__)

import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb
# tokenList = []

@auth.route('/getRouters', methods=['GET'])
def getRouters():
    token = request.cookies.get('Admin-Token')
    if token is None:
        return build_error_response()
    user = get_user_by_token(token)
    if not user:
        return build_error_response(msg="会话未建立，请重新登录")
    
    if user['roles'] == 'admin':
        return build_success_response(adminRouterData)
    elif user['roles'] == 'tagger':
        return build_success_response(taggerRouterData)
    elif user['roles'] == 'common':
        return build_success_response(commonRouterData)

    return build_success_response(commonRouterData)

def authorize_username_password(username,password):
    try:
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
        return user
    except Exception as e:
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        return None

def register_user_sql(data):
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute('insert into user(username,nickname,password,roles) values(%s,%s,%s,%s)',(data['username'],data['username'],generate_password_hash(data['password']),'common'))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)

#检查username是不是唯一的，如果是则返回True，否则返回False
def checkUsernameIsUnique(username):
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute('select * from user where username=%s',(username))
        rows = cursor.fetchall()
        pooldb.close_conn(conn,cursor)
        if(len(rows) == 0):
            return True
        return False
            
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
 
@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if('username' not in data or 'password' not in data):
            raise Exception('前端数据错误！缺少username或password')
        if not checkUsernameIsUnique(data['username']):
            return build_error_response(msg='该用户名已存在')
        register_user_sql(data)        
        return build_success_response()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response(msg='注册失败')

#收到用户名密码，返回会话对应的toKen
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if('username' not in data or 'password' not in data):
            raise Exception('前端数据不正确，无用户名或密码')
        username = data['username']
        
        password = data['password']
        user = authorize_username_password(username,password)
        if user is None:
            return build_error_response(msg='用户名或密码错误')
        
        token = build_session(user['uid'])
        print('[DEBUG] get token, token = ',token)
        # tokenList.append(token)
        return build_raw_response({"msg":'操作成功',"token":token})
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response(msg='登录失败')    
    

#获取用户的详细信息
@auth.route('/getInfo', methods=['GET'])
def getInfo():
    try:
        token = request.cookies.get('Admin-Token')
        if token is None:
            raise Exception('token不存在，无法查询')

        state = checkTokens(token,'common')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')
        
        user = get_user_by_token(token)
        # print(2)
        if not isinstance(user['createTime'],str):
            user['createTime'] = user['createTime'].strftime('%Y-%m-%d %H:%M:%S')
        response = {
            "msg": "操作成功",
            "roles": [user['roles']],
            "user":{
                "userId": user['uid'],
                "userName": user['username'],
                "nickName": user['nickname'],
                "email": user['email'],
                "phonenumber": user['phonenumber'],
                "avator":user['avator'],
                "createTime":user['createTime']
            }
        }
        # print(3)
        if user['roles'] == 'admin':
            response['user']['admin']=True
        else:
            response['user']['admin']=False
        
        if user['roles'] == 'admin':
            response['roleGroup'] = '管理员'
        elif user['roles'] == 'tagger':
            response['roleGroup'] = '标记员'
        elif user['roles'] == 'common':
            response['roleGroup'] = '普通用户'
            
        # print(4)
        return build_raw_response(response)
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
        
#退出登录，本质上就是删除与用户建立的对话
@auth.route('/logout', methods=['POST','GET'])
def logout():
    try:
        token = request.cookies.get('Admin-Token')
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

def user_profile_update_user_sql(data):
    try:
        conn, cursor = pooldb.get_conn()
        sql = 'update user set nickname=%s,email=%s,phonenumber=%s where uid=%s'
        cursor.execute(sql,(data['nickName'],data['email'],data['phonenumber'],data['userId']))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        raise Exception('update_ser_sql错误')

@auth.route('/profile', methods=['GET','POST'])
def getprofile():
    try:
        if request.method == 'GET':
            token = request.cookies.get('Admin-Token')
            if token is None:
                raise Exception('token不存在，无法查询')

            state = checkTokens(token,'common')
            if state == 404:
                return build_error_response(400,'会话未建立，请重新登录')
            elif state == 403:
                return build_error_response(403,'您没有该操作的权限，请联系管理员')
            elif state == 500:
                return build_error_response(500,'服务器内部发生错误，请联系管理员')
            
            user = get_user_by_token(token)
            
            if not isinstance(user['createTime'],str):
                user['createTime'] = user['createTime'].strftime('%Y-%m-%d %H:%M:%S')
            response = {
                "msg": "操作成功",
                "roles": [user['roles']],
                "data":{
                    "userId": user['uid'],
                    "userName": user['username'],
                    "nickName": user['nickname'],
                    "email": user['email'],
                    "phonenumber": user['phonenumber'],
                    "avator":user['avator'],
                    "createTime":user['createTime']
                }
            }
           
            if user['roles'] == 'admin':
                response['data']['admin']=True
            else:
                response['data']['admin']=False
            
            if user['roles'] == 'admin':
                response['roleGroup'] = '管理员'
            elif user['roles'] == 'tagger':
                response['roleGroup'] = '标记员'
            elif user['roles'] == 'common':
                response['roleGroup'] = '普通用户'
                
            
            return build_raw_response(response)
        
        elif request.method == 'POST':
            token = request.cookies.get('Admin-Token')
            if token is None:
                raise Exception('token不存在，无法修改信息')

            state = checkTokens(token,'common')
            if state == 404:
                return build_error_response(400,'会话未建立，请重新登录')
            elif state == 403:
                return build_error_response(403,'您没有该操作的权限，请联系管理员')
            elif state == 500:
                return build_error_response(500,'服务器内部发生错误，请联系管理员')

            data = request.json
            user_profile_update_user_sql(data)
            
            return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


def user_profile_update_user_pwd(uid,pwd):
    try:
        sql = 'update user set password=%s where uid=%s'
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(generate_password_hash(pwd),uid))
        conn.commit()
        pooldb.close_conn(conn,cursor)
    except Exception as e:
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        raise Exception(f'用户{uid}密码修改失败')

@auth.route('/profile/updatePwd', methods=['POST'])
def updatePwd():
    try:
        
        data = request.json
        if('oldPassword' not in data or 'newPassword' not in data):
            raise Exception('前端数据错误，不存在oldPassword或newPassword')
        
        
        token = request.cookies.get('Admin-Token')
        if token is None:
            raise Exception('token不存在')
        
        state = checkTokens(token,'common')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        user = get_user_by_token(token)
        
        
        res = authorize_username_password(user['username'],data['oldPassword'])
        if res is None:
            raise Exception('密码不正确')
        
        
        user_profile_update_user_pwd(user['uid'],data['newPassword'])
        
        
        return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()

