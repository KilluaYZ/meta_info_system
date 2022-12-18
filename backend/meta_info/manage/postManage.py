from flask import Flask
from flask import request
from flask import Blueprint
import json
import os
import sys
import inspect

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# sys.path.append("..")

from manage.buildResponse import build_response,build_success_response,build_error_response
from utils.check import is_number
from database.connect import Conndb
conndb = Conndb(cursor_mode='dict')
posts = Blueprint('posts', __name__)

#帖子
def add_post_sql(data:dict):
    #假设data中的属性都是确定无误的
    sql = 'insert into posts ('
    sql2 = ' values ('
    val_list = []
    data_key_val = data.items()
    for i in range(len(data_key_val)-1):
        val_list.append(data_key_val[i][1])
        sql += " %s ," % (data_key_val[i][0])
        sql2 += "%s ,"

    val_list.append(data_key_val[-1][1])
    sql += "%s)"
    sql2 += "%s)"
    sql += sql2
    try:
        conndb.cursor.execute(sql,tuple(val_list))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"add_sql::数据库sql执行错误")
        print(e)
        conndb.db.rollback()

def add_post_tag_sql(postid,tagName):
    sql = 'insert into posts_tags(postID,tagName) values(%d,%s)'
    try:
        conndb.cursor.execute(sql,(postid,tagName))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()

def del_post_tag_sql(postid,tagName):
    sql = 'delete from posts_tags where postid=%d and tagname=%s'
    try:
        conndb.cursor.execute(sql,(postid,tagName))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()

def add_post_keywords_sql(postid,keyword):
    sql = 'insert into posts_keywords(postID,keyword) values(%d,%s)'
    try:
        conndb.cursor.execute(sql,(postid,keyword))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()

def del_post_keywords_sql(postid,keyword):
    sql = 'delete from posts_keywords where postid=%d and keyword=%s'
    try:
        conndb.cursor.execute(sql,(postid,keyword))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()

def update_post_keywords(postid,new_post_keywords_list):
    pass

def update_post_tag(postid,new_post_tag_list):
    pass

def update_post_sql(postid, new_post_data):
    pass

def del_post_sql(postid):
    pass

def query_post_sql(queryParam):
    pass

#增加帖子
@posts.route('/add', methods=['POST'])
def addPost():
    data = request.json
    post_add_data = {}
    post_tag_list = []
    post_keywords_list = []
    for item in data.items():
        if(item[0] in ["postTitle",'postContent','postTime','postAnswer','postPopularity','remark']):
            post_add_data[item[0]]=item[1]

    if('postKeywords' in data):
        post_keywords_list = data['postKeywords']
    
    if('postTag' in data):
        for item in data['postTag']:
            post_tag_list.append(item['tagName'])
            
    try:
        add_post_sql(post_add_data)
        postid = query_post_sql()
        for item in post_tag_list:
            add_post_tag_sql(postid,item)
        for item in post_keywords_list:
            add_post_keywords_sql(postid,item)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


#修改帖子
@posts.route('/update', methods=['POST'])
def updatePost():
    data = request.json
    post_update_data = {}
    post_tag_list = []
    post_keywords_list = []
    postid = data['postID']
    for item in data.items():
        if(item[0] in ["postTitle",'postContent','postTime','postAnswer','postPopularity','remark']):
            post_update_data[item[0]]=item[1]

    if('postKeywords' in data):
        post_keywords_list = data['postKeywords']
    
    if('postTag' in data):
        for item in data['postTag']:
            post_tag_list.append(item['tagName'])
            
    try:
        update_post_sql(postid, post_update_data)
        update_post_tag(postid,post_tag_list)
        update_post_keywords(postid,post_keywords_list)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()



#删除帖子
@posts.route('/del', methods=['POST'])
def delPost():
    postid = request.json.get('postID')        
    try:
        del_post_sql(postid)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()       

