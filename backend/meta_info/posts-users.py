import pymysql
import numpy as np


#连接数据库
def get_db():
    conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd="",
    charset="utf8",
    autocommit=True # 这里不设置会出现无法插入值的奇怪bug
    )
    return conn

#创建用户表
def create_users():
    conn=get_db()
    cursor = conn.cursor()
    sql="""create table users(
            userID char(8) not null primary key,
            username varchar(10) not null unique,
            password varchar(18) not null unique)"""
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return

#生成验证码
def create_vercode():
    conn=get_db()
    cursor = conn.cursor()

    sql1="""create table vercode_tagker(
            code int(6) not null unique primary key)"""
    cursor.execute(sql1)
    conn.commit()

    #生成随机六位验证码
    for i in range(30):
        code=random.randint(000000,555555)
        sql="""insert into vercode_tagker(code) values("%d")"""
        cursor.execute(sql)
        conn.commit()
    
    sql2="""create table vercode_admin(
            code int(6) not null unique primary key)"""
    cursor.execute(sql1)
    conn.commit()

    #生成随机六位验证码
    for i in range(30):
        code=random.randint(555556,999999)
        sql="""insert into vercode_admin(code) values("%d")"""
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()
    return

#用户登录
def log_user(username,ID,password):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select password from users where user_name="%s"""%(username)
    cursor.execute(sql)
    find_password=cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if find_password == password:
        return 200
    else:
        return 400

#用户注册
#普通用户
def register_user_regular(username,password):
    conn = get_db()
    cursor = conn.cursor()
    #随机生成ID
    uID=random.randint(10000000,99999999)
    sql="""insert into users(uID,username,password) values("%s","%s","%s")"""
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return uID

#标注员
def register_user_tagker(username,password，vercode):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select code="%d" from vercode_tagker"""%(code)
    cursor.execute(sql)
    ret=cursor.fetchone()
    if ret!=NULL:
        #随机生成ID
        uID=random.randint(10000000,99999999)
        sql="""insert into users(uID,username,password) values("%s","%s","%s")"""
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return 200
    else:
        return 400

#管理员
def register_user_admin(username,password):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select code="%d" from vercode_admin"""%(code)
    cursor.execute(sql)
    ret=cursor.fetchone()
    if ret!=NULL:
        #随机生成ID
        uID=random.randint(10000000,99999999)
        sql="""insert into users(uID,username,password) values("%s","%s","%s")"""
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return 200
    else:
        return 400

#删除用户
def delete_user(ID):
    conn = get_db()
    cursor = conn.cursor() 
    sql="""delete from users where ID="%s"""%(ID)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 

#寻找用户
#根据ID
def select_user(ID):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where ID="%s"""%(ID)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 

#根据用户名
def select_user(username):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where username="%s"""%(username)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 

#修改用户信息
#修改用户名
def alter_user_username(ID,newname):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where ID="%s"
            update users set username="%s"""%(ID,newname)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 

#修改用户密码
def alter_user_password(ID,newword):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where ID="%s"
            update users set password="%s"""%(ID,newword)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    return 
    
#帖子
#建帖子（posts）表
def create_post():
    conn=get_db()
    cursor = conn.cursor()
    sql="""create table posts(
            posttag VARCHAR(4) not null unique primary key,
            posttitle TEXT not null,
            postkeywords1 TEXT not null,
            postkeywords2 TEXT,
            postkeywords3 TEXT,
            postanswer TEXT,
            posts_time DATE,
            postcontent TEXT，
            postpopularity VARCHAR(3),
            remark TEXT"""        
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return
     
#删除帖子
def delete_user(posttag):
    conn = get_db()
    cursor = conn.cursor() 
    sql="""delete from posts where posttag="%s"""%(posttag)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 
        

#查询帖子
#根据帖子编号
def select_post_tag(posttag):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from posts where posttag="%s"""%(posttag)
    cursor.execute(sql)
    ret=cursor.fetchall()
    cursor.close()
    conn.close()
    return ret

#根据帖子标题
def select_post_tag(posttitle):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from posts where posttitle="%s"""%(posttitle)
    cursor.execute(sql)
    ret=cursor.fetchall()
    cursor.close()
    conn.close()
    return ret