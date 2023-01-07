use meta_info_db;

-------------------------------------------------------------------------
--帖子
SET foreign_key_checks=0;
DROP Table if EXISTS posts;
SET foreign_key_checks=1;
create table posts(
    postID int primary key,
    postTitle TEXT not null,
    postAnswer TEXT,
    postTime DATE,
    postContent TEXT not null,
    postPopularity int default 0,
    remark TEXT
);

-------------------------------------------------------------------------
-- 标签
SET foreign_key_checks=0;
DROP Table if EXISTS tag;
SET foreign_key_checks=1;
CREATE TABLE tag(
    tagID INT PRIMARY KEY AUTO_INCREMENT,
    tagName VARCHAR(50) UNIQUE  NOT NULL,
    tagClass SMALLINT NOT NULL check(tagClass >= 1 and tagClass <= 3),
    tagParentName VARCHAR(50),
    tagPopularity INT default 0,
    remark TEXT,
    createTime datetime not null default current_timestamp
);

-------------------------------------------------------------------------
--帖子标签
DROP Table if EXISTS posts_tags;
create table posts_tags(
    postID int not null AUTO_INCREMENT,
    tagID int not null,
    primary key(postID,tagID),
    foreign key(postID) references posts(postID) on delete cascade on update cascade,
    foreign key(tagID) references tag(tagID) on delete cascade on update cascade
);


-------------------------------------------------------------------------
--帖子关键词
DROP Table if EXISTS posts_keywords;
create table posts_keywords(
    postID int not null,
    keyword VARCHAR(50) not null,
    primary key(postID,keyword),
    foreign key(postID) references posts(postID) on delete cascade on update cascade
); 

--------------------------------------------------------------------------
--定义触发器，维护完整性约束
drop trigger if EXISTS posts_tags_insert_tri ; 
create trigger posts_tags_insert_tri 
after insert on posts_tags 
for each row 
update tag set tagPopularity=(select count(*) as cnt from posts_tags where NEW.tagID=posts_tags.tagID group by NEW.tagID ) where tagID = NEW.tagID ;

drop trigger if EXISTS posts_tags_delete_tri ; 
create trigger posts_tags_delete_tri 
after delete on posts_tags 
for each row 
update tag set tagPopularity=(select count(*) as cnt from posts_tags where old.tagID=posts_tags.tagID  group by old.tagID ) where tagID = old.tagID ; 

-------------------------------------------------------------------------
--用户表
SET foreign_key_checks=0;
DROP Table if EXISTS user;
SET foreign_key_checks=1;

create table user( 
    uid int PRIMARY KEY AUTO_INCREMENT, 
    username varchar(50) not null UNIQUE, 
    nickname varchar(50) not null, 
    password TEXT not null, 
    roles varchar(8) not null , 
    email varchar(50), 
    phonenumber varchar(50), 
    avator TEXT, 
    createTime datetime not null  default CURRENT_TIMESTAMP 
); 

--用户会话表
SET foreign_key_checks=0;
DROP Table if EXISTS user_token;
SET foreign_key_checks=1;
create table user_token( 
    uid int not null, 
    token VARCHAR(128) not null, 
    createTime datetime not null  default CURRENT_TIMESTAMP, 
    visitTime datetime not null default CURRENT_TIMESTAMP , 
    PRIMARY key(uid,token), 
    foreign key(uid) references user(uid) on delete cascade on update cascade 
); 
--用户会话表触发器
-- drop trigger if EXISTS user_token_insert_tri ; 
-- create trigger user_token_insert_tri 
-- before insert on user_token 
-- for each row 
-- delete from user_token where user_token.uid=new.uid; 

INSERT INTO user(username,nickname,password,roles) 
VALUES('admin','ruc', 
'pbkdf2:sha256:260000$twMVANMQb6phGZEV$bd84550842562a5e597c8f4eb57237ac5e7fda7f5177656447b5016a5f1d89c4','admin'); 

-------------------------------------------------------------------------

