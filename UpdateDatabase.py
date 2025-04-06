import os
from werkzeug.utils import secure_filename

class dbInsert:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, query, params):
            if not params:
                raise ValueError("Params are required for insert")
            try:
                self.db_connection.cur.execute(query, params)
            except Exception as e:
                print(f"An error occurred during table insert: {e}")
                raise

    def find_table_columns(self, table_name):
        tables = {
            "Users": ["username", "fullname", "password", "role", "phone", "email", "gender", "link", "bio", "lastLogin", "profilePicture", "penalty"],
            "Recruitment": ["userID", "header", "description", "image", "status"],
            "RecruitmentComment": ["userID", "recruitmentID", "comment"],
            "RecruitmentEngagement": ["userID", "recruitmentID", "bookmark", "liked"],
            "Application": ["recruitmentID", "userID", "TPNumber", "eventPosition", "description", "status"],
            "Post": ["userID", "description", "image"],
            "PostComment": ["userID", "postID", "comment"],
            "PostEngagement": ["userID", "postID", "bookmark", "liked"],
            "Reports": ["placementID", "type", "status"],
            "PenaltyHistory": ["userID", "reportID", "penaltyType"],
            "Activity": ["userID"],
            "Notification": ["userID", "ActedUserID", "Action"]
        }
        return tables.get(table_name, [])
        
    def insert(self, table_name, data):
        columns = self.find_table_columns(table_name)

        if len(data) != len(columns):
            raise ValueError("Data length does not match table column count.")

        column_string = ", ".join(columns)
        placeholder_string = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({column_string}) VALUES ({placeholder_string}) RETURNING *;"
        
        self.execute_query(query, tuple(data))

        inserted_row = self.db_connection.cur.fetchone()

        column_names = [desc[0] for desc in self.db_connection.cur.description]
        result = {column_names[i]: inserted_row[i] for i in range(len(inserted_row))}

        self.db_connection.commit()
        
        return result

class dbModify(dbInsert):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def update(self, table_name, update_data, condition):
        valid_columns = self.find_table_columns(table_name)

        updates = {columns: update_data[columns] for columns in update_data if columns in valid_columns}
        if not updates:
            raise ValueError("No valid columns to update.")
        
        query = f"""
            UPDATE {table_name} 
            SET {", ".join(f"{columns} = %s" for columns in updates)}
            WHERE {" AND ".join(f"{columns} = %s" for columns in condition)};
        """

        params = tuple(updates.values()) + tuple(condition.values())
        print(params)
        print(query)
        self.execute_query(query, params)
        self.db_connection.conn.commit() 

    def delete(self, table_name, condition):

        where_clause = " AND ".join(f"{columns} = %s" for columns in condition)
        
        query = f"""
            DELETE FROM {table_name} 
            WHERE {where_clause};
        """
        
        params = tuple(condition.values())
        
        self.execute_query(query, params)
        self.db_connection.conn.commit()

    def toggle_engagement(self, user_id, post_id, action, post_type):
        if action not in ["liked", "bookmark"]:
            raise ValueError("Invalid action. Must be 'liked' or 'bookmark'.")

        if post_type == "post": 
            query = f"""
                INSERT INTO PostEngagement (userID, PostID, {action})
                VALUES (%s, %s, TRUE)
                ON CONFLICT (userID, PostID)
                DO UPDATE SET {action} = NOT PostEngagement.{action}
                RETURNING {action};
            """
        
        elif post_type == "recruitment": 
            query = f"""
                INSERT INTO RecruitmentEngagement (userID, RecruitmentID, {action})
                VALUES (%s, %s, TRUE)
                ON CONFLICT (userID, RecruitmentID)
                DO UPDATE SET {action} = NOT RecruitmentEngagement.{action}
                RETURNING {action};
            """

        cursor = self.db_connection.cur
        cursor.execute(query, (user_id, post_id))
        self.db_connection.conn.commit() 

        result = cursor.fetchone() 

        return result[0] if result else False 

class imageUploader:
    def __init__(self, upload_folder):
        self.upload_folder = os.path.join(upload_folder) 
        os.makedirs(self.upload_folder, exist_ok=True)  

    def upload(self, file):
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath) 
            return filepath  

        return None