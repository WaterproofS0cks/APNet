from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from auth import auth
from user_profile import user_profile
# import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from werkzeug.exceptions import HTTPException


from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from CreateDatabase import dbCreate
from UpdateDatabase import dbModify, imageUploader, dbInsert
from ChartDatabase import dbChart
from LoadingContent import Content


load_dotenv()
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

db_conn = dbConnection( 
    dbname= os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
)

db_conn.connect()
db_create = dbCreate(db_conn)

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user_profile, url_prefix="/user")
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = os.path.join("static", "src", "post")
app.permanent_session_lifetime = timedelta(days=1)

db_create.create_database()
db_conn.commit()
db_conn.close()

uploader = imageUploader(app.config["UPLOAD_FOLDER"])

#Finished
@app.route("/get_session")
def get_session():
    user_id = session.get('id')
    print(user_id)
    if user_id:
        return jsonify({"session": user_id})
    return redirect(url_for("auth.login"))

#Finished
@app.route('/')
def forum():
    return render_template('forum.html')

#Finished
@app.route('/load_more')
def post():
    return Content.load_post()

#Finished
@app.route('/engagement', methods=['POST'])
def engagement():
    return Content.load_engagement()

#Finished
@app.route('/user/specificpost', methods=["GET", "POST"])
@app.route('/specificpost', methods=["GET", "POST"])
def specific_post():
    return Content.load_specific_forum()

@app.route('/user/specificrecruitment', methods=["GET", "POST"])
@app.route('/specificrecruitment', methods=["GET", "POST"])
def specific_recruitment():
    return Content.load_recruitment_forum()

#Finished
@app.route('/comment', methods=['GET'])
def comment():
    return Content.load_comment()

