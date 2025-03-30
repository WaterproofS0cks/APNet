from flask import request, jsonify, session, url_for, redirect, render_template
import os
import json

from ConnectDatabase import dbConnection
from RetrieveDatabase import dbRetrieve
from UpdateDatabase import dbModify

class Content():
    def load_post(user_id=None):
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        search_term = request.args.get('search', '')
        loaded_ids = request.args.get('loaded_ids', default='[]', type=str)
        post_type = request.args.get('post_type')
        page_type = request.args.get('page_type')
        user_id = request.args.get('user_id')
        entries_per_page = 5

        if not user_id:
            user_id = session.get('id')

        loaded_ids = json.loads(loaded_ids)

        entries = db_retrieve.retrieve_entries(post_type, page_type, entries_per_page, loaded_ids, search_term, user_id)
        
        if not entries:
            return jsonify({'html': '', 'no_more_posts': True, 'user_id': user_id})

        html = ''
        for entry in entries:
            if post_type == "post":
                id = entry['id']

                if user_id and post_type == 'post':
                    engagement = db_retrieve.retrieve(
                        'PostEngagement', 
                        'bookmark, liked', 
                        'postID = %s AND userID = %s', 
                        (id, user_id)
                    )
                else:
                    engagement = None

                like_count = db_retrieve.retrieve_one("PostEngagement", "COUNT(*)", "liked = TRUE AND postID = %s", (id,))[0]
                engagement_data = engagement[0] if engagement else {'bookmark': False, 'liked': False}

                like_icon = "../static/src/icon/icons8-heart-red-50.png" if engagement_data['liked'] else "../static/src/icon/icons8-heart-50.png"
                bookmark_icon = "../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data['bookmark'] else "../static/src/icon/icons8-bookmark-50.png"

                if entry['username'] == session.get('user'):
                    link = f"<a href='/user/profile'>"
                else:
                    link = f"<a href='/user/profile?uid={entry['username']}'>"
                
                html += f'''
                    <div class="fm-post-layout" data-post-id="{entry['id']}" data-user-id="{entry['userid']}">
                        <div class="fm-profiledetails">
                            {link}
                                <img src="{entry['profilepicture']}" alt="Pfp" id="fm-post-pfp">
                                <h1>{entry['username']}</h1>
                            </a>
                            <h2> • </h2>
                            <h2>Posted on {entry['timestamp']}</h2>
                            <div class="fm-more-container">
                                <div class="fm-dropdown">
                                    <span><img src="../static/src/icon/icons8-ellipsis-48.png" alt="Elipses" id="fm-moreicon" height="24" width="24"></span>
                                    <div class="fm-dropdown-content">
                                        <button onclick="editReportPost(this)" class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-flag-48.png" alt="Report Post" id="fm-reportposticon" height="20" width="20"> Report Post
                                        </button>
                                        <button onclick="editReportUser(this)" class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-danger-50.png" alt="Report User" id="fm-reportusericon" height="20" width="20"> Report User
                                        </button>
                                        <button onclick="editPost(this)" class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-edit-96.png" alt="Edit" id="fm-editicon" height="20" width="20">Edit Post
                                        </button>
                                        <button onclick="deletePost(this)" class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-delete-48.png" alt="Delete" id="fm-deleteicon" height="20" width="20">Delete Post
                                        </button>
                                    </div>
                                </div>
                            </div>

                        </div>
                        
                        <div class="fm-image-container">
                            <a href='specificpost?postid={entry["id"]}'> 
                                <img src="{entry["image"]}" alt="Post Image"> 
                            </a>
                        </div>
                        

                        <div class="fm-button-container">
                            <div class="fm-like-icon-container" data-action="liked">
                                <img src="{like_icon}" alt="Heart" id="fm-post-hearticon">
                                <h2>Like</h2>
                                <h4>({like_count})</h4>
                            </div>

                            <div class="fm-comment-icon-container" data-action="specific">
                                <a href='specificpost?postid={entry["id"]}'> 
                                    <img src="../static/src/icon/icons8-comment-50.png" alt="Comment" id="fm-post-commenticon">
                                    <h2>Comment</h2>
                                    <h4>({entry['comments_count']})</h4>
                                </a>
                            </div>

                            <div class="fm-bookmark-icon-container" data-action="bookmark">
                                <img src="{bookmark_icon}" alt="Bookmark" id="fm-post-bookmarkicon">
                            </div>
                        </div>

                        
                        <div class="fm-caption-container">
                            
                            <h1>{entry['username']}</h1>
                            <h2>{entry['description']}</h2>
                        </div>

                    </div>
                '''


            elif post_type == "recruitment":
                id = entry['id']

                if user_id:
                    engagement = db_retrieve.retrieve(
                        'RecruitmentEngagement', 
                        'bookmark, liked', 
                        'recruitmentID = %s AND userID = %s', 
                        (id, user_id)
                    )
                else:
                    engagement = None

                like_count = db_retrieve.retrieve_one("RecruitmentEngagement", "COUNT(*)", "liked = TRUE AND recruitmentID = %s", (id,))[0]
                engagement_data = engagement[0] if engagement else {'bookmark': False, 'liked': False}

                like_icon = "../static/src/icon/icons8-heart-red-50.png" if engagement_data['liked'] else "../static/src/icon/icons8-heart-50.png"
                bookmark_icon = "../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data['bookmark'] else "../static/src/icon/icons8-bookmark-50.png"

                if entry['username'] == session.get('user'):
                    link = f"<a href='/user/profile'>"
                else:
                    link = f"<a href='/user/profile?uid={entry['username']}'>"

                html += f'''
                    <div class="fm-post-layout" data-post-id="{entry['id']}" data-user-id="{entry['userid']}">

                        <div class="rc-title-container">
                            <h1>{entry["header"]}</h1>
                        </div>

                        
                        <div class="rc-profiledetails">
                            {link}
                            <img src="{entry['profilepicture']}" alt="Default pfp icon" id="rc-post-pfp">
                            <h1>{entry['username']}</h1>
                            </a>
                            <h2> • </h2>
                            <h2>Posted on {entry['timestamp']}</h2>

                            <div class="fm-more-container">
                                <div class="fm-dropdown">
                                    <span><img src="../static/src/icon/icons8-ellipsis-48.png" alt="Elipses" id="fm-moreicon" height="24" width="24"></span>
                                    <div class="fm-dropdown-content">
                                        <button class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-flag-48.png" alt="Report Post" id="fm-reportposticon" height="20" width="20"> Report Post
                                        </button>
                                        <button class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-danger-50.png" alt="Report User" id="fm-reportusericon" height="20" width="20"> Report User
                                        </button>
                                        <button class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-edit-96.png" alt="Edit" id="fm-editicon" height="20" width="20">Edit Post
                                        </button>
                                        <button class="fm-dropdown-item">
                                            <img src="../static/src/icon/icons8-delete-48.png" alt="Delete" id="fm-deleteicon" height="20" width="20">Delete Post
                                        </button>
                                    </div>
                                </div>
                            </div>               

                        </div>

                        <div class="rc-image-container">
                            <a href='specificrecruitment?postid={entry["id"]}'> 
                                <img src="{entry["image"]}" alt="Post Image"> 
                            </a>
                        </div>
                        
                        <div class="fm-button-container">
                            <div class="fm-like-icon-container" data-action="liked">
                                <img src="{like_icon}" alt="Heart" id="fm-post-hearticon">
                                <h2>Like</h2>
                                <h4>({like_count})</h4>
                            </div>

                            <div class="fm-comment-icon-container" data-action="specific">
                                <a href='specificrecruitment?postid={entry["id"]}'> 
                                    <img src="../static/src/icon/icons8-comment-50.png" alt="Comment" id="fm-post-commenticon">
                                    <h2>Comment</h2>
                                    <h4>({entry['comments_count']})</h4>
                                </a>
                            </div>

                            <div class="fm-bookmark-icon-container" data-action="bookmark">
                                <img src="{bookmark_icon}" alt="Bookmark" id="fm-post-bookmarkicon">
                            </div>
                        </div>

                        <div class="rc-caption-container">
                            <h1>CLUB DESCRIPTION</h1>

                            <h2>{entry['description']}</h2>
                        </div>

                        <div class="rc-post-footer">
                            <span class="rc-interest-text">Interested? Join Us Now!</span>
                            <a href="recruitment-application?postid={entry["id"]}"><button class="rc-apply-button">Apply</button></a>
                        </div>
                    </div>
                '''
        return jsonify({'html': html, 'no_more_posts': False, 'user_id': user_id})

    def load_engagement():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )
        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)
        db_modify = dbModify(db_conn)

        user_id = session.get('id')

        data = request.json
        post_type = data.get('post_type')
        post_id = data.get('post_id')
        action = data.get('action')

        if not post_id or action not in ["liked", "bookmark"]:
            return jsonify({'error': 'Invalid request'}), 400

        status = db_modify.toggle_engagement(user_id, post_id, action, post_type)

        response = {'bookmark': status} if action == "bookmark" else {}

        if action == "liked":
            if post_type == "post":
                likes_count = db_retrieve.retrieve("PostEngagement", "COUNT(*)", "postID = %s AND liked = TRUE", (post_id,))
            if post_type == "recruitment":
                likes_count = db_retrieve.retrieve("RecruitmentEngagement", "COUNT(*)", "recruitmentID = %s AND liked = TRUE", (post_id,))
            likes_count = likes_count[0] if likes_count else 0  
            response.update({'liked': status, 'likes_count': likes_count})

        return jsonify(response)
    
    def load_specific_forum():
        post_id = request.args.get('postid', '')
        user_id = session.get('id')

        if not post_id:
            return redirect(url_for("forum"))

        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        post_data = db_retrieve.retrieve_one("Post", condition="postID = %s", params=(post_id,))

        if not post_data:
            return redirect(url_for("forum"))

        user_data = db_retrieve.retrieve_one("Users", "*", "userID = %s", (post_data["userid"],))

        like_count = db_retrieve.retrieve_one("PostEngagement", "COUNT(*)", "liked = TRUE AND postID = %s", (post_id,))
        engagement_data = db_retrieve.retrieve_one("PostEngagement", "*", "userID = %s AND postID = %s", (user_id, post_id)) or {}

        userid = post_data["userid"]
        count = like_count['count']
        profile_picture = user_data["profilepicture"]
        like_icon = ("../static/src/icon/icons8-heart-red-50.png" if engagement_data.get("liked") else "../static/src/icon/icons8-heart-50.png")
        bookmark_icon = ("../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data.get("bookmark") else "../static/src/icon/icons8-bookmark-50.png")
        date = post_data["timestamp"].strftime("%d %B %Y")

        return render_template(
            "forumspecific.html",
            post_id=post_id,
            userid=userid,
            profile_picture=profile_picture,
            username=user_data.get("username"),
            timestamp=date,
            image=post_data.get("image"),
            description=post_data.get("description"),
            like_icon=like_icon,
            like_count=count,
            bookmark_icon=bookmark_icon
        )

    def load_recruitment_forum():
        post_id = request.args.get('postid', '')
        user_id = session.get('id')

        if not post_id:
            return redirect(url_for("forum"))

        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        post_data = db_retrieve.retrieve_one("Recruitment", condition="recruitmentID = %s", params=(post_id,))

        if not post_data:
            return redirect(url_for("forum"))

        user_data = db_retrieve.retrieve_one("Users", "*", "userID = %s", (post_data["userid"],))

        like_count = db_retrieve.retrieve_one("RecruitmentEngagement", "COUNT(*)", "liked = TRUE AND recruitmentID = %s", (post_id,))
        engagement_data = db_retrieve.retrieve_one("RecruitmentEngagement", "*", "userID = %s AND recruitmentID = %s", (user_id, post_id)) or {}

        userid = post_data["userid"]
        header = post_data["header"]
        count = like_count['count']
        profile_picture = user_data["profilepicture"]
        like_icon = ("../static/src/icon/icons8-heart-red-50.png" if engagement_data.get("liked") else "../static/src/icon/icons8-heart-50.png")
        bookmark_icon = ("../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data.get("bookmark") else "../static/src/icon/icons8-bookmark-50.png")
        date = post_data["timestamp"].strftime("%d %B %Y")

        return render_template(
            "recruitmentspecific.html",
            post_id=post_id,
            userid=userid,
            profile_picture=profile_picture,
            username=user_data.get("username"),
            timestamp=date,
            header=header,
            image=post_data.get("image"),
            description=post_data.get("description"),
            like_icon=like_icon,
            like_count=count,
            bookmark_icon=bookmark_icon
        )
    
    def load_comment():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        post_id = request.args.get('post_id')
        post_type = request.args.get('post_type')
        user_id = session.get("id")

        if post_type == "post":
            table = "PostComment"
            columns = "Users.username, Users.profilePicture, PostComment.comment, PostComment.userid, PostComment.postcommentid AS id, TO_CHAR(PostComment.timestamp, 'DD Month YYYY HH24:MI') AS timestamp"
            condition = "PostComment.postID = %s"
            params = (post_id,)
            join = "JOIN Users ON PostComment.userID = Users.userID"
            order = "ORDER BY PostComment.timestamp DESC"

        elif post_type == "recruitment":
            table = "RecruitmentComment"
            columns = "Users.username, Users.profilePicture, RecruitmentComment.comment, RecruitmentComment.userid, RecruitmentComment.recruitmentcommentid AS id, TO_CHAR(RecruitmentComment.timestamp, 'DD Month YYYY HH24:MI') AS timestamp"
            condition = "RecruitmentComment.recruitmentID = %s"
            params = (post_id,)
            join = "JOIN Users ON RecruitmentComment.userID = Users.userID"
            order = "ORDER BY RecruitmentComment.timestamp DESC"

        comments = db_retrieve.retrieve(table, columns, condition, params, join, order)

        html = ""
        for comment in comments:
            profile_picture = comment['profilepicture'] if comment['profilepicture'] else "../static/src/img/default-pfp.png"
            html += f"""
            <div class="fms-comment" id="comment-{comment['id']}">
                <img src="{profile_picture}" alt="Profile Picture" class="fms-pfp-placeholder" 
                     style="width:40px; height:40px; border-radius:50%;">
                <span class="fms-username-placeholder">{comment['username']}: </span>
                <span class="fms-comment-text">{comment['comment']}</span>
            """

            if user_id == comment["userid"]:
                html += f'<button class="delete-comment-btn" data-comment-id="{comment['id']}">Delete</button>'

            html += "</div>"
        print(html)
        return jsonify({"html": html})

    def load_application():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        user_id = session.get("id")

        applications = db_retrieve.retrieve(
            "application",
            "application.*, recruitment.header, recruitment.image AS recruitment_image, recruitment.description AS recruitment_description, TO_CHAR(recruitment.timestamp, 'DD Month YYYY') AS recruitment_timestamp",
            "application.userid = %s",
            (user_id,),
            join="INNER JOIN recruitment ON application.recruitmentID = recruitment.recruitmentID"
        )

        html = ""

        for application in applications:
            count_result = db_retrieve.retrieve(
                "application", 
                "COUNT(*)", 
                "recruitmentid = %s", 
                (application["recruitmentid"],)
            )
            count = count_result[0][0] if count_result else 0

            recruitment_image = application['recruitment_image'] or 'static/src/img/default-events.jpg'

            html += f"""
            <div class="activity-card">
                <div class="activity-flex">
                    <div class="activity-attr">
                        <sub>{application["recruitment_timestamp"]}</sub>
                        <h3>{application["header"]}</h3>

                        <div class="applications-activity-img-responsive">
                            <img src="{recruitment_image}" alt="Placeholder Image">
                        </div>

                        <p>{application["recruitment_description"]}</p>
                    </div>
                    <div class="applications-activity-img">
                        <img src="{recruitment_image}" alt="Recruitment Image">
                    </div>
                </div>
                <div class="applications-container">
                    <div>
                        <h3>Applicants</h3>
                        <p>{count}</p>
                    </div>
                    <div>
                        <h3>Status</h3>
                        <p>{application["status"]}</p>
                    </div>
                </div>
            </div>
            """

        return jsonify({"html": html})
    
    def load_applicants():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        user_id = session.get("id")

        recruitment_columns = """
            recruitment.recruitmentID, 
            recruitment.header, 
            recruitment.description AS recruitment_description, 
            TO_CHAR(recruitment.timestamp, 'DD Month YYYY') AS recruitment_timestamp, 
            recruitment.image AS recruitment_image
        """

        recruitment_condition = "recruitment.userid = %s"
        recruitment_params = (user_id,)

        recruitments = db_retrieve.retrieve("Recruitment AS recruitment", recruitment_columns, recruitment_condition, recruitment_params)

        html = ""

        for recruitment in recruitments:

            applicant_columns = """
                users.userid AS applicant_userid, 
                users.username AS applicant_username, 
                users.fullname AS applicant_fullname, 
                users.email AS applicant_email,
                application.status AS application_status
            """

            applicant_condition = "application.recruitmentid = %s"
            applicant_params = (recruitment['recruitmentid'],)

            applicants = db_retrieve.retrieve("Application AS application JOIN Users AS users ON application.userid = users.userid", applicant_columns, applicant_condition, applicant_params)

            html += f"""
            <div class="activity-card">
                <div class="activity-flex">
                    <div class="activity-attr">
                        <sub>{recruitment["recruitment_timestamp"]}</sub>
                        <h3>{recruitment["header"]}</h3>
                        <div class="applications-activity-img-responsive">
                            <img src="{recruitment["recruitment_image"]}" alt="Placeholder Image">
                        </div>
                        <p>{recruitment["recruitment_description"]}</p>
                    </div>
                    <div class="applications-activity-img">
                        <img src="{recruitment["recruitment_image"]}" alt="Placeholder Image">
                    </div>
                </div>
                <div class="activity-margin">
                    <h3>Applicants</h3>
                    <div class="applicant-flex">
            """

            applicants_to_display = applicants[:4]
            for applicant in applicants_to_display:
                if applicant['application_status'] == 'Accepted':
                    applicant_id_tag = 'id="applicant-accepted"'
                elif applicant['application_status'] == 'Rejected':
                    applicant_id_tag = 'id="applicant-rejected"'
                else:
                    applicant_id_tag =""
                    
                html += f"""
                    <a class="applicant-card" href="/applicantspecific"
                    {applicant_id_tag} 
                    data-applicant-id="{applicant['applicant_userid']}" 
                    data-recruitment-id="{recruitment['recruitmentid']}" 
                    onclick="IAMLOSINGMYMIND(this)">
                    {applicant['applicant_username']}
                    </a>
                """
                

            for applicant in applicants[4:]:
                html += f"""
                    <a class="applicant-card applicant-extra"
                    {applicant_id_tag} 
                    data-applicant-id="{applicant['applicant_userid']}" 
                    data-recruitment-id="{recruitment['recruitmentid']}" 
                    onclick="IAMLOSINGMYMIND(this)">
                    {applicant['applicant_username']}
                    </a>
                """

            if len(applicants) > 4:
                    html += f"""
                        <p id="applicant-view-{recruitment['recruitmentid']}" 
                        class="applicant-view" 
                        data-recruitment-id="{recruitment['recruitmentid']}" 
                        onclick="viewToggle(this)">
                        View more
                        </p>
                    """
            elif len(applicants) < 1:
                html += f"""
                    <p>No One Applied Yet D:</p>
                """

            html += f"""
                    </div>
                </div>
            </div>
            """

        return jsonify({"html": html})


    def load_penalized_users_table():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        table_html = """
        <table class="dashboard-table">
            <tr>
                <th>Username</th>
                <th>Reason</th>
                <th>Option</th>
            </tr>
        """

        load_actively_penalized_users_data = db_retrieve.retrieve_actively_penalized()

        if not load_actively_penalized_users_data:
            table_html += f"""
                <tr>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
            </table>
            """
            return table_html

        for entry in load_actively_penalized_users_data:
            if entry["penaltyType"] == "Banned":
                options_html = f"""
                    <td>
                        <u data-user="{entry['userid']}" data-action="Unban">Unban</u>
                    </td>
                """
            elif entry["penaltyType"] == "Muted":
                options_html = f"""
                    <td>
                        <u data-user="{entry['userid']}" data-action="Unmute">Unmute</u>
                    </td>
                """
            else:
                options_html = "<td>No Actions Available</td>"

            table_html += f"""
            <tr>
                <td>{entry["username"]}</td>
                <td>{entry["description"]}</td>
                {options_html}
            </tr>
            """

        table_html += "</table>"
        return table_html

    def load_reported_user_table():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        table_html = """
        <table class="dashboard-table">
            <tr>
                <th>Username</th>
                <th>Reason</th>
                <th>Option</th>
            </tr>
        """

        load_reported_user_data = db_retrieve.retrieve(
            tablename="Reports",
            condition="status = %s AND type = %s",
            params=("Processing", "User")
        )

        if not load_reported_user_data:
            table_html += f"""
                <tr>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
            </table>
            """

        for entry in load_reported_user_data:
            user_data = db_retrieve.retrieve_one(
                tablename="Users",
                columns="username",
                condition="userid = %s",
                params=(entry["placementid"],)
            )

            table_html += f"""
            <tr>
                <td>{user_data["username"]}</td>
                <td>{entry["description"]}</td>
                <td>
                    <u data-id="{entry['placementid']}" data-action="Ban">Ban</u> /
                    <u data-id="{entry['placementid']}" data-action="Mute">Mute</u>
                </td>
            </tr>
            """

        table_html += "</table>"
        return table_html

    def load_reported_post_table():
        db_conn = dbConnection(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        db_conn.connect()
        db_retrieve = dbRetrieve(db_conn)

        table_html = """
        <table class="dashboard-table">
            <tr>
                <th>ID</th>
                <th>Reason</th>
                <th>Option</th>
            </tr>
        """

        load_reported_post_data = db_retrieve.retrieve(
            tablename="Reports",
            condition="status = %s AND (type = %s OR type = %s)",
            params=("Processing", "Forum", "Recruitment")
        )

        if not load_reported_post_data:
            table_html += f"""
                <tr>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
            </table>
            """

        for entry in load_reported_post_data:

            # if entry["type"] == "Forum":
            #     post_data = db_retrieve.retrieve_one(
            #         tablename="Post",
            #         columns="postContent", 
            #         condition="postid = %s",
            #         params=(entry["placementid"],)
            #     )

            # elif entry["type"] == "Recruitment":
            #     post_data = db_retrieve.retrieve_one(
            #         tablename="Recruitment",
            #         columns="recruitmentDetails", 
            #         condition="recruitmentid = %s",
            #         params=(entry["placementid"],)
            #     )

            # if post_data:
            #     post_content = post_data.get("postContent") or post_data.get("recruitmentDetails")

                table_html += f"""
                <tr>
                    <td>{entry['placementid']}</td>
                    <td>{entry["description"]}</td>
                    <td>
                        <u data-id="{entry['placementid']}" data-type="{entry['type']}" data-action="Remove">Remove</u> /
                        <u data-id="{entry['placementid']}" data-type="{entry['type']}" data-action="Dismiss">Dismiss</u>
                    </td>
                </tr>
                """

        table_html += "</table>"
        return table_html

