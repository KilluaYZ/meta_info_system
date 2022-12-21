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
from utils.buildResponse import *
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

#查找最热门的前10个标签，找到其一级标签，并根据一级标签制作词云图保存到本地static/img下并返回给前端对应的url
#查询某个标签的一级标签可以使用现有函数getFrontTagTree
from manage.tagManage import get_front_tag_tree_sql
#该函数作用是传入一个tagName，返回该tagName的前向标签继承关系
#例如：SQL->SQL查询->嵌套子查询
#get_front_tag_tree_sql('SQL') -> [{"tagName":"SQL",...}]
#get_front_tag_tree_sql('SQL查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...}]
#get_front_tag_tree_sql('嵌套子查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...},{"tagName":"嵌套子查询",...}]

#热门标签词云图
@vis.route('/getWordCloud', methods=['GET'])
def getWordCloud():
    
    data = {
        "url":"localhost:5000/static/img/"+"图片名"
    }
    return build_success_response(data)