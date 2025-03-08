class dbCreate:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute_query(self, table_creation_query):
        try:
            self.db_connection.cur.execute(table_creation_query)
            self.db_connection.commit() 
            print(f"Table creation successful")
        except Exception as e:
            print(f"Error table creation: {e}")

    def create_database(self):
        # Users Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Users (
                userID SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                fullname VARCHAR(255) NOT NULL,
                role CHAR(1) NOT NULL CHECK (role IN ('A', 'L', 'S')),
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(50) NOT NULL,
                gender CHAR(1) NOT NULL CHECK (gender IN ('F', 'M')),
                link VARCHAR(255),
                bio TEXT,
                registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lastLogin TIMESTAMP,
                profilePicture VARCHAR(255),
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
                image VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status BOOLEAN
            );
        """)

        # Resume Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Resume (
                resumeID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                description TEXT NOT NULL,
                image VARCHAR(255)
            );
        """)

        # Application Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Application (
                recruitmentID INT NOT NULL REFERENCES Recruitment(recruitmentID),
                resumeID INT NOT NULL REFERENCES Resume(resumeID),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status CHAR(1) NOT NULL CHECK (status IN ('A', 'R', 'P')),
                PRIMARY KEY (recruitmentID, resumeID)
            );
        """)

        # Post Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Post (
                postID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                caption TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image VARCHAR(255)
            );
        """)

        # Comment Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Comment (
                userID INT NOT NULL REFERENCES Users(userID),
                postID INT NOT NULL REFERENCES Post(postID),
                comment TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Engagement Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Engagement (
                userID INT NOT NULL REFERENCES Users(userID),
                postID INT NOT NULL REFERENCES Post(postID),
                bookmark BOOLEAN,
                "like" BOOLEAN,
                PRIMARY KEY (userID, postID)
            );
        """)

        # PenaltyHistory Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS PenaltyHistory (
                penaltyID SERIAL PRIMARY KEY,
                penaltyType CHAR(1) NOT NULL CHECK (penaltyType IN ('B', 'M')),
                duration INT NOT NULL,  -- Added data type for the duration column
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status BOOLEAN,
                description TEXT
            );
        """)

        # Reports Table
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS Reports (
                reportID SERIAL PRIMARY KEY,
                userID INT NOT NULL REFERENCES Users(userID),
                type CHAR(1) NOT NULL CHECK (type IN ('H', 'S', 'N', 'V')),
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status CHAR(1) NOT NULL CHECK (status IN ('P','R','A'))
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