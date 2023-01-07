from flask import request
from flask import Blueprint
import os
import sys
import inspect


from meta_info.utils.buildResponse import build_response,build_success_response,build_error_response
from meta_info.utils.check import is_number
from meta_info.utils.auth import checkTokens
# from database.connect import Conndb
 
tag = Blueprint('tag', __name__)

import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb

'''
    重要数据项
    tagName = request.json.get('tagName')
    tagClass = request.json.get('tagClass')
    tagParentName = request.json.get('tagParentName')
    remark = request.json.get('remark')
    tagPopularity = request.json.get('tagPopularity')
'''

def query_sql(queryParam:dict):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    query_sql = 'select * from tag '
    #限制条件查询的属性
    query_constrain_attr = ['tagName','tagClass','tagParentName','tagID']
    #condition_sql_list是存放queryParam中的查询条件构造出的sql语句的列表
    condition_sql_list = []
    #condition_sql_val_list存放sql对应的值，添加这个是为了参数化查询，防sql注入
    condition_sql_val_list = []
    if 'nameQueryMode' not in queryParam:
        nameQueryMode = 'accurate'
    else:
        nameQueryMode = queryParam['nameQueryMode']
    
    sort_sql = ''
    # print(1)
    for item in queryParam.items():
        key = item[0]
        val = item[1]
        if(key in query_constrain_attr):
            if(key in ['tagName','tagParentName']):
                if(nameQueryMode == 'blur'):
                    condition_sql_list.append(f' {key} like %s ')
                    condition_sql_val_list.append(f'%{val}%')
                else:
                    condition_sql_list.append(key+'=%s')
                    condition_sql_val_list.append(val)
            else:
                condition_sql_list.append(key+'=%s')
                condition_sql_val_list.append(val)
            
    # print(2)  
    if('sort' in queryParam):
        sort_sql = ' order by %s ' %(queryParam['sort']['sortAttr'])
        if(queryParam['sort']['mode'] == 'asc'):
            sort_sql+='ASC'
        elif(queryParam['sort']['mode'] == 'desc'):
            sort_sql+='DESC'
        else:
            print('tagManage.py::query_sql sort错误')
            raise Exception()
    # print(3)
    #构建查询sql语句
    if(len(condition_sql_list)):
        query_sql += ' where '
        for i in range(len(condition_sql_list)-1):
            query_sql += ' %s AND ' % (condition_sql_list[i])
        query_sql += (" " + condition_sql_list[-1] + " ")
    query_sql += sort_sql
    # print('[DEBUG] query_sql='+query_sql)
    try:
        #防止SQL注入，选用参数化查询
        # conndb.cursor.execute(query_sql,tuple(condition_sql_val_list))
        conn,cursor = pooldb.get_conn()
        # print(query_sql)
        cursor.execute(query_sql,tuple(condition_sql_val_list))
        # rows = conndb.cursor.fetchall()
        rows = cursor.fetchall()
    except Exception as e:
        print('tagManage.py::query_sql 查询失败')
        print(e)
        raise Exception()
    
    #根据前端的要求，在tag中添加type属性，满足对不同tagClass有不同显示的需求
    for row in rows:
        if(row['tagClass']==1):
            row['type']='danger'
        elif(row['tagClass']==2):
            row['type']='success'
        elif(row['tagClass']==3):
            row['type']=''
        # print(row)
        if(not isinstance(row['createTime'],str)):
            row['createTime'] = row['createTime'].strftime('%Y-%m-%d')
    return rows



def check_tagParentName(tagParentName,tagClass):
    print(2.1)
    search_tagname_tag = 'select * from tag where tagName = %s'
    # conndb.cursor.execute(search_tagname_tag,(tagParentName))
    # rows = conndb.cursor.fetchall()
    #获取连接池中的连接
    conn,cursor = pooldb.get_conn()
    cursor.execute(search_tagname_tag,(tagParentName))
    rows = cursor.fetchall()
    #释放连接池中的连接
    pooldb.close_conn(conn,cursor)
    print(2.2)
    if(len(rows) <= 0):
        #数据库中没有tagParentName，破坏了完整性约束
        return False
    row = rows[0]
    print(2.3)
    if(int(row['tagClass']) >= int(tagClass)):
        #tagName对应的tagClass小于或等于tagParentName的tagClass，破坏了约束
        return False
    
    return True
    
    
