'''
该文件是主页面可视化展示的后端逻辑
'''
from flask import request,send_file
from wordcloud import WordCloud
import os
from flask import make_response
import sys
import inspect
from urllib.parse import  quote
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
            cursor.execute('select tagName,count(*) as frequency from posts, posts_tags where postTime between %s and %s and posts.postID=posts_tags.postID group by tagName order by count(*) desc',(data['startDate'],data['endDate']))
            rows = cursor.fetchall()
            
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
            rows = pooldb.read('select * from tag order by tagPopularity desc limit 5')
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

import io   
@vis.route('/getWordCloud', methods=['GET'])
def getHotPosts_wordcloud():
    #查找最热门的前10个标签，找到其一级标签，并根据一级标签制作词云图保存到本地static/img下并返回给前端对应的url
    try:
        rows = pooldb.read('select tagName,tagPopularity from tag order by tagPopularity DESC limit 10')
        first_tag_list = []
        for row in rows:
            # print(f"[DEBUG] tagName = {row['tagName']}")
            tmp=get_front_tag_tree_sql(row['tagName'])
            for _ in range(int(row['tagPopularity'])):
                first_tag_list.append(tmp[0]['tagName'])
            first_tag_list.append(tmp[0]['tagName'])
        word_text =  ' '.join(first_tag_list)    
        wc = WordCloud(
            width=400,                  # 设置宽为400px
            height=300,                 # 设置高为300px
            background_color='white',    # 设置背景颜色为白色
            max_font_size=100,           # 设置最大的字体大小，所有词都不会超过100px
            min_font_size=10,            # 设置最小的字体大小，所有词都不会超过10px
            max_words=10,                # 设置最大的单词个数
            scale=2,                     # 扩大两倍
            font_path='/static/font/msyh.ttc'
        )
        # print("[DEBUG] first_tag_list=",first_tag_list)
        # 根据文本数据生成词云
        wc.generate(word_text)
        # 保存词云文件
        img_url = 'static/img/wordcloud_img.jpg'
        wc.to_file(img_url)
        
        # import base64
        # img_stream=""
        # with open(img_url,'rb') as img_f:
        #     img_stream = img_f.read()

        # response = make_response(img_stream)
        # utf_filename = quote(img_url.encode("utf-8"))
        # response.headers["Content-Disposition"] = "attachment;filename*=utf-8''{}".format(utf_filename)
        # response.headers["Content-Type"] = "application/octet-stream; charset=UTF-8"
        return send_file(img_url)
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back))
        print(e)
        return build_error_response()
        


#查询某个标签的一级标签可以使用现有函数getFrontTagTree
from manage.tagManage import get_front_tag_tree_sql
#该函数作用是传入一个tagName，返回该tagName的前向标签继承关系
#例如：SQL->SQL查询->嵌套子查询
#get_front_tag_tree_sql('SQL') -> [{"tagName":"SQL",...}]
#get_front_tag_tree_sql('SQL查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...}]
#get_front_tag_tree_sql('嵌套子查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...},{"tagName":"嵌套子查询",...}]

#热门标签词云图
# @vis.route('/getWordCloud', methods=['GET'])
def getWordCloud():
    
    data = {
        "url":"localhost:5000/static/img/"+"图片名"
    }
    return build_success_response(data)