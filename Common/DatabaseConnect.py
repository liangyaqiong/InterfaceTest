import pymysql

class  Database():

    def database_connect(self):
         self.con = pymysql.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='123456',
                                    database='test',
                                    charset="utf8",
                                    # 游标类型，默认是元组，当前语句是指定为字典游标，控制查询结果的显示数据类型
                                    cursorclass=pymysql.cursors.DictCursor)

         self.cur = self.con.cursor()

    def ExcuteSql(self,sql,query_key):

        self.query_result =   self.cur.execute(sql)
        result =  self.info.get(query_key)
        self.con.close()
        return  result




