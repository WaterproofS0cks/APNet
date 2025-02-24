from flask import Blueprint, render_template, request, url_for, redirect, Response, session
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

page = Blueprint("page", __name__, static_folder="static", template_folder="templates")

@page.route('/forum', methods=['POST', 'GET'])
def forum():
    return render_template('homepage.html')