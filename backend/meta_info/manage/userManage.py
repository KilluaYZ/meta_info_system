from flask import request
from flask import Blueprint
import os
import sys
import inspect
import hashlib

from werkzeug.security import check_password_hash, generate_password_hash

from meta_info.utils.buildResponse import *
from meta_info.utils.check import is_number
from meta_info.utils.auth import checkTokens
# conndb = Conndb(cursor_mode='dict')
user = Blueprint('user', __name__)

import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb



'''
http://vue.ruoyi.vip/prod-api/system/user/list?pageNum=1&pageSize=10&userName=nihao
'''

def query_user_sql(queryParam):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    try:
        # print('queryParam : ',queryParam)
        conn,cursor = pooldb.get_conn()
        if 'userName' in queryParam:
            username = '%'+queryParam['userName']+'%'
            # print(username)
            cursor.execute('select * from user where username like %s',(username))
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
@user.route('/list', methods=['POST'])
def userList():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        queryParam = request.json
        if('pageNum' in queryParam and 'pageSize' in queryParam):
            if(not is_number(queryParam['pageNum']) or not is_number(queryParam['pageSize'])):
                # pageNum和pageSize必须为数字
                print('pageNum和pageSize 正确性检验失败')
                raise Exception('pageNum和pageSize 正确性检验失败')
        rows = query_user_sql(queryParam)
        data_length = len(rows)
        # print('debug',rows)
        #构造前端所需数据
        pageSize = queryParam['pageSize']
        pageNum = queryParam['pageNum']
        rows = rows[(pageNum-1)*pageSize:pageNum*pageSize]
        respon = []
        for row in rows:
            if not isinstance(row['createTime'],str):
                row['createTime'] = row['createTime'].strftime('%Y-%m-%d %H:%M:%S')
            if row['roles'] == 'admin':
                respon.append({
                "userName":row['username'],
                'userId':row['uid'],
                "nickName":row['nickname'],
                "phonenumber":row['phonenumber'],
                'createTime':row['createTime'],
                'roles':'管理员'
                })
            elif row['roles'] == 'tagger':
                respon.append({
                "userName":row['username'],
                'userId':row['uid'],
                "nickName":row['nickname'],
                "phonenumber":row['phonenumber'],
                'createTime':row['createTime'],
                'roles':'标记员'
                })
            elif row['roles'] == 'common':
                respon.append({
                "userName":row['username'],
                'userId':row['uid'],
                "nickName":row['nickname'],
                "phonenumber":row['phonenumber'],
                'createTime':row['createTime'],
                'roles':'普通用户'
                })
        
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

@user.route('/add', methods=['POST'])
def addUser():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

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
    
def user_manage_update_user_sql(data):
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
    
@user.route('/update', methods=['POST'])
def userUpdate():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        data = request.json
        if('userId' not in data):
            raise Exception('前端数据不正确，重要数据缺失')
        
        user_manage_update_user_sql(data)
        
        return build_success_response()
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
    
@user.route('/get', methods=['POST'])
def getUser():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

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

@user.route('/online/list', methods=['GET'])
def getOnlineUser():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

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

@user.route('/online/forceLogout', methods=['POST'])
def forceLogout():    
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

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


from meta_info.auth.auth import user_profile_update_user_pwd
@user.route('/resetPwd', methods=['POST'])
def resetPwd():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        data = request.json
        token = request.cookies.get('Admin-Token')
        if token is None:
            raise Exception('token不存在')
        user_profile_update_user_pwd(data['userId'],data['password'])
        
        return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


def user_manage_del_user(uid):
    try:
        conn, cursor = pooldb.get_conn()
        sql = 'delete from user where uid=%s'
        cursor.execute(sql,(uid))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        raise Exception('user_manage_del_user错误')

@user.route('/del', methods=['POST'])
def updatePwd():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'admin')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        data = request.json
        user_manage_del_user(data['userId'])
        
        return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()

#每过一段时间，都会检查一遍user_token表，看createTime和visitTime之差，如果二者之差>=30min，说明该用户已经长时间未进行操作了，应该该会话关闭
def checkSessionsAvailability():
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute('delete from user_token where timestampdiff(minute,visitTime,CURRENT_TIMESTAMP) >= 30')
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
        return build_success_response()
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        if conn is not None:
            pooldb.close_conn(conn,cursor)
        return build_error_response()