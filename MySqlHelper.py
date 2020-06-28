'''
a module to quickly use mysql
created on 2020.05.24
@auther:lemon
'''
# coding = utf-8
import pymysql
import sys


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

    # 获取查询结果
    def ExecQuery_One(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return result

    # 获取所有查询结果
    def ExecQuery(self, sql, params=()):
        result = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return result

    def ExecNonQuery(self, sql, params=()):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return count

    # def insert(self, sql, params=()):
    #     return self.__ExecNonQuery(sql, params)

    # 执行非查询脚本
    def ExecuteNonQryText(self, sSQLName, params=()):
        sPath = sys.path[0] + r'\\SQL\\{0}'.format(sSQLName)
        count = 0
        try:
            self.connect()
            with open(sPath, 'r', encoding="utf-8") as sqlfile:
                sqllist = sqlfile.read().split(';')[:-1]
                for sql in sqllist:
                    if '\n' in sql:     # 判断是否是空行
                        sql = sql.replace('\n', '')      # 把空行替换为空格
                    if '   ' in sql:  # 判断是否有多个空格
                        sql = sql.replace('   ', '')
                    sCommand = sql+';'
                count = self.cursor.executemany(sCommand, params)
                self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return count

    # 执行查询脚本
    def ExecuteQryText(self, sSQLName, params=()):
        sPath = sys.path[0] + r'\\SQL\\{0}'.format(sSQLName)
        try:
            self.connect()
            with open(sPath, 'r', encoding="utf-8") as sqlfile:
                sqllist = sqlfile.read().split(';')[:-1]
                for sql in sqllist:
                    if '\n' in sql:  # 判断是否是空行
                        sql.replace('\n', ' ')  # 把空行替换为空格
                    if '   ' in sql:  # 判断是否有多个空格
                        sql.replace('   ', '')
                    sCommand = sql + ';'
                self.cursor.executemany(sCommand, params)
                result = self.cursor.fetchall()
                self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return result

    # 执行存储过程
    def ExecuteProcedure(self, sProcName, params=()):
        try:
            self.connect()
            self.cursor.callproc(sProcName, params)
            result = self.cursor.fetchall()
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close()
        return result
