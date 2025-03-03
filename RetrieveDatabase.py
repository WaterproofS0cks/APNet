class dbRetrieve:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, query, params=None):
        try:
            if params:
                self.db_connection.cur.execute(query, params)
            else:
                self.db_connection.cur.execute(query)
        except Exception as e:
            print(f"Error executing query: {e}")

    def retrieve_all(self, tablename):
        query = f'SELECT * FROM "{tablename}";'
        self.execute_query(query)
        return self.db_connection.cur.fetchall()
    


    def retrieve_data_all(self, tablename, column):
        columns = f"{column}::DATE, COUNT(*)"
        query = (
            f"SELECT {column}::DATE, COUNT(*) "
            f"FROM {tablename} "
            f"GROUP BY {column}::DATE "
            f"ORDER BY {column}::DATE;"
        )
        self.execute_query(query)
        return self.db_connection.cur.fetchall()

    def retrieve(self, tablename, columns="*", condition=None, params=None):
        query = f'SELECT {columns} FROM "{tablename}"'
        if condition:
            query += f' WHERE {condition}'
        query += ";"
        print(query)
        self.execute_query(query, params)
        return self.db_connection.cur.fetchall()


