from flask import Blueprint, render_template, request, session, redirect, url_for
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
        if request.method == "POST":
            return render_template("settings.html")
        else:
            return render_template("settings.html")
    else:
        return redirect(url_for('auth.login'))