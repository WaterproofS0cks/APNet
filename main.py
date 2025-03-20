from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from auth import auth
from user_profile import user_profile
# import psycopg2
import os
from dotenv import load_dotenv
from datetime import timedelta
import json

from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from CreateDatabase import dbCreate
from UpdateDatabase import dbModify
from ChartDatabase import dbChart



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

@app.route('/test')
def test():
    return render_template('likedposts.html')

@app.route('/')
def forum():
    return render_template('forum.html')

@app.route('/load_more')
@app.route('/recruitment/load_more')
def load_more():
    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_retrieve = dbRetrieve(db_conn)

    user_id = session.get('id')
    search_term = request.args.get('search', '')
    loaded_ids = request.args.get('loaded_ids', default='[]', type=str)
    type = request.args.get('type')
    entries_per_page = 5

    loaded_ids = json.loads(loaded_ids)

    entries = db_retrieve.retrieve_entries(type, entries_per_page, loaded_ids, search_term)

    if not entries:
        return jsonify({'html': '', 'no_more_posts': True, 'user_id': user_id})

    html = ''
    for entry in entries:
        id = entry['id']

        if user_id and type == 'post':
            engagement = db_retrieve.retrieve(
                'PostEngagement', 
                'bookmark, liked', 
                'postID = %s AND userID = %s', 
                (id, user_id)
            )
        elif user_id and type == 'recruitment':
            engagement = db_retrieve.retrieve(
                'RecruitmentEngagement', 
                'bookmark, liked', 
                'postID = %s AND userID = %s', 
                (id, user_id)
            )

        engagement_data = engagement[0] if engagement else {'bookmark': False, 'liked': False}

        like_icon = "../static/src/icon/icons8-heart-red-50.png" if engagement_data['liked'] else "../static/src/icon/icons8-heart-50.png"
        bookmark_icon = "../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data['bookmark'] else "../static/src/icon/icons8-bookmark-50.png"

        html += f'''
            <div class="fm-post-layout" data-post-id="{entry['id']}" data-user-id="{entry['userid']}">
                <div class="fm-profiledetails">
                    <img src="{entry.get('profilePicture', '/static/src/img/default-pfp.png')}" alt="Pfp" id="fm-post-pfp">
                    <h1>{entry['username']}</h1>
                    <h2>Posted on {entry['timestamp']}</h2>

                    {f'<h2>Posted on {entry["header"]}</h2>' if type == "recruitment" else ''}

                    <div class="fm-more-container">
                        <div class="fm-dropdown">
                            <span><img src="../static/src/icon/icons8-ellipsis-48.png" alt="Elipses" id="fm-moreicon" height="24" width="24"></span>
                            <div class="fm-dropdown-content">
                                <a href="#" class="fm-dropdown-item">
                                    <img src="../static/src/icon/icons8-flag-48.png" alt="Report Post" id="fm-reportposticon" height="20" width="20"> Report Post
                                </a>
                                <a href="#" class="fm-dropdown-item">
                                    <img src="../static/src/icon/icons8-danger-50.png" alt="Report User" id="fm-reportusericon" height="20" width="20"> Report User
                                </a>
                                <a href="#" class="fm-dropdown-item">
                                    <img src="../static/src/icon/icons8-edit-96.png" alt="Edit" id="fm-editicon" height="20" width="20">Edit Post
                                </a>
                                <a href="#" class="fm-dropdown-item">
                                    <img src="../static/src/icon/icons8-delete-48.png" alt="Delete" id="fm-deleteicon" height="20" width="20">Delete Post
                                </a>
                            </div>
                        </div>
                    </div>

                </div>

                <a class="fm-image-container" href="specificpost?postid={entry['id']}">
                    <img src="{entry['image']}" alt="Post Image">
                </a>

                <div class="fm-button-container">

                    <div class="fm-like-icon-container" data-action="liked">
                        <img src="{like_icon}" alt="Heart" id="fm-post-hearticon">
                        <h2>Like</h2>
                        <h4>({entry['likes_count']})</h4>
                    </div>

                    <div class="fm-comment-icon-container" data-action="specific">
                        <img src="../static/src/icon/icons8-comment-50.png" alt="Comment" id="fm-post-commenticon">
                        <h2>Comment</h2>
                        <h4>({entry['comments_count']})</h4>
                    </div>

                    <div class="fm-bookmark-icon-container" data-action="bookmark">
                        <img src="{bookmark_icon}" alt="Bookmark" id="fm-post-bookmarkicon">
                    </div>
                </div>

                
                <div class="fm-caption-container">
                    
                    <h1>{entry['username']}</h1>
                    <h2>{entry['description']}</h2>
                </div>

                {'<div class="post-footer">'
                '<span class="interest-text">Interested? Join Us Now!</span>'
                '<button class="apply-button">Apply</button>'
                '</div>' if type == "recruitment" else ''}

            </div>
        '''
    return jsonify({'html': html, 'no_more_posts': False, 'user_id': user_id})