#Finished
@app.route("/createcomment", methods=["POST"])
def create_comment():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_insert = dbInsert(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    user_data = db_retrieve.retrieve_one("users", "username, profilepicture", "userid=%s", (user_id,))

    data = request.get_json()
    post_id = data.get("id")
    comment = data.get("comment")
    post_type = data.get("post_type")

    if post_type == "post":
        inserted = db_insert.insert("PostComment", (user_id, post_id, comment))
    elif post_type == "recruitment":
        inserted = db_insert.insert("RecruitmentComment", (user_id, post_id, comment))
    else:
        return redirect(url_for('auth.login'))
    comment_id = inserted.get("postcommentid")
    print("creating")
    return jsonify({ "username":user_data["username"], "pfp":user_data["profilepicture"], "comment_id":comment_id})

@app.route("/deletecomment", methods=["POST"])
def delete_comment():

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_modify = dbModify(db_conn)

    data = request.get_json()
    comment_id = data.get("comment_id")
    post_type = data.get("post_type")

    if post_type == "post":
        condition = {"postcommentid": comment_id}
        db_modify.delete("PostComment", condition)
    elif post_type == "recruitment":
        condition = {"recruitmentcommentid": comment_id}
        db_modify.delete("RecruitmentComment", condition)

    return jsonify({"delete": True})

#Finished  
@app.route('/create', methods=["GET", "POST"])
def create_post():
    if "user" in session:
        return render_template('createpost.html')
    else:
        return redirect(url_for('auth.login'))

@app.route("/createapplication", methods=["GET", "POST"])
def create_application():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_insert = dbInsert(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    recruitment = request.form.get("recruitmentid")
    eventposition = request.form.get("position")
    tpnumber = request.form.get("tpnumber")
    description = request.form.get("description")
    status = "Pending"

    check_recruitment = db_retrieve.retrieve_one("recruitment", "recruitmentid", "recruitmentid=%s and status=%s", (recruitment, True))
    
    if not check_recruitment:
        return redirect(url_for('Recruitment'))

    try:
        value = db_insert.insert("Application", (recruitment, user_id, tpnumber, eventposition, description, status))
        return redirect(url_for('Recruitment'))
    except Exception as e:
        return redirect(url_for('Recruitment'))

@app.route("/load_application", methods=["GET", "POST"])
def application():
    return Content.load_application()

@app.route("/load_applicant", methods=["GET", "POST"])
def applicant():
    return Content.load_applicants()

#Finished
@app.route('/upload', methods=["GET", "POST"])
def upload_post():
    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_insert = dbInsert(db_conn)

    if request.method == "POST":

        post_type = request.form["post_type"]
        user_id = session.get("id")
        caption = request.form["caption"]
        title = request.form.get("title", None)
        file = request.files.get('file')
           
        filename = None
        if file:
            filename = uploader.upload(file)

        if post_type == "forum":
            db_insert.insert("Post", [user_id, caption, filename])
        elif post_type == "recruitment":
            db_insert.insert("Recruitment", [user_id, title, caption, filename, True])

    return redirect("/")

#Finished
@app.route('/terms', methods=['GET'])
def TermsOfService():
    return render_template("termsofservice.html")



@app.route('/faq', methods=['GET'])
def FrequentlyAskedQuestions():
    return render_template("faq.html")



@app.route('/recruitment', methods=['POST', 'GET'])
def Recruitment():
    return render_template("recruitment.html")



@app.route('/recruitment-application', methods=['POST', 'GET'])
def RecruitmentApplication():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('auth.login'))

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_retrieve = dbRetrieve(db_conn)
    recruitmentid = request.args.get('postid') 

    recruitment = db_retrieve.retrieve_one("recruitment", "image", "recruitmentid=%s and status=%s", (recruitmentid, "true"))

    if not recruitment:
        return redirect(url_for('forum'))

    return render_template("recruitment_application.html", image=recruitment["image"], recruitmentid=recruitmentid)



@app.route('/dashboard', methods=['POST', 'GET'])
def Dashboard():
    db_conn = dbConnection( 
        dbname= os.getenv("DBNAME"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
    )
    db_conn.connect()

    database_value = request.form.get('database', 'users')
    filter_value = request.form.get('filter', 'all-time')
    # range_value = request.form.get('range', '1') 

    db_chart = dbChart(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    user_count_result = db_retrieve.retrieve("users", "COUNT(*)")
    user_count = user_count_result[0][0]

    post_count_result = db_retrieve.retrieve("post", "COUNT(*)")
    post_count = post_count_result[0][0]

    comment_count_result = db_retrieve.retrieve("postcomment", "COUNT(*)")
    comment_count = comment_count_result[0][0]

    recruitment_count_result = db_retrieve.retrieve("recruitment", "COUNT(*)")
    recruitment_count = recruitment_count_result[0][0]

    application_count_result = db_retrieve.retrieve("application", "COUNT(*)")
    application_count = application_count_result[0][0]

    banned_count_result = db_retrieve.retrieve("users", "COUNT(*)", "penalty = %s", ('b',))
    banned_count = banned_count_result[0][0]  

    muted_count_result = db_retrieve.retrieve("users", "COUNT(*)", "penalty = %s", ('m',))
    muted_count = muted_count_result[0][0]

    reported_count_result = db_retrieve.retrieve("reports", "COUNT(*)")
    reported_count = reported_count_result[0][0]

    # chart_html = chart.plot_graph(
    #     # duration=(filter_value, int(range_value)),
    #     duration = (filter_value, 1),
    #     tablename = database_value, 
    #     # column="registerdate", 
    #     # xLabel="Registration Date", 
    #     # yLabel="Number of Users", 
    #     # title="Registered Users Over Time", 
    #     # lineLabel="Registered Users"
    # )
    count = comment_count + recruitment_count

    chart_html = db_chart.set_graph(database_value, filter_value)

    db_conn.close()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'chart': chart_html})

    return render_template(
        "dashboard.html", 
        chart=chart_html, 
        filter_value=filter_value, 
        database_value=database_value, 
        # range_value=range_value, 
        user_count=user_count,
        post_count=post_count,
        comment_count=count,
        recruitment_count=recruitment_count,
        application_count=application_count,
        banned_count=banned_count, 
        muted_count=muted_count,
        reported_count=reported_count,
    )



@app.route('/load_tables', methods=['GET'])
def load_tables():
    penalized_users_table = Content.load_penalized_users_table()
    reported_users_table = Content.load_reported_user_table()
    reported_posts_table = Content.load_reported_post_table()

    return jsonify({
        "penalized_users": penalized_users_table,
        "reported_users": reported_users_table,
        "reported_posts": reported_posts_table
    })



@app.route("/update_penalty", methods=["POST"])
def update_penalty():
    data = request.json
    user_id = data.get("userId")
    action = data.get("action")

    if action == "Unban" or action == "Unmute":
        penalty_value = None

    dbModify.update("Users", {"penalty": penalty_value}, {"userID": user_id})
    return jsonify({"message": f"User {user_id} has been {action.lower()}ed."})


@app.route("/update_reported_user", methods=["POST"])
def update_reported_user():
    data = request.json
    user_id = data.get("userId")
    action = data.get("action")

    if action == "Ban":
        penalty_value = "B"
    elif action == "Mute":
        penalty_value = "M"

    dbModify.update("Users", {"penalty": penalty_value}, {"userID": user_id})
    return jsonify({"message": f"User {user_id} has been {action.lower()}ed."})


@app.route("/update_reported_post", methods=["POST"])
def update_reported_post():
    data = request.json
    post_id = data.get("postId")
    post_type = data.get("postType")
    action = data.get("action")

    if post_type == "Post":
        table_name = "Post"
    elif post_type == "Recruitment":
        table_name = "Recruitment"

    if action == "Remove":
        dbModify.update(table_name, {"status": False}, {"postID": post_id})
    elif action == "Dismiss":
        dbModify.update("Reports", {"status": "Rejected"}, {"placementID": post_id})

    return jsonify({"message": f"Post {post_id} has been {action.lower()}ed."})


@app.route('/about', methods=['GET'])
def AboutUs():
    return render_template('aboutus.html')


# Reports
@app.route('/reports', methods=['POST', 'GET'])
def Reports():
    return render_template("reports.html")


# [TODO] TEMPORARY ENDPOINTS: ADD A CUSTOM ID AT THE END TO LINK A SPECIFIC POST
@app.route('/edit/forum', methods=['GET'])
def EditForumPost():
    return render_template('editforumpost.html')

@app.route('/edit/recruitment', methods=['GET'])
def EditRecruitmentPost():
    return render_template('editrecruitmentpost.html')

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html",404)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return "<h1>Seems like the page you are trying to find does not exist.</h1>"

    return "<h1>Seems like the page you are trying to find does not exist.</h1>"

if __name__ == "__main__":
    app.run()