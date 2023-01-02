'''
该文件是主页面可视化展示的后端逻辑
'''
from flask import request,send_file,url_for
from wordcloud import WordCloud
import os
from flask import make_response
import sys
import inspect
from urllib.parse import  quote
from flask import Blueprint
from meta_info.utils.buildResponse import *
from meta_info.utils.check import *
from meta_info.utils.fileIO import encode_base64
import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb

vis = Blueprint('vis', __name__)

sys.path.append(r'..')

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

from meta_info.manage.tagManage import get_front_tag_tree_sql
 
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
        cur_path = os.getcwd()
        wc = WordCloud(
            width=400,                  # 设置宽为400px
            height=300,                 # 设置高为300px
            background_color='white',    # 设置背景颜色为白色
            max_font_size=100,           # 设置最大的字体大小，所有词都不会超过100px
            min_font_size=10,            # 设置最小的字体大小，所有词都不会超过10px
            max_words=10,                # 设置最大的单词个数
            scale=2,                     # 扩大两倍
            font_path=cur_path+'\\meta_info\\static\\font\\msyh.ttc'
        )
        # print("[DEBUG] first_tag_list=",first_tag_list)
        # 根据文本数据生成词云
        wc.generate(word_text)
        # 保存词云文件
        # img_url = url_for('static',filename='img/wordcloud_img.jpg')
        img_url = cur_path+'\\meta_info\\static\\img\\wordcloud_img.jpg'
        wc.to_file(img_url)
        return send_file(img_url)
        # res = {
        #     "code":200,
        #     "img":encode_base64(img_url),
        #     "msg":'操作成功'
        # }
        # response = make_response(encode_base64(img_url))
        
        # response.headers['Content-Type']='image/jpg'
        # return response
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back))
        print(e)
        return build_error_response()

@vis.route('/getWordCloudUrl', methods=['GET'])
def getWordCloudUrl():
    try:
        SERVER_IP=os.environ.get('SERVER_IP')
        if SERVER_IP is None:
            SERVER_IP = '127.0.0.1:5000'
        FLASK_ENV = os.environ.get('FLASK_ENV')
        if FLASK_ENV is None or FLASK_ENV == 'production':
            img_url = 'http://'+SERVER_IP+'/prod-api/vis/getWordCloud'
        else:
            img_url = 'http://'+SERVER_IP+'/vis/getWordCloud'

        return build_success_response({"img_url":img_url})

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back))
        print(e)
        return build_error_response()
        