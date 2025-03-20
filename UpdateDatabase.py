import os
from werkzeug.utils import secure_filename

class dbInsert:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, query, params):
            if not params:
                raise ValueError("Params are required for insert")
            try:
                print(f"Executing query: {query}")
                print(f"With parameters: {params}")
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
            "Application": ["recruitmentID", "userID", "TPNumber", "eventPosition", "description", "resume", "status"],
            "Post": ["userID", "description", "image"],
            "PostComment": ["userID", "postID", "comment"],
            "PostEngagement": ["userID", "postID", "bookmark", "liked"],
            "Reports": ["userID", "reportedUserID", "description", "status"],
            "PenaltyHistory": ["userID", "reportID", "issuedBy", "penaltyType"],
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

        query = f"INSERT INTO {table_name} ({column_string}) VALUES ({placeholder_string});"
        
        self.execute_query(query, tuple(data))
        self.db_connection.commit()



class dbModify(dbInsert):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def update(self, table_name, update_data, condition):
        if not update_data or not condition:
            raise ValueError("Update data and condition cannot be empty.")

        valid_columns = self.find_table_columns(table_name)

        updates = {col: update_data[col] for col in update_data if col in valid_columns}
        conditions = {col: condition[col] for col in condition if col in valid_columns}

        if not updates:
            raise ValueError("No valid columns to update.")
        if not conditions:
            raise ValueError("No valid condition columns provided.")
        
        query = f"""
            UPDATE {table_name} 
            SET {", ".join(f"{col} = %s" for col in updates)}
            WHERE {" AND ".join(f"{col} = %s" for col in conditions)};
        """

        params = tuple(updates.values()) + tuple(conditions.values())

        self.execute_query(query, params)

    def toggle_engagement(self, user_id, post_id, action):
        if action not in ["liked", "bookmark"]:
            raise ValueError("Invalid action. Must be 'liked' or 'bookmark'.")

        query = f"""
            INSERT INTO PostEngagement (userID, PostID, {action})
            VALUES (%s, %s, TRUE)
            ON CONFLICT (userID, PostID)
            DO UPDATE SET {action} = NOT PostEngagement.{action}
            RETURNING {action};
        """

        print("Executing Query:", query)
        print("With Values:", (user_id, post_id))

        cursor = self.db_connection.cur
        cursor.execute(query, (user_id, post_id))
        self.db_connection.conn.commit() 

        result = cursor.fetchone() 
        print("Query Result:", result)

        return result[0] if result else False 


class imageUploader:
    def __init__(self, upload_folder, allowed_extensions=None):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions or {"png", "jpg", "jpeg", "gif"}
        os.makedirs(self.upload_folder, exist_ok=True)

    def check_extension(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def upload(self, file):
        if file and self.check_extension(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)

            file_extension = filename.rsplit(".", 1)[1].lower()
            return filename, file_extension
        
        return None, None