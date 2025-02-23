from flask import Blueprint, render_template, request, url_for, redirect, Response
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

profile = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

@profile.route('/profile', methods=["POST", "GET"])
def view_profile():
    if request.method == "POST":
        return 0
    else:
        return render_template("profile.html")