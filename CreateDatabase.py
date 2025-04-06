class dbCreate:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, table_creation_query):
        try:
            self.db_connection.cur.execute(table_creation_query)
            self.db_connection.commit() 
        except Exception as e:
            print(f"Error table creation: {e}")

    def create_database(self):
        # Users Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Users (
                userID SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                fullname VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                role CHAR(1) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                gender CHAR(1),
                link VARCHAR(512),
                bio TEXT,
                registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lastLogin TIMESTAMP,
                profilePicture VARCHAR(512),
                penalty CHAR(1) 
            );
        """)

        # Recruitment Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Recruitment (
                recruitmentID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                header TEXT NOT NULL,
                description TEXT NOT NULL,
                image VARCHAR(512),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status BOOLEAN
            );
        """)

        # RecruitmentComment Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS RecruitmentComment (
                recruitmentCommentID SERIAL PRIMARY KEY,       
                userID INT NOT NULL REFERENCES Users(userID),
                recruitmentID INT NOT NULL REFERENCES Recruitment(recruitmentID) ON DELETE CASCADE,
                comment TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # RecruitmentEngagement Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS RecruitmentEngagement (
                userID INT NOT NULL REFERENCES Users(userID),
                recruitmentID INT NOT NULL REFERENCES Recruitment(recruitmentID) ON DELETE CASCADE,
                bookmark BOOLEAN DEFAULT FALSE,
                liked BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (userID, recruitmentID)
            );
        """)

        # Application Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Application (
                recruitmentID INT NOT NULL REFERENCES Recruitment(recruitmentID),
                userID INT NOT NULL REFERENCES Users(userID),
                TPNumber VARCHAR(10) NOT NULL,
                eventPosition VARCHAR(100),
                description TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(10) CHECK (status IN ('Pending', 'Accepted', 'Rejected')) NOT NULL,
                PRIMARY KEY (recruitmentID, userID)
            );
        """)

        # Post Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Post (
                postID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image VARCHAR(512)
            );
        """)

        # PostComment Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS PostComment (
                postCommentID SERIAL PRIMARY KEY,       
                userID INT NOT NULL REFERENCES Users(userID),
                postID INT NOT NULL REFERENCES Post(postID) ON DELETE CASCADE,
                comment TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # PostEngagement Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS PostEngagement (
                userID INT NOT NULL REFERENCES Users(userID),
                postID INT NOT NULL REFERENCES Post(postID) ON DELETE CASCADE,
                bookmark BOOLEAN DEFAULT FALSE,
                liked BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (userID, postID)
            );
        """)

        # Reports Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Reports (
                reportID SERIAL PRIMARY KEY,
                placementID INT NOT NULL,
                type VARCHAR(20) CHECK (type IN ('User', 'Forum', 'Recruitment')),     
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(10) CHECK (status IN ('Processing', 'Processed'))
            );
        """)

        # PenaltyHistory Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS PenaltyHistory (
                penaltyID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                reportID INT NOT NULL REFERENCES Reports(reportID) ON DELETE CASCADE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                penaltyType VARCHAR(20) CHECK (penaltyType IN ('Banned', 'Muted'))
            );
        """)

        # Activity Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Activity (
                activityID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Notification Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Notification (
                notificationID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                ActedUserID INT NOT NULL REFERENCES Users(userID),
                Action VARCHAR(20) CHECK (Action IN ('Comment', 'Liked', 'Reject Application', 'Accept Application')),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

