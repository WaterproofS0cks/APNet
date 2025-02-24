from flask import Blueprint, render_template, request, url_for, redirect, Response, session
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
        credentials = (client['email'], client['password'])
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        try:
            cur.execute("SELECT EXISTS (SELECT 1 FROM Users WHERE email = %s AND password = %s)", credentials)
            check = cur.fetchone()
            if check[0]:
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cur.execute("UPDATE Users SET LastLogin = %s WHERE email = %s", (date, client["email"]))
                conn.commit()
                cur.execute("SELECT * FROM Users WHERE email = %s LIMIT 1", (client['email'],))
                user_data = cur.fetchone()
                print(user_data)
                conn.close()
                session.permanent = True
                session['id'] = user_data[0]
                session['user'] = user_data[1]
                session['fname'] = user_data[2]
                session['bio'] = user_data[3]
                session['role'] = user_data[4]
                session['email'] = user_data[5]
                session['gender'] = user_data[7]
                session['pfp'] = user_data[10]
                session['penalty'] = user_data[11]
                print(session)
                return redirect('/user/profile')
            else:
                return render_template("login.html", errmsg="Username or Email incorrect. Please try again")
        except Exception as e:
            print('1')
            return Response(response=e)
    else:
        return render_template("login.html")
    
@auth.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        client = request.form
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = (client['username'], client['fullname'], 'U', client['email'], client["password"], client["gender"], date.split(" ")[0], date)
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Users (username, fullname, bio, role, email, password, gender, RegisterDate, LastLogin, ProfilePicture, Penalty) VALUES (%s, %s, NULL, %s, %s, %s, %s, %s, %s, NULL, NULL)", user)          
            conn.commit()
            cur.execute("SELECT * FROM Users WHERE email = %s LIMIT 1", (client['email'],))
            user_data = cur.fetchone()
            conn.close()
            session.permanent = True
            session['id'] = user_data[0]
            session['user'] = user_data[1]
            session['fname'] = user_data[2]
            session['bio'] = user_data[3]
            session['role'] = user_data[4]
            session['email'] = user_data[5]
            session['gender'] = user_data[7]
            session['pfp'] = user_data[10]
            session['penalty'] = user_data[11]
            return redirect('/user/profile')
        except psycopg2.errors.UniqueViolation:
            return render_template("register.html", errmsg="Username or Email already exist. Please try again")
    else:
        return render_template("register.html")

@auth.route('/resetpassword', methods=["POST", "GET"])
def resetpassword():
    conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
    cur = conn.cursor()
    code = 1234
    if request.method == "POST":
        email = request.form['email']
        cur.execute("SELECT EXISTS (SELECT 1 FROM Users WHERE email = %s)", (email,))
        check = cur.fetchone()
        conn.close()
        if check[0] == False:
            return render_template("login.html", errmsg="Email not found. Please try again")
        elif code != 1234:
            return render_template("login.html", errcode="Wrong code. Please try again")
    else:
        return render_template("resetpassword.html")

@auth.route('/logout')
def logout():
    session_data = ['id', 'user', 'fname', 'bio', 'role', 'email', 'gender', 'pfp', 'penalty']
    for i in session_data:
        session.pop(i, None)
    print(session)
    return redirect(url_for('.login'))