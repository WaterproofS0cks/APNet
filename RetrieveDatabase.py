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
        self.execute_query(query, params)
        return self.db_connection.cur.fetchall()

    def retrieve_posts(self, limit=5, loaded_post_ids=None):
        query = """
            SELECT 
                post.postID, 
                post.caption, 
                TO_CHAR(post.timestamp, 'DD-MM-YYYY') AS post_timestamp, 
                post.image AS post_image, 
                post.userID, 
                users.username, 
                users.profilePicture, 
                users.name, 
                users.registerDate,
                COALESCE(COUNT(DISTINCT comment.postID), 0) AS comments_count,
                COALESCE(COUNT(DISTINCT engagement.postID), 0) AS likes_count
            FROM post
            JOIN users ON post.userID = users.userID
            LEFT JOIN comment ON post.postID = comment.postID
            LEFT JOIN engagement ON post.postID = engagement.postID AND engagement."like" = TRUE
        """

        if loaded_post_ids:
            query += f" WHERE post.postID NOT IN ({', '.join(map(str, loaded_post_ids))})"

        query += """
            GROUP BY post.postID, post.caption, post.timestamp, post.image, post.userID, 
                    users.username, users.profilePicture, users.name, users.registerDate
            ORDER BY post.timestamp DESC
            LIMIT %s;
        """

        try:
            self.execute_query(query, (limit,), cursor_type='dict')
            results = self.db_connection.cur.fetchall()

            if not results:
                return []

            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []