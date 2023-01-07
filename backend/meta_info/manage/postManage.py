from flask import request
from flask import Blueprint
import os
import sys
import inspect

from meta_info.utils.buildResponse import build_response,build_success_response,build_error_response
from meta_info.utils.check import is_number
from meta_info.manage.tagManage import query_sql,update_sql
from meta_info.utils.auth import checkTokens
# conndb = Conndb(cursor_mode='dict')
posts = Blueprint('posts', __name__)

import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb

#帖子

#传入postID，返回这个帖子所有的tag的全部信息
def query_post_all_keywords(postID)->list:
    try:
        # conndb.cursor.execute('select * from posts_keywords where postID=%s',(postID))
        conn,cursor = pooldb.get_conn()
        cursor.execute('select * from posts_keywords where postID=%s',(postID))
        #取出帖子所有的关键词
        # rows = conndb.cursor.fetchall()
        rows = cursor.fetchall()
        pooldb.close_conn(conn,cursor)
        #将字典的keyword作映射
        return list(map(lambda x : x['keyword'],rows))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        pooldb.close_conn(conn,cursor)
        raise Exception()

#输入postID，返回该帖子的所有的tag的全部信息
def query_post_all_tags(postID)->list:
    try:
        # conndb.cursor.execute('select * from posts_tags where postID=%s',(postID))
        conn,cursor = pooldb.get_conn()
        cursor.execute('select * from posts_tags where postID=%s',(postID))
        #取出帖子所有的关键词
        # rows = conndb.cursor.fetchall()
        rows = cursor.fetchall()
        pooldb.close_conn(conn,cursor)
        #将字典的tagName作映射
        return list(map(lambda tagID : query_sql({"tagID":tagID})[0],list(map(lambda x : x['tagID'],rows))))

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        pooldb.close_conn(conn,cursor)
        raise Exception()

def update_post_pop(postid_list):
    try:
        conn,cursor = pooldb.get_conn()
        cursor.executemany('update posts set postPopularity=postPopularity+1 where postID = %s',(postid_list))
            
        conn.commit()
        pooldb.close_conn(conn,cursor)
            
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
            pooldb.close_conn(conn,cursor)
        
        raise Exception('update_post_pop出错')

def query_post_sql(queryParam):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    query_sql = 'select * from posts'
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
                query_sql += ',posts_keywords '
                condition_sql_list.append(' posts.postID=posts_keywords.postID and keyword like %s ')
                condition_sql_val_list.append(f'%{val}%')
            elif(key == 'postTag'):
                query_sql += ',posts_tags,tag '
                condition_sql_list.append(' posts.postID=posts_tags.postID and posts_tags.tagID = tag.tagID and tagName=%s ')
                condition_sql_val_list.append(val)
            elif(key == 'postTime'):
                condition_sql_list.append(' postTime between %s and %s ')
                condition_sql_val_list.append(val[0])
                condition_sql_val_list.append(val[1])
            elif key == 'postTitle':
                condition_sql_list.append(f' posts.postTitle like %s')
                condition_sql_val_list.append(f'%{val}%')
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
    # print('[DEBUG] query_sql='+query_sql)

    try:
        #防止SQL注入，选用参数化查询
        # conndb.cursor.execute(query_sql,tuple(condition_sql_val_list))
        conn,cursor = pooldb.get_conn()
        cursor.execute(query_sql,tuple(condition_sql_val_list))

        rows = []
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            # row['postTime']=row['postTime'].strftime('%Y-%m-%d')
            # print(f"[DEBUG] row['postTime']={row['postTime']}")
            rows.append(row)
        
        pooldb.close_conn(conn,cursor)
        
        # postid_list = list(map(lambda x:x['postID'],rows))
        # update_post_pop(postid_list)
        
        return rows

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        print('query_post_sql错误')
        pooldb.close_conn(conn,cursor)
        raise Exception()

def query_post_max_id() -> int:
    try:
        # conndb.cursor.execute("select postID from posts order by postID desc limit 1")
        conn,cursor = pooldb.get_conn()
        cursor.execute("select postID from posts order by postID desc limit 1")
        row = cursor.fetchall()[0]
        pooldb.close_conn(conn,cursor)
        return int(row['postID'])

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        pooldb.close_conn(conn,cursor)
        raise Exception()

