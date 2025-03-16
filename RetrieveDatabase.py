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
    
    def retrieve_one(self, tablename, columns="*", condition=None, params=None):
        query = f'SELECT {columns} FROM "{tablename}"'
        if condition:
            query += f' WHERE {condition}'
        query += ";"
        self.execute_query(query, params, cursor_type='dict')
        return self.db_connection.cur.fetchone()

    def retrieve_entries(self, type, limit=5, loaded_ids=None, searched_term=''):
        if type == "post":
            query = """
                SELECT 
                    post.postID,
                    post.description, 
                    TO_CHAR(post.timestamp, 'DD-MM-YYYY') AS timestamp, 
                    post.image, 
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
            search_column = "post.description"
            timestamp_column = "post.timestamp"

        elif type == "recruitment":
            query = """
                SELECT 
                    recruitment.recruitmentID, 
                    recruitment.header, 
                    recruitment.description, 
                    TO_CHAR(recruitment.timestamp, 'DD-MM-YYYY') AS timestamp, 
                    recruitment.image, 
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
            timestamp_column = "recruitment.timestamp"

        else:
            print("Invalid entry type")
            return []

        # Apply filtering based on search term and loaded IDs
        conditions = []
        params = []

        if searched_term:
            conditions.append(f"{search_column} ILIKE %s")
            params.append(f"%{searched_term}%")

        if loaded_ids:
            placeholders = ", ".join(["%s"] * len(loaded_ids))
            conditions.append(f"{id_column} NOT IN ({placeholders})")
            params.extend(loaded_ids)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += f"""
            GROUP BY {id_column}, {search_column}, {timestamp_column}, 
                    post.image, users.username, users.profilePicture, 
                    users.fullname, users.registerDate
            ORDER BY {timestamp_column} DESC
            LIMIT %s;
        """

        params.append(limit)

        try:
            self.execute_query(query, tuple(params), cursor_type='dict')
            results = self.db_connection.cur.fetchall()
            return results if results else []
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
