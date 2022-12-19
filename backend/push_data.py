#导入数据
load data local infile 'D:/my_user_info.txt' into table user_info
CHARACTER SET utf8 -- 可选，指定导入文件的编码，避免中文乱码问题。假如这里文件 my_user_info.txt 的编码为 gbk，那么这里编码就应该设为 gbk 了
FIELDS TERMINATED BY '||' -- 字段分隔符，每个字段(列)以什么字符分隔，默认是 \t
	OPTIONALLY ENCLOSED BY '' -- 文本限定符，每个字段被什么字符包围，默认是空字符
	ESCAPED BY '\\' -- 转义符，默认是 \
LINES TERMINATED BY '\n' -- 记录分隔符，如字段本身也含\n，那么应先去除，否则load data 会误将其视作另一行记录进行导入
(id, name, age, address, create_date) -- 每一行文本按顺序对应的表字段，建议不要省略

