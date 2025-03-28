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

        if not user_id:
            user_id = session.get('id')

        search_term = request.args.get('search', '')
        loaded_ids = request.args.get('loaded_ids', default='[]', type=str)
        post_type = request.args.get('post_type')
        page_type = request.args.get('page_type')
        entries_per_page = 5

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
                
                html += f'''
                    <div class="fm-post-layout" data-post-id="{entry['id']}" data-user-id="{entry['userid']}">
                        <div class="fm-profiledetails">
                            <a href='/user/profile?uid={entry['username']}'> 
                                <img src="{entry['profilepicture']}" alt="Pfp" id="fm-post-pfp">
                                <h1>{entry['username']}</h1>
                            </a>
                            <h2> • </h2>
                            <h2>Posted on {entry['timestamp']}</h2>
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

                html += f'''
                    <div class="fm-post-layout" data-post-id="{entry['id']}" data-user-id="{entry['userid']}">

                        <div class="rc-title-container">
                            <h1>{entry["header"]}</h1>
                        </div>

                        
                        <div class="rc-profiledetails">
                            <a href='/user/profile?uid={entry['username']}'> 
                            <img src="{entry['profilepicture']}" alt="Default pfp icon" id="rc-post-pfp">
                            <h1>{entry['username']}</h1>
                            </a>
                            <h2> • </h2>
                            <h2>Posted on {entry['timestamp']}</h2>

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
                            <a href="recruitmentapplication?postid={entry["id"]}"><button class="rc-apply-button">Apply</button></a>
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

        like_count = db_retrieve.retrieve("PostEngagement", "COUNT(*)", "liked = TRUE AND postID = %s", (post_id,))[0]
        engagement_data = db_retrieve.retrieve_one("PostEngagement", "*", "userID = %s AND postID = %s", (user_id, post_id)) or {}

        userid = post_data["userid"]
        profile_picture = user_data.get("profilePicture") or "/static/src/img/default-pfp.png"
        like_icon = ("../static/src/icon/icons8-heart-red-50.png" if engagement_data.get("liked") else "../static/src/icon/icons8-heart-50.png")
        bookmark_icon = ("../static/src/icon/icons8-bookmark-evendarkergreen-500.png" if engagement_data.get("bookmark") else "../static/src/icon/icons8-bookmark-50.png")
        date = post_data["timestamp"].strftime("%d %B %Y")

        return render_template(
            "forumspecific.html",
            post_id=post_id,
            userid=userid,
            profile_picture=profile_picture,
            username=user_data.get("username", "Unknown"),
            timestamp=date,
            image=post_data.get("image", ""),
            description=post_data.get("description", "No description available."),
            like_icon=like_icon,
            like_count=like_count,
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

        columns = "Users.username, Users.profilePicture, PostComment.comment, TO_CHAR(PostComment.timestamp, 'DD Month YYYY HH24:MI') AS timestamp"
        condition = "PostComment.postID = %s"
        params = (post_id,)
        join = "JOIN Users ON PostComment.userID = Users.userID"
        order = "ORDER BY PostComment.timestamp DESC"

        comments = db_retrieve.retrieve("PostComment", columns, condition, params, join, order)

        comments_html = ""
        for comment in comments:
            profile_picture = comment['profilepicture'] if comment['profilepicture'] else "../static/src/img/default-pfp.png"
            comments_html += f"""
            <div class="fms-comment">
                <img src="{profile_picture}" alt="Profile Picture" class="fms-pfp-placeholder" 
                     style="width:40px; height:40px; border-radius:50%;">
                <span class="fms-username-placeholder">{comment['username']}: </span>
                <span class="fms-comment-text">{comment['comment']}</span>
            </div>
            """
        return jsonify({"html": comments_html})

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

