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
from manage.buildResponse import build_response,build_success_response,build_error_response
from utils.check import *
import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

vis = Blueprint('vis', __name__)

@vis.route('/getHotTags', methods=['POST'])
def getHotTags():
    try:
        data = request.json
        if('startDate' not in data or 'endDate' not in data):
            raise Exception('前端数据不正确！startDate或endDate缺失')
        conn, cursor = pooldb.get_conn()
        cursor.execute('select tagName,count(*) from posts, posts_tags where postTime between %s and %s and posts.postID=posts_tags.postID group by tagName order by count(*) desc',(data['startDate'],data['endDate']))
        rows = cursor.fetchall()
        pooldb.close_conn(conn,cursor)
        return build_success_response(rows,len(rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        pooldb.close_conn(conn,cursor)
        return build_error_response()
    

