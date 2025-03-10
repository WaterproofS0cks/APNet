from flask import Flask, render_template, request, jsonify
from auth import auth
from user_profile import user_profile
import psycopg2
import os
from dotenv import load_dotenv
from datetime import timedelta
import json

from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from ChartDatabase import dbChart
from CreateDatabase import dbCreate
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

# conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD)
# cur = conn.cursor()

# cur.execute("""CREATE TABLE IF NOT EXISTS Users (
#             id SERIAL NOT NULL PRIMARY KEY,
#             username VARCHAR(255) UNIQUE NOT NULL,
# 			fullname VARCHAR(255) NOT NULL,
#             bio VARCHAR(255),
#             link VARCHAR(255),
#             role CHAR(1) NOT NULL,
#             email VARCHAR(255) UNIQUE NOT NULL,
#             password VARCHAR(255) NOT NULL,
#             gender CHAR(1),
# 			RegisterDate DATE NOT NULL,
# 			LastLogin TIMESTAMP,
# 			ProfilePicture VARCHAR(255),
#             Penalty CHAR(1)
#             );
# """)

# conn.commit()
# conn.close()


@app.route('/test')
def test():
    return render_template('likedposts.html')

@app.route('/')
def forum():
    return render_template('forum.html')

@app.route('/load_more_post')
def load_more_post():
    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_retrieve = dbRetrieve(db_conn)

    search_term = request.args.get('search', '')
    loaded_post_ids = request.args.get('loaded_post_ids', default='[]', type=str)
    posts_per_page = 5

    loaded_post_ids = json.loads(loaded_post_ids)

    posts = db_retrieve.retrieve_posts(posts_per_page, loaded_post_ids, search_term)

    if not posts:
        return jsonify({'post_html': '', 'no_more_posts': True})

    post_html = ''.join([f'''
        <div class="fm-post-layout" data-post-id="{post['postid']}">
            <div class="fm-profiledetails">
                <img src="/static/{post.get('profilePicture', 'src/img/default-pfp.png')}" alt="Pfp" id="fm-post-pfp">
                <h1>{post['username']}</h1>
                <h2>Posted on {post['post_timestamp']}</h2>

                <div class="fm-more-container">
                    <div class="dropdown">
                        <span><img src="../static/src/icon/icons8-ellipsis-48.png" alt="Elipses" class="fm-moreicon" data-post-id="{post['postid']}" height="24" width="24"></span>
                        <div class="dropdown-content">
                            <a href="#" class="dropdown-item">Item 1</a>
                            <a href="#" class="dropdown-item">Item 2</a>
                            <a href="#" class="dropdown-item">Item 3</a>
                        </div>
                    </div>
                </div>

            </div>

            <div class="fm-image-container">
                <img src="/static/{post['post_image']}" alt="Post Image">
            </div>

            <div class="fm-button-container">
                <div class="fm-like-icon-container">
                    <img src="../static/src/icon/icons8-heart-50.png" alt="Heart" id="fm-post-hearticon">
                    <h2>Like</h2>
                    <h4>({post['likes_count']})</h4>
                </div>

                <div class="fm-comment-icon-container">
                    <img src="../static/src/icon/icons8-comment-50.png" alt="Comment" id="fm-post-commenticon">
                    <h2>Comment</h2>
                    <h4>({post['comments_count']})</h4>
                </div>

                <img src="../static/src/icon/icons8-bookmark-50.png" alt="Bookmark" id="fm-post-bookmarkicon">
            </div>

            <div class="fm-caption-container">
                <h1>{post['username']}</h1>
                <h2>{post['caption'] if post.get('caption') else 'No caption available'}</h2>
            </div>
        </div>
    ''' for post in posts])

    return jsonify({'post_html': post_html, 'no_more_posts': False})



@app.route('/terms', methods=['GET'])
def TermsOfService():
    return render_template("termsofservice.html")



@app.route('/faq', methods=['GET'])
def FrequentlyAskedQuestions():
    return render_template("faq.html")



@app.route('/recruitment', methods=['POST', 'GET'])
def Recruitment():
    return render_template("recruitment.html")



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

    post_count_result = db_retrieve.retrieve("post", "COUNT(*)")
    post_count = post_count_result[0][0]

    comment_count_result = db_retrieve.retrieve("comment", "COUNT(*)")
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
        comment_count=comment_count,
        recruitment_count=recruitment_count,
        application_count=application_count,
        banned_count=banned_count, 
        muted_count=muted_count,
        reported_count=reported_count
        )



if __name__ == "__main__":
    app.run(debug=True)