def add_post_sql(data:dict) -> int:
    try:
        #假设data中的属性都是确定无误的
        gen_postid = query_post_max_id()+1
        sql = 'insert into posts ('
        sql2 = ' values ('
        val_list = []
        data_key_val = [['postID',gen_postid]] + list(data.items())
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
        #返回当前post的id
        return gen_postid
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        raise Exception()

def add_post_tag_sql(postID,tagName):
    try:
        rows = query_sql({'tagName':tagName})
        if rows is None:
            raise Exception(f'找不到tagName={tagName}对应的数据')
        if len(rows) == 0:
            raise Exception(f'找不到tagName={tagName}对应的数据')
        tagID = rows[0]['tagID']
        sql = 'insert into posts_tags(postID,tagID) values(%s,%s)'
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(postID,tagID))
        conn.commit()
        pooldb.close_conn(conn,cursor)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        raise Exception()

def del_post_tag_sql(postID,tagName):
    try:
        rows = query_sql({'tagName':tagName})
        if rows is None:
            raise Exception(f'找不到tagName={tagName}对应的数据')
        if len(rows) == 0:
            raise Exception(f'找不到tagName={tagName}对应的数据')
        tagID = rows[0]['tagID']
        
        sql = 'delete from posts_tags where postID=%s and tagID=%s'
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(postID,tagID))
        conn.commit()
        pooldb.close_conn(conn,cursor)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        raise Exception()

def add_post_keywords_sql(postID,keyword):
    sql = 'insert into posts_keywords(postID,keyword) values(%s,%s)'
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(postID,keyword))
        conn.commit()
        pooldb.close_conn(conn,cursor)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        raise Exception()

def del_post_keywords_sql(postID,keyword):
    sql = 'delete from posts_keywords where postID=%s and keyword=%s'
    try:
        conn,cursor = pooldb.get_conn()
        cursor.execute(sql,(postID,keyword))
        conn.commit()
        pooldb.close_conn(conn,cursor)
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        raise Exception()

# 传入postID和新的keyword列表，分析差异，进行更新
def update_post_keywords(postID,new_post_keywords_list):
    del_keywords_list = []
    add_keywords_list = []
    try:
        cur_keywords = query_post_all_keywords(postID)
        for item in new_post_keywords_list:
            if item not in cur_keywords:
                #新表中的数据不在原表中，则添加
                add_keywords_list.append(item)
        for item in cur_keywords:
            if item not in new_post_keywords_list:
                #新表中没有当前表中的数据，删除
                del_keywords_list.append(item)
        for item in add_keywords_list:
            add_post_keywords_sql(postID,item)
        for item in del_keywords_list:
            del_post_keywords_sql(postID,item)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        raise Exception()

# 传入postID和新的tagName列表，分析差异，进行更新
def update_post_tag(postID,new_post_tag_list):
    #下面两个list储存的都是tagName
    del_tag_list = []
    add_tag_list = []
    try:
        cur_keywords = list(map(lambda x : x['tagName'],query_post_all_tags(postID)))
        for item in new_post_tag_list:
            if item not in cur_keywords:
                #新表中的数据不在原表中，则添加
                add_tag_list.append(item)
        for item in cur_keywords:
            if item not in new_post_tag_list:
                #新表中没有当前表中的数据，删除
                del_tag_list.append(item)
        for item in add_tag_list:
            add_post_tag_sql(postID,item)
        for item in del_tag_list:
            del_post_tag_sql(postID,item)
            
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2]+"::数据库sql执行错误")
        print(e)
        raise Exception()

# 传入postID和新的post数据，分析差异，进行更新
def update_post_sql(postID, new_post_data):
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
        update_sql += (' ' + sql_list[-1] +' where postID=%s')
        val_list.append(postID)
        conn,cursor = pooldb.get_conn()
        cursor.execute(update_sql,tuple(val_list))
        #提交事务
        conn.commit()
        pooldb.close_conn(conn,cursor)
    except Exception as e:
        #出现错误回滚
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()

#传入postID，删除对应的post，并级联删除帖子关键词表和帖子标签表上的所有信息
#级联删除部分由DBMS完成，应用层只需要删除就行
def del_post_sql(postID):
    try:
        del_sql = 'DELETE FROM posts WHERE postID=%s'
        conn,cursor = pooldb.get_conn()
        cursor.execute(del_sql,(postID))
        #提交事务
        conn.commit()
        pooldb.close_conn(conn,cursor)
        return build_success_response()

    except Exception as e:
        #出现错误回滚
        print("[ERROR] 删除帖子失败")
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()


