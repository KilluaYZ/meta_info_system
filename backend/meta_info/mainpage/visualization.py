'''
该文件是主页面可视化展示的后端逻辑
'''
from flask import request
import os
import sys
import inspect
from flask import Blueprint
# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils.buildResponse import build_response,build_success_response,build_error_response,build_404_response
from utils.check import *
import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

vis = Blueprint('vis', __name__)

@vis.route('/getHotTags', methods=['POST','GET'])
def getHotTags():
    if(request.method=='POST'):
        try:
            data = request.json
            if('startDate' not in data or 'endDate' not in data):
                raise Exception('前端数据不正确！startDate或endDate缺失')
            conn, cursor = pooldb.get_conn()
            cursor.execute('select tagName,count(*) from posts, posts_tags where postTime between %s and %s and posts.postID=posts_tags.postID group by tagName order by count(*) desc',(data['startDate'],data['endDate']))
            rows = cursor.fetchall()
            for row in rows:
                if(not isinstance(row['createTime'],str)):
                    row['createTime']=row['createTime'].strftime('%Y-%m-%d')

            pooldb.close_conn(conn,cursor)
            return build_success_response(rows,len(rows))

        except Exception as e:
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
            print(e)
            pooldb.close_conn(conn,cursor)
            return build_error_response()

    elif(request.method=='GET'):
        #查找最热门的5个tag
        try:
            rows = pooldb.read('select * from tag order by createTime desc limit 5')
            for row in rows:
                if(not isinstance(row['createTime'],str)):
                    row['createTime']=row['createTime'].strftime('%Y-%m-%d')
            return build_success_response(rows,len(rows))

        except Exception as e:
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back))
            print(e)
            return build_error_response()
    else:
        return build_404_response()
        
@vis.route('/getNewTags', methods=['GET'])
def getNewTags():
    #查找最新的5个tag
    try:
        rows = pooldb.read('select * from tag order by createTime desc limit 5')
        for row in rows:
            if(not isinstance(row['createTime'],str)):
                row['createTime']=row['createTime'].strftime('%Y-%m-%d')
            
        return build_success_response(rows,len(rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


@vis.route('/getHotPosts', methods=['GET'])
def getHotPosts():
    #查找最热门的5个post
    try:
        rows = pooldb.read('select * from posts order by  postPopularity desc limit 5')
        for row in rows:
            if(not isinstance(row['postTime'],str)):
                row['postTime']=row['postTime'].strftime('%Y-%m-%d')

        return build_success_response(rows,len(rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back))
        print(e)
        return build_error_response()

@vis.route('/getNewPosts', methods=['GET'])
def getNewPosts():
    #查找最新的5个post
    try:
        rows = pooldb.read('select * from posts order by postTime desc limit 5')
        for row in rows:
            if(not isinstance(row['postTime'],str)):
                row['postTime']=row['postTime'].strftime('%Y-%m-%d')
        return build_success_response(rows,len(rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
