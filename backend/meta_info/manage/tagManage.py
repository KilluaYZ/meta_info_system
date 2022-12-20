from flask import request
from flask import Blueprint
import os
import sys
import inspect


# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# sys.path.append("..")

from manage.buildResponse import build_response,build_success_response,build_error_response
from utils.check import is_number
# from database.connect import Conndb
 
tag = Blueprint('tag', __name__)

import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

'''
    重要数据项
    tagName = request.json.get('tagName')
    tagClass = request.json.get('tagClass')
    tagParentName = request.json.get('tagParentName')
    remark = request.json.get('remark')
    tagPopularity = request.json.get('tagPopularity')
'''

def check_tagParentName(tagParentName,tagClass):
    search_tagname_tag = 'select * from tag where tagName = %s'
    # conndb.cursor.execute(search_tagname_tag,(tagParentName))
    # rows = conndb.cursor.fetchall()
    #获取连接池中的连接
    conn,cursor = pooldb.get_conn()
    cursor.execute(search_tagname_tag,(tagParentName))
    rows = cursor.fetchall()
    #释放连接池中的连接
    pooldb.close_conn(conn,cursor)

    if(len(rows) <= 0):
        #数据库中没有tagParentName，破坏了完整性约束
        return False
    row = rows[0]
    if(int(row['tagClass']) >= int(tagClass)):
        #tagName对应的tagClass小于或等于tagParentName的tagClass，破坏了约束
        return False
    
    return True
    
    
# 添加标签
#前端访问127.0.0.1:5000/tag/add就可以执行该函数，下面的类似~
@tag.route('/add', methods=['POST'])
def addTag():
    try:
        data = request.json  #request.json是一个字典
        # 正确性检验
        tagClass = data['tagClass']
        if(not is_number(str(tagClass))):
            print("Error occurs in tagManage.py::addTag Invalid tagClass")
            raise Exception()
        tagClass = int(tagClass)

        tagName = data['tagName']
        remark = data['remark']
        tagParentName = data['tagParentName']
        if(not check_tagParentName(tagParentName,tagClass)):
            #检验不通过
            print("Error occurs in tagManage.py::addTag Invalid tagClass")
            raise Exception()
        
        #防止sql注入
        try:
            add_sql = 'INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark) VALUES(%s,%d,%s,0,%s)'
            # conndb.cursor.execute(add_sql,(tagName,tagClass,tagParentName,remark))
            conn,cursor = pooldb.get_conn()
            cursor.execute(add_sql,(tagName,tagClass,tagParentName,remark))
            #提交事务
            # conndb.db.commit()
            conn.commit()
            pooldb.close_conn(conn,cursor)
            return build_success_response()

        except Exception as e:
            #出现错误回滚
            # conndb.db.rollback()
            conn.rollback()
            pooldb.close_conn(conn,cursor)
            print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
            print(e)
            raise Exception()

    except:
        print("Error occurs in tagManage.py::addTag")
        return build_error_response()


#删除标签
@tag.route('/del', methods=['POST'])
def delTag():
    try:
        tagName = request.json.get('tagName')
        
        #防止sql注入
        try:
            del_sql = 'DELETE FROM tag WHERE tagName=%s'
            # conndb.cursor.execute(del_sql,(tagName))
            conn,cursor = pooldb.get_conn()
            cursor.execute(del_sql,(tagName))
            #提交事务
            # conndb.db.commit()
            conn.commit()
            pooldb.close_conn(conn,cursor)
            return build_success_response()

        except Exception as e:
            #出现错误回滚
            # conndb.db.rollback()
            conn.roolback()
            pooldb.close_conn(conn,cursor)
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
    

#修改标签
@tag.route('/update', methods=['POST'])
def updateTag():
    try:
        data = request.json
        tagID = data['tagID']
        # print(1)
        if(not check_tagID(tagID)):
            print('[ERROR] tagID检查不通过')
            #tagID检查不通过
            raise Exception()
        # print(2)
        if('tagName' in data):
            update_sql(tagID,'tagName',data['tagName'])
        # print(3)
        if('tagClass' in data):
            if(not is_number(data['tagClass'])):
                raise Exception()
            update_sql(tagID,'tagClass',data['tagClass'])
        # print(4)
        if('tagParentName' in data):
            if(not check_tagParentName(data['tagParentName'],data['tagClass'])):
                print('updateTag::tagParentName检查不通过')
                raise Exception()
            update_sql(tagID,'tagParentName',data['tagParentName'])
        # print(5)
        if('tagPopularity' in data):
            if(not is_number(data['tagPopularity'])):
                raise Exception()
            update_sql(tagID,'tagPopularity',data['tagPopularity'])
        # print(6)
        if('remark' in data):
            update_sql(tagID,'remark',data['remark'])
        print(7)
        return build_success_response()

    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()

def query_sql(queryParam:dict):
    #假设queryParam是绝对正确的，本函数就忽略对queryParam的正确性检验，将注意力集中在功能上
    query_sql = 'select * from tag '
    #限制条件查询的属性
    query_constrain_attr = ['tagName','tagClass','tagParentName']
    #condition_sql_list是存放queryParam中的查询条件构造出的sql语句的列表
    condition_sql_list = []
    #condition_sql_val_list存放sql对应的值，添加这个是为了参数化查询，防sql注入
    condition_sql_val_list = []

    sort_sql = ''
    # print(1)
    for item in queryParam.items():
        key = item[0]
        val = item[1]
        if(key in query_constrain_attr):
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
        cursor.execute(query_sql,tuple(condition_sql_val_list))
        # rows = conndb.cursor.fetchall()
        rows = cursor.fetchall()
    except:
        print('tagManage.py::query_sql 查询失败')
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


#查询标签
@tag.route('/get', methods=['POST'])
def getTag():
    try:
        queryParam = request.json
        #正确性检验
        if('tagClass' in queryParam):
            if not is_number(queryParam['tagClass']):
                print('tagClass 正确性检验失败')
                raise Exception('tagClass 正确性检验失败')
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


#查询标签的前向路径
@tag.route('/getFrontTree', methods=['POST'])
def getFrontTagTree():
    try:
        data = request.json
        if('tagName' not in data):
            raise Exception()
        response_data=[]
        row = query_sql({'tagName':data['tagName']})[0]
        if(row['tagClass'] == 1):
            response_data.append(row)
        elif(row['tagClass']==2):
            parent_row = query_sql({'tagName':row['tagParentName']})[0]
            response_data=[parent_row,row]
        elif(row['tagClass']==3):
            second_class_row = query_sql({'tagName':row['tagParentName']})[0]
            first_class_row = query_sql({'tagName':second_class_row['tagParentName']})[0]
            response_data=[first_class_row,second_class_row,row]

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