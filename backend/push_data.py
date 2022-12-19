'''我用了MySQL里的load data方法
上传的三个文件里分别对应的是excel里的三个分页
默认分字符是英文逗号, ，且一条记录中不能有\n，所以我都人工先筛了一下
以防错漏，导入后可以select*再确认下！'''


#导入数据
load data local infile 'path' into table posts(postTitle, postContent,postAnswer,postTime)  #path是txt文件路径
CHARACTER SET utf8 
FIELDS TERMINATED BY ',' # 字段分隔符，每个字段(列)以什么字符分隔，默认是 \t
	OPTIONALLY ENCLOSED BY '' #文本限定符，每个字段被什么字符包围，默认是空字符
	ESCAPED BY '\\' #转义符，默认是 \
LINES TERMINATED BY '\n' #记录分隔符，如字段本身也含\n，那么应先去除，否则load data 会误将其视作另一行记录进行导入

