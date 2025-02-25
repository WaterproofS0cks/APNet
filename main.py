from flask import Flask, render_template
from auth import auth
from user_profile import user_profile
from page import page
import psycopg2
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user_profile, url_prefix="/user")
app.register_blueprint(page, url_prefix="/page")
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(days=1)

conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Users (
            id SERIAL NOT NULL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
			fullname VARCHAR(255) NOT NULL,
            bio VARCHAR(255),
            link VARCHAR(255),
            role CHAR(1) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            gender CHAR(1),
			RegisterDate DATE NOT NULL,
			LastLogin TIMESTAMP,
			ProfilePicture VARCHAR(255),
            Penalty CHAR(1)
            );
""")

conn.commit()
conn.close()

@app.route('/terms-of-service', methods=['GET'])
def TermsAndCondition():
    return render_template("termsofservice.html")

if __name__ == "__main__":
    app.run(debug=True)