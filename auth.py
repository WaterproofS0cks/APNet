from flask import Blueprint, render_template, request, url_for, redirect, Response
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        client = request.form
        user = (client['email'], client['password'])
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        try:
            cur.execute("SELECT EXISTS (SELECT 1 FROM Users WHERE email = %s AND password = %s)", user)
            check = cur.fetchone()
            conn.close()
            if check[0]:
                return redirect(url_for('profile.view_profile'))
            else:
                return Response(response="Username or email incorrect", status=401)
        except Exception as e:
            return Response(response=f"Username or email already exists. {e}", status=400)
    else:
        return render_template("login.html")
    
@auth.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        client = request.form
        date = datetime.now().strftime('%Y-%m-%d')
        user = (client['username'], client['fullname'], 'U', client['email'], client["password"], client["gender"], date)
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Users (username, fullname, role, email, password, gender, RegisterDate, LastLogin, ProfilePicture) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL)", user)          
            conn.commit()
            conn.close()
            return redirect(url_for('profile.view_profile'))
        except psycopg2.errors.UniqueViolation as e:
            return Response(response=f"Username or email already exists. {e}", status=400)
    else:
        return render_template("register.html")
    