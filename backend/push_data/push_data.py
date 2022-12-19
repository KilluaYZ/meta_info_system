

#导入数据
load data local infile 'path' into table posts(postTitle, postContent,postAnswer,postTime)  #path是txt文件路径
CHARACTER SET utf8 
FIELDS TERMINATED BY ',' # 字段分隔符，每个字段(列)以什么字符分隔，默认是 \t
	OPTIONALLY ENCLOSED BY '' #文本限定符，每个字段被什么字符包围，默认是空字符
	ESCAPED BY '\\' #转义符，默认是 \
LINES TERMINATED BY '\n' #记录分隔符，如字段本身也含\n，那么应先去除，否则load data 会误将其视作另一行记录进行导入

