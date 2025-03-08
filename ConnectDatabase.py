import psycopg2
from psycopg2.extras import DictCursor

class dbConnection:
    def __init__(self, dbname, user, password, host="localhost", port = "5432"):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self, cursor_type=None):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
        
        if cursor_type == 'dict':
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
        else:
            self.cur = self.conn.cursor()
        
    def commit(self):
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()