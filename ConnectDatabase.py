import psycopg2

class dbConnection:
    def __init__(self, dbname, user, password, host="localhost", port = "5432"):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host, dbname=self.dbname, user=self.user,
                password=self.password, port=self.port
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Error executing connection: {e}")
        
    def commit(self):
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()