--添加tag数据
-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库概述',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库发展历史',2,'数据库概述',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据管理技术的产生和发展',3,'数据库发展历史',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('我国数据库发展情况介绍',3,'数据库发展历史',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库基本概念',2,'数据库概述',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库管理系统',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库系统',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库系统的模式结构',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库物理独立性',3,'数据库基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库逻辑独立性',3,'数据库基本概念',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库体系结构',2,'数据库概述',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集中式数据库结构',3,'数据库体系结构',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('客户/服务器数据库结构',3,'数据库体系结构',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('并行数据库结构',3,'数据库体系结构',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('分布式数据库结构',3,'数据库体系结构',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('云数据库结构',3,'数据库体系结构',0,'');



-------------------------------------------------------------------------

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系数据模型',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据模型',2,'关系数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据模型的组成',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('层次数据模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('网状数据模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('面向对象数据模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('XML数据模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('文档模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('图模型',3,'数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模型',2,'关系数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模型的数据结构',3,'关系模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系操作',3,'关系模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系的完整性约束',3,'关系模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系代数',2,'关系数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系代数的基本概念',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('选择',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('投影',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集合并',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集合差',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('笛卡尔积',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集合交',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('自然连接',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('除法',3,'关系代数',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系演算',2,'关系数据模型',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系演算的基本概念',3,'关系演算',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('元组关系演算',3,'关系演算',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('域关系演算',3,'关系演算',0,'');


-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('SQL',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据定义',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义数据库中的模式结构（表和索引）',3,'数据定义',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('修改数据库模式结构',3,'数据定义',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('删除数据库模式结构',3,'数据定义',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本SQL查询',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('简单查询',3,'基本SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('连接查询',3,'基本SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集合查询',3,'基本SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('空值查询',3,'基本SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('聚集查询',3,'基本SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('复杂SQL查询',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('嵌套查询',3,'复杂SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于派生表的查询',3,'复杂SQL查询',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据更新',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('向表中添加若干数据',3,'数据更新',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('修改表中的数据',3,'数据更新',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('删除表中的数据',3,'数据更新',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('视图',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('视图的基本概念',3,'视图',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('视图的用途',3,'视图',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义视图（建立和删除）',3,'视图',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('视图查询',3,'视图',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('视图更新',3,'视图',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库完整性',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义实体完整性',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义参照完整性',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义值域',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义唯一取值',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定义非空取值',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('用触发器实现完整性',3,'数据库完整性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库安全性',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的不安全因素分析',3,'数据库安全性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库安全性控制方法',3,'数据库安全性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('自主访问控制（授权与回收，角色）',3,'数据库安全性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('强制访问控制',3,'数据库安全性',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库编程',2,'SQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库高级语言接口原理',3,'数据库编程',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('PL/SQL',3,'数据库编程',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('存储过程',3,'数据库编程',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('存储函数',3,'数据库编程',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('JDBC',3,'数据库编程',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('ODBC',3,'数据库编程',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库设计',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('概念结构设计',2,'数据库设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('概念结构设计的任务描述',3,'概念结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('概念模型的特点',3,'概念结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('E-R模型中实体型和联系的表示方法',3,'概念结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('概念结构设计中的基本原则',3,'概念结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('E-R图的集成方法',3,'概念结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('逻辑结构设计',2,'数据库设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('逻辑结构设计的任务描述',3,'逻辑结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('E-R图向关系模型的转换',3,'逻辑结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据模型的优化',3,'逻辑结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('用户子模式的设计',3,'逻辑结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('物理结构设计',2,'数据库设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('物理设计的任务描述',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模式存取方法--B+树',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模式存取方法--Hash',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模式存取方法--聚簇存取',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的存储结构--垂直分片',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的存储结构--水平分片',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的存储结构--分片策略',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的存储结构--索引方法',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库的存储结构--数据压缩',3,'物理结构设计',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('评价物理结构',3,'物理结构设计',0,'');


-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系数据库设计理论',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据依赖',2,'关系数据库设计理论',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模式可能存在的几类异常',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('函数依赖',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('平凡函数依赖与非平凡函数依赖',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('完全函数依赖与部分函数依赖',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('传递函数依赖',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多值依赖',3,'数据依赖',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系规范化',2,'关系数据库设计理论',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('码',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('主属性',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('非主属性',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('外码',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('候选码',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('主码',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('范式',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('通过模式分解实现规范化的过程',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('2NF',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('3NF',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('BCNF',3,'关系规范化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('4NF',3,'关系规范化',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('函数依赖推理系统',2,'关系数据库设计理论',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('逻辑蕴涵',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Armstrong公理系统',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Armstrong公理系统定律及推理规则',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('函数依赖集的闭包',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('属性集关于函数依赖集的闭包',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('求属性集闭包的算法',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Armstrong公理完备性及有效性的分析',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('函数依赖集等价',3,'函数依赖推理系统',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('最小覆盖',3,'函数依赖推理系统',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('模式分解',2,'关系数据库设计理论',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('函数依赖集在属性集上的投影',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系模式的分解',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('模式等价的定义',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('无损连接性',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('保持函数依赖',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('判别分解是否具备无损连接性、是否保持函数依赖的方法',3,'模式分解',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('模式分解的算法',3,'模式分解',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('存储管理',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库存储基本原理',2,'存储管理',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据存储模型',3,'数据库存储基本原理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('存储介质及磁盘管理',3,'数据库存储基本原理',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('文件存储组织',2,'存储管理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('堆文件',3,'文件存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('顺序文件',3,'文件存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('聚簇文件',3,'文件存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('B+树文件',3,'文件存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Hash文件',3,'文件存储组织',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('记录存储组织',2,'存储管理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('定长记录组织',3,'记录存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('变长记录组织',3,'记录存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('记录不跨块存储',3,'记录存储组织',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('记录跨块存储',3,'记录存储组织',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('缓冲区管理',2,'存储管理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('缓冲区组织方式',3,'缓冲区管理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('缓冲区管理策略',3,'缓冲区管理',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引',1,NULL,0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('顺序索引',2,'索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('稠密索引及其查找算法',3,'顺序索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('稀疏索引及其查找算法',3,'顺序索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多级索引及其查找算法',3,'顺序索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('辅助索引',3,'顺序索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('B+树索引',2,'索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('B+树索引结构',3,'B+树索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引查找',3,'B+树索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引维护',3,'B+树索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('散列索引',2,'索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本Hash索引',3,'散列索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('可扩展Hash索引',3,'散列索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('线性Hash索引',3,'散列索引',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Bitmap索引',2,'索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Bitmap索引结构',3,'Bitmap索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Bitmap索引查找',3,'Bitmap索引',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('编码Bitmap索引',3,'Bitmap索引',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理的基本步骤',2,'查询处理',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理的基本步骤--查询检查',3,'查询处理的基本步骤',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理的基本步骤--查询分析',3,'查询处理的基本步骤',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理的基本步骤--查询优化',3,'查询处理的基本步骤',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询处理的基本步骤--查询执行',3,'查询处理的基本步骤',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('扫描算法',2,'查询处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('全表扫描',3,'扫描算法',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引扫描',3,'扫描算法',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('连接算法',2,'查询处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('嵌套循环连接',3,'连接算法',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('排序-合并连接',3,'连接算法',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Hash连接',3,'连接算法',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引连接',3,'连接算法',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('其他算子的处理',2,'查询处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('取消重复值',3,'其他算子的处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('分组聚集',3,'其他算子的处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('集合操作',3,'其他算子的处理',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询优化',1,NULL,0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('逻辑查询优化',2,'查询优化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('关系表达式等价变换规则',3,'逻辑查询优化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于规则的优化策略',3,'逻辑查询优化',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('代价模型及估算',2,'查询优化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('代价模型',3,'代价模型及估算',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('统计信息收集与存储',3,'代价模型及估算',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('各类关系操作符代价估算方法',3,'代价模型及估算',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('物理查询优化',2,'查询优化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('代价优化的搜索空间',3,'物理查询优化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('搜索优化计划的方法',3,'物理查询优化',0,'穷举法，启发式方法，动态规划等');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询执行引擎',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('查询执行框架',2,'查询执行引擎',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('自底向上执行',3,'查询执行框架',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('自顶向下执行',3,'查询执行框架',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('物化和流水线技术',3,'查询执行框架',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('物化执行模型',3,'查询执行框架',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('向量化执行模型(SIMD)',3,'查询执行框架',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('编译执行',2,'查询执行引擎',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('静态预编译AOT',3,'编译执行',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('动态实时编译JIT',3,'编译执行',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务处理',1,NULL,0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务的基本概念',2,'事务处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务的背景及其其重要性',3,'事务的基本概念',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务的定义',3,'事务的基本概念',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务的ACID特性',3,'事务的基本概念',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据异常与隔离级别',2,'事务处理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('事务的执行模型',3,'数据异常与隔离级别',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('SQL-92中定义的3类数据异常及形式化定义',3,'数据异常与隔离级别',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于数据异常的隔离级别定义',3,'数据异常与隔离级别',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('主流数据库管理系统能够支持的常见隔离级别',3,'数据异常与隔离级别',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('并发控制',1,NULL,0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于锁的并发控制',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('封锁协议',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('相容矩阵',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('活锁与死锁',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('避免活锁策略',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('死锁预防',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('死锁检测',3,'基于锁的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多粒度封锁',3,'基于锁的并发控制',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('可串行化与冲突可串行化',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('串行调度',3,'可串行化与冲突可串行化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('可串行化调度',3,'可串行化与冲突可串行化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('冲突可串行化调度的定义、区别及联系',3,'可串行化与冲突可串行化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于等价交换的冲突可串行化检测',3,'可串行化与冲突可串行化',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于依赖图的冲突可串行化检测',3,'可串行化与冲突可串行化',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('两阶段封锁协议',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('两阶段协议内容',3,'两阶段封锁协议',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('两阶段封锁协议存在的问题：死锁与级联回滚',3,'两阶段封锁协议',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('死锁预防策略',3,'两阶段封锁协议',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('严格两阶段封锁协议',3,'两阶段封锁协议',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于时间戳的并发控制',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本的时间戳并发控制算法',3,'基于时间戳的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于时间戳的并发控制--确定等价的事务冲突可串行化顺序',3,'基于时间戳的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于时间戳的冲突检测与事务回滚',3,'基于时间戳的并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本的时间戳并发控制算法实现举例',3,'基于时间戳的并发控制',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('乐观并发控制',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本的乐观并发控制算法',3,'乐观并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('乐观并发控制确定等价的事务冲突可串行化顺序',3,'乐观并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('乐观并发控制冲突检测与事务回滚',3,'乐观并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基本的乐观并发控制算法实现举例',3,'乐观并发控制',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多版本并发控制',2,'并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('并发控制协议',3,'多版本并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('版本管理',3,'多版本并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('垃圾回收',3,'多版本并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('索引管理',3,'多版本并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多版本并发控制删除',3,'多版本并发控制',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多版本并发控制实现举例',3,'多版本并发控制',0,'');


-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('故障恢复',1,NULL,0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('故障恢复基本原理',2,'故障恢复',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('故障的分类',3,'故障恢复基本原理',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('故障恢复的正确性度量',3,'故障恢复基本原理',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于备份与日志的恢复策略',2,'故障恢复',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('静态备份',3,'基于备份与日志的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('动态备份',3,'基于备份与日志的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('全量备份',3,'基于备份与日志的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('增量备份',3,'基于备份与日志的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('WAL日志',3,'基于备份与日志的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于备份和日志的恢复策略',3,'基于备份与日志的恢复策略',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于检查点的恢复策略',2,'故障恢复',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('检查点概念',3,'基于检查点的恢复策略',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('基于检查点的恢复策略细节',3,'基于检查点的恢复策略',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('恢复算法ARIES',2,'故障恢复',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('LSN',3,'恢复算法ARIES',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('日志结构',3,'恢复算法ARIES',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('日志缓冲区管理',3,'恢复算法ARIES',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('ARIES算法',3,'恢复算法ARIES',0,'');

-------------------------------------------------------------------------
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('新技术',1,NULL,0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('分布式OLTP数据库',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLTP',3,'分布式OLTP数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLTP系统架构',3,'分布式OLTP数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLTP数据分片',3,'分布式OLTP数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLTP分布式事务',3,'分布式OLTP数据库',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLAP数据库',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLAP列存储',3,'OLAP数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLAP分布式查询处理',3,'OLAP数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('OLAP复杂查询加速技术',3,'OLAP数据库',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据仓库',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('ODS',3,'数据仓库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('ETL',3,'数据仓库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据集市/DataMart',3,'数据仓库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据湖/DataLake',3,'数据仓库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('CUBE计算',3,'数据仓库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('实体化视图',3,'数据仓库',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据概述',3,'大数据',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据管理',3,'大数据',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据处理',3,'大数据',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据分析与可视化',3,'大数据',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大数据应用',3,'大数据',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('NoSQL',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据复制',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('CAP理论',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('Raft算法/Paxos协议',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('键值对/KV',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('大表/宽表',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('文档数据库',3,'NoSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('图数据库',3,'NoSQL',0,'');


INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('NewSQL',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('严格可串行化',3,'NewSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('原子钟与延迟提交',3,'NewSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('逻辑时钟与混合逻辑时钟',3,'NewSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('多协调器架构下的分布式事务处理',3,'NewSQL',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('混合事务/分析处理(HTAP)',3,'NewSQL',0,'');

INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('云数据库',2,'新技术',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('垂直扩展与水平扩展',3,'云数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库服务/DaaS',3,'云数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('云原生数据库',3,'云数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('数据库模块解耦',3,'云数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('存算分离',3,'云数据库',0,'');
INSERT INTO tag (tagName,tagClass,tagParentName,tagPopularity,remark)
VALUES ('弹性伸缩',3,'云数据库',0,'');

-------------------------------------------------------------------------
load data local infile 'meta_info/database/data1.txt' into table posts 
CHARACTER SET utf8  
FIELDS TERMINATED BY ',' 
(postID, postTitle, postContent,postAnswer,postTime);
