import pymysql
from pymysql.cursors import DictCursor

class Conndb:
    def __init__(
        self,cursor_mode='dict',host="43.138.62.72", user="root", password="123456", database="meta_info_db",port=6666
    ):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        
        # 打开数据库连接
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database,
            local_infile=True
        )
        if cursor_mode=='tuple':
            self.cursor = self.db.cursor()
        elif cursor_mode=='dict':
            self.cursor = self.db.cursor(DictCursor)

    def read(self, sql):
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def write(self, sql):
        # write，更新数据库，所以需要用commit
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            #发生错误时回滚
            self.db.rollback()
            print('connect.py::write 数据库提交失败')
            
    def execute_scirpt(self,file):
        with open(file,'r',encoding='utf8') as f:
            data = f.read()
            lines = data.splitlines()
            # print("lines:",lines)
            sql_data = ''
            for line in lines:
                if len(line) == 0:
                    continue
                elif line.startswith('--'):
                    continue
                else:
                    sql_data += line
            # print("sql_data:",sql_data)

            sql_list = sql_data.split(';')[:-1]
            sql_list = [x.replace('\n',' ')if '\n' in x else x for x in sql_list]
            sql_item = ""
            print(sql_list)
            try:
                for sql_item in sql_list:
                    print("[DEBUG] execute : ",sql_item)
                    self.cursor.execute(sql_item)
                    
            except:
                print('connect.py::execute_scirpt sql脚本执行失败')
                print('错误的sql语句：',sql_item)
                self.db.rollback()
                raise Exception()
            
            try:
                self.db.commit()
            except:
                print('connect.py::execute_scirpt 事务提交失败')
                raise Exception()

    def __del__(self):
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()