# 添加标签
#前端访问127.0.0.1:5000/tag/add就可以执行该函数，下面的类似~
@tag.route('/add', methods=['POST'])
def addTag():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')
        
        data = request.json  #request.json是一个字典
        # 正确性检验
        tagClass = data['tagClass']
        if(not is_number(str(tagClass))):
            print("Error occurs in tagManage.py::addTag Invalid tagClass")
            raise Exception()
        tagClass = int(tagClass)

        
        tagName = data['tagName']
        if('remark' in data):
            remark = data['remark']
        else:
            remark = ""
        
        if('tagParentName' in data):
            if not check_tagParentName(data['tagParentName'],tagClass):
                #检验不通过
                print("Error occurs in tagManage.py::addTag Invalid tagParentName")
                raise Exception()
            tagParentName = data['tagParentName']
        else:
            if tagClass != 1:
                raise Exception('前端数据错误，tagClass应为1')
            tagParentName = None
        
        #防止sql注入
        try:
            add_sql = 'INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark) VALUES(%s,%s,%s,0,%s)'
            # conndb.cursor.execute(add_sql,(tagName,tagClass,tagParentName,remark))
            conn,cursor = pooldb.get_conn()
            cursor.execute(add_sql,(tagName,tagClass,tagParentName,remark))
            #提交事务
            # conndb.db.commit()
            conn.commit()
            pooldb.close_conn(conn,cursor)
            print(4)
            return build_success_response()

        except Exception as e:
            #出现错误回滚
            # conndb.db.rollback()
            conn.rollback()
            pooldb.close_conn(conn,cursor)
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
            print(e)
            raise Exception()

    except Exception as e:
        print("Error occurs in tagManage.py::addTag")
        print(e)
        return build_error_response()

def del_tag_sql(tagName):
    try:
        #先将child删完
        childTagData = query_sql({"tagParentName":tagName})
        for childTag in childTagData:
            del_tag_sql(childTag['tagName'])
        #再删他本身
        
        del_sql = 'DELETE FROM tag WHERE tagName=%s'
        # conndb.cursor.execute(del_sql,(tagName))
        conn,cursor = pooldb.get_conn()
        cursor.execute(del_sql,(tagName))
        conn.commit()
        pooldb.close_conn(conn,cursor)
        
    except Exception as e:
            #出现错误回滚
            # conndb.db.rollback()
            conn.roolback()
            pooldb.close_conn(conn,cursor)


#删除标签
@tag.route('/del', methods=['POST'])
def delTag():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')
        print('[DEBUG] state=',state)
        tagName = request.json.get('tagName')
        
        #防止sql注入
        try:
            del_tag_sql(tagName)
            return build_success_response()

        except Exception as e:
            #出现错误回滚
            # conndb.db.rollback()
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
            print(e)
            raise Exception()

    except:
        print("Error occurs in tagManage.py::delTag")
        return build_error_response()

def update_sql(tagID,attr:str,val):
    if(attr not in ['tagClass','tagName','tagParentName','tagPopularity','remark']):
        # tag表不存在该属性
        print("Error occurs in tagManage.py::update_sql")
        raise Exception()

    #防止sql注入
    try:
        del_sql = 'UPDATE tag SET %s' % (attr)
        del_sql += '=%s WHERE tagID=%s'
        # conndb.cursor.execute(del_sql,(val,tagID))
        conn,cursor = pooldb.get_conn()
        cursor.execute(del_sql,(val,tagID))
        #提交事务
        # conndb.db.commit()
        conn.commit()
        pooldb.close_conn(conn,cursor)

    except Exception as e:
        #出现错误回滚
        # conndb.db.rollback()
        conn.rollback()
        pooldb.close_conn(conn,cursor)
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        raise Exception()

def check_tagID(tagID):
    #tagID必须为数字
    if(not is_number(tagID)):
        return False
    # conndb.cursor.execute('select * from tag where tagID=%s',(tagID));
    conn,cursor = pooldb.get_conn()
    cursor.execute('select * from tag where tagID=%s',(tagID))
    # rows = conndb.cursor.fetchall()
    rows = cursor.fetchall()
    pooldb.close_conn(conn,cursor)
    if(len(rows) <= 0):
        #数据库中不存在该tagID
        return False
    return True
    

def update_tag_sql(data):
    #认为data中的数据是绝对正确的，忽略正确性检查
    try:
        update_sql = 'UPDATE tag SET '
        sql_list = []
        val_list = []
        #可以修改的项
        valid_update_keys = ['tagName','tagParentName','remark']
        #构建单个sql修改语句
        for item in data.items():
            if(item[0] in valid_update_keys):
                sql_list.append(' '+item[0]+'=%s ' )
                val_list.append(item[1])
        #拼接sql语句
        for i in range(len(sql_list)-1):
            update_sql += (' '+sql_list[i]+', ')

        update_sql += (' ' + sql_list[-1] +' where tagID=%s')
        val_list.append(data['tagID'])
        conn,cursor = pooldb.get_conn()

        #先维护完整性约束，再改名
        #如果该标签改名了，标签的子标签的tagParentName也得改名
        if('tagName' in data):
            rows = query_sql({"tagID":data['tagID']})
            if(rows and not len(rows)):
                raise Exception('数据错误！找不到tagID对应的数据')
            tag_data = rows[0]
            print('[DEBUG] rag_data[tagName]=',tag_data['tagName'])
            print('[DEBUG] data[tagName]=',data['tagName'])
            print(data)
            print(tag_data)
            cursor.execute('update tag set tagParentName=%s where tagParentName=%s',(data['tagName'],tag_data['tagName']))
        
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

