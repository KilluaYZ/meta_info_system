import pymysql


class Conndb:
    def __init__(
        self, host="47.102.217.210", user="root", password="C1emdFuIwH-!", database="cstra"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        # 打开数据库连接
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.db.cursor()

    def read(self, sql):
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def write(self, sql):
        # write，更新数据库，所以需要用commit
        self.cursor.execute(sql)
        self.db.commit()
        return 200

    def __del__(self):
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    conndb = Conndb()
    data = conndb.read("select * from traj limit 10;")
    print(data)