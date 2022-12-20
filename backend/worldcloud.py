import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

#从前端获取起始时间数据项
begin_time=request.json.get('begin_time')
end_time=request.json.get('end_time')

def get_txt(begin_time,end_time):
    



# 导入模块
from wordcloud import WordCloud
# 文本数据
text = 
# 设置参数，创建WordCloud对象
wc = WordCloud(
    width=200,                  # 设置宽为400px
    height=150,                 # 设置高为300px
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