#post查询返回构造函数，输入postID列表，就可以返回该列表下所有post的全部数据
def build_post_response_data(postID_list:list):
    res = []
    for postID in postID_list:
        # print("current ID = ",postID)
        post_data = query_post_sql({"postID":postID})
        if post_data and len(post_data):
            #查询到了post
            post_data = post_data[0]
            tag_data = query_post_all_tags(postID)
            keyword_data = query_post_all_keywords(postID)
            post_data['postTag'] = tag_data
            post_data['postKeywords'] = keyword_data
            if not isinstance(post_data['postTime'],str):
                post_data['postTime'] = post_data['postTime'].strftime('%Y-%m-%d')
            res.append(post_data)
    return res


#增加帖子
@posts.route('/add', methods=['POST'])
def addPost():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        data = request.json
        post_add_data = {}
        post_tag_list = []
        post_keywords_list = []
        # print(1)
        for item in data.items():
            if(item[0] in ["postTitle",'postContent','postTime','postAnswer','postPopularity','remark']):
                post_add_data[item[0]]=item[1]
        # print(2)
        if('postPopularity' in data.keys()):
            if(not is_number(data['postPopularity'])):
                raise Exception('postPopularity不合法')
        # print(3)
        if('postKeywords' in data.keys()):
            post_keywords_list = data['postKeywords']
        # print(4)
        if('postTag' in data.keys()):
            for item in data['postTag']:
                post_tag_list.append(item['tagName'])
        # print(5)
        postID = add_post_sql(post_add_data)
        # print(7)
        # print("[DEBUG] postID=",postID)
        for item in post_tag_list:
            add_post_tag_sql(postID,item)
        for item in post_keywords_list:
            add_post_keywords_sql(postID,item)
        
        return build_success_response()
        
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


#修改帖子
@posts.route('/update', methods=['POST'])
def updatePost():
    state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
    if state == 404:
        return build_error_response(400,'会话未建立，请重新登录')
    elif state == 403:
        return build_error_response(403,'您没有该操作的权限，请联系管理员')
    elif state == 500:
        return build_error_response(500,'服务器内部发生错误，请联系管理员')

    data = request.json
    post_update_data = {}
    post_tag_list = []
    post_keywords_list = []
    postID = data['postID']
    for item in data.items():
        if(item[0] in ["postTitle",'postContent','postTime','postAnswer','postPopularity','remark']):
            post_update_data[item[0]]=item[1]

    if('postKeywords' in data):
        post_keywords_list = data['postKeywords']
    
    if('postTag' in data):
        for item in data['postTag']:
            post_tag_list.append(item['tagName'])
            
    try:
        update_post_sql(postID, post_update_data)
        update_post_tag(postID,post_tag_list)
        update_post_keywords(postID,post_keywords_list)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()



#删除帖子
@posts.route('/del', methods=['POST'])
def delPost():
    state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
    if state == 404:
        return build_error_response(400,'会话未建立，请重新登录')
    elif state == 403:
        return build_error_response(403,'您没有该操作的权限，请联系管理员')
    elif state == 500:
        return build_error_response(500,'服务器内部发生错误，请联系管理员')

    postID = request.json.get('postID')        
    try:
        del_post_sql(postID)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()

#查询帖子
@posts.route('/get', methods=['POST'])    
def getPost():
    try:
        
        state = checkTokens(request.cookies.get('Admin-Token'),'common')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        queryParam = request.json
        #正确性检验
        if('sort' in queryParam):
            #sort中必须要包含sortAttr和mode
            if ('sortAttr' not in queryParam['sort'] or 'mode' not in queryParam['sort']):
                print('sort 正确性检验失败')
                raise Exception('sort 正确性检验失败')
        # print(queryParam["postTime"])
        if('postTime' in queryParam and queryParam['postTime'] == [None]):
            queryParam.pop("postTime")
        
        tmp_data = query_post_sql(queryParam)
        
        data_length = len(tmp_data)

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
            tmp_data = tmp_data[(pageNum-1)*pageSize:pageNum*pageSize]
            # print("data cur len=",len(data))


        # print("[DEBUG] tmp_data = \n",tmp_data)
        postid_list = list(map(lambda x : x['postID'],tmp_data))
        # print("[DEBUG] postid_list = ",postid_list)
        # print(1)
    
        data = build_post_response_data(postid_list)
        # print(2)
        # print(data)
        # print("data_length=",data_length)
    
        # print(8)
        return build_success_response(data,data_length)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response() 

