import pymysql


class Database:

    # constructor
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.db = "precious"

    # Connect to DB
    def connect(self):
        self.con = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            cursorclass=pymysql.cursors.DictCursor)

        self.cur = self.con.cursor()

    # Disconnect from DB
    def disconnect(self):
        self.con.close()

    # Query the DB
    def query(self, sql):
        self.connect()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.disconnect()
        return result

    # execute statements
    def execute(self, sql):
        self.connect()
        self.cur.execute(sql)
        self.disconnect()
