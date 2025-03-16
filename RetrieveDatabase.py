from psycopg2.extras import DictCursor

class dbRetrieve:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, query, params=None, cursor_type=None):
        try:
            if cursor_type == 'dict':
                self.db_connection.cur = self.db_connection.conn.cursor(cursor_factory=DictCursor)
            else:
                self.db_connection.cur = self.db_connection.conn.cursor()

            if params:
                self.db_connection.cur.execute(query, params)
            else:
                self.db_connection.cur.execute(query)

        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def retrieve_all(self, tablename):
        query = f'SELECT * FROM "{tablename}";'
        self.execute_query(query)
        return self.db_connection.cur.fetchall()
    
    def retrieve_data_all(self, tablename, column):
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
        self.execute_query(query, params, cursor_type='dict')
        return self.db_connection.cur.fetchall()

    def retrieve_entries(self, type, limit=5, loaded_ids=None, searched_term=''):
        if type == "post":
            query = """
                SELECT 
                    post.postID AS id, 
                    post.caption AS title, 
                    TO_CHAR(post.timestamp, 'DD-MM-YYYY') AS timestamp, 
                    post.image AS image, 
                    post.userID, 
                    users.username, 
                    users.profilePicture, 
                    users.fullname,
                    users.registerDate,
                    COALESCE(COUNT(DISTINCT comment.postID), 0) AS comments_count,
                    COALESCE(COUNT(DISTINCT engagement.postID), 0) AS likes_count
                FROM post
                JOIN users ON post.userID = users.userID
                LEFT JOIN postcomment AS comment ON post.postID = comment.postID
                LEFT JOIN postengagement AS engagement ON post.postID = engagement.postID AND engagement.liked = TRUE
            """
            id_column = "post.postID"
            search_column = "post.caption"
        
        elif type == "recruitment":
            query = """
                SELECT 
                    recruitment.recruitmentID AS id, 
                    recruitment.header AS title, 
                    recruitment.description AS description, 
                    TO_CHAR(recruitment.timestamp, 'DD-MM-YYYY') AS timestamp, 
                    recruitment.image AS image, 
                    recruitment.userID, 
                    users.username, 
                    users.profilePicture, 
                    users.fullname,
                    users.registerDate,
                    COALESCE(COUNT(DISTINCT comment.recruitmentID), 0) AS comments_count,
                    COALESCE(COUNT(DISTINCT engagement.recruitmentID), 0) AS likes_count
                FROM recruitment
                JOIN users ON recruitment.userID = users.userID
                LEFT JOIN recruitmentcomment AS comment ON recruitment.recruitmentID = comment.recruitmentID
                LEFT JOIN recruitmentengagement AS engagement ON recruitment.recruitmentID = engagement.recruitmentID AND engagement.liked = TRUE
            """
            id_column = "recruitment.recruitmentID"
            search_column = "recruitment.header"

        else:
            print("Invalid entry type")
            return []

        if searched_term:
            query += f" WHERE {search_column} ILIKE %s"
            if loaded_ids:
                query += f" AND {id_column} NOT IN ({', '.join(map(str, loaded_ids))})"
        else:
            if loaded_ids:
                query += f" WHERE {id_column} NOT IN ({', '.join(map(str, loaded_ids))})"

        query += f"""
            GROUP BY {id_column}, title, timestamp, image, users.username, 
                    users.profilePicture, users.fullname, users.registerDate
            ORDER BY timestamp DESC
            LIMIT %s;
        """

        try:
            params = (f"%{searched_term}%", limit) if searched_term else (limit,)
            self.execute_query(query, params)
            results = self.db_connection.cur.fetchall()
            return results if results else []
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
