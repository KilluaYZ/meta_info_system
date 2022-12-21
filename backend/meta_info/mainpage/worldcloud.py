import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

#从前端获取起始时间数据项
begin_time=request.json.get('begin_time')
end_time=request.json.get('end_time')

#从数据库获得热度前十的标签
def get_txt(begin_time,end_time):
    conn=get_db()
    cursor = conn.cursor()
    sql="""select tagname from
            (select postID,tagname from posts_tags where postID in
            (select postID from posts where posttime between "%s" and "%s" ))as new
            group by tagname order by count(tagname) DESC"""%(begin_time,end_time)
    cursor.execute(sql)
    txt=cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return txt

# 导入模块
from wordcloud import WordCloud
# 文本数据
text = get_txt(begin_time,end_time)
# 设置参数，创建WordCloud对象
wc = WordCloud(
    width=400,                  # 设置宽为400px
    height=300,                 # 设置高为300px
    background_color='white',    # 设置背景颜色为白色
    max_font_size=100,           # 设置最大的字体大小，所有词都不会超过100px
    min_font_size=10,            # 设置最小的字体大小，所有词都不会超过10px
    max_words=10,                # 设置最大的单词个数
    scale=2                     # 扩大两倍
)
# 根据文本数据生成词云
wc.generate(text)
# 保存词云文件
wc.to_file('img.jpg')