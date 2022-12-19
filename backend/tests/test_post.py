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
                condition_sql_list.append('posts.'+key+'=%s')
                condition_sql_val_list.append(val)
            
    if('sort' in queryParam):
        sort_sql = 'order by %s ' %(queryParam['sort']['sortAttr'])
        if(queryParam['sort']['mode'] == 'asc'):
            sort_sql+='ASC'
        elif(queryParam['sort']['mode'] == 'desc'):
            sort_sql+='DESC'
        else:
            # print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
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
    print('[DEBUG] query_param=',condition_sql_val_list)

query_post_sql(
    {
        "postTitle":"待查询帖子标题",   
    }
)