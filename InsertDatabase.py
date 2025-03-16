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
        if table_name == "Users":
            return ["username", "fullname", "password", "role", "phone", "email", "gender", "link", "bio", "lastLogin", "profilePicture", "penalty"]
        elif table_name == "Recruitment":
            return ["userID", "header", "description", "image", "status"]
        elif table_name == "RecruitmentComment":
            return ["userID", "recruitmentID", "comment"]
        elif table_name == "RecruitmentEngagement":
            return ["userID", "recruitmentID", "bookmark", "liked"]
        elif table_name == "Application":
            return ["recruitmentID", "userID", "TPNumber", "eventPosition", "description", "resume", "status"]
        elif table_name == "Post":
            return ["userID", "description", "image"]
        elif table_name == "PostComment":
            return ["userID", "postID", "comment"]
        elif table_name == "PostEngagement":
            return ["userID", "postID", "bookmark", "liked"]
        elif table_name == "Reports":
            return ["userID", "reportedUserID", "description", "status"]
        elif table_name == "PenaltyHistory":
            return ["userID", "reportID", "issuedBy", "penaltyType"]
        elif table_name == "Activity":
            return ["userID"]
        elif table_name == "Notification":
            return ["userID", "ActedUserID", "Action"]
        else:
            return []

        
    def to_join(self, columns):
        return ', '.join(columns)

    def insert(self, tablename, information):

        columns = self.find_table_columns(tablename)
        print(columns)
        if len(information) == len(columns):
        
            column_string = self.to_join(columns) 
            placeholder_string = self.to_join(['%s'] * len(columns))  

            query = f'INSERT INTO {tablename} ({column_string}) VALUES ({placeholder_string});'
            
            self.execute_query(query, tuple(information))  
            
            self.db_connection.commit() 



class imageUploader:
    def __init__(self, upload_folder, allowed_extensions=None):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions or {'png', 'jpg', 'jpeg', 'gif'}

        os.makedirs(self.upload_folder, exist_ok=True)
    
    def check_extension(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload(self, file):
        if file and self.allowed_extensions(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)

            file_extension = filename.rsplit('.', 1)[1].lower()
            return filename, file_extension
        
        return None, None