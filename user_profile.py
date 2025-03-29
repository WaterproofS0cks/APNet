from flask import Blueprint, current_app, render_template, request, session, redirect, url_for
from psycopg2.errors import StringDataRightTruncation
import psycopg2
import os
from dotenv import load_dotenv

from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from UpdateDatabase import dbModify, imageUploader

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

user_profile = Blueprint("user_profile", __name__, static_folder="static", template_folder="templates")

@user_profile.route('/profile', methods=['POST', 'GET'])
def profile():
    if "user" in session:
        if request.method == "GET" and request.args.get('uid') == None:
            return render_template("profile.html", name = session.get('user'), bio = session.get('bio'), link = session.get('link'))
        elif request.method == "GET" and request.args.get('uid') != None:
            value = request.args.get('uid')
            db_conn = dbConnection(
                dbname=os.getenv("DBNAME"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
            )

            db_conn.connect()
            db_retrieve = dbRetrieve(db_conn)

            user_data = db_retrieve.retrieve_one("users", "*", "username = %s", (value,))
            return render_template("profile.html", pfp = user_data['profilepicture'], name = user_data['username'], bio = user_data['bio'], link = user_data['link'])
    else:
        return redirect(url_for('auth.login'))
    
@user_profile.route('/settings', methods=['POST', 'GET'])
def setting():
    if "user" in session:
        if request.method == "POST":
            return redirect('/user/profile')
        else:
            
            db_conn = dbConnection(
                dbname=os.getenv("DBNAME"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
            )

            db_conn.connect()
            db_retrieve = dbRetrieve(db_conn)
            user_id = session.get("id")

            user_data = db_retrieve.retrieve_one("users", "*", "userid = %s", (user_id,))

            erruser = request.args.get("erruser")
            errbio = request.args.get("errbio")
            errlink = request.args.get("errlink")

            return render_template(
                "settings.html",
                pfp=user_data["profilepicture"],
                username=user_data["username"],
                bio=user_data["bio"] if user_data["bio"] else "",
                link=user_data["link"] if user_data["link"] else "",
                fullname=user_data["fullname"],
                email=user_data["email"],
                phone=user_data["phone"],
                erruser=erruser if erruser else "",
                errbio=errbio if errbio else "",
                errlink=errlink if errlink else ""
                )
    else:
        return redirect(url_for('auth.login'))
    
# @user_profile.route('/updateProfile', methods=['POST'])
# def updateProfile():
#     if "user" in session:
#         if request.method == "POST":
#             conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
#             cur = conn.cursor()
#             new_data = request.form
#             if new_data['pfp'] != '':
#                 cur.execute("UPDATE Users SET pfp = %s WHERE username = %s", (new_data['pfp'], session.get('user')))
#                 session['pfp'] = new_data['pfp']
#             if new_data['username'] != '':
#                 try:
#                     cur.execute("UPDATE Users SET username = %s WHERE username = %s", (new_data['username'], session.get('user')))
#                     session['user'] = new_data['username']
#                 except psycopg2.errors.UniqueViolation:
#                     return render_template('settings.html', erruser="Username already exist.")
#             if new_data['bio'] != '':
#                 try:
#                     cur.execute("UPDATE Users SET bio = %s WHERE username = %s", (new_data['bio'], session.get('user')))
#                     session['bio'] = new_data['bio']
#                 except psycopg2.errors.StringDataRightTruncation:
#                     return render_template('settings.html', errbio="Bio max length 255 characters.")
#             if new_data['link'] != '':
#                 try:
#                     cur.execute("UPDATE Users SET link = %s WHERE username = %s", (new_data['link'], session.get('user')))
#                     session['link'] = new_data['link']
#                 except psycopg2.errors.StringDataRightTruncation:
#                     return render_template('settings.html', errlink="Link max length 512 characters.")
#             conn.commit()
#             conn.close()
#             return redirect('/user/profile')
#         else:
#             return redirect("/user/profile")
#     else:
#         return redirect(url_for("auth.login"))
    
@user_profile.route('/updateAccount', methods=['POST'])
def updateAccount():
    if "user" in session:
        if request.method == "POST":
            conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
            cur = conn.cursor()
            new_data = request.form
            if new_data['fullname'] != '':
                try:
                    cur.execute("UPDATE Users SET fullname = %s WHERE username = %s", (new_data['fullname'], session.get('user')))
                    session['fullname'] = new_data['fullname']
                except psycopg2.errors.StringDataRightTruncation:
                    return render_template('settings.html', errname="Full name max length 255 characters.")
            if new_data['email'] != '':
                try:
                    cur.execute("UPDATE Users SET email = %s WHERE username = %s", (new_data['email'], session.get('email')))
                    session['email'] = new_data['email']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', erremail="Email already exist.")
            if new_data['email'] != '':
                try:
                    cur.execute("UPDATE Users SET phone = %s WHERE username = %s", (new_data['phone'], session.get('phone')))
                    session['phone'] = new_data['phone']
                except psycopg2.errors.UniqueViolation:
                    return render_template('settings.html', erremail="Phone Number already exist.")
            conn.commit()
            conn.close()
            return redirect('/user/profile')
        else:
            return redirect("/user/profile")
    else:
        return redirect(url_for("auth.login"))

@user_profile.route('/likes', methods=['POST', 'GET'])
def likedPosts():
    return render_template("likedposts.html")

@user_profile.route('/bookmarks', methods=['POST', 'GET'])
def bookmarkedPosts():
    return render_template("bookmarkedposts.html")

@user_profile.route('/otherprofile', methods=['POST', 'GET'])
def otherProfile():
    return render_template("otherprofile.html")


# Applications Pages
@user_profile.route('/applications', methods=['POST', 'GET'])
def applications():
    return render_template("applications.html")

@user_profile.route('/applications-applied', methods=['POST', 'GET'])
def applicationsApplied():
    return render_template("applications_applied.html")

@user_profile.route('/applications-created', methods=['POST', 'GET'])
def applicationsCreated():
    return render_template("applications_created.html")

@user_profile.route('/updateProfile', methods=['POST'])
def updateProfile():
    if "id" not in session:
        return redirect(url_for("auth.login"))

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_modify = dbModify(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    user_id = session.get("id")
    pfp = request.files.get("pfp")
    username = request.form.get("username")
    bio = request.form.get("bio")
    link = request.form.get("link")

    uploader = imageUploader(current_app.config["UPLOAD_FOLDER"])

    pfp_filename = session.get("pfp", "/static/src/img/default-pfp.png")
    if pfp:
        pfp_filename = uploader.upload(pfp)

    try:
        if username:
            existing_user = db_retrieve.retrieve_one("users", "userid", "username = %s", (username,))
            if existing_user and existing_user[0] != user_id:
                return redirect(url_for("user_profile.setting", erruser="Username already exists."))

        data = {"profilePicture": pfp_filename, "username": username, "bio": bio, "link": link}
        condition = {"userid": user_id}
        
        if not username:
            return redirect(url_for("user_profile.setting", erruser="Username cannot be empty"))

        db_modify.update("Users", data, condition)

        session["pfp"] = pfp_filename
        session["username"] = username
        session["bio"] = bio
        session["link"] = link

    except StringDataRightTruncation as e:
        if "bio" in str(e):
            return redirect(url_for("user_profile.setting", errbio="Bio max length 255 characters."))
        if "link" in str(e):
            return redirect(url_for("user_profile.setting", errlink="Link max length 512 characters."))

    return redirect("/user/profile")


# @user_profile.route('/updateAccount', methods=['POST'])
# def updateProfile():

#     db_conn = dbConnection(
#         dbname=os.getenv("DBNAME"),
#         user=os.getenv("USER"),
#         password=os.getenv("PASSWORD"),
#     )

#     db_conn.connect()
#     db_modify = dbModify(db_conn)

#     if request.method == "POST":

#         user_id = session.get("id")
#         fullname = request.form.get("fullname")
#         email = request.form.get("email")

#         data = {"fullname": fullname, "email": email}
#         condition = {"userid": user_id}

#     db_modify.update("users", data, condition)

#     return redirect("profile")