#修改标签
@tag.route('/update', methods=['POST'])
def updateTag():
    try:
        state = checkTokens(request.cookies.get('Admin-Token'),'tagger')
        if state == 404:
            return build_error_response(400,'会话未建立，请重新登录')
        elif state == 403:
            return build_error_response(403,'您没有该操作的权限，请联系管理员')
        elif state == 500:
            return build_error_response(500,'服务器内部发生错误，请联系管理员')

        data = request.json
        update_data = {}
        if('tagID' not in data):
            raise Exception('前端数据不正确，缺少tagID')
        
        if('tagClass' not in data):
            raise Exception('前端数据不正确，缺少tagClass')

        if('tagParentName' in data and 'tagClass' in data and data['tagParentName']):
            if(not check_tagParentName(data['tagParentName'],data['tagClass'])):
                print('updateTag::tagParentName检查不通过')
                raise Exception('前端数据不正确')
        

        update_data['tagID'] = data['tagID']
        if('tagName' in data):
            update_data['tagName'] = data['tagName']
        if('tagParentName' in data):
            update_data['tagParentName'] = data['tagParentName']
        if('remark' in data):
            update_data['remark'] = data['remark']
        if('tagClass' in data):
            update_data['tagClass'] = data['tagClass']

        update_tag_sql(update_data)
        
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


#查询标签
@tag.route('/get', methods=['POST'])
def getTag():
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
        if('tagClass' in queryParam and len(str(queryParam['tagClass']))):
            if not is_number(str(queryParam['tagClass'])):
                print('tagClass 正确性检验失败')
                raise Exception('tagClass 正确性检验失败')
        
        if('tagClass' in queryParam and len(str(queryParam['tagClass'])) == 0):
            queryParam.pop('tagClass')
        
        if('sort' in queryParam):
            #sort中必须要包含sortAttr和mode
            if ('sortAttr' not in queryParam['sort'] or 'mode' not in queryParam['sort']):
                print('sort 正确性检验失败')
                raise Exception('sort 正确性检验失败')
        
        data = query_sql(queryParam)
        data_length = len(data)
        # print('data_length=',data_length)
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

#该函数作用是传入一个tagName，返回该tagName的前向标签继承关系
#例如：SQL->SQL查询->嵌套子查询
#get_front_tag_tree_sql('SQL') -> [{"tagName":"SQL",...}]
#get_front_tag_tree_sql('SQL查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...}]
#get_front_tag_tree_sql('嵌套子查询') -> [{"tagName":"SQL",...},{"tagName":"SQL查询",...},{"tagName":"嵌套子查询",...}]
def get_front_tag_tree_sql(tagName):
    response_data=[]
    row = query_sql({'tagName':tagName})[0]
    if(row['tagClass'] == 1):
        response_data.append(row)
    elif(row['tagClass']==2):
        parent_row = query_sql({'tagName':row['tagParentName']})[0]
        response_data=[parent_row,row]
    elif(row['tagClass']==3):
        second_class_row = query_sql({'tagName':row['tagParentName']})[0]
        first_class_row = query_sql({'tagName':second_class_row['tagParentName']})[0]
        response_data=[first_class_row,second_class_row,row]
    return response_data

#查询标签的前向路径
@tag.route('/getFrontTree', methods=['POST'])
def getFrontTagTree():
    try:
        data = request.json
        if('tagName' not in data):
            raise Exception()
        response_data = get_front_tag_tree_sql(data['tagName'])

        return build_success_response(response_data)

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()


#查询标签树
@tag.route('/getTagTree', methods=['GET','POST'])
def getTagTree():
    try:
        first_class_data = query_sql({'tagClass':1})
        second_class_data = query_sql({'tagClass':2})
        third_class_data = query_sql({'tagClass':3})
        for row2 in second_class_data:
            row2['children']=[]
        for row1 in first_class_data:
            row1['children']=[]

        for row3 in third_class_data:
            for row2 in second_class_data:
                if(row2['tagName'] == row3['tagParentName']):
                    row2['children'].append(row3)

        for row2 in second_class_data:
            for row1 in first_class_data:
                if(row1['tagName'] == row2['tagParentName']):
                    row1['children'].append(row2)
        
        return build_success_response(row1,len(row1))
            
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()