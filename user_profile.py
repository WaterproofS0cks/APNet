from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

user_profile = Blueprint("user_profile", __name__, static_folder="static", template_folder="templates")

@user_profile.route('/profile', methods=['POST', 'GET'])
def profile():
    if "user" in session:
        if request.method == "GET":
            print(session.get("pfp"))
            return render_template("profile.html", name = session.get('user'), bio = session.get('bio'), link = session.get('link'))
    else:
        return redirect(url_for('auth.login'))
    
@user_profile.route('/settings', methods=['POST', 'GET'])
def setting():
    if "user" in session:
        if request.method == "POST":
            return redirect('/user/profile')
        else:
            return render_template("settings.html")
    else:
        return redirect(url_for('auth.login'))
    
@user_profile.route('/updateProfile', methods=['POST'])
def updateProfile():
    if "user" in session:
        if request.method == "POST":
            conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
            cur = conn.cursor()
            new_data = request.form
            if new_data['pfp'] != '':
                cur.execute("UPDATE Users SET pfp = %s WHERE username = %s", (new_data['pfp'], session.get('user')))
                session['pfp'] = new_data['pfp']
            if new_data['username'] != '':
                try:
                    cur.execute("UPDATE Users SET username = %s WHERE username = %s", (new_data['username'], session.get('user')))
                    session['user'] = new_data['username']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', erruser="Username Already Exist.")
            if new_data['bio'] != '':
                try:
                    cur.execute("UPDATE Users SET bio = %s WHERE username = %s", (new_data['bio'], session.get('user')))
                    session['bio'] = new_data['bio']
                except psycopg2.errors.StringDataRightTruncation:
                    return render_template('settings.html', errbio="Bio max length 255 characters.")
            if new_data['link'] != '':
                try:
                    cur.execute("UPDATE Users SET link = %s WHERE username = %s", (new_data['link'], session.get('user')))
                    session['link'] = new_data['link']
                except psycopg2.errors.StringDataRightTruncation:
                    return render_template('settings.html', errbio="Link max length 255 characters.")
            conn.commit()
            conn.close()
            return redirect('/user/profile')
        else:
            return redirect("/user/profile")
    else:
        return redirect(url_for("auth.login"))
    
@user_profile.route('/updateAccount', methods=['POST'])
def updateAccount():
    if "user" in session:
        if request.method == "POST":
            conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
            cur = conn.cursor()
            new_data = request.form
            if new_data['fullname'] != '':
                cur.execute("UPDATE Users SET fullname = %s WHERE username = %s", (new_data['fullname'], session.get('user')))
                session['fullname'] = new_data['fullname']
            if new_data['email'] != '':
                try:
                    cur.execute("UPDATE Users SET email = %s WHERE username = %s", (new_data['email'], session.get('email')))
                    session['email'] = new_data['email']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', erremail="Email Already Exist.")
            conn.commit()
            conn.close()
            return redirect('/user/profile')
        else:
            return redirect("/user/profile")
    else:
        return redirect(url_for("auth.login"))

@user_profile.route('/events', methods=['POST', 'GET'])
def events():
    return render_template("events.html")

@user_profile.route('/likes', methods=['POST', 'GET'])
def likedPosts():
    return render_template("likedposts.html")

@user_profile.route('/bookmarks', methods=['POST', 'GET'])
def bookmarkedPosts():
    return render_template("bookmarkedposts.html")

@user_profile.route('/applications', methods=['POST', 'GET'])
def applications():
    return render_template("applications.html")

@user_profile.route('/otherprofile', methods=['POST', 'GET'])
def otherProfile():
    return render_template("otherprofile.html")