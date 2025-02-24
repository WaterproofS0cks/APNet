from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

user_profile = Blueprint("user_profile", __name__, static_folder="static", template_folder="templates")

@user_profile.route('/profile', methods=["POST", "GET"])
def profile():
    if "user" in session:
        if request.method == "POST":
            return render_template("profile.html")
        else:
            if session.get('pfp') == None:
                session['pfp'] = url_for('static', filename='src/img/default-pfp.png')
            return render_template("profile.html", name = session.get('user'), pfp = session['pfp'], bio = session['bio'])
    else:
        return redirect(url_for('auth.login'))
    
@user_profile.route('/setting', methods=['POST', 'GET'])
def setting():
    if "user" in session:
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
        cur = conn.cursor()
        if request.method == "POST":
            new_data = request.form
            if new_data['username'] != '':
                try:
                    cur.execute("UPDATE Users SET username = %s WHERE username = %s", (new_data['username'], session.get('user')))
                    session['user'] = new_data['username']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', errmsg="Username Already Exist.")
            if new_data['bio'] != '':
                cur.execute("UPDATE Users SET bio = %s WHERE username = %s", (new_data['bio'], session.get('user')))
                session['bio'] = new_data['bio']
            if new_data['pfp'] != '':
                cur.execute("UPDATE Users SET pfp = %s WHERE username = %s", (new_data['pfp'], session.get('user')))
                session['pfp'] = new_data['pfp']
            if new_data['name'] != '':
                cur.execute("UPDATE Users SET pfp = %s WHERE username = %s", (new_data['name'], session.get('user')))
                session['pfp'] = new_data['pfp']
            if new_data['email'] != '':
                try:
                    cur.execute("UPDATE Users SET username = %s WHERE username = %s", (new_data['email'], session.get('email')))
                    session['email'] = new_data['email']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', erremail="Email Already Exist.")
            conn.commit()
            conn.close()
            return redirect('/user/profile')
        else:
            return render_template("settings.html")
    else:
        return redirect(url_for('auth.login'))