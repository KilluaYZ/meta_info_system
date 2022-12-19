from ast import keyword
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
from manage.tagManage import query_sql

conndb = Conndb(cursor_mode='dict')
posts = Blueprint('posts', __name__)

#帖子

#传入postid，返回这个帖子所有的tag的全部信息
def query_post_all_keywords(postid)->list:
    try:
        conndb.cursor.execute('select * from posts_keywords where postid=%d',(postid))
        #取出帖子所有的关键词
        rows = conndb.cursor.fetchall()
        #将字典的keyword作映射
        return list(map(lambda x : x['keyword'],rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()

#输入postid，返回该帖子的所有的tag的全部信息
def query_post_all_tags(postid)->list:
    try:
        conndb.cursor.execute('select * from posts_tags where postid=%d',(postid))
        #取出帖子所有的关键词
        rows = conndb.cursor.fetchall()
        #将字典的tagName作映射
        return list(map(lambda tagname : query_sql({"tagName":tagname})[0],list(map(lambda x : x['tagName'],rows))))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()

def query_post_sql(queryParam):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    query_sql = 'select * from posts,posts_keywords,posts_tags '
    #限制条件查询的属性
    query_constrain_attr = ['postTitle','postID','postKeywords','postTag','postTime']
    #condition_sql_list是存放queryParam中的查询条件构造出的sql语句的列表
    condition_sql_list = []
    #condition_sql_val_list存放sql对应的值，添加这个是为了参数化查询，防sql注入
    condition_sql_val_list = []

    sort_sql = ''
    #形成参数条件列表
    for item in queryParam.items():
        key = item[0]
        val = item[1]
        if(key in query_constrain_attr):
            if(key == 'postKeywords'):
                condition_sql_list.append(' posts.postid=posts_keywords.postid and keyword=%s ')
                condition_sql_val_list.append(val)
            elif(key == 'postTag'):
                condition_sql_list.append(' posts.postid=posts_tags.postid and tagName=%s ')
                condition_sql_val_list.append(val)
            elif(key == 'postTime'):
                condition_sql_list.append(' postTime between %s and %s ')
                condition_sql_val_list.append(val[0])
                condition_sql_val_list.append(val[1])
            else:
                condition_sql_list.append(' posts.'+key+'=%s ')
                condition_sql_val_list.append(val)
            
    if('sort' in queryParam):
        sort_sql = 'order by %s ' %(queryParam['sort']['sortAttr'])
        if(queryParam['sort']['mode'] == 'asc'):
            sort_sql+='ASC'
        elif(queryParam['sort']['mode'] == 'desc'):
            sort_sql+='DESC'
        else:
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
            print('postManage.py::query_post_sql sort错误')
            raise Exception()
    
    #构建查询sql语句
    if(len(condition_sql_list)):
        query_sql += ' where '
        for i in range(len(condition_sql_list)-1):
            query_sql += ' %s AND' % (condition_sql_list[i])
        query_sql += (" "+condition_sql_list[-1] + " ")
    query_sql += sort_sql
    print('[DEBUG] query_sql='+query_sql)

    try:
        #防止SQL注入，选用参数化查询
        conndb.cursor.execute(query_sql,tuple(condition_sql_val_list))
        rows = conndb.cursor.fetchall()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()
    
    return rows



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
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        conndb.db.rollback()
        raise Exception()

def add_post_tag_sql(postid,tagName):
    sql = 'insert into posts_tags(postID,tagName) values(%d,%s)'
    try:
        conndb.cursor.execute(sql,(postid,tagName))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

def del_post_tag_sql(postid,tagName):
    sql = 'delete from posts_tags where postid=%d and tagname=%s'
    try:
        conndb.cursor.execute(sql,(postid,tagName))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

def add_post_keywords_sql(postid,keyword):
    sql = 'insert into posts_keywords(postID,keyword) values(%d,%s)'
    try:
        conndb.cursor.execute(sql,(postid,keyword))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

def del_post_keywords_sql(postid,keyword):
    sql = 'delete from posts_keywords where postid=%d and keyword=%s'
    try:
        conndb.cursor.execute(sql,(postid,keyword))
        conndb.db.commit()
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

# 传入postid和新的keyword列表，分析差异，进行更新
def update_post_keywords(postid,new_post_keywords_list):
    del_keywords_list = []
    add_keywords_list = []
    try:
        cur_keywords = query_post_all_keywords(postid)
        for item in new_post_keywords_list:
            if item not in cur_keywords:
                #新表中的数据不在原表中，则添加
                add_keywords_list.append(item)
        for item in cur_keywords:
            if item not in new_post_keywords_list:
                #新表中没有当前表中的数据，删除
                del_keywords_list.append(item)
        for item in add_keywords_list:
            add_post_keywords_sql(postid,item)
        for item in del_keywords_list:
            del_post_keywords_sql(postid,item)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

# 传入postid和新的tagName列表，分析差异，进行更新
def update_post_tag(postid,new_post_tag_list):
    #下面两个list储存的都是tagName
    del_tag_list = []
    add_tag_list = []
    try:
        cur_keywords = list(map(lambda x : x['tagName'],query_post_all_tags(postid)))
        for item in new_post_tag_list:
            if item not in cur_keywords:
                #新表中的数据不在原表中，则添加
                add_tag_list.append(item)
        for item in cur_keywords:
            if item not in new_post_tag_list:
                #新表中没有当前表中的数据，删除
                del_tag_list.append(item)
        for item in add_tag_list:
            add_post_tag_sql(postid,item)
        for item in del_tag_list:
            del_post_tag_sql(postid,item)
            
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conndb.db.rollback()
        raise Exception()

# 传入postid和新的post数据，分析差异，进行更新
def update_post_sql(postid, new_post_data):
    #防止sql注入
    try:
        update_sql = 'UPDATE posts SET '
        sql_list = []
        val_list = []
        for item in new_post_data.items():
            sql_list.append(' '+item[0]+'=%s ' )
            val_list.append(item[1])
        for i in range(len(sql_list)-1):
            update_sql += (' '+sql_list[i]+', ')
        update_sql += (' ' + sql_list[-1] +' where postid=%s')
        val_list.append(postid)

        conndb.cursor.execute(update_sql,tuple(val_list))
        #提交事务
        conndb.db.commit()

    except Exception as e:
        #出现错误回滚
        conndb.db.rollback()
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()

#传入postid，删除对应的post，并级联删除帖子关键词表和帖子标签表上的所有信息
#级联删除部分由DBMS完成，应用层只需要删除就行
def del_post_sql(postid):
    try:
        del_sql = 'DELETE FROM posts WHERE postid=%s'
        conndb.cursor.execute(del_sql,(postid))
        #提交事务
        conndb.db.commit()
        return build_success_response()

    except Exception as e:
        #出现错误回滚
        conndb.db.rollback()
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()


#post查询返回构造函数，输入postid列表，就可以返回该列表下所有post的全部数据
def build_post_response_data(postid_list:list):
    res = []
    for postid in postid_list:
        post_data = query_post_sql({"postID":postid})
        tag_data = query_post_all_tags(postid)
        keyword_data = query_post_all_keywords(postid)
        post_data['postTag'] = tag_data
        post_data['postKeywords'] = keyword_data
        res.append(post_data)
    return res


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

#查询帖子
@posts.route('/get', methods=['POST'])    
def getPost():
    try:
        queryParam = request.json
        #正确性检验
        if('sort' in queryParam):
            #sort中必须要包含sortAttr和mode
            if ('sortAttr' not in queryParam['sort'] or 'mode' not in queryParam['sort']):
                print('sort 正确性检验失败')
                raise Exception('sort 正确性检验失败')

        data = query_post_sql(queryParam)
        data_length = len(data)
        
        # 返回某一页的数据
        if('pageNum' in queryParam and 'pageSize' in queryParam):
            if(not is_number(queryParam['pageNum']) or not is_number(queryParam['pageSize'])):
                # pageNum和pageSize必须为数字
                print('pageNum和pageSize 正确性检验失败')
                raise Exception('pageNum和pageSize 正确性检验失败')
            pageSize = queryParam['pageSize']
            pageNum = queryParam['pageNum']
            # print("pageSize=",pageSize)
            # print("pageNum=",pageNum)
            data = data[(pageNum-1)*pageSize:pageNum*pageSize]
            # print("data cur len=",len(data))
        
        return build_success_response(data,data_length)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response() 