@app.route('/engagement', methods=['POST'])
def engagement_render():
    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )
    db_conn.connect()
    db_retrieve = dbRetrieve(db_conn)
    db_modify = dbModify(db_conn)

    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('auth/register'))

    data = request.json
    post_id = data.get('post_id')
    action = data.get('action')

    if not post_id or action not in ["liked", "bookmark"]:
        return jsonify({'error': 'Invalid request'}), 400

    status = db_modify.toggle_engagement(user_id, post_id, action)

    response = {'bookmark': status} if action == "bookmark" else {}

    if action == "liked":
        likes_count = db_retrieve.retrieve("PostEngagement", "COUNT(*)", "postID = %s AND liked = TRUE", (post_id,))
        likes_count = likes_count[0] if likes_count else 0  
        response.update({'liked': status, 'likes_count': likes_count})

    print(response)
    return jsonify(response)

@app.route('/specificpost', methods=["GET", "POST"])
def specific_post():
    post_id = request.args.get('postid', '')
    user_id = session.get('id')

    if not post_id:
        return # Should Send To Homepage

    db_conn = dbConnection(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
    )

    db_conn.connect()
    db_retrieve = dbRetrieve(db_conn)

    post_data = db_retrieve.retrieve_one("Post", "*", "postID = %s", (post_id,))
    if not post_data: # Need To Figure Out What To Do
        return 
    print("Post Data:", post_data)
    post_user_id = post_data.get("userID")
    user_data = db_retrieve.retrieve_one("Users", "*", "userID = %s", (post_user_id,))
    if not user_data: # Need To Figure Out What To Do
        return

    like_count = db_retrieve.retrieve_one("PostEngagement", "COUNT(*)", "liked = TRUE AND postID = %s", (post_id,))[0]
    engagement_data = db_retrieve.retrieve_one("PostEngagement", "*", "userID = %s AND postID = %s", (user_id, post_id)) or {}

    profile_picture = user_data.get("profilePicture") or "/static/src/img/default-pfp.png"
    like_icon = ("../static/src/icon/icons8-heart-red-50.png" if engagement_data.get("liked") else "../static/src/icon/icons8-heart-50.png")
    bookmark_icon = ("../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data.get("bookmark") else "../static/src/icon/icons8-bookmark-50.png")

    return render_template(
        "forumspecific.html",
        profile_picture=profile_picture,
        username=user_data.get("username", "Unknown"),
        timestamp=post_data.get("timestamp", "N/A"),
        image=post_data.get("image", ""),
        description=post_data.get("description", "No description available."),
        like_icon=like_icon,
        like_count=like_count,
        bookmark_icon=bookmark_icon
    )


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



@app.route('/aboutus', methods=['GET'])
def AboutUs():
    return render_template('aboutus.html')



if __name__ == "__main__":
    app.run(debug=True)