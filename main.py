from flask import Flask, render_template, Response
from auth import auth
from user_profile import profile
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(profile, url_prefix="/user")

conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Users (
            id SERIAL NOT NULL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
			fullname VARCHAR (255) NOT NULL,
            role CHAR(1) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            gender CHAR(1),
			RegisterDate DATE NOT NULL,
			LastLogin TIMESTAMP,
			ProfilePicture VARCHAR(255)
            );
""")

conn.commit()
conn.close()

if __name__ == "__main__":
    app.run(debug=True)