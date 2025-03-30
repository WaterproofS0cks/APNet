from flask import Blueprint, render_template, request, url_for, redirect, Response, session
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import smtplib
import random

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
MAILTRAP_PASSWORD = os.getenv("MAILTRAP_PASSWORD")

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
                cur.execute("SELECT userid, username, fullname, bio, link, role, email, gender, profilepicture, penalty FROM Users WHERE email = %s LIMIT 1", (client['email'],))
                user_data = cur.fetchone()
                conn.close()
                session.permanent = True
                session['id'] = user_data[0]
                session['user'] = user_data[1]
                session['fname'] = user_data[2]
                session['bio'] = user_data[3]
                session['link'] = user_data[4]
                session['role'] = user_data[5]
                session['email'] = user_data[6]
                session['gender'] = user_data[7]
                session['pfp'] = user_data[8]
                session['penalty'] = user_data[9]
                #[TODO] Add entry to Activity Table
                return redirect('/')
            else:
                return render_template("login.html", errmsg="Email or Password incorrect. Please try again")
        except Exception as e:
            return Response(response=e)
    else:
        return render_template("login.html")
    
@auth.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        client = request.form
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = (client['username'], client['fullname'], 'U', client['email'], client["password"], client["phone"], client["gender"], date.split(" ")[0], date, "/static/src/img/default-pfp.png")
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Users (username, fullname, bio, link, role, email, password, phone, gender, registerdate, lastLogin, profilepicture, penalty) VALUES (%s, %s, NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s, NULL)", user)      
            conn.commit()
            cur.execute("SELECT userid, username, fullname, bio, link, role, email, gender, profilepicture, penalty FROM USERS WHERE email = %s LIMIT 1", (client['email'],))
            user_data = cur.fetchone()
            conn.close()
            session.permanent = True
            session['id'] = user_data[0]
            session['user'] = user_data[1]
            session['fname'] = user_data[2]
            session['bio'] = user_data[3]
            session['link'] = user_data[4]
            session['role'] = user_data[5]
            session['email'] = user_data[6]
            session['gender'] = user_data[7]
            session['pfp'] = user_data[8]
            session['penalty'] = user_data[9]
            #[TODO] Add entry to Activity Table
            return redirect('/')
        except psycopg2.errors.UniqueViolation:
            return render_template("register.html", errmsg="Username or Email already exist. Please try again")
    else:
        return render_template("register.html")

@auth.route('/resetpassword/1', methods=["POST", "GET"])
def resetpassword():
    if request.method == "POST":
        email = request.form['email']
        code = str(random.randint(100000,999999))
        sender = "no-reply@demomailtrap.co"
        receiver = email.strip()
        message = f"""\
Subject: APNet - Reset Password
To: {receiver}
From: {sender}

Your code is {code}

If you did not attempt to reset your password. Please ignore this message."""
        
        session['reset_code'] = code
        session['target_email'] = email
        print(MAILTRAP_PASSWORD+'\n\n\n\n\nabcdefg')

        with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
            server.starttls()
            server.login("api", MAILTRAP_PASSWORD)
            server.sendmail(sender, receiver, message)
        return redirect(url_for('.resetpassword_code'))
    else:
        return render_template("resetpassword.html")

@auth.route("/resetpassword/2", methods=["POST", "GET"])
def resetpassword_code():
    if "target_email" in session:
        if request.method == "POST":
            if session.get("reset_code") == request.form['code']:
                return redirect(url_for('.resetpassword_password'))
            else:
                return render_template("resetpassword_code.html", errcode="Incorrect code.")
        else:
            return render_template("resetpassword_code.html")
    else:
        return redirect(url_for(".resetpassword"))
    
@auth.route("/resetpassword/3", methods=['POST', 'GET'])
def resetpassword_password():
    if "target_email" in session:
        if request.method == "POST":
            conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
            cur = conn.cursor()
            cur.execute("UPDATE Users SET password = %s WHERE email = %s", (request.form['new-password'], session.get('target_email')))
            conn.commit()
            conn.close()
            session.pop("reset_code")
            session.pop("target_email")
            return redirect(url_for(".resetpassword_complete"))
        else: 
            return render_template("resetpassword_new_password.html")
    else:
        return redirect(url_for(".resetpassword"))
    
@auth.route("/resetpassword/4", methods=['GET'])
def resetpassword_complete():
    return render_template("resetpassword_complete.html")
    

@auth.route('/logout')
def logout():
    session_data = ['id', 'user', 'fname', 'bio', 'link', 'role', 'email', 'gender', 'pfp', 'penalty', 'fullname', 'phone']
    for i in session_data:
        session.pop(i, None)
    print(session)
    return redirect(url_for('.login'))