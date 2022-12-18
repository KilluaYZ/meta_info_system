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
            username VARCHAR(10) not null unique,
            password varchar(18) not null unique)"""
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return

#用户登录
def log_user(username,ID,password):
    conn = get_db()
    cursor = conn.cursor()
    sql='select password from users where username="%s"'%(username)
    cursor.execute(sql)
    real_password=cursor.fetchone()
    cursor.close()
    conn.close()

    if real_password == password:
        return 200
    else:
        return 400

#判断UID是否已有
def wheather_UID(UID)
    conn = get_db()
    cursor = conn.cursor()
    sql='select * from users where userid="%s"'%(UID)
    cursor.execute(sql)
    ret=cursor.fetchone()
    cursor.close()
    conn.close()
    if len(ret)!=0:  #结果非空，该UID已被占用
        return 1
    else:  #该UID可用
        return 0

def create_UID():
    uID=random.randint(10000000,99999999)
    if wheather_UID(uID)==1:
        return create_UID
    else:
        return UID

#用户注册
#普通用户
def register_user_regular(username,password):
    conn = get_db()
    cursor = conn.cursor()
    uID=create_UID()
    sql='insert into users(uID,username,password) values("%s","%s","%s")'%(uID,username,password)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return uID

#生成验证码
def create_vercode():
    conn=get_db()
    cursor = conn.cursor()

    sql1="""create table vercode_tagker(
            code CHAR(6) not null unique primary key)"""
    cursor.execute(sql1)
    conn.commit()

    #生成随机六位验证码
    for i in range(30):
        code=random.randint(000000,555555)
        sql='insert into vercode_tagker(code) values("%s")'%(code)
        cursor.execute(sql)
        conn.commit()
    
    sql2="""create table vercode_admin(
            code CHAR(6) not null unique primary key)"""
    cursor.execute(sql1)
    conn.commit()

    #生成随机六位验证码
    for i in range(30):
        code=random.randint(555556,999999)
        sql='insert into vercode_admin(code) values("%s")'%(code)
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()
    return


#标注员
def register_user_tagker(username,password,vercode):
    conn = get_db()
    cursor = conn.cursor()
    sql='select* from vercode_tagker where code="%s"'%(code)
    cursor.execute(sql)
    ret=cursor.fetchone()
    if len(ret)!=0:  #结果非空，验证成功，允许注册
        uID=create_UID()
        sql='insert into users(uID,username,password) values("%s","%s","%s")'%(uID,username,password)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return uID
    else:
        return 400

#管理员
def register_user_admin(username,password):
    conn = get_db()
    cursor = conn.cursor()
    sql='select* from vercode_admin where code="%s"'%(code)
    cursor.execute(sql)
    ret=cursor.fetchone()
    if len(ret)!=0:  #结果非空，验证成功，允许注册
        uID=create_UID()
        sql='insert into users(uID,username,password) values("%s","%s","%s")'%(uID,username,password)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return uID
    else:
        return 400

#删除用户
def delete_user(ID):
    conn = get_db()
    cursor = conn.cursor() 
    sql='delete from users where userID="%s"'%(ID)
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
    sql='select * from users where userID="%s"'%(ID)
    cursor.execute(sql)
    ret=cursor.fetchone()
    cursor.close()
    conn.close()
    return ret

#根据用户名
def select_user(username):
    conn = get_db()
    cursor = conn.cursor()
    sql='select * from users where username="%s"'%(username)
    cursor.execute(sql)
    ret=cursor.fetchone()
    cursor.close()
    conn.close()
    return ret

#修改用户信息
#修改用户名
def alter_user_username(ID,newname):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where userID="%s"
            update users set username="%s""""%(ID,newname)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 200

#修改用户密码
def alter_user_password(ID,newword):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from users where userID="%s"
            update users set password="%s""""%(ID,newword)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 
    
#帖子
#建帖子（posts）表
def create_posts():
    conn=get_db()
    cursor = conn.cursor()
    sql="""create table posts(
            tagname VARCHAR(4) not null,
            post_title TEXT not null unique primary key,
            postanswer TEXT,
            posts_time DATE,
            postcontent TEXT not null，
            post_popularity VARCHAR(5),
            remark TEXT"""        
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return
     
#删除帖子
def delete_user(post_title):
    conn = get_db()
    cursor = conn.cursor() 
    sql='delete from posts where post_title="%s"'%(post_title)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 
        

#查询帖子
#根据帖子标题
def select_post_tag(post_title):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select * from posts where post_title="%s"""%(post_title)
    cursor.execute(sql)
    ret=cursor.fetchall()
    cursor.close()
    conn.close()
    return ret

#查询帖子的标签
def select_post_tag(post_title):
    conn = get_db()
    cursor = conn.cursor()
    sql="""select tagname from posts where post_title="%s"""%(post_title)
    cursor.execute(sql)
    ret=cursor.fetchall()
    cursor.close()
    conn.close()
    return ret

#帖子——标签关系表
def create_posts_tags()
    conn=get_db()
    cursor = conn.cursor()
    sql="""create table posts_tags(
            post_title VARCHAR(20) not null,
            tagname VARCHAR(10) not null,
            tagclass INT(1) not null,
            tag_parentname VARCHAR(10),
            post_popularity VARCHAR(5) not null,
            tag_popularity VARCHAR(5) not null,
            remark TEXT，
            primary key(post_title,tagname),
            foreign key(post_title) references posts(post_title),
            foreign key(tagname) references tags(tagname),
            foreign key(post_popularity) references posts(post_popularity),
            foreign key(tag_popularity) references tags(tag_popularity))"""        
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return

#帖子——关键词关系表
def create_posts_keywords()
    conn=get_db()
    cursor = conn.cursor()
    sql="""create table posts_keywords(
            post_title VARCHAR(20) not null primary key,
            keyword TEXT not null)"""        
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return