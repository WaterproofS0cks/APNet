from psycopg2.extras import DictCursor
from flask import session

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

            return self.db_connection.cur
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

    def retrieve(self, tablename, columns="*", condition=None, params=None, join="", order=""):
        query = f"SELECT {columns} FROM {tablename} {join}"
        if condition:
            query += f" WHERE {condition}"
        if order:
            query += f" {order}"
        query += ";"
        self.execute_query(query, params, cursor_type='dict')
        return self.db_connection.cur.fetchall()
    
    def retrieve_one(self, tablename, columns="*", condition=None, params=None):
        query = f'SELECT {columns} FROM {tablename}'
        if condition:
            query += f' WHERE {condition}'
        query += ";"
        self.execute_query(query, params, cursor_type='dict')
        return self.db_connection.cur.fetchone()

    def retrieve_actively_penalized(self):
        query = """
            SELECT u.userid, u.username, ph.description, ph.penaltyType
            FROM Users u
            JOIN PenaltyHistory ph ON u.userID = ph.userID
            WHERE u.penalty IS NOT NULL
            AND ph.timestamp = (
                SELECT MAX(timestamp) FROM PenaltyHistory 
                WHERE userID = u.userID
            )
        """
        self.execute_query(query, cursor_type='dict')
        return self.db_connection.cur.fetchall()



    def base_post_query(self):
        query = """
            SELECT 
                post.postID AS id,
                post.description, 
                TO_CHAR(post.timestamp, 'DD Month YYYY') AS timestamp, 
                post.image, 
                post.userID, 
                users.username, 
                users.profilePicture, 
                users.fullname,
                users.registerDate,
                COALESCE(COUNT(DISTINCT comment.postCommentID), 0) AS comments_count,
                COALESCE(COUNT(DISTINCT engagement.userID), 0) AS likes_count
            FROM post
            JOIN users ON post.userID = users.userID
            LEFT JOIN postcomment AS comment ON post.postID = comment.postID
            LEFT JOIN postengagement AS engagement ON post.postID = engagement.postID
        """
        return query

    def base_recruitment_query(self):
        query = """
            SELECT 
                recruitment.recruitmentID AS id, 
                recruitment.header, 
                recruitment.description, 
                TO_CHAR(recruitment.timestamp, 'DD Month YYYY') AS timestamp, 
                recruitment.image, 
                recruitment.userID, 
                users.username, 
                users.profilePicture, 
                users.fullname,
                users.registerDate,
                COALESCE(COUNT(DISTINCT comment.recruitmentCommentID), 0) AS comments_count,
                COALESCE(COUNT(DISTINCT engagement.userID), 0) AS likes_count
            FROM recruitment
            JOIN users ON recruitment.userID = users.userID
            LEFT JOIN recruitmentcomment AS comment ON recruitment.recruitmentID = comment.recruitmentID
            LEFT JOIN recruitmentengagement AS engagement ON recruitment.recruitmentID = engagement.recruitmentID
        """
        return query
    
    def retrieve_entries(self, post_type, page_type, entries_per_page, loaded_ids, search_term, user_id=None):
        params = []

        if post_type == "post":
            table_name = "post"
            id_column = "post.postID"
            search_column = "post.description"
            timestamp_column = "post.timestamp"
            user_id_column = "post.userID"
            base_query = self.base_post_query()

        elif post_type == "recruitment":
            table_name = "recruitment"
            id_column = "recruitment.recruitmentID"
            search_column = "recruitment.header"
            timestamp_column = "recruitment.timestamp"
            user_id_column = "recruitment.userID"
            base_query = self.base_recruitment_query()
        else:
            return []
        if page_type == "bookmark" and user_id:
            base_query += " WHERE engagement.bookmark = TRUE AND engagement.userID = %s"
            params.append(user_id)

        elif page_type == "liked" and user_id:
            base_query += " WHERE engagement.liked = TRUE AND engagement.userID = %s"
            params.append(user_id)

        elif page_type == "self" and user_id:
            base_query += f" WHERE {user_id_column} = %s"
            params.append(user_id)


        if loaded_ids:
            base_query += " AND " if "WHERE" in base_query else " WHERE "
            base_query += f"{id_column} NOT IN ({','.join(['%s'] * len(loaded_ids))})"
            params.extend(loaded_ids)

        if search_term:
            base_query += " AND " if "WHERE" in base_query else " WHERE "
            base_query += f"{search_column} ILIKE %s"
            params.append(f"%{search_term}%")

        base_query += f"""
            GROUP BY {id_column}, {user_id_column}, users.username, users.profilePicture, users.fullname, 
                    {table_name}.description, {table_name}.timestamp, {table_name}.image, users.registerDate
            ORDER BY {timestamp_column} DESC 
            LIMIT %s
        """
        params.append(entries_per_page)
        try:
            return self.execute_query(base_query, params, cursor_type='dict')
        except Exception as e:
            print("Database Query Error:", e)
            return []
