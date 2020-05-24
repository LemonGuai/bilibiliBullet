'''
created on 2020.05.24
@auther:lemon
'''
# coding = utf-8
import pymysql


class DBHelper(object):
    conn = None

    def __init__(self, flag, host='', user='', password='', db='', charset='utf8', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset
        self.flag = flag

    # 连接数据库
    def connect(self):
        if self.flag == 1:
            self.conn = pymysql.connect(host='localhost', user='root', password='salieri2022', db='pyspider', port=3306, charset='utf8')
        else:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset=self.charset)
        self.cursor = self.conn.cursor()

    # 关闭数据库
    def close(self):
        self.cursor.close()
        self.conn.close()

    def query_one(self, sql, params=[]):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result

    def query_all(self, sql, params=[]):
        result = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return result

    def insert(self, sql, params=[]):
        return self.__edit(sql, params)

    def update(self, sql, params=[]):
        return self.__edit(sql, params)

    def delete(self, sql, params=[]):
        return self.__edit(sql, params)

    def __edit(self, sql, params=[]):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql,params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count