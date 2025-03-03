from flask import Flask, render_template, request, jsonify
from auth import auth
from user_profile import user_profile
import psycopg2
import os
from dotenv import load_dotenv
from datetime import timedelta

from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from ChartDatabase import dbChart

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user_profile, url_prefix="/user")
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


@app.route('/', methods=['POST', 'GET'])
def Forum():
    return render_template("forum.html")

@app.route('/terms', methods=['GET'])
def TermsOfService():
    return render_template("termsofservice.html")

@app.route('/faq', methods=['GET'])
def FrequentlyAskedQuestions():
    return render_template("faq.html")

@app.route('/recruitment', methods=['POST', 'GET'])
def Recruitment():
    return render_template("recruitment.html")

@app.route('/dashboard', methods=['POST', 'GET'])
def Dashboard():
    db_conn = dbConnection( 
        dbname= os.getenv("DBNAME"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
    )
    db_conn.connect()

    filter_value = request.form.get('filter', 'days')
    range_value = request.form.get('range', '100') 

    chart = dbChart(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    user_count_result = db_retrieve.retrieve("users", "COUNT(*)")
    user_count = user_count_result[0][0]

    # post_count_result = db_retrieve.retrieve("post", "COUNT(*)")
    # post_count = post_count_result[0][0]

    banned_count_result = db_retrieve.retrieve("users", "COUNT(*)", "penalty = %s", ('b',))
    banned_count = banned_count_result[0][0]  

    muted_count_result = db_retrieve.retrieve("users", "COUNT(*)", "penalty = %s", ('m',))
    muted_count = muted_count_result[0][0]

    chart_html = chart.plot_registration_graph(
        # duration=(filter_value, int(range_value)),
        duration=(filter_value, 1),
        tablename="users", 
        column="registerdate", 
        xLabel="Registration Date", 
        yLabel="Number of Users", 
        title="Registered Users Over Time", 
        lineLabel="Registered Users"
    )

    db_conn.close()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'chart': chart_html})

    # [TO-DO] Removed post_count=post_count for now
    return render_template("dashboard.html", chart=chart_html, filter_value=filter_value, range_value=range_value, user_count=user_count, banned_count=banned_count, muted_count=muted_count)

if __name__ == "__main__":
    app.run(debug=True)