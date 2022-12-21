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
from auth.routerdata import routerData

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
        token = request.headers.get('Authorization')
        if token is None:
            raise Exception('token不存在，无法查询')
        # print(1)
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

def update_user_sql(data):
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
            token = request.headers.get('Authorization')
            if token is None:
                raise Exception('token不存在，无法查询')
            print(1)
            user = get_user_by_token(token)
            print(2)
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
            print(3)
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
                
            print(4)
            return build_raw_response(response)
        
        elif request.method == 'POST':
            token = request.headers.get('Authorization')
            if token is None:
                raise Exception('token不存在，无法修改信息')
            data = request.json
            update_user_sql(data)
            
            return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


def update_user_pwd(uid,pwd):
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
        # print(1)
        data = request.json
        if('oldPassword' not in data or 'newPassword' not in data):
            raise Exception('前端数据错误，不存在oldPassword或newPassword')
        # print(2)
        
        token = request.headers.get('Authorization')
        if token is None:
            raise Exception('token不存在')
        # print(3)
        # print('token=',token)
        user = get_user_by_token(token)
        if user is None:
            raise Exception('会话不存在')
        # print(3.5)
        res = authorize_username_password(user['username'],data['oldPassword'])
        if res is None:
            raise Exception('密码不正确')
        # print(4)
        
        update_user_pwd(user['uid'],data['newPassword'])
        # print(5)
        
        return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
'''
http://vue.ruoyi.vip/prod-api/system/user/list?pageNum=1&pageSize=10&userName=nihao
'''

def query_user_sql(queryParam):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    try:
        conn,cursor = pooldb.get_conn()
        if 'userName' in queryParam:
            cursor.execute('select * from user where username=%s',(queryParam['userName']))
        else:
            cursor.execute('select * from user')
        rows = cursor.fetchall()
        
        return rows
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)        
'''
{
    "tokenId": "f7856a4c-82f9-4f0f-bc42-9fe68dd6f8ee",
    "deptName": "研发部门",
    "userName": "admin",
    "ipaddr": "211.101.240.111",
    "loginLocation": "北京市 北京市",
    "browser": "Chrome 10",
    "os": "Windows 10",
    "loginTime": 1671592539893
}
'''
@auth.route('/user/list', methods=['POST'])
def userList():
    try:
        print(1)
        queryParam = request.json
        if('pageNum' in queryParam and 'pageSize' in queryParam):
            if(not is_number(queryParam['pageNum']) or not is_number(queryParam['pageSize'])):
                # pageNum和pageSize必须为数字
                print('pageNum和pageSize 正确性检验失败')
                raise Exception('pageNum和pageSize 正确性检验失败')
        print(2)
        rows = query_user_sql(queryParam)
        data_length = len(rows)
        print(3)
        #构造前端所需数据
        pageSize = queryParam['pageSize']
        pageNum = queryParam['pageNum']
        rows = rows[(pageNum-1)*pageSize:pageNum*pageSize]
        respon = []
        for row in rows:
            if not isinstance(row['createTime'],str):
                row['createTime'] = row['createTime'].strftime('%Y-%m-%d %H:%M:%S')
            
            respon.append({
                "userName":row['username'],
                'userId':row['uid'],
                "nickName":row['nickname'],
                "phonenumber":row['phonenumber'],
                'createTime':row['createTime']
            })
        print(4)
        return build_success_response(respon,data_length)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)    
        return build_error_response()

def add_user_sql(data):
    try:
        #假设data中的属性都是确定无误的
        sql = 'insert into user ('
        sql2 = ' values ('
        val_list = []
        data_key_val = list(data.items())
        for i in range(len(data_key_val)-1):
            val_list.append(data_key_val[i][1])
            sql += " %s ," % (data_key_val[i][0])
            sql2 += "%s ,"

        val_list.append(data_key_val[-1][1])
        sql += "%s)" % (data_key_val[-1][0])
        sql2 += "%s)"
        sql += sql2
        # print("[DEBUG] insert sql=",sql)
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,tuple(val_list))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            conn.rollback()
            pooldb.close_conn(conn,cursor)
        raise Exception()

@auth.route('/user/add', methods=['POST'])
def addUser():
    try:
        data = request.json
        if('userName' not in data or 'password' not in data
           or 'roles' not in data):
            raise Exception('前端数据不正确，重要数据缺失')
        user_add_data = {}
        # print(1)
        for item in data.items():
            if(item[0] == 'nickName'):
                user_add_data['nickname']=item[1]
            elif(item[0] == 'roles'):
                user_add_data['roles']=item[1]
            elif(item[0] == 'phonenumber'):
                user_add_data['phonenumber']=item[1]
            elif(item[0] == 'email'):
                user_add_data['email']=item[1]
            elif(item[0] == 'userName'):
                user_add_data['username']=item[1]
            elif(item[0] == 'password'):
                user_add_data['password']=generate_password_hash(item[1])
        
        add_user_sql(user_add_data)
        
        return build_success_response()
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
    
def update_user_sql(data):
    #假定data绝对正确
    try:
        sql = 'update user set username=%s, nickname=%s, phonenumber=%s,email=%s, password=%s, roles=%s where uid=%s'
        
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(data['userName'],data['nickName'],
                            data['phonenumber'],data['email'],
                            generate_password_hash(data['password']),data['roles'],data['userId']))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            conn.rollback()
            pooldb.close_conn(conn,cursor)
        raise Exception()
    
@auth.route('/user/update', methods=['POST'])
def userUpdate():
    try:
        data = request.json
        if('userId' not in data):
            raise Exception('前端数据不正确，重要数据缺失')
        
        update_user_sql(data)
        
        return build_success_response()
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
    
@auth.route('/user/get', methods=['POST'])
def getUser():
    try:
        data = request.json
        if('userId' not in data):
            raise Exception('前端数据错误，无userId')
        
        sql = 'select * from user where uid=%s'
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(data['userId']))
        row = cursor.fetchone()
        pooldb.close_conn(conn,cursor)
        if not isinstance(row['createTime'],str):
            row['createTime'] = row['createTime'].strftime('%Y-%m-%d %H:%M:%S')
        row['userName'] = row['username']
        row['nickName'] = row['nickname']
        row['userId'] = row['uid']
        
        return build_success_response(row)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        raise Exception()

@auth.route('/online/list', methods=['GET'])
def getOnlineUser():
    try:
        userName = request.args.get('userName')
        if userName is None:
            rows = pooldb.read('select token,username as userName ,roles,user.uid as userId,user_token.createTime as loginTime from user, user_token where user.uid=user_token.uid')
            
        else:
            conn,cursor = pooldb.get_conn()
            cursor.execute('select token,username as userName ,roles,user.uid as userId,user_token.createTime as loginTime from user, user_token where username = %s and user.uid=user_token.uid',(userName))
            rows = cursor.fetchall()
            pooldb.close_conn(conn,cursor)
            
        length = len(rows)
        for row in rows:
            if not isinstance(row['loginTime'],str):
                row['loginTime']=row['loginTime'].strftime('%Y-%m-%d %H:%M:%S')
                
        return build_success_response(rows,length)
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if not conn is None:
            pooldb.close_conn(conn,cursor)
        return build_error_response()

@auth.route('/online/forceLogout', methods=['POST'])
def forceLogout():    
    try:
        token = request.json.get('token')
        if token is None:
            raise Exception('前端数据错误')

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
