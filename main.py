from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from auth import auth
from user_profile import user_profile
# import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


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
app.permanent_session_lifetime = timedelta(days=1)

db_create.create_database()
db_conn.commit()
db_conn.close()



@app.route("/session")
def check_session():
    user_id = session.get('id')
    if user_id:
        return jsonify({"session": True})
    return jsonify({"session": False})



@app.route('/')
def forum():
    return render_template('forum.html')



@app.route('/load_more')
@app.route('/recruitment/load_more')
def post():
    return Content.load_post()



@app.route('/engagement', methods=['POST'])
def engagement():
    return Content.load_engagement()



@app.route('/specificpost', methods=["GET", "POST"])
def specific_post():
    return Content.load_specific_forum()
    
@app.route('/create', methods=["GET", "POST"])
def create_post():
    return render_template('createpost.html')

def upload_post():
    post_type = request.form["post_type"]
    user_id = request.form["userID"]
    caption = request.form["caption"]
    title = request.form.get("title") 
    filename, _ = imageUploader.upload(request.files.get("image")) if "image" in request.files else (None, None)

    try:
        if post_type == "forum":
            dbInsert.insert("Post", [user_id, caption, filename])
        elif post_type == "recruitment":
            dbInsert.insert("Post", [user_id, title, caption, filename])

        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

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
    return render_template("recruitment_application.html")



@app.route('/dashboard', methods=['POST', 'GET'])
def Dashboard():
    db_conn = dbConnection( 
        dbname= os.getenv("DBNAME"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
    )
    db_conn.connect()

    filter_value = request.form.get('filter', 'all-time')
    database_value = request.form.get('database', 'users')
    # range_value = request.form.get('range', '1') 

    db_chart = dbChart(db_conn)
    db_retrieve = dbRetrieve(db_conn)

    user_count_result = db_retrieve.retrieve("users", "COUNT(*)")
    user_count = user_count_result[0][0]

    # post_count_result = db_retrieve.retrieve("post", "COUNT(*)")
    # post_count = post_count_result[0][0]

    # comment_count_result = db_retrieve.retrieve("comment", "COUNT(*)")
    # comment_count = comment_count_result[0][0]

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
        # post_count=post_count,
        # comment_count=comment_count,
        recruitment_count=recruitment_count,
        application_count=application_count,
        banned_count=banned_count, 
        muted_count=muted_count,
        reported_count=reported_count
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


@app.route('/aboutus', methods=['GET'])
def AboutUs():
    return render_template('aboutus.html')



if __name__ == "__main__":
    app.run(debug=True)