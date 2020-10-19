import pymysql


class MysqlController:
    def __init__(self, host, id, pw, db_name):
        self.conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def insert_menu(self, mname, url):
        sql = 'INSERT INTO menu(mname, url) VALUES (%s, %s)'
        self.curs.execute(sql, (mname, url))
        self.conn.commit()
        return self.curs.lastrowid

    def insert_ingredient(self, menuId, iname):
        sql = 'INSERT INTO ingredient(menuId, iname) VALUES (%s, %s)'
        self.curs.execute(sql, (menuId, iname))
        self.conn.commit()

    def insert_recipeOrder(self, context, menuId):
        sql = 'INSERT INTO recipeorder(context, menuId) VALUES (%s, %s)'
        self.curs.execute(sql, (context, menuId))
        self.conn.commit()

    def insert_sauce(self, menuId, sname):
        sql = 'INSERT INTO sauce(menuId, sname) VALUES (%s, %s)'
        self.curs.execute(sql, (menuId, sname))
        self.conn.commit()